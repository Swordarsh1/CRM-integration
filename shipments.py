from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
import os
import json
from uuid import uuid4

app = FastAPI()

ship_file = "shipments.json"

def get_shipments():
    if os.path.exists(ship_file):
        with open(ship_file, "r") as ff:
            return json.load(ff)
    return []

def put_shipments(s):
    with open(ship_file, "w") as out:
        json.dump(s, out, indent=2)

shipments = get_shipments()

class Shipment(BaseModel):
    recipient_id: str
    recipient_name: str
    recipient_email: EmailStr

@app.post("/shipments")
def add_ship(s: Shipment):
    print("Got new shipment request") 
    sid = str(uuid4())
    d = {
        "shipment_id": sid,
        "recipient_id": s.recipient_id,
        "recipient_name": s.recipient_name,
        "recipient_email": s.recipient_email
    }

    for sh in shipments:
        if sh["recipient_id"] == s.recipient_id:
            raise HTTPException(status_code=400, detail="already shipped!")

    shipments.append(d)
    put_shipments(shipments)
    return {"msg": "added", "data": d}

@app.get("/shipments")
def view_shipments(skip: int = Query(0), limit: int = Query(10)):
    return shipments[skip:skip+limit]
