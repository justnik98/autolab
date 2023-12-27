import json
import os.path
from typing import Union
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

file_extensions = {
    "cpp": ".cpp",
    "python": ".py"
}


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/op")
def read_root(request: Request):
    return templates.TemplateResponse("op.html", {"request": request})





@app.post("/post_code")
def post_code(stud_id: Union[int, None] = None, task_id: Union[int, None] = None, code=Form(), lang=Form()):
    stud_id = 123
    task_id = "1123"
    path = f"./works/{stud_id}"
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
    file = open(f"{path}/main{file_extensions[lang]}", 'w')
    file.write(code)
    return RedirectResponse("/op", status_code=302)


def run_tests(params: json, k: int):
    return 0


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
