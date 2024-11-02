# pymmich

An easy-to-use API client for the Immich API. You can use this client to interact with a number of
elements

## Install requirements

```bash
pip install -r requirements.txt --break-system-packages
```

## Getting started

```python
import asyncio
from datetime import datetime

from pymmich.client import PymmichClient
from pymmich.enums.library_type import LibraryType

BASE_URL = "https://immich.mydomain.com"
API_KEY = "ABCDEFGHIJKLMNOPQRZTUVWXYZ0123456789"


async def main() -> None:
    async with PymmichClient(BASE_URL, API_KEY) as client:
        albums = client.get_albums(shared_album=True)
        libraries = client.get_libraries(library_type=LibraryType.EXTERNAL)
        assets = client.get_assets(updated_after=datetime(2024, 1, 31, 12, 34, 56))
        # ...


asyncio.run(main())
```