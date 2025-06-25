import asyncio
from database import court_collection

async def get_court_ids():
    courts = await court_collection.find({}).to_list(None)
    for court in courts:
        print(f"{court['name']}: {court['_id']}")

asyncio.run(get_court_ids())
