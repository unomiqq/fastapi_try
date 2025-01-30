from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config = config)


class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post("/login",
          tags = ["Auth"],
          summary = "Login")
def login(credentials: UserLoginSchema, response: Response):
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid = "12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code = 401, detail="Incorrect username or password")
@app.get("/protected", dependencies = [Depends(security.access_token_required)],
         tags = ["Auth"],
         summary = "Protected")
def protected():
    return {"data": "TOP SECRET"}