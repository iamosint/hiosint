![](https://i.ibb.co/DK40cC4/hiosint-blue.png)

### What is hiosint?
hiosint was developed to gather reliable PII (Personal Identifiable Information) from email addresses utilizing sources like data breaches, search engines, and more.
## Installation

Install hiosint with PyPI (pip)

```bash
pip install hiosint
```

Install hiosint from source

```bash
git clone https://github.com/iamosint/hiosint.git
cd hiosint/
python3 setup.py install
```
## Usage

With CLI

```bash
hiosint --help
```

With Library

- **hiosint Uses [aiohttp](https://docs.aiohttp.org/en/stable/) behind the scenes for HTTP requests**

```py
import asyncio
from hiosint.modules.leaks import leakcheck


async def main():
    results = await leakcheck(
        "target email",
        "leakcheck.io API key",
        "email",  # default query type is "auto"
    )
    print(results)


asyncio.run(main())
```
## License

[GNU General Public License v3 or later (GPLv3+)](https://choosealicense.com/licenses/gpl-3.0/)

