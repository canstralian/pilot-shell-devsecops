"""Extended tests for shell config step — edge cases not in test_shell_config.py.

Covers: nonexistent files, fish shell PATH format, write errors, ctx.config
        tracking, pilot function removal, remove_old_alias with pilot() syntax.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from installer.steps.shell_config import (
    BUN_BIN_PATH,
    CLAUDE_ALIAS_MARKER,
    PILOT_BIN_DIR,
    ShellConfigStep,
    alias_exists_in_file,
    get_alias_lines,
    remove_old_alias,
)


# ---------------------------------------------------------------------------
# alias_exists_in_file — edge cases
# ---------------------------------------------------------------------------


class TestAliasExistsInFileEdgeCases:
    """Edge cases for alias_exists_in_file."""

    def test_returns_false_for_nonexistent_file(self):
        """alias_exists_in_file returns False when the file does not exist."""
        result = alias_exists_in_file(Path("/nonexistent/path/.bashrc"))
        assert result is False

    def test_detects_pilot_alias_without_marker(self):
        """alias_exists_in_file detects 'alias pilot' without any marker."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text("alias pilot='/path/to/pilot'\n")
            assert alias_exists_in_file(config) is True

    def test_returns_false_for_unrelated_config(self):
        """alias_exists_in_file returns False for config with unrelated aliases."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text("alias ll='ls -la'\nalias grep='grep --color'\n")
            assert alias_exists_in_file(config) is False


# ---------------------------------------------------------------------------
# remove_old_alias — edge cases
# ---------------------------------------------------------------------------


class TestRemoveOldAliasEdgeCases:
    """Edge cases for remove_old_alias."""

    def test_returns_false_for_nonexistent_file(self):
        """remove_old_alias returns False when file does not exist."""
        result = remove_old_alias(Path("/nonexistent/.bashrc"))
        assert result is False

    def test_removes_pilot_alias(self):
        """remove_old_alias removes 'alias pilot=' line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text("# config\nalias pilot='/path/to/pilot'\n# more\n")

            result = remove_old_alias(config)

            assert result is True
            content = config.read_text()
            assert "alias pilot=" not in content

    def test_removes_pilot_function(self):
        """remove_old_alias removes pilot() function definition."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text("# before\npilot() {\n    /path/to/pilot \"$@\"\n}\n# after\n")

            result = remove_old_alias(config)

            assert result is True
            content = config.read_text()
            assert "pilot()" not in content
            assert "# before" in content
            assert "# after" in content

    def test_removes_old_bun_only_path_export(self):
        """remove_old_alias removes old-style PATH with only .bun/bin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text('# config\nexport PATH="$HOME/.bun/bin:$PATH"\n# more\n')

            result = remove_old_alias(config)

            assert result is True
            content = config.read_text()
            assert 'export PATH="$HOME/.bun/bin:$PATH"' not in content

    def test_removes_old_pilot_bin_path_export(self):
        """remove_old_alias removes old-style PATH with .pilot/bin and .bun/bin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text('export PATH="$HOME/.pilot/bin:$HOME/.bun/bin:$PATH"\n')

            result = remove_old_alias(config)

            assert result is True
            content = config.read_text()
            assert 'export PATH="$HOME/.pilot/bin:$HOME/.bun/bin:$PATH"' not in content

    def test_collapses_consecutive_blank_lines(self):
        """remove_old_alias collapses consecutive blank lines after removal."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / ".bashrc"
            config.write_text("# before\n\nalias ccp='old'\n\n\n# after\n")

            remove_old_alias(config)

            content = config.read_text()
            # Should not have 3+ consecutive blank lines
            assert "\n\n\n" not in content

    def test_removes_fish_pilot_function(self):
        """remove_old_alias removes fish 'function pilot ... end' block."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / "config.fish"
            config.write_text("# before\nfunction pilot\n    /path/to/pilot $argv\nend\n# after\n")

            result = remove_old_alias(config)

            assert result is True
            content = config.read_text()
            assert "function pilot" not in content
            assert "# before" in content
            assert "# after" in content

    def test_removes_fish_ccp_function(self):
        """remove_old_alias removes fish 'function ccp ... end' block."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / "config.fish"
            config.write_text("# before\nfunction ccp\n    pilot $argv\nend\n# after\n")

            result = remove_old_alias(config)

            assert result is True
            content = config.read_text()
            assert "function ccp" not in content
            assert "# before" in content
            assert "# after" in content


# ---------------------------------------------------------------------------
# get_alias_lines — shell-type specifics
# ---------------------------------------------------------------------------


class TestGetAliasLinesShellTypes:
    """Tests for get_alias_lines with different shell types."""

    def test_bash_uses_export_path_syntax(self):
        """get_alias_lines for bash uses 'export PATH=...' syntax."""
        result = get_alias_lines("bash")
        assert "export PATH=" in result
        assert PILOT_BIN_DIR in result
        assert BUN_BIN_PATH in result

    def test_fish_uses_set_gx_path_syntax(self):
        """get_alias_lines for fish uses 'set -gx PATH' syntax."""
        result = get_alias_lines("fish")
        assert "set -gx PATH" in result
        assert PILOT_BIN_DIR in result
        assert BUN_BIN_PATH in result

    def test_fish_does_not_use_export_syntax(self):
        """get_alias_lines for fish does not use 'export PATH=' syntax."""
        result = get_alias_lines("fish")
        assert "export PATH=" not in result

    def test_bash_does_not_use_set_gx_syntax(self):
        """get_alias_lines for bash does not use 'set -gx' syntax."""
        result = get_alias_lines("bash")
        assert "set -gx" not in result

    def test_unknown_shell_falls_back_to_bash_syntax(self):
        """get_alias_lines for unknown shell type uses bash 'export PATH=' syntax."""
        result = get_alias_lines("zsh")
        assert "export PATH=" in result


# ---------------------------------------------------------------------------
# ShellConfigStep.run — additional scenarios
# ---------------------------------------------------------------------------


class TestShellConfigStepRunEdgeCases:
    """Additional tests for ShellConfigStep.run."""

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_skips_nonexistent_config_files(self, mock_get_files):
        """ShellConfigStep.run skips files that do not exist."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            nonexistent = Path(tmpdir) / ".bashrc_that_does_not_exist"
            mock_get_files.return_value = [nonexistent]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            step.run(ctx)

            assert ctx.config.get("modified_shell_configs") == []

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_records_modified_files_in_ctx_config(self, mock_get_files):
        """ShellConfigStep.run stores modified file paths in ctx.config."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            bashrc = Path(tmpdir) / ".bashrc"
            bashrc.write_text("# existing\n")
            zshrc = Path(tmpdir) / ".zshrc"
            zshrc.write_text("# existing\n")
            mock_get_files.return_value = [bashrc, zshrc]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            step.run(ctx)

            modified = ctx.config.get("modified_shell_configs", [])
            assert str(bashrc) in modified
            assert str(zshrc) in modified

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_shell_needs_reload_set_when_new_alias_added(self, mock_get_files):
        """ShellConfigStep.run sets shell_needs_reload=True when adding alias to fresh file."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            bashrc = Path(tmpdir) / ".bashrc"
            bashrc.write_text("# fresh config\n")  # No existing alias
            mock_get_files.return_value = [bashrc]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            step.run(ctx)

            assert ctx.config.get("shell_needs_reload") is True

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_shell_needs_reload_false_when_only_updating_existing_alias(self, mock_get_files):
        """ShellConfigStep.run does not set shell_needs_reload when updating an existing alias."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            bashrc = Path(tmpdir) / ".bashrc"
            bashrc.write_text(f"{CLAUDE_ALIAS_MARKER}\nalias pilot='/old/path'\n")
            mock_get_files.return_value = [bashrc]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            step.run(ctx)

            assert not ctx.config.get("shell_needs_reload", False)

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_uses_fish_alias_syntax_for_fish_config(self, mock_get_files):
        """ShellConfigStep.run writes fish-style PATH when config filename contains 'fish'."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            fish_config = Path(tmpdir) / "config.fish"
            fish_config.write_text("# fish config\n")
            mock_get_files.return_value = [fish_config]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            step.run(ctx)

            content = fish_config.read_text()
            assert "set -gx PATH" in content
            assert "export PATH=" not in content

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_handles_write_error_gracefully(self, mock_get_files):
        """ShellConfigStep.run continues when a file write fails with OSError."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            bashrc = Path(tmpdir) / ".bashrc"
            bashrc.write_text("# config\n")
            mock_get_files.return_value = [bashrc]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            with patch("builtins.open", side_effect=OSError("Permission denied")):
                # Should not raise
                step.run(ctx)

            assert ctx.config.get("modified_shell_configs") == []

    @patch("installer.steps.shell_config.get_shell_config_files")
    def test_alias_written_only_once_in_fresh_install(self, mock_get_files):
        """ShellConfigStep.run writes the alias marker exactly once in a fresh config."""
        from installer.context import InstallContext
        from installer.ui import Console

        step = ShellConfigStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            bashrc = Path(tmpdir) / ".bashrc"
            bashrc.write_text("")
            mock_get_files.return_value = [bashrc]

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
            )

            step.run(ctx)

            content = bashrc.read_text()
            assert content.count(CLAUDE_ALIAS_MARKER) == 1
