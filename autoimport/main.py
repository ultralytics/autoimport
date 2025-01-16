# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import builtins
import importlib
import sys
import time
import types


class LazyLoader(types.ModuleType):
    """Lazy loading module wrapper."""

    def __init__(self, name):
        """Initializes a lazy-loading module wrapper that defers actual module imports until first access."""
        super().__init__(name)
        self.__path__ = [name]  # Required for some packages to work correctly
        self._module = None
        self._loading = False  # Flag to indicate if we are already loading

    def _load_module(self):
        """Loads and caches a module on first access using Python's importlib to enable lazy module importing."""
        if self._module is None and not self._loading:
            self._loading = True  # Set loading flag
            try:
                self._module = importlib.import_module(self.__name__)
            finally:
                self._loading = False  # Reset loading flag

    def __getattr__(self, attr):
        """Lazily loads and returns module attributes when first accessed via attribute lookup."""
        self._load_module()
        return getattr(self._module, attr)

    def __dir__(self):  # For better autocompletion
        """Returns built-in dir() result when module is not loaded to support autocompletion without triggering load."""
        if self._module is not None:  # Only load if already loaded
            return dir(self._module)
        else:
            return super().__dir__()  # Return default dir() for unloaded modules

    def __repr__(self):
        """Returns a string representation of the LazyLoader module wrapper instance."""
        return f"<LazyLoader for '{self.__name__}'>"


class lazy:
    """Context manager for lazy imports."""

    def __init__(self):
        """Initializes a context manager for lazy module imports to optimize startup time and memory usage."""
        self._original_import = builtins.__import__
        self._lazy_modules = {}  # Store lazy modules here

    def __enter__(self):
        """Enters a context where imports are lazy-loaded, replacing Python's default import mechanism."""

        def lazy_import(name, globals=None, locals=None, fromlist=(), level=0):
            module_name = name
            if level > 0:
                # Calculate absolute name for relative imports
                package = globals["__package__"]
                for _ in range(level - 1):
                    package = package.rpartition(".")[0]
                module_name = f"{package}.{name}" if package else name

            if fromlist:
                # Handle 'from x import y'
                for from_item in fromlist:
                    full_name = f"{module_name}.{from_item}"
                    if full_name not in self._lazy_modules:
                        self._lazy_modules[full_name] = LazyLoader(full_name)

                # Return a proxy namespace to access LazyLoaders
                return types.SimpleNamespace(
                    **{from_item: self._lazy_modules[f"{module_name}.{from_item}"] for from_item in fromlist}
                )
            else:
                if module_name not in self._lazy_modules:
                    self._lazy_modules[module_name] = LazyLoader(module_name)
                return self._lazy_modules[module_name]

        builtins.__import__ = lazy_import
        return self

    def __exit__(self, *args):
        """Restores the original import mechanism and updates sys.modules with any loaded lazy modules."""
        builtins.__import__ = self._original_import
        # Now that builtins is restored, we can load any modules that need loading
        for name, lazy_module in self._lazy_modules.items():
            if name in sys.modules:  # Update sys.modules to avoid issues with subsequent imports
                sys.modules[name] = lazy_module


if __name__ == "__main__":
    # Context manager tests -----------------------------
    with lazy():
        t0 = time.perf_counter()
        import numpy as np
        import seaborn
        import torch
        from numpy import linalg
        from torch import cuda, nn

        print(time.perf_counter() - t0)

    t1 = time.perf_counter()
    print(cuda.is_available())
    print(time.perf_counter() - t1)

    t2 = time.perf_counter()
    print(torch.cuda.is_available())
    print(time.perf_counter() - t2)

    t3 = time.perf_counter()
    net = nn.Linear(10, 2)
    print(net)
    print(time.perf_counter() - t3)

    t5 = time.perf_counter()
    A = np.array([[1, 2], [3, 4]])
    print(linalg.det(A))
    print(time.perf_counter() - t5)

    # Direct LazyLoader() tests ------------------------
    t6 = time.perf_counter()
    seaborn_lazy = LazyLoader("seaborn")
    print(time.perf_counter() - t6)

    t7 = time.perf_counter()
    print(seaborn.colors.crayons)
    print(time.perf_counter() - t7)
