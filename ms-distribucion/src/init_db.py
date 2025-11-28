from infrastructure.db.session import engine, Base
from infrastructure.db.models import EntregaModel

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created for ms-distribucion")

if __name__ == "__main__":
    init_db()