import pandas as pd
import numpy as np
import math
import os
import dill
import traceback
from abc import ABC, abstractmethod
from loguru import logger
from numpy.random import seed, choice
from pathos.multiprocessing import ProcessingPool
from typing import Tuple

from syngen.ml.vae import *
from syngen.ml.reporters import Report
from syngen.ml.data_loaders import MetadataLoader


class AbstractHandler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, data: pd.DataFrame, **kwargs):
        pass


class BaseHandler(AbstractHandler):
    def __init__(self, metadata: dict, paths: dict):
        self.metadata = metadata
        self.paths = paths
        try:
            self.table_name = metadata["table_name"]
        except KeyError:
            raise KeyError("No table name was provided.")

    _next_handler: AbstractHandler = None

    def set_next(self, handler: AbstractHandler) -> AbstractHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, data: pd.DataFrame, **kwargs):

        if self._next_handler:
            return self._next_handler.handle(data, **kwargs)

        return None

    @staticmethod
    def create_wrapper(cls_name, **kwargs):
        return globals()[cls_name](
            kwargs["metadata"], kwargs["paths"], kwargs["keys_mode"]
        )


class RootHandler(BaseHandler):
    def __init__(self, metadata: dict, paths: dict):
        super().__init__(metadata, paths)

    def __prepare_dirs(self):
        os.makedirs(self.paths["model_artifacts_path"], exist_ok=True)
        tmp_store_path = self.paths["tmp_store_path"]
        os.makedirs(tmp_store_path, exist_ok=True)
        os.makedirs(self.paths["pk_path"], exist_ok=True)

    @staticmethod
    def prepare_data(data, options):
        if options["dropna"]:
            data = data.dropna()

        if options["row_subset"]:
            data = data.sample(n=options["row_subset"])

        if options["epochs"] < 1:
            raise AttributeError("Number of epochs should be > 0")

        data_columns = set(data.columns)
        # remove completely empty columns
        data = data.dropna(how="all", axis=1)
        dropped_cols = set(data.columns) - data_columns
        if len(dropped_cols) > 0:
            logger.info(f"Empty columns {dropped_cols} were removed")
        return data

    def handle(self, data: pd.DataFrame, **kwargs):
        self.__prepare_dirs()
        data = self.prepare_data(data, kwargs)

        data.to_csv(self.paths["input_data_path"], index=False)
        return super().handle(data, **kwargs)


class VaeTrainHandler(BaseHandler):
    def __init__(
        self, metadata: dict, paths: dict, wrapper_name, keys_mode: str = None
    ):
        super().__init__(metadata, paths)
        self.keys_mode = keys_mode
        self.model = self.create_wrapper(
            wrapper_name,
            metadata=self.metadata,
            paths=self.paths,
            keys_mode=self.keys_mode,
        )
        self.state_path = self.paths["state_path"]
        self.vae_infer_path = self.paths["vae_infer_path"]

    def __fit_model(
        self, data: pd.DataFrame, epochs: int, batch_size: int, keys_mode: str
    ):
        os.makedirs(self.state_path, exist_ok=True)
        logger.info("Start VAE training")
        if data is None:
            logger.error("For mode = 'train' path must be provided")
            raise ValueError("Can't read data from path or path is None")

        self.model.batch_size = min(batch_size, len(data))
        self.model.fit_on_df(
            data,
            epochs=epochs,
            keys_mode=keys_mode,
        )

        self.model.save_state(self.state_path)
        sampled_df = self.model.predict_sampled_df(len(data))
        sampled_df.to_csv(self.vae_infer_path, index=False)
        logger.info("Finished VAE training")

    def handle(self, data: pd.DataFrame, **kwargs):
        self.__fit_model(
            data,
            kwargs["epochs"],
            kwargs["batch_size"],
            keys_mode=kwargs["keys_mode"],
        )
        return super().handle(data, **kwargs)


class VaeInferHandler(BaseHandler):
    def __init__(
        self,
        metadata: dict,
        paths: dict,
        wrapper_name: str,
        random_seed: int = None,
        keys_mode: str = None,
    ):
        super().__init__(metadata, paths)
        self.random_seed = random_seed
        self.random_seeds_list = []
        if random_seed:
            seed(random_seed)
        self.keys_mode = keys_mode
        self.vae = None
        self.wrapper_name = wrapper_name
        self.vae_state_path = self.paths["state_path"]
        self.vae_infer_path = self.paths["vae_infer_path"]
        self.path_to_merged_infer = self.paths["path_to_merged_infer"]

    def __prepare_dir(self):
        tmp_store_path = self.paths["tmp_store_path"]
        os.makedirs(tmp_store_path, exist_ok=True)

    def kde_gen(self, pk_column, size):
        if np.array_equal(pk_column, pk_column.astype(int)):
            orig_column = pk_column.dataset
            range_gen = np.arange(
                start=int(min(orig_column) * len(orig_column) / size),
                stop=int(max(orig_column) * size / len(orig_column)),
                step=1,
            )
            probs = pk_column.pdf(range_gen)
            kde = [
                np.random.choice(
                    range_gen,
                    size=size,
                    p=probs / sum(probs),
                    replace=size < len(orig_column),
                )
            ]
        else:
            kde = pk_column.resample(size)
        return pd.Series(kde[0], name=pk_column)

    def run_separate(self, params: Tuple):
        i, size = params

        if self.random_seed:
            seed(self.random_seeds_list[i])

        self.vae = self.create_wrapper(
            self.wrapper_name,
            metadata={"table_name": self.table_name},
            paths=self.paths,
            keys_mode=self.keys_mode,
        )
        self.vae.load_state(self.vae_state_path)
        synthetic_infer = self.vae.predict_sampled_df(size)
        return synthetic_infer

    def split_by_batches(self, size, nodes):
        quote = int(size / nodes)
        data = [quote] * nodes
        data.append((size - nodes * quote) + data.pop())
        return data

    def run(self, size: int, run_parallel: bool = True):
        logger.info("Start data synthesis")
        if run_parallel:
            pool = ProcessingPool()
            if self.random_seed:
                self.random_seeds_list = choice(
                    range(0, max(100, pool.nodes)), pool.nodes, replace=False
                )

            frames = pool.map(
                self.run_separate, enumerate(self.split_by_batches(size, pool.nodes))
            )
            generated = pd.concat(frames)
        else:
            if self.random_seed:
                self.random_seeds_list = [self.random_seed]
            generated = self.run_separate((0, size))
        return generated

    def generate_keys(self, generated, size, metadata):
        if metadata.get("fk", None):
            pk_table = [v["pk_table"] for k, v in metadata["fk"].items()][0]
            pk_path = f"model_artifacts/resources/{pk_table}/pk/pk_column.pkl"
            if not os.path.exists(pk_path):
                raise FileNotFoundError(
                    "The table with a primary key specified in the metadata file does not "
                    "exist or is not trained. Ensure that the metadata contains the "
                    "name of the table with a primary key in the foreign key declaration section "
                    "following pattern 'fk': {'fk_column_name': {'pk_table': 'pk_table_name', 'pk_column': 'pk_column_name'}}}'"
                )
            with open(pk_path, "rb") as pk_pickle:
                pk_column = dill.load(pk_pickle)
            if type(pk_column) is pd.Series:
                kde_pk = pk_column.sample(
                    size, replace=size > len(pk_column)
                ).reset_index(drop=True)
            else:
                kde_pk = self.kde_gen(pk_column, size).reset_index(drop=True)

            generated = pd.concat([generated, kde_pk], axis=1)
        return generated

    def handle(
        self,
        size: int,
        run_parallel: bool = True,
        batch_size: int = None,
        print_report: bool = False,
        keys_mode: str = None,
        metadata_path: str = None,
    ):
        self.__prepare_dir()
        try:
            if not batch_size:
                batch_size = size
            batch_num = math.ceil(size / batch_size)
            logger.info(f"Total of {batch_num} batch(es)")
            batches = self.split_by_batches(size, batch_num)
            generated = pd.DataFrame()
            for batch in batches:
                generated_batch = self.run(batch, run_parallel)
                generated = pd.concat([generated, generated_batch])
            if keys_mode == "multable":
                if not metadata_path:
                    raise Exception(
                        "If keys_mode is set to multable, the metadata path must be provided"
                    )
                metadata = MetadataLoader().load_data(metadata_path)
                generated = self.generate_keys(generated, size, metadata)

            generated.to_csv(self.path_to_merged_infer, index=False)
            if print_report:
                Report().generate_report()

            logger.info(
                f"Synthesis was completed. Synthetic data saved in {self.path_to_merged_infer}"
            )
        except Exception as e:
            logger.info("Generation failed on running stage.")
            logger.error(e)
            logger.error(traceback.format_exc())
            raise

