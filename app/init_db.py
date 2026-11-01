from sqlalchemy import create_engine
from models import Base

# Creates a temporary local test database
engine = create_engine("sqlite:///test_crm.db", echo=True)

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")