import asyncio
import time
import json

async def async_external_function(data):
    print("Data Insert:", data)
    await asyncio.sleep(1)
    print("Data Insert Succeed")
    return data

async def async_external_function_error(data):
    print("Data Insert:", data)
    raise ValueError("Invalid Data")

def external_function(data):
    print("Data Insert:", data)
    time.sleep(1)
    print("Data Insert Succeed")
    return data

def external_function_error(data):
    print("Data Insert:", data)
    raise ValueError("Invalid Data")

def find_backup_data_by_backup_id(backup_id: str):
    f = open(f"./data/{backup_id}.json", "r")
    data = json.loads(f.read())
    f.close()
    return data