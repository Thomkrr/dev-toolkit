import tempfile
import os
from pathlib import Path
from dev_toolkit import DevToolkit


def test_scaffold_fastapi():
    with tempfile.TemporaryDirectory() as tmpdir:
        toolkit = DevToolkit()
        toolkit.project_root = Path(tmpdir)
        toolkit.scaffold("fastapi", "test-api")
        assert (Path(tmpdir) / "test-api" / "pyproject.toml").exists()
        assert (Path(tmpdir) / "test-api" / "app" / "main.py").exists()
        assert (Path(tmpdir) / "test-api" / "README.md").exists()


def test_scaffold_cli():
    with tempfile.TemporaryDirectory() as tmpdir:
        toolkit = DevToolkit()
        toolkit.project_root = Path(tmpdir)
        toolkit.scaffold("cli", "test-cli")
        assert (Path(tmpdir) / "test-cli" / "pyproject.toml").exists()
        assert (Path(tmpdir) / "test-cli" / "test_cli" / "cli.py").exists()


def test_dockerize_generates_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        toolkit = DevToolkit()
        toolkit.project_root = Path(tmpdir)
        toolkit.dockerize()
        assert (Path(tmpdir) / "Dockerfile").exists()
        assert (Path(tmpdir) / "docker-compose.yml").exists()


def test_clean_removes_artifacts():
    with tempfile.TemporaryDirectory() as tmpdir:
        toolkit = DevToolkit()
        toolkit.project_root = Path(tmpdir)
        # Create some artifacts
        (Path(tmpdir) / "__pycache__").mkdir()
        (Path(tmpdir) / "__pycache__" / "test.pyc").write_text("")
        (Path(tmpdir) / "dist").mkdir()
        (Path(tmpdir) / "build").mkdir()
        (Path(tmpdir) / ".pytest_cache").mkdir()
        toolkit.clean()
        assert not (Path(tmpdir) / "__pycache__").exists()
        assert not (Path(tmpdir) / "dist").exists()
        assert not (Path(tmpdir) / "build").exists()
        assert not (Path(tmpdir) / ".pytest_cache").exists()


if __name__ == "__main__":
    test_scaffold_fastapi()
    test_scaffold_cli()
    test_dockerize_generates_files()
    test_clean_removes_artifacts()
    print("All tests passed!")
