import json

# Backup API
async def backup_api(backup_id, is_flushed, time, database_id, collection_id, data):
    f = open(f"./data/{backup_id}.json", "w")
    f.write(
        json.dumps(
            {
                "id": backup_id,
                "is_flushed": is_flushed,
                "time": time,
                "database_id": database_id,
                "collection_id": collection_id,
                "data": data
            },
            indent=4
        )
    )
    f.close()

    f = open("./temp.txt", "w")
    f.write(backup_id)
    f.close()