from infrastructure.db.session import engine, Base
from infrastructure.db.models import EmpleadoModel

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created for ms-rrhh")

if __name__ == "__main__":
    init_db()