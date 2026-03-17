from flask import Flask, render_template, request, jsonify
import random
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Order, Locker
from models import find_available_locker

from utils.messaging import send_code, send_pickup_notice

app = Flask(__name__)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def landing():
    return render_template("landing/index.html")


@app.route("/delivery")
def delivery():
    return render_template("delivery/delivery.html")

@app.route("/debug")
def debug():
    return render_template("debug/debug.html")

@app.route("/locker")
def locker():
    return render_template("locker/locker.html")

@app.route("/api/lockers")
def api_lockers():
    lockers = Locker.query.all()

    return jsonify([
        {
            "id": l.id,
            "size": l.size,
            "status": l.status
        }
        for l in lockers
    ])



@app.route("/close_locker", methods=["POST"])
def close_locker():

    order = Order.query.get(request.json["order_id"])

    locker = order.locker

    locker.status = "free"
    order.status = "delivered"

    db.session.commit()

    return jsonify({
        "status":"success",
        "locker_id": locker.id
    })
@app.route("/delivery_create", methods=["POST"])
def delivery_create():

    data = request.json

    locker = find_available_locker(data["size"])

    if not locker:
        print("Nenhum locker disponível")
        return {"status":"error"}

    code = str(random.randint(100000,999999))

    order = Order(
        name=data["name"],
        email=data["email"],
        size=data["size"],
        code=code,
        locker=locker
    )

    locker.status = "open"

    db.session.add(order)
    db.session.commit()

    print("\nNOVO PEDIDO CRIADO")
    print("Cliente:", order.name)
    print("Email:", order.email)
    print("Locker:", locker.id)
    print("Código do cliente:", code)
    print("Locker aberto para o entregador colocar o pacote\n")

    return {
        "status":"success",
        "locker_id":locker.id
    }

@app.route("/delivery_close", methods=["POST"])
def delivery_close():

    locker_id = request.json["locker_id"]

    locker = Locker.query.get(locker_id)

    order = Order.query.filter_by(locker_id=locker_id).first()

    locker.status = "occupied"

    db.session.commit()

    send_code(order.email, order.code, locker.id)

    print("\n PACOTE ENTREGUE NO LOCKER")
    print("Locker:", locker.id)
    print("Cliente:", order.name)
    print("Email:", order.email)
    print("Código para retirada:", order.code)
    print("Cliente notificado (DEBUG)\n")

    return {"status":"success"}

@app.route("/open_locker", methods=["POST"])
def open_locker():

    code = request.json["code"]

    order = Order.query.filter_by(code=code).first()

    if not order:
        return {"status":"error","message":"Código inválido"}

    locker = order.locker

    locker.status = "open"

    db.session.commit()

    print("🔓 Cliente abriu locker", locker.id)

    return {
        "status":"success",
        "locker_id":locker.id,
        "order_id":order.id
    }

@app.route("/client_close", methods=["POST"])
def client_close():

    order_id = request.json["order_id"]

    order = Order.query.get(order_id)

    locker = order.locker

    locker.status = "free"

    print("\nPACOTE RETIRADO")
    print("Cliente:", order.name)
    print("Locker:", locker.id)

    send_pickup_notice(order.email, locker.id)

    order.status = "completed"
    order.locker = None   # remove ligação com locker

    db.session.commit()

    return {"status":"success"}

@app.route("/debug/set_locker", methods=["POST"])
def debug_set_locker():

    locker_id = request.json["locker_id"]
    status = request.json["status"]

    locker = Locker.query.get(locker_id)

    locker.status = status

    if status == "free" and locker.order:
        locker.order.locker = None
        locker.order.status = "completed"
        print("DEBUG limpou ligação do pedido")

    db.session.commit()

    return {"status":"success"}

@app.route("/api/debug")
def debug_data():

    lockers = Locker.query.all()

    data = []

    for l in lockers:

        order = Order.query.filter_by(locker_id=l.id).first()

        order_data = None

        if order:
            order_data = {
                "id": order.id,
                "name": order.name,
                "email": order.email,
                "code": order.code,
                "status": order.status
            }

        data.append({
            "id": l.id,
            "size": l.size,
            "status": l.status,
            "order": order_data
        })

    return jsonify(data)

@app.route("/debug/close_locker", methods=["POST"])
def debug_close_locker():

    locker_id = request.json["locker_id"]

    locker = Locker.query.get(locker_id)

    if locker.status == "open":

        if locker.order and locker.order.status != "completed":
            locker.status = "occupied"
            print("DEBUG: locker fechado com encomenda")

        else:
            locker.status = "free"
            print("DEBUG: locker fechado e ficou livre")

        db.session.commit()

    return {"status":"success"}

if __name__ == "__main__":
    app.run(debug=True)
