<?php
require_once get_template_directory() . '/vendor/autoload.php';

use Dotenv\Dotenv;

try {
    $dotenv = Dotenv::createImmutable(get_template_directory());
    $dotenv->load();
} catch (Exception $e) {
    error_log('Errore durante il caricamento del file .env: ' . $e->getMessage());
    $_ENV['API_URL'] = 'http://127.0.0.1:5000/check-coverage'; // Default
    error_log('Impossibile caricare API_URL dal file .env. Usando il valore di default.');
}

// Carica gli script
function fiber_enqueue_scripts() {
    wp_enqueue_script('fiber-js', get_template_directory_uri() . '/js/modulo.js', array('jquery'), null, true);

    wp_localize_script('fiber-js', 'fiberAjax', array(
        'ajax_url' => $_ENV['API_URL'], // URL del server Flask
        'security' => wp_create_nonce('fiber_nonce'),
    ));
}
add_action('wp_enqueue_scripts', 'fiber_enqueue_scripts');

// Gestore delle richieste AJAX
function fiber_check_handler() {
    check_ajax_referer('fiber_nonce', 'security');

    $provincia = isset($_POST['provincia']) ? sanitize_text_field($_POST['provincia']) : '';
    $comune = isset($_POST['comune']) ? sanitize_text_field($_POST['comune']) : '';
    $indirizzo = isset($_POST['indirizzo']) ? sanitize_text_field($_POST['indirizzo']) : '';

    error_log("Dati ricevuti dal frontend:");
    error_log(print_r($_POST, true)); // Logga i dati ricevuti

    if (empty($provincia) || empty($comune) || empty($indirizzo)) {
        wp_send_json_error(['message' => 'Tutti i campi sono obbligatori.']);
        return;
    }

    $response = wp_remote_post($_ENV['API_URL'], [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode([
            'provincia' => $provincia,
            'comune' => $comune,
            'indirizzo' => $indirizzo,
        ]),
        'timeout' => 30,
    ]);

    if (is_wp_error($response)) {
        error_log('Errore nella richiesta: ' . $response->get_error_message());
        wp_send_json_error(['message' => 'Errore durante la connessione al server Flask.']);
        return;
    }

    $body = wp_remote_retrieve_body($response);
    error_log("Risposta da Flask: " . $body);
    $data = json_decode($body, true);

    if (!empty($data['success']) && $data['success'] === true) {
        wp_send_json_success($data['data']);
    } else {
        wp_send_json_error(['message' => $data['message'] ?? 'Nessun risultato trovato.']);
    }
}
add_action('wp_ajax_fiber_check', 'fiber_check_handler');
add_action('wp_ajax_nopriv_fiber_check', 'fiber_check_handler');
?>

