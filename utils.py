from auth import *
from fastapi import Body


class Student(BaseModel):
    name: str | None
    surname: str | None
    patronymic: str | None
    group: str | None
    email: str | None


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


@app.post("/search_students", dependencies=[Depends(get_admin_user)])
async def search_students(data=Body()):
    res = []
    surname = f"{data['surname']}%"
    name = f"{data['first_name']}%"
    patronymic = f"{data['patronymic']}%"
    group = data['group']
    group_id = -1
    cur = db.cursor()
    cmd = f"SELECT * FROM students WHERE " \
          f"surname LIKE '{surname}' AND " \
          f"first_name LIKE '{name}' AND " \
          f"patronymic LIKE '{patronymic}'"
    if group != "":
        cur.execute(f"SELECT id from groups WHERE group_num = '{group}'")
        group_id = cur.fetchone()[0]
        cmd = f"{cmd} AND group_id = {group_id}"
    cur.execute(cmd)
    cur2 = db.cursor()
    for row in cur:
        cur2.execute(f"SELECT group_num from groups WHERE id = '{row[6]}'")
        group = cur2.fetchone()[0]
        s = {'surname': row[2], 'name': row[3], 'patronymic': row[4], 'email': row[5], 'group': group}
        res.append(s)
        print(s)
    return res
