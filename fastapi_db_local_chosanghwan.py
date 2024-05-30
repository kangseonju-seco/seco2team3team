from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from databases import Database
from datetime import datetime
from contextlib import asynccontextmanager

# FastAPI 인스턴스 생성
DATABASE_URL = "mysql://admin:Seigakushakorea0308(!@52.195.216.34/csh0905_db"
database = Database(DATABASE_URL)

async def start():
    print("Start Up.")
    await database.connect() 

async def shutdown():
    print("Shutdown")
    await database.disconnect()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start()  # await 추가
    try:
        yield
    finally:
        await shutdown()  # await 추가

app = FastAPI(lifespan=lifespan)

# 데이터 생성 시 사용할 Pydantic 모델 정의
class CreateData(BaseModel):
    entry_number: str
    objective: str
    message: str
    schedule: str
    date_time: str
    sender: str

# 데이터 업데이트 시 사용할 Pydantic 모델 정의
class UpdateData(BaseModel):
    entry_number: str
    objective: str
    message: str
    schedule: str
    date_time: str
    sender: str

# 모든 데이터를 가져오는 엔드포인트 정의
@app.get("/datas")
async def get_all_datas():
    query = "SELECT * FROM datas"
    datas = await database.fetch_all(query)
    if datas is None:
        raise HTTPException(status_code=404, detail="Datas not found")
    return datas

# 특정 ID의 데이터를 가져오는 엔드포인트 정의
@app.get("/data/{data_id}")
async def get_data(data_id: int):
    query = "SELECT * FROM datas WHERE data_id = :data_id"
    data = await database.fetch_one(query, values={"data_id": data_id})
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

# 새로운 데이터를 생성하는 엔드포인트 정의
@app.post("/data")
async def create_data(data: CreateData):
    query = """
    INSERT INTO datas (entry_number, objective, message, schedule, date_time, sender)
    VALUES (:entry_number, :objective, :message, :schedule, :date_time, :sender)
    """
    values = data.model_dump()
    await database.execute(query, values=values)
    return {"message": "Data created successfully"}

# 기존 데이터를 업데이트하는 엔드포인트 정의
@app.put("/data/{data_id}")
async def update_data(data_id: int, data: UpdateData):
    query = "SELECT * FROM datas WHERE data_id = :data_id"
    existing_data = await database.fetch_one(query, values={"data_id": data_id})
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    query = """
    UPDATE datas
    SET entry_number = :entry_number,
        objective = :objective,
        message = :message,
        schedule = :schedule,
        date_time = :date_time,
        sender = :sender
    WHERE data_id = :data_id
    """
    values = data.dict()
    values["data_id"] = data_id
    await database.execute(query, values=values)
    return {"message": "Data updated successfully"}

# 특정 ID의 데이터를 삭제하는 엔드포인트 정의
@app.delete("/data/{data_id}")
async def delete_data(data_id: int):
    query = "SELECT * FROM datas WHERE data_id = :data_id"
    existing_data = await database.fetch_one(query, values={"data_id": data_id})
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    query = "DELETE FROM datas WHERE data_id = :data_id"
    await database.execute(query, values={"data_id": data_id})
    return {"message": "Data deleted successfully"}

