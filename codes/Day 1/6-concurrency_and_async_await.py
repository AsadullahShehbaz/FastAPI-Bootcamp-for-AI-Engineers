import asyncio
from fastapi import FastAPI

app = FastAPI()

async def simulate_network_call():
    print('Wait for 2 seconds...')
    await asyncio.sleep(2)
    return "Network data"

@app.get("/network")
async def get_network_data():
    data = await simulate_network_call()
    return {"response": data}

async def students(id: int):
    print('Wait for 1 seconds...')
    await asyncio.sleep(1)
    return {'Student ID':id,'Name':f'Student {id}'}

@app.get('/read')
async def read():
    results = await asyncio.gather(students(1),students(2),students(3))
    return results 