<?php get_header(); ?>
<div id="fiber-search">
    <h1>Verifica Copertura Fibra</h1>
    <form id="fiber-form">
        <label for="provincia">Provincia:</label>
        <input type="text" id="provincia" name="provincia" required>
        
        <label for="comune">Comune:</label>
        <input type="text" id="comune" name="comune" required>
        
        <label for="indirizzo">Indirizzo:</label>
        <input type="text" id="indirizzo" name="indirizzo" required>
        
        <button type="submit">Verifica</button>
    </form>
    <div id="fiber-results"></div>
</div>
<script>
    document.getElementById('fiber-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const response = await fetch('<?php echo admin_url('admin-ajax.php'); ?>', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        document.getElementById('fiber-results').innerHTML = JSON.stringify(result.data);
    });
</script>
<?php get_footer(); ?>