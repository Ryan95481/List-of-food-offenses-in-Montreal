function rechercher_date(){

    let dateDebut = document.getElementById('date_debut').value;
    let dateFin = document.getElementById('date_fin').value;
    let table = document.getElementById('tableDate');
    let etabNb = {};
    fetch('/contrevenants?du=' + dateDebut + '&au=' + dateFin)
        .then(response => response.json())
        .then(data => { 
            table.innerHTML = '';
            table.innerHTML = '<thead><tr><th>etablissement</th><th>nombre_violations</th></tr></thead><tbody>';
            data.forEach(violation => {
                etabNb[violation.etablissement] = (etabNb[violation.etablissement] || 0) + 1;
            });

            for (let etab in etabNb) {
                table.innerHTML += `<tr><td>${etab}</td><td>${etabNb[etab]}</td></tr>`;
            }

            table.innerHTML += '</tbody>';
        })
        .catch(error => {
            console.log("Error:", error);
        });
}

document.getElementById('search_date_btn').addEventListener('click', function(event) {
    event.preventDefault();
    rechercher_date();
});

