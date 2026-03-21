"""Extended tests for installer CLI — covers functions not tested in test_cli.py.

Covers: _get_trial_days_remaining, _start_trial, _check_trial_used,
        _validate_license_key, _prompt_license_key, cmd_launch,
        find_pilot_binary, cmd_version.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest


# ---------------------------------------------------------------------------
# _get_trial_days_remaining
# ---------------------------------------------------------------------------


class TestGetTrialDaysRemaining:
    """Tests for _get_trial_days_remaining."""

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_days_from_json_on_success(self, mock_run, mock_home, tmp_path: Path):
        """_get_trial_days_remaining returns days_remaining from pilot JSON output."""
        from installer.cli import _get_trial_days_remaining

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        pilot_bin = bin_dir / "pilot"
        pilot_bin.touch()

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"days_remaining": 5}),
        )

        result = _get_trial_days_remaining(pilot_bin)
        assert result == 5

    @patch("subprocess.run")
    def test_defaults_to_7_on_subprocess_error(self, mock_run, tmp_path: Path):
        """_get_trial_days_remaining defaults to 7 when subprocess raises."""
        from installer.cli import _get_trial_days_remaining

        mock_run.side_effect = OSError("No such file")
        pilot_bin = tmp_path / "pilot"

        assert _get_trial_days_remaining(pilot_bin) == 7

    @patch("subprocess.run")
    def test_defaults_to_7_on_invalid_json(self, mock_run, tmp_path: Path):
        """_get_trial_days_remaining defaults to 7 when output is not valid JSON."""
        from installer.cli import _get_trial_days_remaining

        mock_run.return_value = MagicMock(returncode=0, stdout="not json")
        pilot_bin = tmp_path / "pilot"

        assert _get_trial_days_remaining(pilot_bin) == 7

    @patch("subprocess.run")
    def test_defaults_to_7_on_nonzero_exit(self, mock_run, tmp_path: Path):
        """_get_trial_days_remaining defaults to 7 when pilot exits non-zero."""
        from installer.cli import _get_trial_days_remaining

        mock_run.return_value = MagicMock(returncode=1, stdout="")
        pilot_bin = tmp_path / "pilot"

        assert _get_trial_days_remaining(pilot_bin) == 7

    @patch("subprocess.run")
    def test_defaults_to_7_when_days_remaining_missing(self, mock_run, tmp_path: Path):
        """_get_trial_days_remaining defaults to 7 when JSON has no days_remaining key."""
        from installer.cli import _get_trial_days_remaining

        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps({"other_key": 3}))
        pilot_bin = tmp_path / "pilot"

        assert _get_trial_days_remaining(pilot_bin) == 7

    @patch("subprocess.run")
    def test_defaults_to_7_on_timeout(self, mock_run, tmp_path: Path):
        """_get_trial_days_remaining defaults to 7 when subprocess times out."""
        from installer.cli import _get_trial_days_remaining

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pilot", timeout=10)
        pilot_bin = tmp_path / "pilot"

        assert _get_trial_days_remaining(pilot_bin) == 7


# ---------------------------------------------------------------------------
# _start_trial
# ---------------------------------------------------------------------------


class TestStartTrial:
    """Tests for _start_trial."""

    @patch("installer.cli.Path.home")
    def test_returns_none_when_pilot_binary_missing(self, mock_home, tmp_path: Path):
        """_start_trial returns None when pilot binary doesn't exist."""
        from installer.cli import _start_trial
        from installer.ui import Console

        mock_home.return_value = tmp_path
        console = Console(non_interactive=True, quiet=True)

        result = _start_trial(console, tmp_path, False, None)
        assert result is None

    @patch("installer.cli._get_trial_days_remaining", return_value=7)
    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_days_remaining_on_success(self, mock_run, mock_home, _mock_days, tmp_path: Path):
        """_start_trial returns days remaining when trial starts successfully."""
        from installer.cli import _start_trial
        from installer.ui import Console

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        console = Console(non_interactive=True, quiet=True)

        result = _start_trial(console, tmp_path, False, None)
        assert result == 7

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_none_when_trial_already_used(self, mock_run, mock_home, tmp_path: Path):
        """_start_trial returns None when pilot reports trial_already_used."""
        from installer.cli import _start_trial
        from installer.ui import Console

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(
            returncode=1,
            stdout=json.dumps({"error": "trial_already_used"}),
            stderr="",
        )
        console = Console(non_interactive=True, quiet=True)

        result = _start_trial(console, tmp_path, False, None)
        assert result is None

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_none_on_timeout(self, mock_run, mock_home, tmp_path: Path):
        """_start_trial returns None when subprocess times out."""
        from installer.cli import _start_trial
        from installer.ui import Console

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pilot", timeout=30)
        console = Console(non_interactive=True, quiet=True)

        result = _start_trial(console, tmp_path, False, None)
        assert result is None


# ---------------------------------------------------------------------------
# _check_trial_used
# ---------------------------------------------------------------------------


class TestCheckTrialUsed:
    """Tests for _check_trial_used."""

    @patch("installer.cli.Path.home")
    def test_returns_none_false_when_binary_missing(self, mock_home, tmp_path: Path):
        """_check_trial_used returns (None, False) when pilot binary doesn't exist."""
        from installer.cli import _check_trial_used

        mock_home.return_value = tmp_path
        trial_used, can_reactivate = _check_trial_used(tmp_path, False, None)

        assert trial_used is None
        assert can_reactivate is False

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_trial_used_and_can_reactivate_from_json(self, mock_run, mock_home, tmp_path: Path):
        """_check_trial_used parses trial_used and can_reactivate from pilot JSON output."""
        from installer.cli import _check_trial_used

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"trial_used": True, "can_reactivate": True}),
            stderr="",
        )

        trial_used, can_reactivate = _check_trial_used(tmp_path, False, None)
        assert trial_used is True
        assert can_reactivate is True

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_false_false_when_trial_not_used(self, mock_run, mock_home, tmp_path: Path):
        """_check_trial_used returns (False, False) when trial has not been used."""
        from installer.cli import _check_trial_used

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"trial_used": False, "can_reactivate": False}),
            stderr="",
        )

        trial_used, can_reactivate = _check_trial_used(tmp_path, False, None)
        assert trial_used is False
        assert can_reactivate is False

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_none_false_on_invalid_json(self, mock_run, mock_home, tmp_path: Path):
        """_check_trial_used returns (None, False) when pilot output is not valid JSON."""
        from installer.cli import _check_trial_used

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(returncode=0, stdout="not json", stderr="")

        trial_used, can_reactivate = _check_trial_used(tmp_path, False, None)
        assert trial_used is None
        assert can_reactivate is False

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_none_false_on_timeout(self, mock_run, mock_home, tmp_path: Path):
        """_check_trial_used returns (None, False) when subprocess times out."""
        from installer.cli import _check_trial_used

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pilot", timeout=30)

        trial_used, can_reactivate = _check_trial_used(tmp_path, False, None)
        assert trial_used is None
        assert can_reactivate is False


# ---------------------------------------------------------------------------
# _validate_license_key
# ---------------------------------------------------------------------------


class TestValidateLicenseKey:
    """Tests for _validate_license_key."""

    @patch("installer.cli.Path.home")
    def test_warns_and_returns_true_when_pilot_binary_missing(self, mock_home, tmp_path: Path):
        """_validate_license_key returns True (skip) when pilot binary doesn't exist."""
        from installer.cli import _validate_license_key
        from installer.ui import Console

        mock_home.return_value = tmp_path
        console = Console(non_interactive=True, quiet=True)

        result = _validate_license_key(console, tmp_path, "TEST-KEY")
        assert result is True

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_true_on_successful_activation(self, mock_run, mock_home, tmp_path: Path):
        """_validate_license_key returns True when pilot activate succeeds."""
        from installer.cli import _validate_license_key
        from installer.ui import Console

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        console = Console(non_interactive=True, quiet=True)

        result = _validate_license_key(console, tmp_path, "VALID-KEY")
        assert result is True

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_returns_false_on_failed_activation(self, mock_run, mock_home, tmp_path: Path):
        """_validate_license_key returns False when pilot activate fails."""
        from installer.cli import _validate_license_key
        from installer.ui import Console

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        (bin_dir / "pilot").touch()

        mock_run.return_value = MagicMock(
            returncode=1,
            stdout=json.dumps({"error": "invalid_key"}),
            stderr="",
        )
        console = Console(non_interactive=True, quiet=True)

        result = _validate_license_key(console, tmp_path, "INVALID-KEY")
        assert result is False

    @patch("installer.cli.Path.home")
    @patch("subprocess.run")
    def test_passes_license_key_to_pilot_activate(self, mock_run, mock_home, tmp_path: Path):
        """_validate_license_key passes the license key as an argument to pilot activate."""
        from installer.cli import _validate_license_key
        from installer.ui import Console

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        pilot_bin = bin_dir / "pilot"
        pilot_bin.touch()

        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        console = Console(non_interactive=True, quiet=True)

        _validate_license_key(console, tmp_path, "MY-LICENSE-KEY")

        call_args = mock_run.call_args[0][0]
        assert "activate" in call_args
        assert "MY-LICENSE-KEY" in call_args


# ---------------------------------------------------------------------------
# _prompt_license_key
# ---------------------------------------------------------------------------


class TestPromptLicenseKey:
    """Tests for _prompt_license_key."""

    @patch("installer.cli._validate_license_key", return_value=True)
    def test_returns_true_on_first_valid_key(self, _mock_validate, tmp_path: Path):
        """_prompt_license_key returns True immediately on a valid key."""
        from installer.cli import _prompt_license_key
        from installer.ui import Console

        console = Console(non_interactive=True, quiet=True)
        with patch.object(console, "input", return_value="VALID-KEY"):
            result = _prompt_license_key(console, tmp_path)

        assert result is True

    @patch("installer.cli._validate_license_key", return_value=False)
    def test_returns_false_after_max_attempts_with_invalid_key(self, _mock_validate, tmp_path: Path):
        """_prompt_license_key returns False after exhausting all attempts."""
        from installer.cli import _prompt_license_key
        from installer.ui import Console

        console = Console(non_interactive=True, quiet=True)
        with patch.object(console, "input", return_value="BAD-KEY"):
            result = _prompt_license_key(console, tmp_path, max_attempts=3)

        assert result is False
        assert _mock_validate.call_count == 3

    def test_returns_false_when_empty_key_entered_repeatedly(self, tmp_path: Path):
        """_prompt_license_key returns False when user repeatedly enters empty key."""
        from installer.cli import _prompt_license_key
        from installer.ui import Console

        console = Console(non_interactive=True, quiet=True)
        with patch.object(console, "input", return_value="   "):
            result = _prompt_license_key(console, tmp_path, max_attempts=2)

        assert result is False

    @patch("installer.cli._validate_license_key", side_effect=[False, False, True])
    def test_succeeds_on_third_attempt(self, _mock_validate, tmp_path: Path):
        """_prompt_license_key returns True when key is valid on the third try."""
        from installer.cli import _prompt_license_key
        from installer.ui import Console

        console = Console(non_interactive=True, quiet=True)
        with patch.object(console, "input", return_value="SOME-KEY"):
            result = _prompt_license_key(console, tmp_path, max_attempts=3)

        assert result is True
        assert _mock_validate.call_count == 3


# ---------------------------------------------------------------------------
# find_pilot_binary
# ---------------------------------------------------------------------------


class TestFindPilotBinary:
    """Tests for find_pilot_binary."""

    @patch("installer.cli.Path.home")
    def test_returns_path_when_binary_exists(self, mock_home, tmp_path: Path):
        """find_pilot_binary returns the path to the pilot binary when it exists."""
        from installer.cli import find_pilot_binary

        mock_home.return_value = tmp_path
        bin_dir = tmp_path / ".pilot" / "bin"
        bin_dir.mkdir(parents=True)
        pilot = bin_dir / "pilot"
        pilot.touch()

        result = find_pilot_binary()
        assert result == pilot

    @patch("installer.cli.Path.home")
    def test_returns_none_when_binary_missing(self, mock_home, tmp_path: Path):
        """find_pilot_binary returns None when the pilot binary doesn't exist."""
        from installer.cli import find_pilot_binary

        mock_home.return_value = tmp_path
        result = find_pilot_binary()
        assert result is None


# ---------------------------------------------------------------------------
# cmd_version
# ---------------------------------------------------------------------------


class TestCmdVersion:
    """Tests for cmd_version."""

    def test_cmd_version_prints_version_and_returns_zero(self, capsys):
        """cmd_version prints version info and returns exit code 0."""
        import argparse

        from installer.cli import cmd_version

        args = argparse.Namespace()
        result = cmd_version(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "pilot" in captured.out.lower() or "installer" in captured.out.lower()

    def test_cmd_version_returns_integer(self):
        """cmd_version returns an integer exit code."""
        import argparse

        from installer.cli import cmd_version

        args = argparse.Namespace()
        result = cmd_version(args)
        assert isinstance(result, int)


# ---------------------------------------------------------------------------
# cmd_launch
# ---------------------------------------------------------------------------


class TestCmdLaunch:
    """Tests for cmd_launch."""

    @patch("installer.cli.find_pilot_binary", return_value=None)
    @patch("subprocess.call", return_value=0)
    def test_falls_back_to_claude_when_pilot_not_found(self, mock_call, _mock_find):
        """cmd_launch falls back to 'claude' when pilot binary is not found."""
        import argparse

        from installer.cli import cmd_launch

        args = argparse.Namespace(args=[])
        cmd_launch(args)

        call_args = mock_call.call_args[0][0]
        assert call_args[0] == "claude"

    @patch("installer.cli.find_pilot_binary")
    @patch("subprocess.call", return_value=0)
    def test_uses_pilot_binary_when_found(self, mock_call, mock_find, tmp_path: Path):
        """cmd_launch uses the pilot binary when it exists."""
        import argparse

        from installer.cli import cmd_launch

        pilot_path = tmp_path / "pilot"
        pilot_path.touch()
        mock_find.return_value = pilot_path

        args = argparse.Namespace(args=[])
        cmd_launch(args)

        call_args = mock_call.call_args[0][0]
        assert call_args[0] == str(pilot_path)

    @patch("installer.cli.find_pilot_binary", return_value=None)
    @patch("subprocess.call", return_value=0)
    def test_passes_extra_args_to_subprocess(self, mock_call, _mock_find):
        """cmd_launch passes extra args through to the subprocess."""
        import argparse

        from installer.cli import cmd_launch

        args = argparse.Namespace(args=["--model", "claude-opus-4-6"])
        cmd_launch(args)

        call_args = mock_call.call_args[0][0]
        assert "--model" in call_args
        assert "claude-opus-4-6" in call_args

    @patch("installer.cli.find_pilot_binary", return_value=None)
    @patch("subprocess.call", return_value=42)
    def test_returns_subprocess_exit_code(self, mock_call, _mock_find):
        """cmd_launch returns the exit code from the subprocess."""
        import argparse

        from installer.cli import cmd_launch

        args = argparse.Namespace(args=[])
        result = cmd_launch(args)

        assert result == 42

    @patch("installer.cli.find_pilot_binary", return_value=None)
    @patch("subprocess.call", return_value=0)
    def test_handles_none_args_gracefully(self, mock_call, _mock_find):
        """cmd_launch handles args=None without raising."""
        import argparse

        from installer.cli import cmd_launch

        args = argparse.Namespace(args=None)
        result = cmd_launch(args)

        assert result == 0
        call_args = mock_call.call_args[0][0]
        assert call_args[0] == "claude"


# ---------------------------------------------------------------------------
# Parser completeness
# ---------------------------------------------------------------------------


class TestParserCommands:
    """Tests for create_parser — ensure all subcommands are registered."""

    def test_parser_has_version_subcommand(self):
        """create_parser includes 'version' subcommand."""
        from installer.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["version"])
        assert args.command == "version"

    def test_parser_has_launch_subcommand(self):
        """create_parser includes 'launch' subcommand."""
        from installer.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["launch"])
        assert args.command == "launch"

    def test_parser_launch_passes_extra_args(self):
        """create_parser 'launch' subcommand collects positional extra arguments."""
        from installer.cli import create_parser

        parser = create_parser()
        # The launch subparser collects args as positional (nargs="*"), not flags
        args = parser.parse_args(["launch", "some-project", "--", "--model", "claude-sonnet-4-6"])
        assert "some-project" in args.args

    def test_parser_install_has_target_version_flag(self):
        """create_parser 'install' subcommand has --target-version flag."""
        from installer.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["install", "--target-version", "dev-abc1234-20260124"])
        assert args.target_version == "dev-abc1234-20260124"

    def test_parser_install_has_local_repo_dir_flag(self):
        """create_parser 'install' subcommand has --local-repo-dir flag."""
        from installer.cli import create_parser

        parser = create_parser()
        args = parser.parse_args(["install", "--local-repo-dir", "/tmp/repo"])
        assert args.local_repo_dir == Path("/tmp/repo")
