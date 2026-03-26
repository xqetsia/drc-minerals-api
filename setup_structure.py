from pathlib import Path

dirs = [
    "app/api/v1/endpoints",
    "app/core",
    "app/db",
    "app/models",
    "app/schemas",
    "app/services",
    "scripts",
    "tests",
]

for d in dirs:
    path = Path(d)
    path.mkdir(parents=True, exist_ok=True)
    (path / "__init__.py").touch()
    print(f"created {path}")