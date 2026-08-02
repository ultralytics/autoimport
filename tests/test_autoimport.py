# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from autoimport import lazy_import


class TestLazyImport(unittest.TestCase):
    """Test explicit lazy module imports."""

    def setUp(self):
        """Create an isolated import directory for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name)
        sys.path.insert(0, str(self.path))
        self.module_names = []

    def tearDown(self):
        """Remove temporary modules and their import path."""
        sys.path.remove(str(self.path))
        for name in self.module_names:
            sys.modules.pop(name, None)
        self.temp_dir.cleanup()

    def write_module(self, name, source):
        """Write a temporary module and register its name for cleanup."""
        path = self.path.joinpath(*name.split(".")).with_suffix(".py")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        self.module_names.append(name)

    def test_defers_execution_until_first_attribute(self):
        """Defer the module body while preserving repeated access and sys.modules identity."""
        marker = self.path / "loaded"
        self.write_module("deferred_module", f"from pathlib import Path\nPath({str(marker)!r}).touch()\nFIRST = 1\nSECOND = 2\n")

        module = lazy_import("deferred_module")

        self.assertFalse(marker.exists())
        self.assertIs(module, sys.modules["deferred_module"])
        self.assertEqual(module.FIRST, 1)
        self.assertTrue(marker.exists())
        self.assertEqual(module.SECOND, 2)
        self.assertIs(module, sys.modules["deferred_module"])

    def test_returns_existing_module(self):
        """Reuse the canonical module when it has already been imported."""
        self.assertIs(lazy_import("sys"), sys)

    def test_missing_module_raises_immediately(self):
        """Report invalid module names during discovery instead of hiding typos until use."""
        name = "definitely_missing_autoimport_test_module"
        with self.assertRaises(ModuleNotFoundError):
            lazy_import(name)
        self.assertNotIn(name, sys.modules)

    def test_defers_module_execution_error(self):
        """Raise errors on first use and retry the clean module body on later access."""
        marker = self.path / "attempts"
        self.write_module(
            "broken_module",
            f"from pathlib import Path\n"
            f"marker = Path({str(marker)!r})\n"
            f"attempt = int(marker.read_text()) + 1 if marker.exists() else 1\n"
            f"marker.write_text(str(attempt))\n"
            f"if attempt == 1:\n    raise RuntimeError('broken import')\n"
            f"VALUE = 4\n",
        )

        module = lazy_import("broken_module")

        with self.assertRaisesRegex(RuntimeError, "broken import"):
            module.VALUE
        self.assertEqual(module.VALUE, 4)
        self.assertEqual(marker.read_text(), "2")

    def test_module_can_delete_attributes_while_loading(self):
        """Allow module initialization code to delete attributes from its canonical module object."""
        self.write_module(
            "deleting_module",
            "import sys\nREMOVE = True\ndelattr(sys.modules[__name__], 'REMOVE')\nVALUE = 5\n",
        )

        module = lazy_import("deleting_module")

        self.assertEqual(module.VALUE, 5)
        self.assertFalse(hasattr(module, "REMOVE"))

    def test_first_access_is_thread_safe(self):
        """Execute the module body once when multiple threads make the first access concurrently."""
        marker = self.path / "thread-loads"
        self.write_module(
            "threaded_module",
            f"from pathlib import Path\n"
            f"from time import sleep\n"
            f"marker = Path({str(marker)!r})\n"
            f"count = int(marker.read_text()) + 1 if marker.exists() else 1\n"
            f"sleep(0.05)\n"
            f"marker.write_text(str(count))\n"
            f"VALUE = 6\n",
        )
        module = lazy_import("threaded_module")

        with ThreadPoolExecutor(max_workers=8) as executor:
            values = list(executor.map(lambda _: module.VALUE, range(8)))

        self.assertEqual(values, [6] * 8)
        self.assertEqual(marker.read_text(), "1")

    def test_dotted_module_defers_child_execution(self):
        """Import dotted modules while deferring the requested child module body."""
        package = self.path / "lazy_package"
        package.mkdir()
        (package / "__init__.py").write_text("PARENT = True\n")
        marker = self.path / "child-loaded"
        (package / "child.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\nVALUE = 3\n")
        self.module_names.extend(("lazy_package.child", "lazy_package"))

        module = lazy_import("lazy_package.child")

        self.assertIn("lazy_package", sys.modules)
        self.assertIs(sys.modules["lazy_package"].child, module)
        self.assertFalse(marker.exists())
        self.assertEqual(module.VALUE, 3)
        self.assertTrue(marker.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
