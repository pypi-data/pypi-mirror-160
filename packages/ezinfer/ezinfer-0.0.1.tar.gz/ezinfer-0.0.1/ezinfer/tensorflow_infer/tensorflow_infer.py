from ezinfer.base_infer import BaseInfer
import tensorflow as tf
from tensorflow import keras
class TensorflowInfer(BaseInfer):
    def __init__(self, model_path:str, use_gpu:bool=False, **kwargs):
        self._src = model_path
        if not use_gpu:
            tf.config.set_visible_devices([], "GPU")
        self._load_weights(kwargs=kwargs)

    def _load_weights(self, **kwargs):
        self._model = keras.models.load_model(self._src, kwargs=kwargs)

    
    def __call__(self, input, **kwargs):
        return self._model(self.force_input(input), training=False, kwargs=kwargs)

    def get_session(self):
        return self._model