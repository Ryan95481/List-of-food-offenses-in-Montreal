function send_plainte(){
    let champEtab = document.getElementById('champ_etablissement').value;
    let champAdresse = document.getElementById('champ_adresse').value;
    let champVille = document.getElementById('champ_ville').value;
    let champDateVisite = document.getElementById('champ_date_visite').value;
    let champNom = document.getElementById('champ_nom').value;
    let champPrenom = document.getElementById('champ_prenom').value;
    let champDescription = document.getElementById('champ_description').value;

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                alert("Plainte créée");
            } else{
                alert("Une erreur est survenue");
            }
        }
    };
    xhr.open('POST', '/inspection', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        'etablissement': champEtab,
        'adresse': champAdresse,
        'ville': champVille,
        'date_visite': champDateVisite,
        'nom': champNom,
        'prenom': champPrenom,
        'description': champDescription
    }));
}

document.getElementById('btn_plainte').addEventListener('click', function(event) {
    event.preventDefault();
    send_plainte();
});