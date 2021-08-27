<div align="center">
    <a href="https://github.com/Hostagen/tarkov-market.py">
        <img src="https://user-images.githubusercontent.com/68284806/130361774-5fe5866f-d61b-40a3-afc1-2978ad530f17.png" height="128">
    </a>
</div>

<p align="center">
    <a href="#アバウト">About</a> |
    <a href="https://pypi.org/project/tarkov-market.py/">PyPI</a>

tarkov-market.pyは非同期処理を支援するTarkov-Market.com API用のAPIラッパーです。

# アバウト
## Tarkov-Market.pyは何ですか?
- `async`と`await`を使ったPython API。

## インストール
**Python 3.8以上が必須です。**

```sh
# Linux/macOS
python3 -m pip install -U tarkov-market.py

# ウィンドウズ
py -3 -m pip install -U tarkov-market.py
```

# 簡単な例

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
