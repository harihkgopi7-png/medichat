from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)


def load_medicines():
    with open("medicines.json", encoding="utf-8") as f:
        items = json.load(f)
    # prices.json is optional: {"Dolo 650": "₹30 for 15 tablets", ...}
    try:
        with open("prices.json", encoding="utf-8") as f:
            prices = json.load(f)
    except FileNotFoundError:
        prices = {}
    for m in items:
        p = prices.get(m["name"], "").strip()
        if p:
            m["price"] = p
    return items


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    q = request.args.get("q", "").lower().strip()
    if not q:
        return jsonify([])
    medicines = load_medicines()  # re-read so edits to prices.json show on refresh
    result = [
        m for m in medicines
        if q in m["name"].lower()
        or q in m["generic"].lower()
        or q in m["purpose"].lower()
    ]
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
