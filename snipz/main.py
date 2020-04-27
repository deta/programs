import secrets, string
from deta.lib import App, Database
from fastapi.responses import HTMLResponse
from deta.lib.responses import JSON
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pydantic import BaseModel
from jinja2 import Template

# This is a regular FastAPI app. Read the docs of FastAPI:
# https://fastapi.tiangolo.com/


# suggest.html: https://cclwqvx4995d.deta.dev/snippets/chek-0030
# review.html: https://cclwqvx4995d.deta.dev/snippets/pvmh-1775
# main.html: https://cclwqvx4995d.deta.dev/snippets/xrdi-1512
# snipz.css: https://cclwqvx4995d.deta.dev/snippets/hipy-1460
# main.py: https://cclwqvx4995d.deta.dev/snippets/fptk-6045
# README.md: https://cclwqvx4995d.deta.dev/snippets/oulg-9883

fast = FastAPI()


app = App(fast)


snippets = Database("snippets")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    

def get_password_hash(password):
    return pwd_context.hash(password)


def get_snippet(snip_id):
    try:
        snippet = snippets.get(snip_id)["data"]
        return snippet
    except KeyError:
        return None


@app.lib.run("snipper")
def snip_handler(event):
    key = event.json.get("key")
    val = get_snippet(key)
    return val



def gen_id():
    alpha = "".join(secrets.choice(string.ascii_lowercase) for i in range(4))
    digits = "".join(secrets.choice(string.digits) for i in range(4))
    key = f"{alpha}-{digits}"
    if get_snippet(key):
        return gen_id()
    return key

  
def get_change(snippet_id, change_id):
    try:
        changes = snippets.get(snippet_id)["data"]["proposed_changes"]
        change = changes["change_id"]
        return change
    except KeyError:
        return None


def gen_change_id(snippet_id):
    alpha = "".join(secrets.choice(string.ascii_lowercase) for i in range(2))
    digits = "".join(secrets.choice(string.digits) for i in range(2))
    key = f"{alpha}{digits}"
    if get_change(snippet_id, f"{alpha}{digits}"):
        return gen_change_id()
    return key


class Snippet(BaseModel):
    name: str
    code: str
    snip_id: str = gen_id()
    proposed_changes: dict = {}
    history: list = []
    password: str = "community merge"


class Password(BaseModel):
    password: str


class SnipInDB(Snippet):
    hashed_password: str


class Change(BaseModel):
    code: str


def authenticate_merge(snip_id: str, password: str):
    snippet = get_snippet(snip_id)
    if not snippet:
        return False
    else:
        snippet = SnipInDB(**snippet)
        if not verify_password(password, snippet.hashed_password):
            return False
        return True
    


@app.get("/")
def main_handler():
    main = open("main.html").read()
    return HTMLResponse(main)
    

@app.get("/snipz.css")
def main_handler():
    css = open("snipz.css").read()
    return Response(content=css, media_type="text/css")


@app.post("/create_snippet")
async def make_snippet(new_snip: Snippet):
    snip_dict = new_snip.dict()
    snip_dict["hashed_password"] = get_password_hash(new_snip.password)
    del snip_dict["password"]
    snippets.put(new_snip.snip_id, snip_dict)
    del snip_dict["hashed_password"]
    return Snippet(**snip_dict)


@app.get("/snippets/{snippet_id}")
async def show_snippet(snippet_id: str):
    try:
        suggest_template = Template((open("suggest.html").read()))
        snippet = Snippet(**snippets.get(snippet_id)["data"]).dict()
        return HTMLResponse(suggest_template.render(snippet_data=snippet))
    except KeyError:
        return {"error": "no such snippet"}


@app.post("/snippets/{snippet_id}/changes")
async def suggest_change(snippet_id: str, change: Change):
    try:
        snippet = SnipInDB(**snippets.get(snippet_id)["data"])
        snippet.proposed_changes[gen_change_id(snippet_id)] = change.dict()
        snippets.put(snippet_id, snippet.dict())
        return Snippet(**snippet.dict())
    except KeyError:
        return {"error": "no such snippet"}


@app.get("/snippets/{snippet_id}/review")
async def review_snippet(snippet_id: str):
    try:
        review_template = Template((open("review.html").read()))
        snippet = Snippet(**snippets.get(snippet_id)["data"]).dict()
        return HTMLResponse(review_template.render(snippet_data=snippet))
    except KeyError:
        return {"error": "no such snippet"}


@app.patch("/snippets/{snippet_id}/merge/{change_id}")
async def merge_change(snippet_id: str, change_id: str, password: Password):
    if not authenticate_merge(snippet_id, password.password):
        return {"error": "Invalid merge password"}
    try:
        snippet = SnipInDB(**snippets.get(snippet_id)["data"])
        change = Change(**snippet.proposed_changes[change_id])
        snippet.history.append(snippet.code)
        snippet.code = change.code
        del snippet.proposed_changes[change_id]
        snippets.put(snippet_id, snippet.dict())
        return Snippet(**snippet.dict())
    except KeyError:
        return {"error": "no such snippet"}


@app.lib.run()
def handler(event):
    return len(snippets.all())



@app.lib.run(action="del_snip")
def handler(event):
    snip_id = event.json["snip_id"]
    snippets.delete(snip_id)
    return len(snippets.all())