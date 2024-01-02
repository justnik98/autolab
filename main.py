import json
import os.path
import shutil
import threading
import subprocess
from typing import Union
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# globals
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
async def op(request: Request):
    return templates.TemplateResponse("op.html", {"request": request})


def update_id():
    global task_id
    task_id += 1
    return task_id


@app.post("/post_code", response_class=HTMLResponse)
async def post_code(request: Request, stud_id: Union[int, None] = None, code=Form(), lang=Form()):
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
    os.system(f"docker build . "
              f"--build-arg lang={lang} "
              f"--build-arg task_id={id} "
              f"--build-arg problem_id={problem_id} "
              f"-t {id}")
    command = f"docker run {id} > {path}/out.txt --rm"
    os.popen(command)
    os.wait()
    command = f"docker rmi {id} -f"
    os.popen(command)
    file = open(f"{path}/out.txt", 'r')
    output = file.read()
    file.close()
    shutil.rmtree(path)
    return templates.TemplateResponse(name="op.html",
                                      context={"request": request, "id": id, "output": output,
                                               "code": code})
    # return RedirectResponse("/op", status_code=302)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
