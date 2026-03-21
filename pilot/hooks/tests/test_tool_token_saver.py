"""Tests for tool_token_saver hook — rewrites Bash commands via rtk for token savings."""

from __future__ import annotations

import json
import subprocess
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tool_token_saver import (
    MIN_RTK_VERSION,
    _get_rtk_version,
    _parse_version,
    _rewrite_command,
    run_tool_token_saver,
)

HOOK_PATH = Path(__file__).resolve().parent.parent / "tool_token_saver.py"


def _run_with_input(tool_input: dict | None = None, tool_name: str = "Bash") -> tuple[int, str, str]:
    """Simulate hook invocation via direct import. Returns (exit_code, stdout, stderr)."""
    hook_data: dict = {"tool_name": tool_name}
    if tool_input is not None:
        hook_data["tool_input"] = tool_input
    stdin = StringIO(json.dumps(hook_data))
    with (
        patch("sys.stdin", stdin),
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.stderr", new_callable=StringIO) as mock_stderr,
    ):
        code = run_tool_token_saver()
        return code, mock_stdout.getvalue(), mock_stderr.getvalue()


# ---------------------------------------------------------------------------
# _parse_version
# ---------------------------------------------------------------------------


class TestParseVersion:
    """Tests for _parse_version helper."""

    def test_parses_standard_semver(self):
        """_parse_version parses 'X.Y.Z' into an integer tuple."""
        result = _parse_version("0.23.1")
        assert result == (0, 23, 1)

    def test_parses_major_minor_patch_with_prefix_words(self):
        """_parse_version picks the first word that looks like a version."""
        result = _parse_version("  1.2.3  ")
        assert result == (1, 2, 3)

    def test_returns_none_for_non_numeric_string(self):
        """_parse_version returns None for non-version strings."""
        assert _parse_version("not-a-version") is None

    def test_returns_none_for_empty_string(self):
        """_parse_version returns None for empty input."""
        assert _parse_version("") is None

    def test_returns_none_for_partial_garbage(self):
        """_parse_version returns None when parts can't be converted to int."""
        assert _parse_version("a.b.c") is None

    def test_handles_extra_version_components(self):
        """_parse_version takes only the first three components."""
        result = _parse_version("1.2.3.4")
        assert result == (1, 2, 3)


# ---------------------------------------------------------------------------
# _get_rtk_version
# ---------------------------------------------------------------------------


class TestGetRtkVersion:
    """Tests for _get_rtk_version."""

    @patch("subprocess.run")
    def test_returns_version_tuple_from_stdout(self, mock_run):
        """_get_rtk_version extracts a version tuple from rtk --version output."""
        mock_run.return_value = MagicMock(returncode=0, stdout="rtk 0.25.0\n")
        result = _get_rtk_version()
        assert result == (0, 25, 0)

    @patch("subprocess.run")
    def test_returns_none_when_rtk_exits_nonzero(self, mock_run):
        """_get_rtk_version returns None when rtk --version fails."""
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        assert _get_rtk_version() is None

    @patch("subprocess.run")
    def test_returns_none_when_rtk_not_found(self, mock_run):
        """_get_rtk_version returns None when rtk binary is missing."""
        mock_run.side_effect = OSError("No such file")
        assert _get_rtk_version() is None

    @patch("subprocess.run")
    def test_returns_none_on_timeout(self, mock_run):
        """_get_rtk_version returns None when subprocess times out."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="rtk", timeout=5)
        assert _get_rtk_version() is None

    @patch("subprocess.run")
    def test_returns_none_when_no_version_in_output(self, mock_run):
        """_get_rtk_version returns None when output has no parseable version."""
        mock_run.return_value = MagicMock(returncode=0, stdout="no version here\n")
        assert _get_rtk_version() is None


# ---------------------------------------------------------------------------
# _rewrite_command
# ---------------------------------------------------------------------------


class TestRewriteCommand:
    """Tests for _rewrite_command."""

    @patch("subprocess.run")
    def test_returns_rewritten_command_on_success(self, mock_run):
        """_rewrite_command returns the rewritten command when rtk rewrites it."""
        mock_run.return_value = MagicMock(returncode=0, stdout="find . -name '*.py' | head -20\n")
        result = _rewrite_command("find . -name '*.py'")
        assert result == "find . -name '*.py' | head -20"

    @patch("subprocess.run")
    def test_returns_none_when_output_matches_input(self, mock_run):
        """_rewrite_command returns None when rtk outputs the same command (no rewrite)."""
        cmd = "echo hello"
        mock_run.return_value = MagicMock(returncode=0, stdout=cmd + "\n")
        assert _rewrite_command(cmd) is None

    @patch("subprocess.run")
    def test_returns_none_when_output_is_empty(self, mock_run):
        """_rewrite_command returns None when rtk returns empty output."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        assert _rewrite_command("ls -la") is None

    @patch("subprocess.run")
    def test_returns_none_when_rtk_exits_nonzero(self, mock_run):
        """_rewrite_command returns None when rtk rewrite fails."""
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        assert _rewrite_command("some command") is None

    @patch("subprocess.run")
    def test_returns_none_on_os_error(self, mock_run):
        """_rewrite_command returns None when rtk binary is unavailable."""
        mock_run.side_effect = OSError("No such file")
        assert _rewrite_command("ls") is None

    @patch("subprocess.run")
    def test_returns_none_on_timeout(self, mock_run):
        """_rewrite_command returns None when rtk times out."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="rtk", timeout=5)
        assert _rewrite_command("ls") is None


# ---------------------------------------------------------------------------
# run_tool_token_saver — integration-style
# ---------------------------------------------------------------------------


class TestRunToolTokenSaver:
    """Integration tests for run_tool_token_saver."""

    def test_returns_zero_on_invalid_json_input(self):
        """Hook returns 0 (no-op) when stdin contains invalid JSON."""
        with patch("sys.stdin", StringIO("not json {")):
            assert run_tool_token_saver() == 0

    def test_returns_zero_when_no_command_in_input(self):
        """Hook returns 0 when tool_input has no 'command' key."""
        code, _out, _err = _run_with_input(tool_input={})
        assert code == 0

    @patch("shutil.which", return_value=None)
    def test_returns_zero_and_warns_when_rtk_not_installed(self, _mock_which):
        """Hook returns 0 and writes a warning when rtk is not in PATH."""
        code, _out, err = _run_with_input(tool_input={"command": "find . -name '*.py'"})
        assert code == 0
        assert "rtk" in err.lower() or "WARNING" in err

    @patch("tool_token_saver._rewrite_command", return_value=None)
    @patch("tool_token_saver._get_rtk_version", return_value=(1, 0, 0))
    @patch("shutil.which", return_value="/usr/bin/rtk")
    def test_returns_zero_when_no_rewrite_needed(self, _which, _ver, _rewrite):
        """Hook returns 0 without output when rtk has no rewrite for the command."""
        code, out, _err = _run_with_input(tool_input={"command": "echo hello"})
        assert code == 0
        assert out == ""

    @patch("tool_token_saver._rewrite_command", return_value="find . | head -20")
    @patch("tool_token_saver._get_rtk_version", return_value=(1, 0, 0))
    @patch("shutil.which", return_value="/usr/bin/rtk")
    def test_outputs_updated_input_json_when_rewrite_occurs(self, _which, _ver, _rewrite):
        """Hook outputs JSON with updated command when rtk rewrites it."""
        code, out, _err = _run_with_input(tool_input={"command": "find ."})
        assert code == 0
        data = json.loads(out)
        hook_out = data["hookSpecificOutput"]
        assert hook_out["permissionDecision"] == "allow"
        assert hook_out["updatedInput"]["command"] == "find . | head -20"

    @patch("tool_token_saver._rewrite_command", return_value="find . | head -20")
    @patch("tool_token_saver._get_rtk_version", return_value=(1, 0, 0))
    @patch("shutil.which", return_value="/usr/bin/rtk")
    def test_preserves_other_input_fields_when_rewriting(self, _which, _ver, _rewrite):
        """Hook preserves extra fields in tool_input when rewriting the command."""
        original_input = {"command": "find .", "timeout": 30, "restart": False}
        code, out, _err = _run_with_input(tool_input=original_input)
        assert code == 0
        data = json.loads(out)
        updated = data["hookSpecificOutput"]["updatedInput"]
        assert updated["timeout"] == 30
        assert updated["restart"] is False

    @patch("tool_token_saver._get_rtk_version", return_value=(0, 22, 9))
    @patch("shutil.which", return_value="/usr/bin/rtk")
    def test_warns_and_skips_when_rtk_version_too_old(self, _which, _ver):
        """Hook warns and returns 0 without rewriting when rtk is below minimum version."""
        code, out, err = _run_with_input(tool_input={"command": "find ."})
        assert code == 0
        assert out == ""
        assert "WARNING" in err or "too old" in err.lower() or "rtk" in err.lower()

    @patch("tool_token_saver._rewrite_command", return_value="ls -la")
    @patch("tool_token_saver._get_rtk_version", return_value=MIN_RTK_VERSION)
    @patch("shutil.which", return_value="/usr/bin/rtk")
    def test_accepts_minimum_rtk_version(self, _which, _ver, _rewrite):
        """Hook proceeds normally when rtk is exactly the minimum required version."""
        code, out, _err = _run_with_input(tool_input={"command": "ls"})
        assert code == 0
        data = json.loads(out)
        assert data["hookSpecificOutput"]["updatedInput"]["command"] == "ls -la"

    def test_returns_zero_when_tool_input_key_missing(self):
        """Hook returns 0 when hook_data has no 'tool_input' at all."""
        hook_data = {"tool_name": "Bash"}
        stdin = StringIO(json.dumps(hook_data))
        with patch("sys.stdin", stdin):
            assert run_tool_token_saver() == 0


# ---------------------------------------------------------------------------
# MIN_RTK_VERSION constant
# ---------------------------------------------------------------------------


class TestMinRtkVersion:
    """Ensure the minimum version constant is correctly defined."""

    def test_min_rtk_version_is_tuple_of_ints(self):
        """MIN_RTK_VERSION is a tuple of three integers."""
        assert isinstance(MIN_RTK_VERSION, tuple)
        assert len(MIN_RTK_VERSION) == 3
        assert all(isinstance(v, int) for v in MIN_RTK_VERSION)

    def test_min_rtk_version_is_at_least_0_23_0(self):
        """MIN_RTK_VERSION is at least (0, 23, 0)."""
        assert MIN_RTK_VERSION >= (0, 23, 0)
