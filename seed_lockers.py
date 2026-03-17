from app import app
from models import db, Locker

def seed_manual():


    # ===== ESQUERDA =====
    db.session.add(Locker(id=1, size="small", status="free"))   # S1
    db.session.add(Locker(id=2, size="medium", status="free"))  # M1
    db.session.add(Locker(id=3, size="small", status="free"))   # S2
    db.session.add(Locker(id=4, size="large", status="free"))   # L1
    db.session.add(Locker(id=5, size="small", status="free"))   # S3
    db.session.add(Locker(id=6, size="small", status="free"))   # S4
    db.session.add(Locker(id=7, size="medium", status="free"))  # M2
    db.session.add(Locker(id=8, size="small", status="free"))   # S5
    db.session.add(Locker(id=9, size="small", status="free"))   # S6
    db.session.add(Locker(id=21, size="small", status="free"))  # S7
    db.session.add(Locker(id=22, size="small", status="free"))  # S8

    # ===== DIREITA =====
    db.session.add(Locker(id=10, size="small", status="free"))  # S9
    db.session.add(Locker(id=11, size="medium", status="free")) # M3
    db.session.add(Locker(id=12, size="small", status="free"))  # S10
    db.session.add(Locker(id=13, size="large", status="free"))  # L2
    db.session.add(Locker(id=14, size="small", status="free"))  # S11
    db.session.add(Locker(id=15, size="small", status="free"))  # S12
    db.session.add(Locker(id=16, size="medium", status="free")) # M4
    db.session.add(Locker(id=17, size="small", status="free"))  # S13
    db.session.add(Locker(id=18, size="small", status="free"))  # S14
    db.session.add(Locker(id=19, size="small", status="free"))  # S15
    db.session.add(Locker(id=20, size="small", status="free"))  # S16

    db.session.commit()
    print("Lockers criados manualmente com IDs fixos!")

# Executa seed
with app.app_context():
    seed_manual()