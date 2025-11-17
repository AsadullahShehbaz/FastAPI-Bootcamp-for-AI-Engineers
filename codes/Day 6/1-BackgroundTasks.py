from fastapi import FastAPI,BackgroundTasks , Depends
from typing import Annotated
app = FastAPI()

@app.get('/')
async def welcome():
    return {'Message':'Welcome to Day 6'}

def write_notification(email:str,message:str):
    with open('log.txt',mode='w') as file:
        content = f"Notification for {email} : {message}"
        file.write(content)

def get_query(background_tasks : BackgroundTasks,q : str | None = None):
    if q:
        background_tasks.add_task(write_notification,q,'Query is :'+q)
    return q 

@app.post('/send_notification/{email_id}')
async def send_notification(email:str,background_tasks : BackgroundTasks,q:Annotated[str,Depends(get_query)]):
    message='\nDear Ayan Ahmed, You have a new notification'
    background_tasks.add_task(write_notification,email,message)

    return {'Message':'Notification Sent'}
