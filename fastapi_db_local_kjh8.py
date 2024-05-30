
# 잘못된 요청이 들어왔을 때 FastAPI에서 오류는 HTTPException을 사용해 예외를 발생시켜 처리한다.
# HTTPException은 API와 연관된 추가 데이터를 사용하는 보통의 파이썬 예외이다.
# 파이썬 예외이기에 return을 사용하지 않고 raise를 사용한다.

from fastapi import FastAPI, HTTPException

# pydantic은 파이썬의 type annotation을 활용해서 data의 validation(검증)과 setting 관리를 해주는 라이브러리.
# BaseModel1에서 정의한 type 말고 다른 type의 데이터가 들어오면 오류가 난다.
# 예를 들어 CreateData(BaseModel)에서는 str로 정의했는데 문자열이 아닌 다른 type의 데이터가 오면 오류가 난다.
# 즉, 데이터의 type이 올바르게 들어올 수 있도록 검증해준다.

from pydantic import BaseModel

# 파이썬은 동적 언어로 코드 양이 많아지고 복잡해질 수록 잘못된 타입으로 인한 에러를 만날 확률이 높다.
# 그래서 이런 동적 언어들에게 Typing을 사용해 변수나 함수의 인자, 리턴 값에 타입을 명시하고 검사하고자 사용한다.
# List는 리스트 안에 있는 타입을 나타내기 위해 사용
# Optional은 union[<타입>, None]로 대체한 것이다. 즉, 타입 또는 None의 값을 받는다.

# Null이란 미확인 값이나 적용되지 않은 값을 의미한다. 즉, 문자 공백이나 숫자 0조차 아니다(중요)

from typing import List, Optional

# databases 모듈에서 Database 클래스를 가져와서 사용할 준비를 한다는 의미. 이를 통해 Database 클래스를 직접 사용할 수 있다.
# databases 모듈은 MySQL, SQLite 등 여러 데이터 베이스 시스템을 지원한다.
# 따라서 특정 데이터 베이스 시스템에 종속되지 않고 여러 종류의 데이터 베이스와 유연하게 작업할 수 있다.
# 데이터 베이스 연결, 쿼리 실행, 트랜잭션 관리 등이 편리하게 가능하다.
# 즉, 비동기 프로그래밍을 통해 데이터베이스 작업의 효율성을 높이고, 
# 다양한 데이터베이스와의 호환성을 유지하며, 간편한 API로 개발 생산성을 높이기 위해서 사용한다.

from databases import Database

# 날짜와 시간 데이터 처리를 위해 내장 모듈 datatime을 사용
# datetime 클래스는 날짜와 시간을 동시에 표현하기 위해서 사용된다
# datetine 클래스의 생성자는 연, 월, 일, 시, 분, 초, 마이크로초, 시간대를 인자로 받는다.
# 시간 이하의 인자는 필수 인자가 아니며 생략할 경우, 0이 기본값으로 사용된다.

from datetime import datetime

# 비동기 문맥 관리자(asynccontextmanager)를 제공하는 contextlib 모듈 기능을 가져온다. 
# 이를 사용하면 async with 문의 비동기 작업 설정 및 정리를 명확하게 할 수 있다.

from contextlib import asynccontextmanager


# FastAPI 웹 프레임워크를 사용하여 새로운 어플리케이션 인스턴스를 생성
# FastAPI는 Python으로 작성된 현대적이고 빠른 웹 프레임워크.
# 이 프레임워크는 타입 힌팅을 활용하여 자동으로 API 문서를 생성하고, 높은 성능을 제공.
# app = FastAPI()는 생성한 애플리케이션의 인스턴스를 app이란 변수에 할당.
# app 인스턴스를 사용하여 경로, 요청 핸들러 등을 정의할 수 있다.

# app = FastAPI()


# DB 접속 설정

DATABASE_URL = "mysql://admin:Seigakushakorea0308(!@52.195.216.34/kjh8_db" # ksj0_db 는 본인의 데이터베이스 이름으로 바꿔주세요.
database = Database(DATABASE_URL)


# BaseModel1 요소를 문자열 자료형 str 타입으로 정의

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

# @app.on_event("startup") 
# async def startup(): 
#     await database.connect() 
    
# FastAPI 어플리케이션이 시작될 때 실행할 함수 등록
# startup 이벤트가 발생할 때 실행될 비동기 함수, 데이터 베이스에 연결하는 작업을 한다.
# 데이터베이스 연결을 초기화하고 애플리케이션이 시작될 때 필요한 설정을 완료한다.

# 비동기식 방식은 비동기는 동시에 일어나지 않는다를 의미한다. 요청과 결과가 동시에 일어나지 않을 거라는 약속이다.
# 먼저 시작된 작업의 완료 여부와는 상관없이 새로운 작업을 시작하는 방식.
# 작업이 병렬로 배치되어 실행되며 작업의 순서가 확실치 않아 나중에 시작된 작업이 먼저 끝나는 경우도 있다.
# 작업이 완료될 때까지 기다리지 않고 다른 작업을 계속 수행할 수 있어 시스템이 중단 없이 운영 가능하다.
# 설계가 Synchronous보다 복잡하지만 결과가 주어지는데 그 시간 작업할 수 있으므로 자원을 효율적으로 사용가능하다.

# @app.on_event("shutdown") 
# async def shutdown():   
#     await database.disconnect() 

# 애플리케이션이 종료될 때 shutdown 함수가 호출되어 데이터 베이스 연결을 종료한다.
# 리소스를 적절히 정리하고 데이터 손실을 방지하기 위해 사용된다.

# The method "on_event" in class "FastAPI" is deprecated 
# on_event is deprecated, use lifespan event handlers instead.
# @app.on_event("startup") 및 @app.on_event("shutdown") 메서드가 FastAPI에서 더 이상 사용되지 않으며, 
# 대신 lifespan 이벤트 핸들러를 사용해야 한다는 경고 메시지.
# 이는 FastAPI의 새로운 버전에서 이벤트 핸들링을 위해 더 나은 방식이 도입되었기 때문.

# lifespan은 애플리케이션의 수명 주기 전체를 관리하기 위해 도입된 새로운 접근 방식으로, on_event에 비해 몇 가지 장점이 있다.
# 라이프사이클 관리 : lifespan은 애플리케이션의 시작과 종료 단계를 명확하게 정의하고 관리할 수 있도록 설계되었습니다. 이를 통해 애플리케이션의 수명 주기 이벤트(시작, 종료)를 더 명확하게 처리할 수 있다.
# 더 나은 유지 보수성 : lifespan을 사용하면 애플리케이션의 시작과 종료 로직이 하나의 함수 내에서 관리되기 때문에 코드가 더 깔끔하고 유지보수하기 쉬워진다. 
# on_event를 사용할 경우 여러 함수에 분산될 수 있는 로직이 하나의 장소에서 관리됩니다.
# 유연성 증가 : lifespan은 비동기 함수와 동기 함수를 모두 지원하며, 다양한 초기화 및 종료 로직을 유연하게 작성할 수 있습니다. 이는 복잡한 초기화 및 종료 시퀀스가 필요한 경우 특히 유용하다.
# 표준화된 방식: lifespan은 FastAPI의 새로운 표준 방식으로 채택되어, 앞으로의 업데이트나 다른 라이브러리와의 호환성 측면에서 더 나은 지원을 받을 가능성이 크다.


async def start(): # 데이터베이스 연결을 초기화하고 애플리케이션이 시작될 때 필요한 설정을 완료한다.
    print("Start Up.")
    await database.connect() 


async def shutdown(): # 애플리케이션이 종료될 때 shutdown 함수가 호출되어 데이터 베이스 연결을 종료한다.
    print("Shutdown") # 리소스를 적절히 정리하고 데이터 손실을 방지하기 위해 사용된다.
    await database.disconnect()

@asynccontextmanager # 리소스 관리가 간편해지고 애플리케이션의 수명 주기 동안 필요한 설정 및 작업을 명확하게 정의 가능
async def lifespan(app:FastAPI): #app 객체를 선언할 때 인자로 lifespan를 정의한다.
    await start()
    yield # yield를 기준으로 앞에 오는 코드는 서비스가 시작될 때 호출하는 함수 뒤에 오는 코드는 서비스가 종료될 때 호출하는 함수
    await shutdown()

# FastAPI 애플리케이션 인스턴스를 생성하고, 이 인스턴스의 수명 주기(lifespan)를 lifespan 함수로 설정한다. 
# 이렇게 하면 애플리케이션이 시작될 때 start()가 호출되고, 애플리케이션이 종료될 때 shutdown()이 호출된다.

app = FastAPI(lifespan=lifespan)

# 비동기식으로 작동해서 await가 핵심! 안붙이면 코드 오류 500 Internal Server Error가 나와서 포스트맨이 먹통이 된다


# FastAPI 애플리케이션의 엔드포인트를 정의하고, 데이터베이스에서 데이터를 조회하여 반환하는 함수
# API가 두 시스템(어플리케이션)이 상호작용할 수 있게 하는 프로토콜의 총집합이라면 API가 서버에서 리소스에 접근할 수 있도록 가능하게 하는 URL이다.
# 엔드포인트란, 애플리케이션 프로그래밍 인터페이스(API)와의 클라이언트 간 연결의 서버쪽 엔드다.
# 예를 들어, 웹 사이트에 운전 경로를 제공하기 위해 지도 제작 API가 통합된 경우 웹 사이트 서버는 API 클라이언트가 되고 지도 제작 API 서버는 API 엔드포인트가 된다.

@app.get("/datas") # HTTP GET 요청에 대해 "/datas" 경로로 들어오는 요청을 처리하는 엔드포인트를 정의
async def get_all_datas(): # 비동기 함수로, 데이터베이스에서 데이터를 가져온다
    query = "SELECT * FROM datas" # 데이터베이스에서 모든 데이터 조회하는 쿼리
    datas = await database.fetch_all(query) # 비동기 방식으로 쿼리를 실행하고 결과를 가져온다. fetch_all 매서드는 쿼리의 결과를 리스트 형태로 반환한다.
    if datas is None: # 조회된 datas가 비어 있는 리스트일 경우 참이 된다.
        raise HTTPException(status_code=404, detail="Datas not found") # 데이터가 없으면 HTTPException을 발생시켜 기본 응답 코드 200 대신  404코드와 상세메세지 반환
    return datas # 조회된 데이터를 클라이언트에 반환

# FastAPI 애플리케이션에서 특정 'data_id'에 해당하는 데이터를 데이터 베이스에서 조회하여 반환하는 함수

@app.get("/data/{data_id}") # HTTP GET 요청을 처리하는 엔드포인트 정의. 여기서 {data_id}는 경로 매개변수로, URL의 일부로 전달된다.
async def get_data(data_id: int): # 비동기 함수로 'data_id'를 받아 데이터베이스에서 해당 데이터를 조회한다.
    query = "SELECT * FROM datas WHERE data_id = :data_id" #특정 data_id에 해당하는 데이터를 조회하는 쿼리.
    data = await database.fetch_one(query, values={"data_id": data_id}) #위와 동일하게 실행하고 결과를 가져오고 fetch_one 메서드는 쿼리의 결과를 단일 레코드로 반환한다.
    if data is None: # 조회된 data가 비어 있는 경우 참
        raise HTTPException(status_code=404, detail="Data not found") #위와 동일
    return data #위와 동일

# FastAPI 애플리케이션에서 새로운 데이터를 데이터베이스에 삽입하는 POST 요청을 처리하는 함수

# @app.post("/data") # HTTP POST 요청에 "/data" 경로로 들어오는 요청을 처리하는 엔드포인트를 정의
# async def create_data(data: CreateData): #CreatData를 사용해 요청 본문에서 데이터를 받는다
#     query = """ 
#     INSERT INTO datas (entry_number, objective, message, schedule, date_time, sender)
#     VALUES (:entry_number, :objective, :message, :schedule, :date_time, :sender)
#     """ # datas 테이블에 새로운 데이터를 삽입하는 쿼리
#     values = data.dict() # CreateData 모델의 인스턴스를 딕셔너리로 변환한다. 쿼리에 사용될 값을 제공한다.
#     await database.execute(query, values=values) # 비동기 방식으로 쿼리를 실행하여 데이터를 데이터베이스에 삽입합니다.
#     return {"message": "Data created successfully"} # 데이터 삽입 성공시 반환되는 메세지를 json 형태로 클라이언트에 반환한다.

# The method "dict" in class "BaseModel" is deprecated
# The `dict` method is deprecated; use `model_dump` instead.
# Pydantic의 최신 버전에서는 BaseModel 클래스의 dict 메서드가 더 이상 사용되지 않으며, 
# 대신 model_dump 메서드를 사용해야 한다는 경고 메시지

# FastAPI에서 dict() 대신 model_dump()를 사용하는 이유는 주로 Pydantic v2로의 마이그레이션과 관련이 있습니다. 
# Pydantic은 FastAPI에서 데이터 검증과 설정 관리를 위해 사용되는 핵심 라이브러리인데, Pydantic v2에서는 몇 가지 중요한 변경 사항이 도입되었다.
# dict() 메서드의 변경 : 더 명확한 의미 전달과 새로운 기능 지원을 위해 도입된 변경 사항
# 더 명확한 API : model_dump()는 모델 데이터를 덤프하는 명확한 의미를 가지며, Pydantic의 다른 유틸리티 함수들과 일관된 네이밍 규칙을 따른다. 이는 코드의 가독성을 높이고, 새로운 사용자에게 더 직관적인 API를 제공하기 위함
# 추가 기능과 유연성 : model_dump() 메서드는 dict() 메서드에 비해 더 많은 옵션과 기능을 제공한다. 예를 들어, 필드를 선택적으로 포함하거나 제외하는 등의 고급 사용 사례를 더 잘 지원한다.


@app.post("/data") # HTTP POST 요청에 "/data" 경로로 들어오는 요청을 처리하는 엔드포인트를 정의
async def create_data(data: CreateData): #CreatData를 사용해 요청 본문에서 데이터를 받는다
    query = """ 
    INSERT INTO datas (entry_number, objective, message, schedule, date_time, sender)
    VALUES (:entry_number, :objective, :message, :schedule, :date_time, :sender)
    """ # datas 테이블에 새로운 데이터를 삽입하는 쿼리
    values = data.model_dump() # CreateData 모델의 인스턴스를 딕셔너리로 변환한다. 쿼리에 사용될 값을 제공한다.
    await database.execute(query, values=values) # 비동기 방식으로 쿼리를 실행하여 데이터를 데이터베이스에 삽입합니다.
    return {"message": "Data created successfully"} # 데이터 삽입 성공시 반환되는 메세지를 json 형태로 클라이언트에 반환한다.


# FastAPI 애플리케이션에서 특정 {data_id}에 해당하는 데이터를 업데이트하는 PUT 요청을 처리하는 함수

@app.put("/data/{data_id}") # HTTP PUT 요청에 대해 /data/{data_id} 경로로 들어오는 요청을 처리하는 엔드포인트 정의. 여기서 {data_id}는 경로 매개변수로, URL의 일부로 전달.
async def update_data(data_id: int, data: UpdateData): # 비동기 함수로, data_id와 UpdateData 모델을 사용하여 요청 본문에서 데이터를 받는다.
    query = "SELECT * FROM datas WHERE data_id = :data_id" # data_id에 해당하는 데이터를 조회하는 쿼리.
    existing_data = await database.fetch_one(query, values={"data_id": data_id}) # existing_data는 조회된 데이터로 데이터가 없으면 HTTPException 예외처리 발생.
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
    """ #  datas 테이블의 특정 data_id에 해당하는 데이터를 업데이트하는 쿼리
    values = data.dict() # UpdateData 모델의 인스턴스를 딕셔너리로 변환한다. 쿼리에 사용될 값을 제공한다.
    values["data_id"] = data_id # 업데이트할 데이터의 "data_id" 값을 추가한다.
    await database.execute(query, values=values) # 비동기 방식으로 쿼리를 실행하여 데이터를 업데이트한다.
    return {"message": "Data updated successfully"} # 데이터 업데이트가 성공하면 메세지 반환

# FastAPI 애플리케이션에서 특정 data_id에 해당하는 데이터를 삭제하는 DELETE 요청을 처리하는 함수

@app.delete("/data/{data_id}") # # HTTP DELETE 요청에 대해 /data/{data_id} 경로로 들어오는 요청을 처리하는 엔드포인트 정의. 여기서 {data_id}는 경로 매개변수로, URL의 일부로 전달.
async def delete_data(data_id: int): # delete_data 함수는 비동기 함수로, data_id를 받아 데이터베이스에서 해당 데이터를 삭제.
    query = "SELECT * FROM datas WHERE data_id = :data_id" # data_id에 해당하는 데이터를 조회하는 쿼리.
    existing_data = await database.fetch_one(query, values={"data_id": data_id}) # existing_data는 조회된 데이터로 데이터가 없으면 HTTPException 예외처리 발생.
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    query = "DELETE FROM datas WHERE data_id = :data_id" # datas 테이블에서 특정 data_id에 해당하는 데이터를 삭제하는 쿼리
    await database.execute(query, values={"data_id": data_id}) # 비동기 방식으로 쿼리를 실행하여 데이터 삭제
    return {"message": "Data deleted successfully"} # 데이터 삭제 성공 시 메시지 반환

