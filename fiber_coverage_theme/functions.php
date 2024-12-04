<?php
require_once get_template_directory() . '/vendor/autoload.php'; // Carica il gestore per il file .env

// Carica le variabili dal file .env
$dotenv = Dotenv\Dotenv::createImmutable(get_template_directory());
$dotenv->load();
$api_url = $_ENV['API_URL'];

function fiber_enqueue_scripts() {
    wp_enqueue_style('fiber-style', get_stylesheet_uri());
    wp_enqueue_script('fiber-js', get_template_directory_uri() . '/js/fiber.js', array('jquery'), null, true);

    // Passa variabili JavaScript al file frontend
    wp_localize_script('fiber-js', 'fiberAjax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'security' => wp_create_nonce('fiber_nonce'),
    ));
}
add_action('wp_enqueue_scripts', 'fiber_enqueue_scripts');

function fiber_check_handler() {
    // Controlla il nonce per la sicurezza
    check_ajax_referer('fiber_nonce', 'security');

    // Validazione e sanificazione dei dati
    $provincia = isset($_POST['provincia']) ? sanitize_text_field($_POST['provincia']) : '';
    $comune = isset($_POST['comune']) ? sanitize_text_field($_POST['comune']) : '';
    $indirizzo = isset($_POST['indirizzo']) ? sanitize_text_field($_POST['indirizzo']) : '';

    if (empty($provincia) || empty($comune) || empty($indirizzo)) {
        wp_send_json_error('Parametri mancanti.');
        return;
    }

    // Effettua la chiamata all'API Python
    $response = wp_remote_post($GLOBALS['api_url'], [
        'headers' => ['Content-Type' => 'application/json'],
        'body'    => json_encode([
            'provincia' => $provincia,
            'comune'    => $comune,
            'indirizzo' => $indirizzo
        ]),
        'timeout' => 15,
    ]);

    if (is_wp_error($response)) {
        wp_send_json_error('Errore durante la connessione al server.');
        return;
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    if (isset($data['success']) && $data['success'] === true) {
        wp_send_json_success($data['data']);
    } else {
        wp_send_json_error('Nessun risultato trovato.');
    }
}
add_action('wp_ajax_fiber_check', 'fiber_check_handler');
add_action('wp_ajax_nopriv_fiber_check', 'fiber_check_handler');
?>
