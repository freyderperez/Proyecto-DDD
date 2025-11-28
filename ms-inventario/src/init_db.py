from infrastructure.db.session import engine, Base
from infrastructure.db.models import InsumoModel

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created for ms-inventario")

if __name__ == "__main__":
    init_db()