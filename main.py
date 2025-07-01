import uvicorn
from db.supabase import supabase_manager
from models import User, Transaction  
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer



app = FastAPI()
# Middleware para permitir todos los orígenes (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,  # Permitir el uso de cookies/autenticación
    allow_methods=["*"],     # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Permitir todas las cabeceras personalizadas
)

# # Bases de datos temporales en memoria
# users_db = []
# transactions_db = []

# Cargar variables de entorno


# Inicializar FastAPI
app = FastAPI()


# Endpoints actualizados para usar Supabase

@app.post("/register")
async def register(user: User):
    try:
        # Verificar si el usuario ya existe
        existing_user = supabase_manager.client.from_("user") \
            .select("*") \
            .eq("email", user.email) \
            .execute()
        
        if existing_user.data:
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
        # Insertar nuevo usuario
        new_user = {
            "username": user.email,  # Asumiendo que el username es el email
            "email": user.email,
            "password": user.password  # En producción, esto debería estar hasheado
        }
        
        response = supabase_manager.client.from_("user") \
            .insert(new_user) \
            .execute()
            
        if not response.data:
            raise HTTPException(status_code=400, detail="Error al registrar usuario")
            
        return {"msg": "Usuario registrado exitosamente", "user_id": response.data[0]['id']}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login(user: User):
    try:
        # Buscar usuario en Supabase
        user_data = supabase_manager.client.from_("user") \
            .select("*") \
            .eq("email", user.email) \
            .eq("password", user.password) \
            .execute()
        
        if not user_data.data:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
            
        return {"msg": "Bienvenido", "user": user_data.data[0]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions")
async def create_transaction(tx: Transaction):
    try:
        # Verificar si la transacción ya existe por ID
        existing_tx = supabase_manager.client.from_("transactions") \
            .select("*") \
            .eq("id", tx.id) \
            .execute()
        
        if existing_tx.data:
            raise HTTPException(status_code=400, detail="ID de transacción ya existe")
        
        # Insertar nueva transacción
        new_transaction = {
            "id": tx.id,
            "amount": tx.amount,
            "type": tx.type,
            "description": tx.description
        }
        
        response = supabase_manager.client.from_("transactions") \
            .insert(new_transaction) \
            .execute()
            
        if not response.data:
            raise HTTPException(status_code=400, detail="Error al registrar transacción")
            
        return {"msg": "Transacción registrada", "transactions": response.data[0]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Ver todas las transacciones
@app.get("/transactions")
def get_transactions():
    try:
        transactions_db = supabase_manager.client.from_("transaction").select("*").execute()
        if transactions_db.data is None:
            raise HTTPException(status_code=404, detail="No transactions found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return transactions_db

if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
