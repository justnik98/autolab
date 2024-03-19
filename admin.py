from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Union
from auth import *

templates = Jinja2Templates(directory="templates")


@app.get("/admin", dependencies=[Depends(get_admin_user)])
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


user_id = 0


@app.post("/add_student", dependencies=[Depends(get_admin_user)])
async def add_student(data=Body()):
    username = data['username']
    password = data['password']
    surname = data['surname']
    name = data['first_name']
    patronymic = data['patronymic']
    group = data['group']
    email = data['email']

    cur = db.cursor()
    cur.execute(f"INSERT INTO auth (username, password, role_id) "
                f"VALUES('{username}', '{pwd_context.hash(password)}', 0) RETURNING id")
    global user_id
    user_id = cur.fetchone()[0]
    cur.execute(f"INSERT INTO students (user_id, surname, first_name, patronymic, group_num, email) "
                f"VALUES({user_id}, '{surname}' , '{name}' ,'{patronymic}', {group} ,'{email}')")
    db.commit()
    return


# TODO: сделать чтение данных из json
@app.post("/delete_user", dependencies=[Depends(get_admin_user)])
async def delete_user(request: Request):
    cur = db.cursor()
    cur.execute(f"DELETE FROM auth WHERE id ={user_id}")
    db.commit()


@app.get("/add_teacher")
async def add_teacher(request: Request, data=Body()):
    return
