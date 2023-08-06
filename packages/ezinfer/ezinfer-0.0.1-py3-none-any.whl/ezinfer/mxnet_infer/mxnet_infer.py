import mxnet as mx
from mxnet import gluon, nd
from ezinfer.base_infer import BaseInfer

class MxnetInfer(BaseInfer):
    def __init__(self, weights:str, model_obj:gluon.nn.Sequential, use_gpu:bool=False, **kwargs):
        self._weights_path = weights
        self._model = model_obj
        self._context = mx.gpu() if use_gpu else mx.cpu()
        self._load_weights(kwargs=kwargs)
    
    def _load_weights(self, **kwargs):
        self._model.load_parameters(self._weights_path, ctx=self._context, kwargs=kwargs)

    def __call__(self, input, **kwargs):
        return self._model(nd.array(self.force_input(input), ctx=self._context), kwargs=kwargs)

    def get_session(self):
        return self._model