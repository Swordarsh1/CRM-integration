from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
import os
import json
import requests
from uuid import uuid4

app = FastAPI()

# just using this file for now (should move to DB later maybe)
file_name = "clients.json"

def read_clients():
    if os.path.exists(file_name):
        with open(file_name, "r") as fh:
            return json.load(fh)
    return []

def write_clients(clients):
    with open(file_name, "w") as f:
        json.dump(clients, f, indent=2)

clients_data = read_clients()

class Client(BaseModel):
    full_name: str
    email_address: EmailStr


@app.post("/clients")
def create_new_client(c: Client):
    # generate id
    id_ = str(uuid4())
    info = {
        "id": id_,
        "full_name": c.full_name,
        "email_address": c.email_address
    }

    for cl in clients_data:
        if cl["email_address"].lower() == c.email_address.lower():
            # email already there
            raise HTTPException(status_code=400, detail="already added lol")

    print("Adding new client")  # debug

    clients_data.append(info)
    write_clients(clients_data)

    try:
        print("Sending to shipment...")  # debug
        res = requests.post("http://localhost:9001/shipments", json={
            "recipient_id": id_,
            "recipient_name": c.full_name,
            "recipient_email": c.email_address
        })
        if res.status_code != 200:
            print("Shipment not ok", res.status_code)
    except Exception as e:
        print("Something broke with shipment:", e)
        return {"status": "added but no shipment", "details": str(e)}

    return {"status": "ok", "client": info}


@app.get("/clients")
def get_em(skip: int = Query(0), limit: int = Query(10)):
    # TODO: maybe add sorting later?
    return clients_data[skip:skip+limit]
