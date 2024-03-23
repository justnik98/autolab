from auth import *
from fastapi import Body


@app.get("/getall_groups", dependencies=[Depends(get_admin_user)])
async def getall_groups():
    res = []
    cur = db.cursor()
    cur.execute("SELECT group_num FROM groups")
    for row in cur:
        res.append(row[0])
    return res
