from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'super_secret_key'

user_order = []

# Load menu from JSON
def load_menu():
    with open("data/menu.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Save orders to a file
def save_order(order_data):
    orders_file = "data/orders.json"
    if not os.path.exists(orders_file):
        with open(orders_file, "w") as f:
            json.dump([], f)

    with open(orders_file, "r+", encoding="utf-8") as f:
        orders = json.load(f)
        orders.append(order_data)
        f.seek(0)
        json.dump(orders, f, indent=4)

# Homepage
@app.route("/")
def homepage():
    return render_template("home.html")

# Chatbot page
@app.route("/chat")
def chat():
    menu = load_menu()
    return render_template("chat.html", menu=menu)

# Handle chatbot logic
@app.route("/message", methods=["POST"])
def message():
    user_input = request.json.get("message", "").strip().lower()
    language = request.json.get("language", "en")  # default to English
    session["language"] = language  # Save selected language
    menu = load_menu()
    reply = ""

    if user_input in ["hi", "hello"]:
        reply = "👋 Hi there! What would you like to order?"
    elif user_input in ["no", "nothing", "that's all"]:
        reply = "👍 Got it. You can type 'confirm' to place your order or 'cancel' to discard."
    elif user_input in ["thanks", "thank you"]:
        reply = "😊 You’re welcome! Let me know if you need anything else."
    elif user_input in ["bye", "goodbye"]:
        reply = "👋 Goodbye! Hope to see you again at Café NovaBot."
    elif "receipt" in user_input or "reciept" in user_input or "bill" in user_input:
        if session.get("last_order"):
            reply = "🧾 You can view your receipt at /order-confirmed"
        else:
            reply = "📭 You haven’t placed an order yet. Try ordering something first!"
    elif "menu" in user_input:
        menu_items = [f"{item['name']['en']} - ₹{item['price']}" for item in menu]
        reply = "📋 Here's our menu:\n" + "\n".join(menu_items)
    elif "cancel" in user_input:
        user_order.clear()
        reply = "❌ Your order has been canceled. Let me know if you’d like to start a new one."
    elif "confirm" in user_input:
        if user_order:
            total = sum(item["price"] for item in user_order)
            tax = round(total * 0.05, 2)  # 5% tax
            grand_total = round(total + tax, 2)
            order_data = {
                "order_id": str(uuid.uuid4())[:8].upper(),
                "items": user_order.copy(),
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "language": language
            }
            session["last_order"] = order_data
            save_order(order_data)
            user_order.clear()
            reply = "✅ Your order is confirmed! Visit /order-confirmed to view your receipt."
        else:
            reply = "🛒 Your cart is empty. Please add items before confirming."
    else:
        item_lookup = {}
        for item in menu:
            for lang, name in item["name"].items():
                item_lookup[name.lower()] = item

        matched_item = None
        for name in item_lookup.keys():
            if name == user_input:
                matched_item = item_lookup[name]
                break

        if matched_item:
            user_order.append(matched_item)
            reply = f"✅ {matched_item['name'].get(language, matched_item['name']['en'])} added to your order.\n☕ Would you like anything else?"
        else:
            reply = "🤖 I didn’t quite get that. Try typing ‘menu’, a food item, ‘confirm’, or ‘cancel’."

    return jsonify({"reply": reply})

# Order confirmation page
@app.route("/order-confirmed")
def order_confirmed():
    last_order = session.get("last_order", None)
    if last_order:
        return render_template(
            "order_confirmed.html",
            order=last_order["items"],
            total=last_order["total"],
            tax=last_order["tax"],
            grand_total=last_order["grand_total"],
            order_id=last_order["order_id"],
            timestamp=last_order["timestamp"],
            language=last_order.get("language", "en")
        )
    else:
        return redirect(url_for("chat"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
