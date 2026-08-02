# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event, Thread
from types import ModuleType

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

    def test_concurrent_registration_returns_one_configured_module(self):
        """Publish one canonical lazy module when multiple threads register the same name."""
        marker = self.path / "registered-load"
        self.write_module(
            "registered_module",
            f"from pathlib import Path\nPath({str(marker)!r}).touch()\nVALUE = 7\n",
        )

        with ThreadPoolExecutor(max_workers=8) as executor:
            modules = list(executor.map(lambda _: lazy_import("registered_module"), range(8)))

        self.assertTrue(all(module is modules[0] for module in modules))
        self.assertIs(modules[0], sys.modules["registered_module"])
        self.assertFalse(marker.exists())
        self.assertEqual(modules[0].VALUE, 7)

    def test_concurrent_circular_modules_do_not_deadlock(self):
        """Serialize mutually dependent lazy modules while allowing same-thread recursive loading."""
        support = ModuleType("cycle_support")
        support.a_started, support.b_started = Event(), Event()
        sys.modules["cycle_support"] = support
        self.module_names.append("cycle_support")
        self.write_module(
            "cycle_a",
            "import cycle_support\n"
            "A_READY = 1\n"
            "cycle_support.a_started.set()\n"
            "cycle_support.b_started.wait(0.2)\n"
            "VALUE = cycle_support.b.B_READY + 1\n",
        )
        self.write_module(
            "cycle_b",
            "import cycle_support\n"
            "B_READY = 1\n"
            "cycle_support.b_started.set()\n"
            "cycle_support.a_started.wait(0.2)\n"
            "VALUE = cycle_support.a.A_READY + 1\n",
        )
        support.a, support.b = lazy_import("cycle_a"), lazy_import("cycle_b")
        values, errors = {}, []

        def access(name, module):
            try:
                values[name] = module.VALUE
            except BaseException as error:
                errors.append(error)

        threads = [
            Thread(target=access, args=("a", support.a), daemon=True),
            Thread(target=access, args=("b", support.b), daemon=True),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(2)

        self.assertFalse(any(thread.is_alive() for thread in threads), "circular lazy imports deadlocked")
        if errors:
            raise errors[0]
        self.assertEqual(values, {"a": 2, "b": 2})

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
