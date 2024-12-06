import requests
import logging
import time

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Configurazione di base
SERVER_URL = "https://honeytools.warian.net:4443"  # URL del server
ENDPOINT = "/geonets/caserta/alife/strade"  # Endpoint specifico
ACCESS_TOKEN = "r8tgzETmBPreAgmWghAvaFHRzeHgW9WS"  # Token Bearer fornito

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

PARAMS = {
    "term": "sp ",
    "filter": "active",
    "limit": 100,
    "offset": 0
}

# Funzione per effettuare una richiesta GET
def make_get_request():
    """
    Effettua una richiesta GET all'endpoint specificato
    """
    url = f"{SERVER_URL}{ENDPOINT}"  # URL completo
    logger.info(f"Effettuando una richiesta a: {url} con parametri {PARAMS}")

    try:
        response = requests.get(url, headers=HEADERS, params=PARAMS, timeout=10)
        if response.status_code == 429:  # Too Many Requests
            retry_after = response.headers.get("Retry-After", 1)  # Default a 1 secondo se non specificato
            logger.warning(f"Raggiunto il limite di richieste. Ritento tra {retry_after} secondi...")
            time.sleep(int(retry_after))  # Aspetta prima di ritentare
            return make_get_request()  # Ritenta la richiesta
        response.raise_for_status()  # Solleva eccezione per altri codici di errore
        logger.info("Risposta ricevuta:")
        logger.info(response.json())  # Logga la risposta in formato JSON
        return response.json()
    except requests.exceptions.ConnectTimeout:
        logger.error("Errore: Timeout nella connessione al server.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore nella richiesta: {e}")
        raise

# Funzione per gestire la paginazione
def fetch_all_pages():
    """
    Esegue richieste paginando i risultati con gestione dei limiti
    """
    all_results = []
    current_offset = 0
    while True:
        logger.info(f"Richiesta con offset: {current_offset}")
        PARAMS["offset"] = current_offset
        try:
            data = make_get_request()
            if not data or len(data) == 0:
                break
            all_results.extend(data)
            current_offset += len(data)
            time.sleep(1)  # Aspetta tra le richieste
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante la richiesta con offset {current_offset}: {e}")
            break
    return all_results

# Esecuzione dello script
if __name__ == "__main__":
    try:
        logger.info("### Avviando la richiesta all'API ###")
        all_data = fetch_all_pages()
        logger.info(f"Dati totali ricevuti: {len(all_data)}")
        logger.info(all_data)
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione dello script: {e}")

import requests
import logging
import time

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Configurazione di base
SERVER_URL = "https://honeytools.warian.net:4443"  # URL del server
ENDPOINT = "/geonets/caserta/alife/strade"  # Endpoint specifico
ACCESS_TOKEN = "r8tgzETmBPreAgmWghAvaFHRzeHgW9WS"  # Token Bearer fornito

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

PARAMS = {
    "term": "sp ",
    "filter": "active",
    "limit": 100,
    "offset": 0
}

# Funzione per effettuare una richiesta GET
def make_get_request():
    """
    Effettua una richiesta GET all'endpoint specificato
    """
    url = f"{SERVER_URL}{ENDPOINT}"  # URL completo
    logger.info(f"Effettuando una richiesta a: {url} con parametri {PARAMS}")

    try:
        response = requests.get(url, headers=HEADERS, params=PARAMS, timeout=10)
        if response.status_code == 429:  # Too Many Requests
            retry_after = response.headers.get("Retry-After", 1)  # Default a 1 secondo se non specificato
            logger.warning(f"Raggiunto il limite di richieste. Ritento tra {retry_after} secondi...")
            time.sleep(int(retry_after))  # Aspetta prima di ritentare
            return make_get_request()  # Ritenta la richiesta
        response.raise_for_status()  # Solleva eccezione per altri codici di errore
        logger.info("Risposta ricevuta:")
        logger.info(response.json())  # Logga la risposta in formato JSON
        return response.json()
    except requests.exceptions.ConnectTimeout:
        logger.error("Errore: Timeout nella connessione al server.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore nella richiesta: {e}")
        raise

# Funzione per gestire la paginazione
def fetch_all_pages():
    """
    Esegue richieste paginando i risultati con gestione dei limiti
    """
    all_results = []
    current_offset = 0
    while True:
        logger.info(f"Richiesta con offset: {current_offset}")
        PARAMS["offset"] = current_offset
        try:
            data = make_get_request()
            if not data or len(data) == 0:
                break
            all_results.extend(data)
            current_offset += len(data)
            time.sleep(1)  # Aspetta tra le richieste
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante la richiesta con offset {current_offset}: {e}")
            break
    return all_results

# Esecuzione dello script
if __name__ == "__main__":
    try:
        logger.info("### Avviando la richiesta all'API ###")
        all_data = fetch_all_pages()
        logger.info(f"Dati totali ricevuti: {len(all_data)}")
        logger.info(all_data)
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione dello script: {e}")
