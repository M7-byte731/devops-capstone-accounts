from flask import jsonify, request, make_response
from service import app
from service.models import DataValidationError, store


@app.route("/", methods=["GET"])
def index():
    return jsonify({"service": "Customer Accounts Microservice", "version": "1.0.0", "status": "running"}), 200


@app.route("/accounts", methods=["POST"])
def create_accounts():
    data = request.get_json(silent=True) or {}
    try:
        account = store.create(data)
    except DataValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    response = make_response(jsonify(account.to_dict()), 201)
    response.headers["Location"] = f"/accounts/{account.id}"
    return response


@app.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify([acc.to_dict() for acc in store.list_all()]), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id: int):
    account = store.get(account_id)
    if not account:
        return jsonify({"error": f"Account [{account_id}] not found"}), 404
    return jsonify(account.to_dict()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id: int):
    data = request.get_json(silent=True) or {}
    try:
        updated = store.update(account_id, data)
    except DataValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    if not updated:
        return jsonify({"error": f"Account [{account_id}] not found"}), 404
    return jsonify(updated.to_dict()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id: int):
    store.delete(account_id)
    return make_response("", 204)
