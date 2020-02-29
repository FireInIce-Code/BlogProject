from fastapi import FastAPI
import uvicorn
app=FastAPI()
@app.get("/")
async def helloWorld():
    return {"message":"hello World"}
uvicorn.run(app)