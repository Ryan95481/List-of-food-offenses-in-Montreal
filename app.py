import hashlib
import uuid
from flask import (Flask, g, render_template, send_file, make_response,
                   request, jsonify, session)
from flask_json_schema import JsonValidationError, JsonSchema
from schema import (contravention_schema, nouvel_inspection_schema,
                    nouveau_user_schema)
from database import Database
from inspection import Inspection
from utilisateur import Utilisateur
from apscheduler.schedulers.background import BackgroundScheduler
import xml.etree.ElementTree as ET
import csv
import io

scheduler = BackgroundScheduler()
app = Flask(__name__)
schema = JsonSchema(app)


def get_db():
    if not hasattr(g, '_database'):
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close_connection()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        recherche = request.form.get("search")
        resultat = get_db().rechercher_violation(recherche)
        return render_template('resultat.html', Violation=resultat)
    else:
        violations = get_db().afficher_violation()
        return render_template('index.html', Violation=violations)


@app.route('/contrevenants', methods=['GET'])
def contrevenants():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')
    violations = get_db().rechercher_violation_par_date(date_debut,
                                                        date_fin)
    return jsonify([violations.afficher_info()
                    for violations in violations])


@app.route('/infractions', methods=['GET'])
def infractions():
    violations = get_db().trier_par_nombre_infractions()
    return jsonify([{"business_id": violation[0],
                     "etablissement": violation[1],
                     "nombre_violations": violation[2]}
                    for violation in violations])


@app.route('/infractions-xml', methods=['GET'])
def infractions_xml():
    violations = get_db().trier_par_nombre_infractions()
    root = ET.Element('violations')
    for violation in violations:
        violation_element = ET.SubElement(root, 'violation')
        business_id = ET.SubElement(violation_element, 'business_id')
        etablissement = ET.SubElement(violation_element, 'etablissement')
        nombre_violations = ET.SubElement(violation_element, 'nb_violations')
        business_id.text = str(violation[0])
        etablissement.text = violation[1]
        nombre_violations.text = str(violation[2])

    xml_data = ET.tostring(root, encoding='utf8').decode('utf8')
    response = make_response(xml_data)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/infractions-csv', methods=['GET'])
def infractions_csv():
    violations = get_db().trier_par_nombre_infractions()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["business_id", "etablissement", "nombre_violations"])
    writer.writerows(violations)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment;"
    "filename=infractions.csv"
    response.headers["Content-type"] = "text/csv; charset=UTF-8"
    return response


@app.route('/inspection', methods=['POST'])
@schema.validate(nouvel_inspection_schema)
def inspection():
    data = request.get_json()
    inspection = Inspection(None, data['etablissement'], data['adresse'],
                            data['ville'], data['date_visite'], data['nom'],
                            data['prenom'], data['description'])
    inspection = get_db().creer_inspection(inspection)
    return jsonify(inspection.afficher_inspection()), 201


@app.route('/inspection', methods=['GET'])
def get_inspections():
    inspections = get_db().read_inspections()
    return jsonify([inspection.afficher_inspection()
                    for inspection in inspections])


@app.route('/inspection/<id>', methods=['DELETE'])
def suppression_inspection(id):
    inspection = get_db().read_one_inspection(id)
    if inspection is None:
        return "", 404
    else:
        get_db().supprimer_inspection(inspection)
        return "", 200


@app.route('/utilisateur', methods=['POST'])
@schema.validate(nouveau_user_schema)
def creer_utilisateur():
    data = request.get_json()
    user = Utilisateur(None, data['nom'], data['adresse'],
                       data['etablissements'], data['mot_de_passe'])
    user = get_db().sauvegarder_utilisateur(user)
    return jsonify(user.afficher_user()), 201


@app.route('/utilisateur', methods=['GET'])
def obtenir_utilisateurs():
    utilisateurs = get_db().read_utilisateurs()
    return jsonify([utilisateur.afficher_user()
                    for utilisateur in utilisateurs])


@app.route('/authentification', methods=["GET", "POST"])
def authentification():

    username = session.get("username")
    cursor = get_db().get_connection().cursor()
    if request.method == "POST":
        nom = request.form['nom']
        courriel = request.form['courriel']
        etablissements = request.form.getlist('etablissements')
        mot_de_passe = request.form['password']

        if not nom or not courriel or not etablissements or not mot_de_passe:
            return render_template('authentification.html',
                                   error="Tous les champs"
                                   "doivent être remplis.")
        else:
            salt = uuid.uuid4().hex
            hash_pass = hashlib.sha512((mot_de_passe + salt).
                                       encode("utf-8")).hexdigest()
            user = Utilisateur(None, nom, courriel, etablissements, hash_pass)
            get_db().sauvegarder_utilisateur(user)
            return render_template('index.html')
    else:
        cursor.execute("SELECT DISTINCT etablissement FROM Violation")
        etabs = cursor.fetchall()
        return render_template('authentification.html', etablissements=etabs)


@app.route('/plainte', methods=['GET', 'POST'])
def plainte():
    return render_template('plainte.html')


@app.route('/doc')
def doc():
    return render_template('doc.html')


if __name__ == "__main__":
    with app.app_context():
        scheduler.add_job(func=get_db().download_csv, trigger="cron",
                          day_of_week="mon-sun", hour=0, minute=00)
        scheduler.start()
        app.run(debug=True, use_reloader=False)
