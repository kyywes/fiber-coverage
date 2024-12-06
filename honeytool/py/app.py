from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Il server Flask è attivo!</h1>"

@app.route('/check-coverage', methods=['POST'])
def check_coverage():
    print("Headers:", request.headers)
    print("Body:", request.data)
    print("JSON:", request.get_json())

    # Controlla che il Content-Type sia application/json
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    provincia = data.get('provincia')
    comune = data.get('comune')
    indirizzo = data.get('indirizzo')

    if not all([provincia, comune, indirizzo]):
        return jsonify({"error": "Missing parameters"}), 400

    # Simula una risposta di successo
    return jsonify({"success": True, "data": {"copertura": "FTTH"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



