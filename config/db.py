import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

print(f"Connecting to database at {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)


def crear_db_y_tablas():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Error en la base de datos: {e}")


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            print(f"Error en la sesión de la base de datos: {e}")
            raise
