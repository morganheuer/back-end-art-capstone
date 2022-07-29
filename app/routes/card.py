import re
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board

def handle_id_request(id, db):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid {db.__name__} ID '{id}'."}, 400))

    query = db.query.get(id)

    if not query:
        abort(make_response({"msg": f"{db.__name__} ID '{id}' does not exist."}, 404))

    return query

def validate_card_body(card_body):
    expected_elements = ("title", "artist", "img_src", "year" "board_id")
    for element in expected_elements:
        print(len(element))
        if element not in card_body:
            abort(
                make_response({"msg": f"Invalid data: Missing {element}"},400)
            )
        elif len(card_body["message"]) > 140:
            abort(
                make_response({"msg": f"Invalid data: Message longer than 140 characters"},400)
            )
    return card_body


cards_bp = Blueprint('cards', __name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST"])
def create_new_card():
    request_body = validate_card_body(request.get_json())
    
    handle_id_request(request_body["board_id"], Board)

    new_card = Card(
        artist = request_body["artist"],
        title = request_body["title"],
        year = request_body["year"],
        img_src = request_body["img_src"],
        board_id = request_body["board_id"]
    )
    
    db.session.add(new_card)
    db.session.commit()

    confirmation_msg = jsonify(f"New card #{new_card.card_id} successfully created")
    return make_response(confirmation_msg, 201)

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    active_card = handle_id_request(card_id, Card)

    db.session.delete(active_card)
    db.session.commit()

    confirmation_msg = jsonify({"details": f"Card {card_id} successfully deleted."})
    return make_response(confirmation_msg, 200)