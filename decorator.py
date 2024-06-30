import inspect
import asyncio
from datetime import datetime

from backup import backup_api
from util import generate_id

# Backup Decorator
async def Backup(backup_data, func, args):
    # Backup Parameters
    backup_id = generate_id()
    time = datetime.now().isoformat()
    database_id = backup_data["database_id"] if "database_id" in backup_data else 0
    collection_id = backup_data["collection_id"] if "collection_id" in backup_data else "test"
    data = backup_data["data"]

    # Function Execution
    if inspect.iscoroutinefunction(func): # async function
        _, result = await asyncio.gather(
            *[
                backup_api(
                    backup_id=backup_id,
                    is_flushed=False,
                    time=time,
                    database_id=database_id,
                    collection_id=collection_id,
                    data=data
                ),
                func(*args)
            ]
        )
    else: # default function
        await backup_api(
            backup_id=backup_id,
            is_flushed=False,
            time=time,
            database_id=database_id,
            collection_id=collection_id,
            data=data
        )
        result = func(*args)

    # Backup Data Flush Update
    try:
        await backup_api(
            backup_id=backup_id,
            is_flushed=True,
            time=time,
            database_id=database_id,
            collection_id=collection_id,
            data=data
        )
    except Exception as e:
        print("Backup Server Error:", e)

    # Return result
    return result