import asyncio
import tarkov_market

market = tarkov_market.Client(token='INSERT YOUR API KEY.')


async def main():
    # Must run setup once before use.
    await market.setup()

    item: tarkov_market.Item = await market.fetch_item('TerraGroup Labs keycard (Red)')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
