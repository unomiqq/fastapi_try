from fastapi import FastAPI

from pydantic import BaseModel, Field, EmailStr, ConfigDict


app = FastAPI()

data = {
    "email": "unomiqq@gmail.com",
    "bio": "love pennis",
    "age": 17,
}

data_wo_age = {
    "email": "valya@gmail.com",
    "bio": "love nikita'S pennis",
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=100)

model_config = ConfigDict(extra="forbid")

users = []
@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "massage": "User created"}

@app.get("/users")
def get_users() -> list[UserSchema]:
    return users

class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)
    #greater than or equal to 0 and less than or equal to 130

user = UserAgeSchema(**data)
user2 = UserSchema(**data_wo_age)
print(repr(user))
print(repr(user2))
# UserSchema(email='unomiqq@gmail.com', bio=None, age=17)