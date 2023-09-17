import asyncio
import contextlib
import json
from argparse import ArgumentParser
from collections import defaultdict
from functools import partial
from itertools import chain
from pathlib import Path

from colorama import Fore, init

from .core import fetch_modules

init(autoreset=True)


def ensure_project_dir():
    global project_dir
    project_dir = Path.home() / Path(".hiosint")
    if not project_dir.exists():
        project_dir.mkdir()


def get_args():
    global args
    parser = ArgumentParser("hiosint", epilog="https://github.com/iamosint/hiosint")
    parser.add_argument(
        "email",
        help="The target email to perform OSINT gathering on.",
        type=str,
        action="store",
    )
    parser.add_argument(
        "--no-breaches",
        "-nb",
        help="Do NOT use breached data search engines.",
        action="store_true",
        dest="no_breach",
        required=False,
    )
    args = parser.parse_args()


def convert_leakcheck_plaintext(data: dict) -> str:
    result_str = ""
    for record in data.get("result"):
        result_str += (
            f"{record.get('line')}"
            f" [{record.get('last_breach', None) or 'Unknown date'}]"
            f" [{', '.join(record.get('sources')) or 'Unknown source'}]"
            "\n"
        )
    return result_str.strip()


def convert_snusbase_plaintext(data: dict) -> str:
    result_str = ""
    for breach, records in data.get("results").items():
        result_str += "- " + breach + "\n"
        for record in records:
            for key, value in record.items():
                result_str += f"-- {key.upper()}: {value}" + "\n"
            result_str += "\n\n"
    return result_str.strip()


def convert_dehashed_plaintext(records: dict):
    result_str = ""
    if not records.get("total", -1) > 0:
        return None
    for entry in records.get("entries"):
        result_str += "- " + entry.get("database_name") + "\n"
        for key, value in entry.items():
            if key == "database_name":
                continue
            if value:
                result_str += f"-- {key.upper()}: {value}" + "\n"
        result_str += "\n\n"
    return result_str.strip()


def convert_google_plaintext(urls: list[str]) -> str:
    result_str = ""
    for url in urls:
        result_str += "- " + url + "\n"
    return result_str.strip()


RESULT_PROCESS_PLAINTEXT = {
    "leakcheck": convert_leakcheck_plaintext,
    "snusbase": convert_snusbase_plaintext,
    "dehashed": convert_dehashed_plaintext,
    "google": convert_google_plaintext,
}


def bool_question(prompt: str):
    response = input(prompt)
    return response.casefold().startswith("y")


def setup_keys(fp: Path):
    print(
        f"{Fore.YELLOW}Hello! It seems like this is your first time using hiosint."
        " We need some information from you first."
    )
    updated_keys = defaultdict(dict)
    for service, key, comments in (
        ("snusbase", "activation_code", None),
        ("leakcheck", "api_key", None),
        ("dehashed", "authorization", "email|api_key"),
    ):
        if bool_question(
            f"Do you have a {service.title()} {key.replace('_', ' ')} ({comments})?"
            if comments
            else f"Do you have a {service.title()} {key.replace('_', ' ')}?"
            f" [{Fore.GREEN}y{Fore.RESET}/{Fore.RED}n{Fore.RESET}] -> "
        ):
            answer = input("What is it? -> ")
        updated_keys[service][key] = answer
    fp.write_text(json.dumps(updated_keys, indent=4))


def get_keys():
    key_file_path = project_dir / Path("keys.json")
    if not key_file_path.exists():
        key_file_path.touch()
        setup_keys(key_file_path)
    return json.loads(key_file_path.read_text())


async def maincore():
    global args
    global project_dir
    ensure_project_dir()
    get_args()
    keys = get_keys()
    modules = fetch_modules()
    if args.no_breach:
        del modules["leaks"]
    module_funcs = list(chain.from_iterable(modules.values()))
    for func in module_funcs:
        with contextlib.suppress(KeyError):
            func = partial(func, **keys[func.__name__])
        results = await asyncio.create_task(func(args.email))
        if not results:
            continue
        if (
            func_name := func.func.__name__
            if isinstance(func, partial)
            else func.__name__
        ) in RESULT_PROCESS_PLAINTEXT:
            if plaintext := RESULT_PROCESS_PLAINTEXT[func_name](results):
                print("=" * 45)
                print(f"-| MODULE: {func_name.upper()} |-")
                print()
                print(plaintext)
        else:
            print(results)
    print("- " + Fore.GREEN + "Finished all operations.")


def main():
    asyncio.run(maincore())
