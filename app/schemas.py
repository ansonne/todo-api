from pydantic import BaseModel, ConfigDict


# Usuários
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


# Tarefas
class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    priority: dict[int, int]

    model_config = ConfigDict(from_attributes=True)
