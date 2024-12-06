from flask import Flask, request, jsonify

import requests
import logging

app = Flask(__name__)

# Configurazione API
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
    """
    Route principale per visualizzare un messaggio di benvenuto.
    """
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
        data = request.get_json()
        logger.info(f"Dati ricevuti dal frontend: {data}")

        provincia = data.get('provincia')
        comune = data.get('comune')
        indirizzo = data.get('indirizzo')

        if not provincia or not comune or not indirizzo:
            logger.warning("Parametri mancanti.")
            return jsonify({"success": False, "message": "Parametri mancanti."}), 400

        endpoint = f"{SERVER_URL}/geonets/{provincia}/{comune}/strade"
        params = {
            "term": indirizzo,
            "filter": "active",
            "limit": 10
        }
        logger.info(f"Richiesta all'API: {endpoint} con {params}")
        response = requests.get(endpoint, headers=HEADERS, params=params, timeout=10)

        if response.status_code == 200:
            results = response.json()
            logger.info(f"Risultati ottenuti: {results}")
            return jsonify({"success": True, "data": results})
        else:
            logger.error(f"Errore API: {response.status_code} - {response.text}")
            return jsonify({"success": False, "message": "Errore durante la verifica."}), response.status_code
    except Exception as e:
        logger.error(f"Errore interno: {e}")
        return jsonify({"success": False, "message": "Errore interno del server."}), 500

if __name__ == '__main__':
    logger.info("### Avviando il server Flask ###")
    print("\n******************************************")
    print("*  Server Flask attivo su http://127.0.0.1:5000  *")
    print("******************************************\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
