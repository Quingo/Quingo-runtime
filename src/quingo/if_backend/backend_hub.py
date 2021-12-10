import importlib


class Backend_info():
    def __init__(self, module_name, module_path,  with_timing, is_simulator):
        self.module_name = module_name
        self.module_path = module_path
        self.with_timing = with_timing
        self.is_simulator = is_simulator

    def get_module(self):
        if self.with_timing:
            prefix = 'quingo.if_backend.arch_backend.'
        else:
            prefix = 'quingo.if_backend.non_arch_backend.'

        full_module_path = prefix + self.module_path
        try:
            module = importlib.import_module(full_module_path)
        except:
            print("Cannot import the backend from '{}'".format(full_module_path))
            raise SystemError(
                "Cannot import the backend from '{}'".format(full_module_path))
        return module

    def get_instance(self):
        return getattr(self.get_module(), self.module_name)()


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class Backend_hub():
    def __init__(self):
        self.backends = {}

        self.backends['pyqcas_quantumsim'] = Backend_info(
            'PyQCAS_quantumsim', 'pyqcas_quantumsim', with_timing=False,
            is_simulator=True)

        self.backends['pyqcisim_quantumsim'] = Backend_info(
            'PyQCISim_quantumsim', 'pyqcisim_quantumsim', with_timing=False,
            is_simulator=True)

    def support(self, backend_name):
        return (backend_name in self.backends)

    def get_instance(self, backend_name):
        backend_info = self.backends[backend_name]
        return backend_info.get_instance()
