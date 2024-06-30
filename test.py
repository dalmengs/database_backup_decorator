from decorator import Backup
from external_function import *

import asyncio

test_data = {
    "username": "dalmeng",
    "password": "1234"
}

async def async_succeed_test():
    try:
        result = await Backup(
            backup_data={
                "data": test_data
            },
            func=async_external_function,
            args=[test_data]
        )
        print(result)
    except Exception as e:
        print(e)
    finally:
        backup_id = str(open("./temp.txt", "r").read())
        data = find_backup_data_by_backup_id(backup_id)
        assert data["is_flushed"] == True
    print("Test Succeed")

async def async_failed_test():
    try:
        result = await Backup(
            backup_data={
                "data": test_data
            },
            func=async_external_function_error,
            args=[test_data]
        )
        print(result)
    except Exception as e:
        print(e)
    finally:
        backup_id = str(open("./temp.txt", "r").read())
        data = find_backup_data_by_backup_id(backup_id)
        assert data["is_flushed"] == False
    print("Test Succeed")

async def succeed_test():
    try:
        result = await Backup(
            backup_data={
                "data": test_data
            },
            func=external_function,
            args=[test_data]
        )
        print(result)
    except Exception as e:
        print(e)
    finally:
        backup_id = str(open("./temp.txt", "r").read())
        data = find_backup_data_by_backup_id(backup_id)
        assert data["is_flushed"] == True
    print("Test Succeed")

async def failed_test():
    try:
        result = await Backup(
            backup_data={
                "data": test_data
            },
            func=external_function_error,
            args=[test_data]
        )
        print(result)
    except Exception as e:
        print(e)
    finally:
        backup_id = str(open("./temp.txt", "r").read())
        data = find_backup_data_by_backup_id(backup_id)
        assert data["is_flushed"] == False
    print("Test Succeed")

async def main():
    await async_succeed_test()
    await async_failed_test()
    await succeed_test()
    await failed_test()

if __name__ == "__main__":
    asyncio.run(main())
