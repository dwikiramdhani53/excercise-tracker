from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str

class User(UserBase):
    uid: str

    class Config:
        orm_mode = True

class AllUser(BaseModel):
    count: int
    users: list[User]

class Excercise(BaseModel):
    description: str
    duration: int
    date: date

class ExcerciseBase(Excercise):
    uid: str

    class Config:
        orm_mode = True

class ExcerciseInfo(ExcerciseBase):
    username: str

class UserInfo(User):
    count: int
    logs: list[Excercise]

# {
#   username: "fcc_test",
#   description: "test",
#   duration: 60,
#   date: "Mon Jan 01 1990",
#   _id: "5fb5853f734231456ccb3b05"
# }

# {
#   username: "fcc_test",
#   _id: "5fb5853f734231456ccb3b05"
# }

# {
#   username: "fcc_test",
#   count: 1,
#   _id: "5fb5853f734231456ccb3b05",
#   log: [{
#     description: "test",
#     duration: 60,
#     date: "Mon Jan 01 1990",
#   }]
# }