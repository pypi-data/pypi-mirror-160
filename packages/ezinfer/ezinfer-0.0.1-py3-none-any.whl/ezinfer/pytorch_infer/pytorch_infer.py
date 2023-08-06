from ezinfer.base_infer import BaseInfer
import torch

class PytorchInfer(BaseInfer):
    def __init__(self, weights:str, model_obj: torch.nn.Module, use_gpu:bool=False, **kwargs):
        self._weights_path = weights
        self._model = model_obj
        self._device = torch.device('cpu') if use_gpu else torch.device('cuda')
        self._load_weights(kwargs=kwargs)
    
    def _load_weights(self, **kwargs):
        self._model.load_state_dict(torch.load(self._weights_path, map_location=self._device, pickle_load_args=kwargs))
        self._model.to(self._device)
        self._model.eval()

    def __call__(self, input, **kwargs):
        return self._model(self.force_input(input), kwargs=kwargs)

    def get_session(self):
        return self._model    