import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form
from typing import Annotated
from sqlalchemy import null
from sqlalchemy.orm import Session
from collections import Counter
from keycloak import KeycloakOpenID

from database import database as database
from database.database import Ticket

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

# Данные для подключения к Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "ormanzhi"
KEYCLOAK_REALM = "myrealm"
KEYCLOAK_CLIENT_SECRET = "T678RfL6Jxtk5zmNQygPAn7ahcTnPzTr"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/get-token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def check_user_roles():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "testRole" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")



@app.get("/health", status_code=status.HTTP_200_OK)
async def statistics_alive():
    return {'message': 'service alive'}


@app.get("get_statistics")
async def get_statistics(db: db_dependency):
    if (check_user_roles()):
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
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
