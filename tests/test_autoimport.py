# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import time
import unittest
from autoimport import LazyLoader, lazy

class TestLazyImports(unittest.TestCase):
    """Test suite for lazy imports functionality."""

    def test_simple_imports(self):
        """Test basic import statements."""
        with lazy():
            import numpy as np
        random_number = np.random.rand()
        self.assertIsInstance(json, LazyLoader)
        self.assertLess(random_number, 1.0)
        
    def test_attribute_access(self):
        """Test accessing attributes triggers actual import."""
        with lazy():
            import json
        result = json.dumps({"test": 123})
        self.assertIsInstance(result, str)

    def test_submodule_imports(self):
        """Test nested module imports and functionality."""
        with lazy():
            import numpy.random
        random_number = numpy.random.rand()
        self.assertLess(random_number, 1.0)

    def test_direct_lazyloader(self):
        """Test direct LazyLoader instantiation."""
        base64_lazy = LazyLoader("base64")
        result = base64_lazy.b64encode(b'test')
        self.assertEqual(result, b'dGVzdA==')

if __name__ == '__main__':
    unittest.main(verbosity=2)
