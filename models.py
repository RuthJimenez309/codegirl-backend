from pydantic import BaseModel

# Modelo de Usuario
class User(BaseModel):
    username: str | None = None
    email: str
    password: str

# Modelo de Transacción
class Transaction(BaseModel):
    id: int
    amount: float
    type: str
    description: str
