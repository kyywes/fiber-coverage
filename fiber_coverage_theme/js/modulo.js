document.addEventListener("DOMContentLoaded", function () {
    const fiberForm = document.getElementById("fiber-form");
    const fiberResults = document.getElementById("fiber-results");

    fiberForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita il refresh della pagina
        fiberResults.innerHTML = "<p>Verifica in corso...</p>";

        const formData = new FormData(fiberForm);

        try {
            const response = await fetch(fiberAjax.ajax_url, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Errore HTTP: ${response.status}`);
            }

            const result = await response.json();

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
            fiberResults.innerHTML = `
                <p style="color:red;">
                    Errore durante la verifica: ${error.message}.
                </p>`;
        }
    });
});

