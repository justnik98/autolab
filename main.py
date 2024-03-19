import os.path
import shutil
import threading
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth import *

# app = FastAPI()
templates = Jinja2Templates(directory="templates")

# globals
mutex = threading.Lock()
task_id = 0

file_extensions = {
    "cpp": ".cpp",
    "python": ".py"
}


@app.get("/", dependencies=[Depends(get_auth_user)])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/logout")
async def session_logout(response: Response):
    print("logged out")
    response.delete_cookie(key="Authorization")
    return {"status": "logged out"}


@app.get("/op", dependencies=[Depends(get_auth_user)])
async def op(request: Request):
    return templates.TemplateResponse("op.html", {"request": request})


async def update_id():
    global task_id
    task_id += 1
    return task_id


@app.post("/post_code", response_class=HTMLResponse)
async def post_code(request: Request, stud_id: Union[int, None] = None, code=Form(), lang=Form()):
    problem_id = 123
    global task_id
    id = update_id()
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
