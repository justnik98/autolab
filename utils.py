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


@app.get("/getall_positions", dependencies=[Depends(get_admin_user)])
async def getall_positions():
    res = []
    cur = db.cursor()
    cur.execute("SELECT position FROM positions")
    for row in cur:
        res.append(row[0])
    return res


@app.get("/getall_departments", dependencies=[Depends(get_admin_user)])
async def getall_groups():
    res = []
    cur = db.cursor()
    cur.execute("SELECT department FROM departments")
    for row in cur:
        res.append(row[0])
    return res


@app.get("/search_students", dependencies=[Depends(get_admin_user)])
async def search_students(data=Body()):
    res = []
    surname = f"{data['surname']}%"
    name = f"{data['first_name']}%"
    patronymic = f"{data['patronymic']}%"
    group = f"{data['group']}%"

    cur = db.cursor()
    cur.execute(f"SELECT id from groups WHERE group_num = '{group}'")
    group_id = cur.fetchone()[0]

    cur.execute(f"SELECT students WHERE "
                f"surname LIKE {surname} AND "
                f"first_name LIKE {name} AND "
                f"patronymic LIKE {patronymic} AND "
                f"group_id LIKE {group_id}")

    for row in cur:
        res.append(row)
        print(row)
    return res
