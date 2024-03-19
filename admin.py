from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import *

templates = Jinja2Templates(directory="templates")


@app.get("/admin")
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/add_student")
async def add_student(request: Request, stud_id: Union[int, None] = None, code=Form(), lang=Form()):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/add_teacher", response_class=HTMLResponse)
async def add_teacher(request: Request, stud_id: Union[int, None] = None, code=Form(), lang=Form()):
