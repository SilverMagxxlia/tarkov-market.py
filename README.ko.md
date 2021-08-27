<div align="center">
    <a href="https://github.com/Hostagen/tarkov-market.py">
        <img src="https://user-images.githubusercontent.com/68284806/130361774-5fe5866f-d61b-40a3-afc1-2978ad530f17.png" height="128">
    </a>
</div>

Python으로 이루어진 Tarkov Market API를 위한 비동기 래퍼입니다. 이 API는 [discord.py](https://github.com/Rapptz/discord.py)를 기반으로 하여 역설계 되었습니다..

# 정보
## Tarkov-Market.py는 무엇입니까?
- Tarkov-Market.py는 간단한 `async`와 `await`를 사용한 Python API입니다.

## 설치
**Python 3.8 이상의 버전이 요구됩니다.**

```sh
# Linux/macOS
python3 -m pip install -U tarkov-market.py

# Windows
py  -3 -m pip install -U tarkov-market.py
```

# 빠른 예제

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
