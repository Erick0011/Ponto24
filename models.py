# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Locker(db.Model):
    __tablename__ = "lockers"

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(20), nullable=False)  # ex: 'pequeno', 'medio', 'grande'
    status = db.Column(db.String(20), default="free")  # 'free' ou 'occupied'

    # Relacionamento com pedidos
    order = db.relationship("Order", back_populates="locker", uselist=False)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    size = db.Column(db.String(20))
    code = db.Column(db.String(10))
    status = db.Column(db.String(20), default="pending")  # pending, delivered

    # Locker relacionado
    locker_id = db.Column(db.Integer, db.ForeignKey("lockers.id"))
    locker = db.relationship("Locker", back_populates="order")


def find_available_locker(order_size):
    """
    Retorna o primeiro locker disponível com tamanho compatível.
    """
    # buscar lockers livres
    lockers = Locker.query.filter_by(status="free").all()
    # filtrar pelo tamanho compatível
    for locker in lockers:
        if locker.size == order_size:
            return locker
    return None  # nenhum locker disponível do tamanho correto
