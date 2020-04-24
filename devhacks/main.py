import uuid
from deta.lib import Database, email

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr


app = FastAPI()
db = Database("signups")
PREFIX = "4242"
    
class Entry(BaseModel):
    name: str
    email: EmailStr


@app.get("/")
async def homepage():
    return HTMLResponse(open("index.html").read())


@app.post("/form")
async def form(entry: Entry):
    data = entry.dict()
    key = uuid.uuid4().hex
    name = data.get("name")

    try:
        if name.startswith(PREFIX):
            key = name[4:]
            team = db.get(key)
            email2 = team["data"].get("email2")
            
            if email2:
                return {"full": team["data"]["name"]}

            team["data"]["email2"] = data.get("email")
            db.put(key, team["data"])
            
            email(
                data.get("email"),
                f"DevHacks #1 confirmation", 
                f"Thanks for joining!\n Your team is {name}"
            )
            return {"team": team["data"]["name"]}
    except Exception as e:
        print(e)
        pass
        
    db.put(key, data)
    email(
        data.get("email"),
        "DevHacks #1 confirmation",
        f"Thanks for joining!\n Your team ID is {PREFIX}{key}"
    )
    return {"id": f"{PREFIX}{key}"}

