from fastapi import FastAPI, HTTPException
from models import User, Transaction  # Asegúrate que models.py esté en el mismo directorio

app = FastAPI()

# Bases de datos temporales en memoria
users_db = []
transactions_db = []

# Registro de usuario
@app.post("/register")
def register(user: User):
    users_db.append(user)
    return {"msg": "Usuario registrado"}

# Login de usuario
@app.post("/login")
def login(user: User):
    for u in users_db:
        if u.email == user.email and u.password == user.password:
            return {"msg": "Bienvenido"}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

# Crear transacción
@app.post("/transactions")
def create_transaction(tx: Transaction):
    transactions_db.append(tx)
    return {"msg": "Transacción registrada"}

# Ver todas las transacciones
@app.get("/transactions")
def get_transactions():
    return transactions_db
