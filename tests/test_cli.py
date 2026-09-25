import subprocess
import sys


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_calc_success():
    result = run_cli("calc", "2+3")
    assert result.returncode == 0
    assert result.stdout.strip() == "5"


def test_cli_calc_error():
    result = run_cli("calc", "5/0")
    assert result.returncode == 2
    assert "Error" in result.stderr
