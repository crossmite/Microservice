import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.orm import Session

from database import database as database
from database.database import Ticket

from model.ticket import TicketModel

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def ticket_alive():
    return {'message': 'service alive'}


@app.get("/get_tickets")
async def get_tickets(db: db_dependency):
    try:
        result = db.query(Ticket).limit(100).all()
        return result
    except Exception as e:
        return "Cant access database!"



@app.get("/get_ticket_by_id")
async def get_ticket_by_id(ticket_id: int, db: db_dependency):
    try:
        result = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Ticket not found")



@app.post("/add_ticket")
async def add_ticket(ticket: TicketModel, db: db_dependency):
    ticket_db = Ticket(passenger_name=ticket.passenger_name,
                       passport=ticket.passport,
                       id_ship=ticket.id_ship,
                       direction=ticket.direction)
    try:
        db.add(ticket_db)
        db.commit()
        db.refresh(ticket_db)
        return "Success"
    except Exception:
        return "cant add ticket"


@app.delete("/delete_ticket")
async def delete_ticket(ticket_id: int, db: db_dependency):
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        db.delete(ticket)
        db.commit()
        return "Success"
    except Exception as e:
        return "cant find ticket"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))