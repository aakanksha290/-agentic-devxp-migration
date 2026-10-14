# A tiny sample service so the pipeline has something real to build and test.
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok")


def calculate_fee(amount):
    """Payments fee: 2% with a minimum of 1."""
    fee = amount * 0.02
    if fee < 1:
        fee = 1
    return round(fee, 2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
