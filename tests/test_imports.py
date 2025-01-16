# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import time
import unittest
from autoimport import LazyLoader, lazy

class TestLazyImports(unittest.TestCase):
    """Test suite for lazy imports functionality."""

    def test_simple_imports(self):
        """Test basic import statements."""
        with lazy():
            import json
        self.assertIsInstance(json, LazyLoader)

    def test_attribute_access(self):
        """Test accessing attributes triggers actual import."""
        with lazy():
            import json
        t0 = time.perf_counter()
        result = json.dumps({"test": 123})
        self.assertIsInstance(result, str)
        self.assertLess(time.perf_counter() - t0, 1.0)

    def test_nested_imports(self):
        """Test nested module imports and functionality."""
        with lazy():
            import numpy as np
        random_number = np.random.rand()
        self.assertLess(random_number, 1.0)

    def test_direct_lazyloader(self):
        """Test direct LazyLoader instantiation."""
        base64_lazy = LazyLoader("base64")
        t0 = time.perf_counter()
        result = base64_lazy.b64encode(b'test')
        self.assertEqual(result, b'dGVzdA==')
        self.assertLess(time.perf_counter() - t0, 1.0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
