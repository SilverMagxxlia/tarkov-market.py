<div align="center">
    <a href="https://github.com/Hostagen/tarkov-market.py">
        <img src="https://user-images.githubusercontent.com/68284806/130361774-5fe5866f-d61b-40a3-afc1-2978ad530f17.png" height="128">
    </a>
</div>

async API wrapper for Tarkov Market written in Python. reverse-engineered [discord.py](https://github.com/Rapptz/discord.py).

# About
## What is Tarkov-Market.py?
- Tarkov-Market.py is Modern Python API using `async` and `await`.

## Installing
**Python 3.8 or higher is required**

```sh
# Linux/macOS
python3 -m pip install -U tarkov-market.py

# Windows
py  -3 -m pip install -U tarkov-market.py
```

# Quick Example

```python
import asyncio
import tarkov_market

market = tarkov_market.Client(token='API KEY')


async def main():
    # Must run setup once before use.
    await market.setup()

    item: tarkov_market.Item = await market.fetch_item('TerraGroup Labs keycard (Red)')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```
