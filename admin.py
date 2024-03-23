from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Union
from auth import *

templates = Jinja2Templates(directory="templates")


@app.get("/admin", dependencies=[Depends(get_admin_user)])
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post("/add_student", dependencies=[Depends(get_admin_user)], status_code=201)
async def add_student(data=Body()):
    username = data['username']
    password = data['password']
    surname = data['surname']
    name = data['first_name']
    patronymic = data['patronymic']
    group = data['group']
    email = data['email']

    cur = db.cursor()
    cur.execute(f"SELECT id from groups WHERE group_num = '{group}'")
    group_id = cur.fetchone()[0]
    cur.execute(f"INSERT INTO auth (username, password, role_id) "
                f"VALUES('{username}', '{pwd_context.hash(password)}', 0) RETURNING id")
    user_id = cur.fetchone()[0]
    cur.execute(f"INSERT INTO students (user_id, surname, first_name, patronymic, group_id, email) "
                f"VALUES({user_id}, '{surname}' , '{name}' ,'{patronymic}', {group_id} ,'{email}')")
    db.commit()


@app.post("/add_teacher", dependencies=[Depends(get_admin_user)], status_code=201)
async def add_student(data=Body()):
    username = data['username']
    password = data['password']
    surname = data['surname']
    name = data['first_name']
    patronymic = data['patronymic']
    email = data['email']
    position = data['position']
    department = data['department']

    cur = db.cursor()
    cur.execute(f"SELECT id from positions WHERE position = '{position}'")
    pos_id = cur.fetchone()[0]
    cur.execute(f"SELECT id from departments WHERE department = '{department}'")
    dep_id = cur.fetchone()[0]
    cur.execute(f"INSERT INTO auth (username, password, role_id) "
                f"VALUES('{username}', '{pwd_context.hash(password)}', 0) RETURNING id")

    user_id = cur.fetchone()[0]
    cur.execute(f"INSERT INTO teachers (user_id, surname, first_name, patronymic, email, position_id, departmnet_id) "
                f"VALUES({user_id}, '{surname}' , '{name}' ,'{patronymic}', '{email}, {pos_id}, {dep_id}')")
    db.commit()


@app.post("/delete_user", dependencies=[Depends(get_admin_user)])
async def delete_user(data=Body()):
    cur = db.cursor()
    user_id = data['user_id']
    cur.execute(f"DELETE FROM auth WHERE id ={user_id}")
    db.commit()
