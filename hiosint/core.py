import importlib.util
from collections import defaultdict
from pathlib import Path


def fetch_modules():
    modules = defaultdict(list)
    for ext_file in (Path(__file__).parent / "modules").rglob("[!_]*.py"):
        name = ".".join(ext_file.parts[-3:-1] + (ext_file.stem,))
        module_group = ext_file.parts[:-1][-1]
        module = importlib.import_module("." + name, "hiosint")
        modules[module_group].append(getattr(module, ext_file.stem))
    return modules
