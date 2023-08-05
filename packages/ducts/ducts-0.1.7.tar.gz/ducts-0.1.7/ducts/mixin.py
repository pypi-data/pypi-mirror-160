import inspect
from collections import OrderedDict

class DelegateModuleMixin:

    def __init__(self, event_key):
        self.event_key = event_key
        self.method_name = method_name
        

class MixinParameter:

    @classmethod
    def create(cls, param: inspect.Parameter):
        return MixinParameter(param.name, param.annotation, param.kind, param.default)

    def __init__(self, name: str, annotation: type, kind, default):
        self._name = name
        self._annotaion = annotation if annotation != inspect.Parameter.empty else None
        if kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.VAR_POSITIONAL,  inspect.Parameter.VAR_KEYWORD):
            raise ValueError('kind:[{}] is not supported.'.format(kind))
        self._kind = kind
        self._default = default
        
    @property
    def name(self):
        return self._name

    @property
    def annotation(self):
        return self._annotaion

    @property
    def is_var_args(self):
        return self._kind == inspect.Parameter.VAR_POSITIONAL

    @property
    def is_var_kwargs(self):
        return self._kind == inspect.Parameter.VAR_KEYWORD

    @property
    def is_mandatory(self):
        return self._kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and self._default == inspect.Parameter.empty
    
    @property
    def default(self):
        return default if default != inspect.Parameter.empty else None
        
class MixinMethod:

    @classmethod
    def create(cls, func):
        name = func.__name__
        print(name)
        sig = inspect.signature(func)
        print(sig)
        m = MixinMethod(name)
        m.set_return_annotation(sig.return_annotation)
        for name, param in sig.parameters.items():
            m.append_parameter(MixinParameter.create(param))
        return m

    def __init__(self, method_name):
        self._name = method_name
        self._parameters = OrderedDict()
        self._return_annotation = None

    def set_return_annotation(self, annotation: type = None):
        self._return_annotation = annotation
    
    def append_parameter(self, parameter: MixinParameter):
        if parameter.name in self._parameters:
            raise KeyError('parameter:[{}] already exists'.format(name))
        self._parameters[parameter.name] = parameter

class MixinModule:

    def __init__(self, module_name: str):
        self._name = module_name
        self._methods = OrderedDict()

    def append_method(self, method: MixinMethod):
        self._methods.append(method)

