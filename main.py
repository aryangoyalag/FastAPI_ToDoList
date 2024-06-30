from fastapi import FastAPI
import database
from routes import auth_route,user_route,task_route

app = FastAPI()

database.init_db()

@app.get("/", tags=["Home"])
async def home():
    return {"message": "To access API endpoints, visit '/docs' at the end of the URL."}

app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(task_route.router)

    
