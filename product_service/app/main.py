# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select, Sequence
from fastapi import FastAPI, Depends
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.product_db.engine import create_db_and_tables, get_session
from app.product_db.model import Product
from app.product_db import schema
from app import crud

import asyncio
import json








async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    task = asyncio.create_task(consume_messages('Product', 'broker:19092'))
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Hello balaaj mart & services API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])




@app.get("/")
def read_root():
    return {"Hello": "balaaj mart & services"}

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

# @app.post("/todos/", response_model=Product)
# async def create_todo(todo: Product, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)])->Product:
#         todo_dict = {field: getattr(todo, field) for field in todo.dict()}
#         todo_json = json.dumps(todo_dict).encode("utf-8")
#         print("todoJSON:", todo_json)
#         # Produce message
#         await producer.send_and_wait("todos", todo_json)
#         session.add(todo)
#         session.commit()
#         session.refresh(todo)
#         return todo

@app.post("/products/", response_model=schema.ProductRead)
async def create_product(product: schema.ProductCreate, session: Annotated[Session, Depends(get_session)],
                   producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("todoJSON:", product_json)
     # Produce message
    await producer.send_and_wait("product", product_json)
    return crud.create_product(session, product)



# @app.get("/todos/", response_model=list[Product])
# def read_todos(session: Annotated[Session, Depends(get_session)]):
#         todos = session.exec(select(Product)).all()
#         return todos
