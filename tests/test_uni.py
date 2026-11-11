import runpy
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


WORKFLOW = Path(__file__).resolve().parents[1] / "alfred-search-unicode"
sys.path.insert(0, str(WORKFLOW))

from uni import run_uni_with_arch


class UniTests(unittest.TestCase):
    def test_selects_matching_binary(self):
        for machine, arch in (("x86_64", "amd64"), ("arm64", "arm64")):
            with self.subTest(machine=machine):
                with patch("uni.platform.machine", return_value=machine), patch(
                    "uni.subprocess.check_output", return_value=b"output"
                ) as check_output:
                    self.assertEqual(run_uni_with_arch(["-q", "search", "face"]), "output")
                    check_output.assert_called_once_with(
                        [str(WORKFLOW / f"uni-{arch}"), "-q", "search", "face"]
                    )

    def test_rejects_unsupported_architecture(self):
        with patch("uni.platform.machine", return_value="unknown"), patch(
            "uni.subprocess.check_output"
        ) as check_output:
            with self.assertRaisesRegex(RuntimeError, "Unsupported architecture"):
                run_uni_with_arch([])
            check_output.assert_not_called()

    def test_does_not_hide_execution_errors_or_try_other_binary(self):
        errors = (
            FileNotFoundError("missing binary"),
            PermissionError("not executable"),
            OSError("bad CPU type"),
            subprocess.CalledProcessError(1, "uni"),
        )
        for error in errors:
            with self.subTest(error=error):
                with patch("uni.platform.machine", return_value="arm64"), patch(
                    "uni.subprocess.check_output", side_effect=error
                ) as check_output:
                    with self.assertRaises(type(error)):
                        run_uni_with_arch(["search", "face"])
                    check_output.assert_called_once()

    def test_all_entry_points_use_shared_runner(self):
        for script in ("emoji_search.py", "unicode_search.py", "unicode_identify.py"):
            with self.subTest(script=script):
                with patch.object(sys, "argv", [script, "smile"]), patch(
                    "os.environ", {"UNI_GENDER": "all", "UNI_TONE": "all"}
                ), patch("uni.run_uni_with_arch", return_value="") as runner, patch(
                    "sys.stdout"
                ):
                    runpy.run_path(str(WORKFLOW / script), run_name="__main__")
                    runner.assert_called_once()


if __name__ == "__main__":
    unittest.main()
