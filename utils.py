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
    group = f"{data['group']}%"
    cur = db.cursor()
    cmd = (f"SELECT surname, first_name, patronymic, group_num, email "
           f"FROM students RIGHT JOIN groups ON students.group_id = groups.id WHERE "
           f"surname LIKE '{surname}' AND "
           f"first_name LIKE '{name}' AND "
           f"patronymic LIKE '{patronymic}' AND "
           f"group_num LIKE '{group}'")
    cur.execute(cmd)
    for row in cur:
        print(row)
        s = {'surname': row[0], 'name': row[1], 'patronymic': row[2], 'group': row[3], 'email': row[4]}
        res.append(s)
    return res
