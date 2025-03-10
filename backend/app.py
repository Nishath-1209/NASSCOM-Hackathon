from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/gesture", methods=["POST"])
def recognize_gesture():
    data = request.get_json()
    gesture = data.get("gesture")
    return jsonify({"response": f"Gesture received: {gesture}"})

if __name__ == "__main__":
    app.run(debug=True)
