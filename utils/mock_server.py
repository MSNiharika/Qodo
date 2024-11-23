from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/v1/plugin', methods=['POST'])
def plugin_mock():
    data = request.json
    if data.get("input") == "Hello, AI!":
        return jsonify({"response": "Hello, user!"})
    elif data.get("input") == "Tell me a joke.":
        return jsonify({"response": "Why don't scientists trust atoms? Because they make up everything!"})
    else:
        return jsonify({"response": "Unknown input"}), 400

if __name__ == "__main__":
    app.run(port=8000)