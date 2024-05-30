import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from databases import Database
from datetime import datetime


app = FastAPI()


DATABASE_URL = "mysql://admin:Seigakushakorea0308(!@52.195.216.34/hgj7_db" 
database = Database(DATABASE_URL)


class CreateData(BaseModel):
    entry_number: str
    objective: str
    message: str
    schedule: str
    date_time: str
    sender: str


class UpdateData(BaseModel):
    entry_number: str
    objective: str
    message: str
    schedule: str
    date_time: str
    sender: str


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/datas")
async def get_all_datas():
    query = "SELECT * FROM datas"
    datas = await database.fetch_all(query)
    if datas is None:
        raise HTTPException(status_code=404, detail="Datas not found")
    return datas


@app.get("/data/{data_id}")
async def get_data(data_id: int):
    query = "SELECT * FROM datas WHERE data_id = :data_id"
    data = await database.fetch_one(query, values={"data_id": data_id})
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


@app.post("/data")
async def create_data(data: CreateData):
    query = """
    INSERT INTO datas (entry_number, objective, message, schedule, date_time, sender)
    VALUES (:entry_number, :objective, :message, :schedule, :date_time, :sender)
    """
    values = data.dict()
    await database.execute(query, values=values)
    return {"message": "Data created successfully"}


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


@app.delete("/data/{data_id}")
async def delete_data(data_id: int):
    query = "SELECT * FROM datas WHERE data_id = :data_id"
    existing_data = await database.fetch_one(query, values={"data_id": data_id})
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    query = "DELETE FROM datas WHERE data_id = :data_id"
    await database.execute(query, values={"data_id": data_id})
    return {"message": "Data deleted successfully"}

