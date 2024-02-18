import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy import null
from sqlalchemy.orm import Session
from collections import Counter

from database import database as database
from database.database import Ticket

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
async def statistics_alive():
    return {'message': 'service alive'}


@app.get("get_statistics")
async def get_statistics(db: db_dependency):
    try:
        tickets = db.query(Ticket).limit(100).all()
        directions_counter = Counter([ticket.direction for ticket in tickets])
        most_common_directions = directions_counter.most_common()

        # Количество уникальных пассажиров (по паспортам)
        unique_passengers = len(set([ticket.passport for ticket in tickets]))

        # Самые частые пассажиры (по имени)
        passenger_counter = Counter([ticket.passenger_name for ticket in tickets])
        most_frequent_passengers = passenger_counter.most_common(3)  # Топ-3 пассажира

        # Формирование ответа
        result = {
            "most_common_directions": most_common_directions,
            "unique_passengers": unique_passengers,
            "most_frequent_passengers": most_frequent_passengers
        }
    except Exception:
        return "cant access database!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
