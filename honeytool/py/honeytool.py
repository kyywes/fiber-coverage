from flask import Flask, request, jsonify
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le origini

# Configurazione API remota
SERVER_URL = "https://honeytools.warian.net:4443"
ACCESS_TOKEN = "r8tgzETmBPreAgmWghAvaFHRzeHgW9WS"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

@app.route('/')
def home():
    return """
    <html>
        <head><title>Server Flask</title></head>
        <body>
            <h1 style="text-align: center;">Server Flask Attivo</h1>
            <p style="text-align: center;">Il server è in esecuzione correttamente.</p>
        </body>
    </html>
    """

@app.route('/check-coverage', methods=['POST'])
def check_coverage():
    try:
        if not request.data:
            logger.error("Corpo della richiesta vuoto.")
            logger.error(f"Headers della richiesta: {request.headers}")
            return jsonify({"success": False, "message": "Corpo della richiesta vuoto."}), 400

        logger.info(f"Raw data ricevuto: {request.data.decode('utf-8')}")
        logger.info(f"Headers della richiesta: {request.headers}")
        data = request.get_json(force=True)
        logger.info(f"Dati JSON decodificati: {data}")

        provincia = data.get('provincia')
        comune = data.get('comune')
        indirizzo = data.get('indirizzo')

        if not provincia or not comune or not indirizzo:
            logger.warning("Parametri mancanti.")
            return jsonify({"success": False, "message": "Parametri mancanti."}), 400

        # Chiamata all'API remota
        endpoint = f"{SERVER_URL}/geonets/{provincia}/{comune}/strade"
        params = {
            "term": indirizzo,
            "filter": "active",
            "limit": 10
        }
        logger.info(f"Chiamata all'API remota: {endpoint} con parametri: {params}")
        logger.info(f"Headers utilizzati: {HEADERS}")
        response = requests.get(endpoint, headers=HEADERS, params=params)

        if response.status_code == 200:
            results = response.json()
            logger.info(f"Risultati dall'API remota: {results}")

            if not results:
                logger.info(f"Nessun risultato trovato per i parametri: {params}")
                return jsonify({"success": False, "message": "Nessuna copertura trovata."}), 404
            return jsonify({"success": True, "data": results}), 200
        else:
            logger.error(f"Errore API remota: {response.status_code} - {response.text}")
            return jsonify({"success": False, "message": "Errore API remota."}), response.status_code
    except Exception as e:
        logger.error(f"Errore interno: {e}")
        return jsonify({"success": False, "message": f"Errore interno del server: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
