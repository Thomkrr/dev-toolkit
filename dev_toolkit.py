#!/usr/bin/env python3
"""
Dev Automation Toolkit - 7 CLI commands to automate repetitive coding tasks.
Built for developers who want to ship faster.
"""

import argparse
import subprocess
import os
import json
import shutil
from pathlib import Path
from typing import List, Optional


class DevToolkit:
    def __init__(self):
        self.project_root = Path.cwd()

    # 1. scaffold - Create project structure from templates
    def scaffold(self, template: str, name: str, force: bool = False):
        """Scaffold a new project from template: fastapi, cli, react, nextjs"""
        templates = {
            'fastapi': self._fastapi_template,
            'cli': self._cli_template,
            'react': self._react_template,
            'nextjs': self._nextjs_template,
        }
        if template not in templates:
            print(f"Unknown template: {template}. Available: {list(templates.keys())}")
            return
        target = self.project_root / name
        if target.exists() and not force:
            print(f"Directory {name} exists. Use --force to overwrite.")
            return
        target.mkdir(parents=True, exist_ok=True)
        templates[template](target, name)
        print(f"✅ Scaffolded {template} project at {target}")

    def _fastapi_template(self, target: Path, name: str):
        (target / "app").mkdir()
        (target / "tests").mkdir()
        (target / "app" / "api").mkdir()
        (target / "app" / "core").mkdir()
        (target / "app" / "models").mkdir()
        (target / "app" / "schemas").mkdir()
        (target / "app" / "api" / "v1").mkdir(parents=True)
        
        files = {
            "pyproject.toml": f'''[project]
name = "{name}"
version = "0.1.0"
dependencies = [
    "fastapi>=0.100",
    "uvicorn[standard]>=0.23",
    "pydantic>=2.0",
    "sqlalchemy>=2.0",
    "alembic>=1.11",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "httpx>=0.24", "ruff>=0.1.0"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
''',
            "app/main.py": '''from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import router as api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
''',
            "app/core/config.py": '''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "change-me-in-production"

    class Config:
        env_file = ".env"

settings = Settings()
''',
            "app/api/v1/__init__.py": "from fastapi import APIRouter\nrouter = APIRouter()\n",
            ".env.example": "DATABASE_URL=sqlite:///./app.db\nSECRET_KEY=your-secret-key\n",
            "README.md": f"# {name}\n\nFastAPI project scaffolded by dev-toolkit.\n\n## Setup\n```bash\npip install -e .[dev]\ncp .env.example .env\nuvicorn app.main:app --reload\n```\n",
            ".gitignore": "__pycache__/\n.env\n*.pyc\n*.db\n.pytest_cache/\n",
        }
        for fname, content in files.items():
            (target / fname).write_text(content)

    def _cli_template(self, target: Path, name: str):
        (target / name.replace("-", "_")).mkdir()
        files = {
            "pyproject.toml": f'''[project]
name = "{name}"
version = "0.1.0"
dependencies = ["click>=8.0", "rich>=13.0"]
entry-points = {{"console_scripts": ["{name} = {name.replace('-', '_')}.cli:main"]}}

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
''',
            f"{name.replace('-', '_')}/cli.py": '''import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option()
def main():
    """CLI tool scaffolded by dev-toolkit."""
    pass

@main.command()
@click.argument('name')
def hello(name):
    """Say hello."""
    console.print(f"[green]Hello, {name}![/green]")

if __name__ == "__main__":
    main()
''',
            "README.md": f"# {name}\n\nCLI tool scaffolded by dev-toolkit.\n\n```bash\npip install -e .\n{name} --help\n```\n",
        }
        for fname, content in files.items():
            (target / fname).write_text(content)

    def _react_template(self, target: Path, name: str):
        files = {
            "package.json": f'''{{
  "name": "{name}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }},
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }}
}}''',
            "vite.config.js": "import { defineConfig } from 'vite'\nimport react from '@vitejs/plugin-react'\nexport default defineConfig({ plugins: [react()] })",
            "index.html": f'''<!DOCTYPE html>
<html lang="en">
  <head><meta charset="UTF-8" /><title>{name}</title></head>
  <body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body>
</html>''',
            "src/main.jsx": "import React from 'react'\nimport ReactDOM from 'react-dom/client'\nimport App from './App'\nReactDOM.createRoot(document.getElementById('root')).render(<App />)",
            "src/App.jsx": f"export default function App() {{ return <h1>{name}</h1> }}",
        }
        for fname, content in files.items():
            (target / fname).write_text(content)

    def _nextjs_template(self, target: Path, name: str):
        files = {
            "package.json": f'''{{
  "name": "{name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }},
  "dependencies": {{
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }}
}}''',
            "next.config.js": "/** @type {import('next').NextConfig} */\nconst nextConfig = {}\nmodule.exports = nextConfig",
            "app/page.tsx": f"export default function Home() {{ return <h1>{name}</h1> }}",
            "app/layout.tsx": "export default function RootLayout({ children }: { children: React.ReactNode }) { return (<html><body>{children}</body></html>) }",
        }
        for fname, content in files.items():
            (target / fname).write_text(content)

    # 2. lint-fix - Run linters with auto-fix
    def lint_fix(self, path: str = "."):
        """Run ruff, eslint, prettier with auto-fix."""
        target = Path(path)
        print("🔧 Running auto-fix linters...")
        cmds = [
            ["ruff", "check", "--fix", str(target)],
            ["ruff", "format", str(target)],
        ]
        for cmd in cmds:
            try:
                subprocess.run(cmd, check=True)
            except FileNotFoundError:
                print(f"  ⚠️  {cmd[0]} not installed, skipping")
            except subprocess.CalledProcessError:
                print(f"  ⚠️  {cmd[0]} had issues")
        print("✅ Lint-fix complete")

    # 3. test-cov - Run tests with coverage
    def test_cov(self, path: str = ".", min_cov: int = 80):
        """Run pytest with coverage, fail if below threshold."""
        cmd = ["pytest", "--cov=.", f"--cov-fail-under={min_cov}", "-v", path]
        try:
            subprocess.run(cmd, check=True)
            print("✅ Tests passed with coverage")
        except subprocess.CalledProcessError:
            print("❌ Tests failed or coverage below threshold")
            raise

    # 4. deps-check - Check for outdated/vulnerable deps
    def deps_check(self):
        """Check Python and Node deps for updates and vulnerabilities."""
        print("🔍 Checking dependencies...")
        # Python
        try:
            subprocess.run(["pip", "list", "--outdated"], check=False)
            subprocess.run(["pip-audit"], check=False)
        except FileNotFoundError:
            print("  ⚠️  pip-audit not installed")
        # Node
        if Path("package.json").exists():
            try:
                subprocess.run(["npm", "outdated"], check=False)
                subprocess.run(["npm", "audit"], check=False)
            except FileNotFoundError:
                pass
        print("✅ Dependency check complete")

    # 5. dockerize - Generate Dockerfile + docker-compose
    def dockerize(self, port: int = 8000, python_version: str = "3.11"):
        """Generate optimized Dockerfile and docker-compose.yml."""
        dockerfile = f'''FROM python:{python_version}-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy source
COPY . .

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE {port}
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "{port}"]
'''
        compose = f'''version: '3.8'
services:
  app:
    build: .
    ports:
      - "{port}:{port}"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:
'''
        (self.project_root / "Dockerfile").write_text(dockerfile)
        (self.project_root / "docker-compose.yml").write_text(compose)
        print("✅ Generated Dockerfile and docker-compose.yml")

    # 6. release - Bump version, tag, build
    def release(self, bump: str = "patch"):
        """Bump version (major/minor/patch), create git tag."""
        import re
        pyproject = Path("pyproject.toml")
        if not pyproject.exists():
            print("❌ No pyproject.toml found")
            return
        content = pyproject.read_text()
        match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', content)
        if not match:
            print("❌ Could not parse version")
            return
        major, minor, patch = map(int, match.groups())
        if bump == "major":
            major += 1; minor = 0; patch = 0
        elif bump == "minor":
            minor += 1; patch = 0
        else:
            patch += 1
        new_version = f"{major}.{minor}.{patch}"
        content = re.sub(r'version = "\d+\.\d+\.\d+"', f'version = "{new_version}"', content)
        pyproject.write_text(content)
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        subprocess.run(["git", "commit", "-m", f"chore: release v{new_version}"], check=True)
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        print(f"✅ Released v{new_version} (tagged)")

    # 7. clean - Remove build artifacts
    def clean(self):
        """Remove __pycache__, .pytest_cache, dist, build, node_modules, .next"""
        patterns = [
            "**/__pycache__", "**/*.pyc", ".pytest_cache", ".coverage",
            "dist", "build", "*.egg-info", "node_modules", ".next", ".turbo"
        ]
        removed = 0
        for pattern in patterns:
            for path in self.project_root.rglob(pattern):
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    removed += 1
                except Exception:
                    pass
        print(f"✅ Cleaned {removed} artifacts")


def main():
    parser = argparse.ArgumentParser(prog="dev-toolkit", description="Dev Automation Toolkit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("scaffold", help="Scaffold project from template")
    p.add_argument("template", choices=["fastapi", "cli", "react", "nextjs"])
    p.add_argument("name")
    p.add_argument("--force", action="store_true")

    sub.add_parser("lint-fix", help="Run linters with auto-fix")
    sub.add_parser("test-cov", help="Run tests with coverage")
    sub.add_parser("deps-check", help="Check deps for updates/vulns")
    p = sub.add_parser("dockerize", help="Generate Dockerfile + compose")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--python", default="3.11")
    p = sub.add_parser("release", help="Bump version and tag")
    p.add_argument("bump", choices=["major", "minor", "patch"], nargs="?", default="patch")
    sub.add_parser("clean", help="Remove build artifacts")

    args = parser.parse_args()
    toolkit = DevToolkit()

    cmd_map = {
        "scaffold": lambda: toolkit.scaffold(args.template, args.name, args.force),
        "lint-fix": lambda: toolkit.lint_fix(),
        "test-cov": lambda: toolkit.test_cov(),
        "deps-check": lambda: toolkit.deps_check(),
        "dockerize": lambda: toolkit.dockerize(args.port, args.python),
        "release": lambda: toolkit.release(args.bump),
        "clean": lambda: toolkit.clean(),
    }
    cmd_map[args.cmd]()


if __name__ == "__main__":
    main()