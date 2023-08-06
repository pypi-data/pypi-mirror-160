import json
import os
import pathlib
import shutil
import tempfile
from typing import Any, Dict

import tensorflow as tf

from .model_management import ModelManager
from ..core import CustomNamedTemporaryFile, encode_dir_to_file, decode_file_to_dir


def clean_up(before: set, after: set):
    new = after.difference(before)
    for f in new:
        if pathlib.Path(f).is_file():
            os.remove(f)
        elif pathlib.Path(f).is_dir():
            shutil.rmtree(f)
        else:
            raise ValueError("Not file or directory - cannot clean up.")


# TODO see if we can improve the flow - will require rework of the flow for all models I think
class TensorflowModelManager(ModelManager):
    @staticmethod
    def encode(model: tf.keras.Model) -> bytes:
        # save to folder - SavedModel standard
        before = set(os.listdir())
        with tempfile.TemporaryDirectory() as temp_dir:
            tf.keras.models.save_model(model, temp_dir, save_format="tf")

            # we assume tar is available everywhere - it should be in almost all cases.
            with CustomNamedTemporaryFile() as temp:
                try:
                    with open(temp.name, "wb+") as f:
                        encode_dir_to_file(pathlib.PurePath(temp_dir), f)
                # TODO remove this if tempfile cleans up in error cases...
                except Exception:
                    clean_up(before=before, after=set(os.listdir()))
                    raise

                with open(temp.name, "rb") as read_temp:
                    return read_temp.read()

    @staticmethod
    def decode(data: bytes) -> Any:
        """
        Loads a stored XGBoost model. Note this will always return a Booster (LearningAPI model) even if the original
        model was an SKLearn model. This will impact the methods available on the returned model.
        :param data:
        :return: XGBoost.Booster model.
        """
        before = set(os.listdir())
        with CustomNamedTemporaryFile() as temp:
            with open(temp.name, "wb+") as write_temp:
                write_temp.write(data)

            with open(temp.name, "rb") as read_temp:
                dirname = decode_file_to_dir(read_temp)

            # load model
            try:
                model = tf.keras.models.load_model(dirname)
            except Exception:
                clean_up(before=before, after=set(os.listdir()))
                raise
            clean_up(before=before, after=set(os.listdir()))
            return model

    @staticmethod
    def get_params(model) -> Dict:  # TODO check if this actually gets the parameter
        """
        Extracts the parameters of the model.
        :param model: The model
        """
        return json.loads(model.to_json())
