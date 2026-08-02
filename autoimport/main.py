# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import importlib
import importlib.util
import sys
from threading import RLock
from types import ModuleType

_LOCK = RLock()


class _LazyModule(ModuleType):
    """Module type that executes its loader once on first attribute access."""

    def __getattribute__(self, attr):
        """Load the module before returning an attribute."""
        spec = object.__getattribute__(self, "__spec__")
        state = spec.loader_state
        with _LOCK:
            if object.__getattribute__(self, "__class__") is _LazyModule:
                original_class = state["__class__"]
                if state["is_loading"]:
                    return original_class.__getattribute__(self, attr)

                state["is_loading"] = True
                namespace = original_class.__getattribute__(self, "__dict__")
                initial = state["__dict__"]
                updated = {
                    key: value
                    for key, value in namespace.items()
                    if key not in initial or id(value) != id(initial[key])
                }
                try:
                    spec.loader.exec_module(self)
                    if spec.name in sys.modules and sys.modules[spec.name] is not self:
                        raise ValueError(f"module object for {spec.name!r} substituted in sys.modules during lazy load")
                except BaseException:
                    namespace.clear()
                    namespace.update(initial)
                    namespace.update(updated)
                    if object.__getattribute__(self, "__class__") is not _LazyModule:
                        object.__setattr__(self, "__class__", _LazyModule)
                    raise
                else:
                    namespace.update(updated)
                    if object.__getattribute__(self, "__class__") is _LazyModule:
                        object.__setattr__(self, "__class__", original_class)
                finally:
                    state["is_loading"] = False

        return getattr(self, attr)

    def __delattr__(self, attr):
        """Load before deletion while allowing module code to delete its own attributes."""
        spec = object.__getattribute__(self, "__spec__")
        state = spec.loader_state
        with _LOCK:
            if state["is_loading"]:
                return state["__class__"].__delattr__(self, attr)
            self.__getattribute__(attr)
            return state["__class__"].__delattr__(self, attr)


class _LazyLoader(importlib.util.LazyLoader):
    """Configure modules for thread-safe, retryable lazy execution."""

    def exec_module(self, module):
        """Store eager-loader state and defer execution of the module body."""
        module.__spec__.loader = self.loader
        module.__loader__ = self.loader
        module.__spec__.loader_state = {
            "__dict__": module.__dict__.copy(),
            "__class__": module.__class__,
            "is_loading": False,
        }
        module.__class__ = _LazyModule


def lazy_import(name: str) -> ModuleType:
    """Return a module whose execution is deferred until its first attribute access.

    Module discovery happens immediately, so an invalid name raises ``ModuleNotFoundError`` at this call. If the module
    is already present in ``sys.modules``, that existing module is returned unchanged.

    Args:
        name (str): Fully qualified module name, such as ``"torch"`` or ``"numpy.linalg"``.

    Returns:
        (ModuleType): Module object registered in ``sys.modules`` and configured for lazy execution.
    """
    with _LOCK:
        if name in sys.modules:
            module = sys.modules[name]
            if module is None:
                raise ModuleNotFoundError(f"import of {name!r} halted; None in sys.modules", name=name)
            return module

        spec = importlib.util.find_spec(name)
        if spec is None:
            raise ModuleNotFoundError(f"No module named {name!r}", name=name)
        if spec.loader is None:  # Namespace packages have no module body to defer.
            return importlib.import_module(name)

        loader = _LazyLoader(spec.loader)
        spec.loader = loader
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        sys.modules[name] = module
        if "." in name:
            parent_name, _, child_name = name.rpartition(".")
            setattr(sys.modules[parent_name], child_name, module)
        return module
