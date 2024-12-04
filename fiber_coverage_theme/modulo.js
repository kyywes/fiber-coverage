document.addEventListener("DOMContentLoaded", function () {
    const fiberForm = document.getElementById('fiber-form');
    const fiberResults = document.getElementById('fiber-results');

    fiberForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        fiberResults.innerHTML = "<p>Caricamento in corso...</p>";

        const provincia = document.getElementById('provincia').value.trim();
        const comune = document.getElementById('comune').value.trim();
        const indirizzo = document.getElementById('indirizzo').value.trim();

        if (!provincia || !comune || !indirizzo) {
            fiberResults.innerHTML = "<p style='color:red;'>Tutti i campi sono obbligatori.</p>";
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/check-coverage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ provincia, comune, indirizzo })
            });

            if (!response.ok) {
                throw new Error(`Errore HTTP ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                fiberResults.innerHTML = `<p>Copertura trovata: ${result.data}</p>`;
            } else {
                fiberResults.innerHTML = "<p>Nessun risultato trovato.</p>";
            }
        } catch (error) {
            fiberResults.innerHTML = "<p style='color:red;'>Errore durante la verifica della copertura.</p>";
        }
    });
});
