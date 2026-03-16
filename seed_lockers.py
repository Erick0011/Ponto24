from app import app
from models import db, Locker

def seed():

    lockers = []

    # Pequenos
    for i in range(16):
        lockers.append(Locker(size="small"))

    # Médios
    for i in range(4):
        lockers.append(Locker(size="medium"))

    # Grandes
    for i in range(2):
        lockers.append(Locker(size="large"))

    db.session.add_all(lockers)
    db.session.commit()

    print("Lockers criados com sucesso!")

with app.app_context():
    seed()
