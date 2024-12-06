document.addEventListener("DOMContentLoaded", function () {
    const fiberForm = document.getElementById("fiber-form");
    const fiberResults = document.getElementById("fiber-results");

    fiberForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita il refresh della pagina
        fiberResults.innerHTML = "<p>Verifica in corso...</p>";

        const data = {
            provincia: document.querySelector('[name="provincia"]').value,
            comune: document.querySelector('[name="comune"]').value,
            indirizzo: document.querySelector('[name="indirizzo"]').value,
        };

        console.log("Dati inviati al server:", data); // Debug

        try {
            const response = await fetch('http://127.0.0.1:5000/check-coverage', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // Forza il tipo di contenuto
                },
                body: JSON.stringify(data), // Converte i dati in JSON
            });

            console.log("Risposta del server:", response);

            if (!response.ok) {
                throw new Error(`Errore HTTP: ${response.status}`);
            }

            const result = await response.json();
            console.log("Risultato JSON:", result);

            if (result.success) {
                fiberResults.innerHTML = `
                    <p style="color:green;">
                        Copertura disponibile: ${JSON.stringify(result.data)}.
                    </p>`;
            } else {
                fiberResults.innerHTML = `
                    <p style="color:orange;">
                        ${result.message || 'Copertura non disponibile.'}
                    </p>`;
            }
        } catch (error) {
            console.error("Errore durante la richiesta:", error);
            fiberResults.innerHTML = `
                <p style="color:red;">
                    Errore durante la verifica: ${error.message}.
                </p>`;
        }
    });
});


