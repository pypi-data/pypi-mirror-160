from ezinfer.base_infer import BaseInfer
import onnxruntime

class OnnxInfer(BaseInfer):
    def __init__(self, model_path:str, use_gpu:bool=False, **kwargs):
        self._src = model_path
        self._use_gpu = use_gpu
        self._load_weights(kwargs=kwargs)
    
    def _load_weights(self, **kwargs):
        providers = ['CUDAExecutionProvider'] if self._use_gpu else ['CPUExecutionProvider']
        self._session = onnxruntime.InferenceSession(self._src, providers=providers, kwargs=kwargs)
        self._input_name = self._session.get_inputs()[0].name
        self._output_name = self._session.get_outputs()[0].name
    
    def __call__(self, input, **kwargs):
        return self._session.run(
            output_names=[self._output_name],
            input_feed={self._input_name: self.force_input(input)},
            kwargs=kwargs
        )
    
    def get_session(self):
        return self._session