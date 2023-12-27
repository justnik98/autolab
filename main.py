import json
import os.path
import shutil
import threading
from typing import Union
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#globals
mutex = threading.Lock()
task_id = 0

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



def update_id():
    global task_id
    task_id += 1
    return task_id

@app.post("/post_code")
def post_code(stud_id: Union[int, None] = None, code=Form(), lang=Form()):
    stud_id = 123
    problem_id = 123
    global task_id
    mutex.acquire()
    id = update_id()
    mutex.release()
    path = f"./data/works/{id}"
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)

    file = open(f"{path}/main{file_extensions[lang]}", 'w')
    file.write(code)
    file.close()
    print(f"docker build "
              f"--build-arg lang={lang} "  
              f"--build-arg task_id={id} "
              f"--build-arg problem_id={problem_id}"
              f"-t {id}")
    print(f"docker run {id} --rm &> {id} && docker rmi -f {id}")

    shutil.rmtree(path)
    return RedirectResponse("/op", status_code=302)


def run_tests(params: json, k: int):
    return 0


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
