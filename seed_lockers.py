from app import app
from models import db, Locker

def seed():

    lockers = [

        # ESQUERDA
        "small",   # 1  S1
        "medium",  # 2  M1
        "small",   # 3  S2
        "large",   # 4  L1
        "small",   # 5  S3
        "small",   # 6  S4
        "medium",  # 7  M2
        "small",   # 8  S5
        "small",   # 9  S6
        "small",   # 21 S7
        "small",   # 22 S8

        # DIREITA
        "small",   # 10 S9
        "medium",  # 11 M3
        "small",   # 12 S10
        "large",   # 13 L2
        "small",   # 14 S11
        "small",   # 15 S12
        "medium",  # 16 M4
        "small",   # 17 S13
        "small",   # 18 S14
        "small",   # 19 S15
        "small",   # 20 S16

    ]

    for size in lockers:
        db.session.add(Locker(size=size, status="free"))

    db.session.commit()

    print("Lockers criados")

with app.app_context():
    seed()