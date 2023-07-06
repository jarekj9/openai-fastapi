import logging
import requests
import json
import uvicorn
from typing import Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from logging.handlers import RotatingFileHandler
from pipe import where, select
from dotenv import load_dotenv


import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from uvicorn_logging_helper import *
from openai_azure import *    

load_dotenv() 
app = FastAPI()
ai = AI()
PASSWORD = os.getenv("PASSWORD")


@app.get("/")
def read_root(request: Request):
    uvicorn_access_logger.info(f'Client IP: {request.headers.get("x-forwarded-for")}')
    return {"Just to let you know": "You have been logged."}

@app.get("/question")
def question_get(request: Request):
    uvicorn_access_logger.info(f'Client IP: {request.headers.get("x-forwarded-for")}')
    return FileResponse("./app/html/index.html")

@app.post("/question")
async def question_post(request: Request):
    uvicorn_access_logger.info(f'Client IP: {request.headers.get("x-forwarded-for")}')
    data = await request.json()
    question = data.get("question") if data.get("question") else ""
    password = data.get("guess") if data.get("guess") else ""
    if password != PASSWORD:
        raise HTTPException(status_code=403, detail="Forbidden")
    if(question):
        response_text = ai.ask(question)
        return {
            "response": response_text
        }
    return {"response": "bad input"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8003)
