from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from auth import detect_sql_injection, detect_brute_force, detect_xss_attack, detect_directory_traversal, detect_command_injection
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key1234')

# Erstellung einer Variable mit Benutzernamen und Passwortkombinationen
#benutzer_daten =
benutzername_passwort_kombinationen = {
    "Marco": {"password": "A8d3E4r5T", "security_question": "Was ist dein erstes Auto?", "security_answer": "Volkswagen"},
    "Johannes": {"password": "mN6bV5cX4z", "security_question": "Was ist dein erstes Auto?", "security_answer": "BMW"},
    "Sophia": {"password": "1q2W3e4R5t", "security_question": "Was ist dein erstes Auto?", "security_answer": "Toyota"},
    "Lena": {"password": "Z7x8C9vB0n", "security_question": "Was ist dein erstes Auto?", "security_answer": "Ford"}
}

def is_valid_payload(payload):
    #SSTI Schwachstelle kann durch eingeben von '{{}}' ausgelöst werden
    try:
        # Check if the payload contains the correct SSTI structure
        return '{{' in payload and '}}' in payload
    except Exception:
        # If there's an exception during evaluation, consider it an invalid payload
        return False

@app.route('/')
def index():
    '''if current_user.is_authenticated:
        return render_template('studip.html')'''
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #Passwortprüfung neue Benutzerstruktur
        '''if username in benutzer_daten and benutzer_daten[username]['password’] == password:
            return redirect(url_for('studip'))
            else:
                flash('Invalid username or password. Please try again.', 'danger')
        return render_template('login.html')'''
        ip_address = request.remote_addr  # Client-IP-Adresse für Brute-Force-Erkennung

        # SQL-Injektionsprüfung
        if detect_sql_injection(username, password):
            # Wenn eine SQL-Injektion erkannt wird, anzeigen einer Nachricht
            flash('Nice try! But that won\'t work here. FLAG{SQL_INJECTION_ATTEMPT_DETECTED}', 'danger')
            return redirect(url_for('login'))
        # Brute-Force-Prüfung
        if detect_brute_force(ip_address):
            flash('Too many login attempts. Please try again later. FLAG{Brute_Force_Attempt_Detected}', 'danger')
            return redirect(url_for('login'))
        # XSS-Prüfung
        if detect_xss_attack(username) or detect_xss_attack(password):
            flash('XSS Attack detected! Nice try.', 'danger')
            return redirect(url_for('login'))  
        # Command Injection-Prüfung
        if detect_command_injection(username) or detect_command_injection(password):
            flash('Command Injection attempt detected! Nice try.', 'danger')
            return redirect(url_for('login'))     
        # Überprüfen, ob der Benutzer existiert und das Passwort korrekt ist
        if username in benutzername_passwort_kombinationen and benutzername_passwort_kombinationen[username] == password:
            return redirect(url_for('studip'))
        else:
            # Falsche Anmeldeinformationen, zeige eine Nachricht an
            flash('Invalid username or password. Please try again.', 'danger')
            #return redirect(url_for('login'))
            return render_template('login.html')


    return render_template('login.html')

        # Logik zum Passwort zurücksetzen von x user
        # welche Rechte, welche Flag -> Fehlerhafte Passwortlogik 
        # User kann alles    kann Daten runterladen
        # normaler User     kann auf die Startpage und sachen ansehen
        # User der nach mehr aussieht   kann daten hochladen
        # nach freischaltung sowas wie studip 

#Route Passwortwiederherstellung
'''@app.route('/recover_password', methods=['GET', 'POST'])
def recorver_password():
    if request.method == 'POST':
        username = request.form['username']
        security_answer = request.form['security_answer']

        if username in benutzer_daten and benutzer_daten[username]['security_answer'].lower() == security_answer.lower():
            return redirect(url_for('reset_password, username=username'))
        else:
            flash('Incorrect username or security answer. Please try again.', 'danger')
            return redirect(url_for('login'))
        return render_template('reset:password.html', username=username)'''
    
#Route Passwortzurücksetzen
'''@app.route('reset_password/<username>', methods=['GET', 'POST'])
def rest_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        if username in benutzer_daten:
            benutzer_daten[username]['password'] = new_password
            flash('Your password has been updated successfully.', 'info')
            return redirect(url_for('login'))
        return redirect_template('reset_password.html', username=username)'''
    

@app.route('/view-file', methods=['GET'])
def view_file():
    file_path = request.args.get('file_path')
    
    # Directory Traversal-Prüfung
    if detect_directory_traversal(file_path):
        flash('Directory Traversal attempt detected!', 'danger')
        return redirect(url_for('login'))  # Leite zur Loginsseite, da man dort weiterkommt
    # keine Logik zum Anzeigen einer Datei da Sackgasse
# Angriff: curl "http://localhost:1234/view-file?file_path=../secret.txt"


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    # Logik zum Löschen der Benutzersitzung oder der Cookies
    flash('You have been logged out successfully.', 'infoLogout')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/alumni')
def alumni():
    return render_template('alumni.html')

@app.route('/studip')
def studip():
    return render_template("studip.html")

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        inquiry = request.form.get('inquiry')
        
        # Check if the payload is a valid SSTI structure
        if is_valid_payload(inquiry):
            # If valid, return the FLAG string
            flash('You have successfully exploited the SSTI vulnerability! FLAG{SSTI_EXPLOIT_SUCCESS}', 'danger')
            return redirect(url_for('form'))

    # If not a valid payload or not a POST request, do nothing
    return render_template('form.html')

# Teil für die API logik

# Simulierte Datenbank von Benutzerdaten
professors = {
    "Müller": {"Lehrstuhl": "Informatik", "email": "Professor.Mueller@techforwarduniversity.com"},
    "Schmidt": {"Lehrstuhl": "Maschinenbau", "email": "Professor.Schmidt@techforwarduniversity.com"},
    "Schneider": {"Lehrstuhl": "Physik", "email": "Professor.Schneider@techforwarduniversity.com"},
    "Fischer": {"Lehrstuhl": "Chemie", "email": "Professor.Fischer@techforwarduniversity.com"},
    "Weber": {"Lehrstuhl": "Mathematik", "email": "Professor.Weber@techforwarduniversity.com"},
    "Meyer": {"Lehrstuhl": "Biologie", "email": "Professor.Meyer@techforwarduniversity.com"},
    "Wagner": {"Lehrstuhl": "Geschichte", "email": "Professor.Wagner@techforwarduniversity.com"},
    "Becker": {"Lehrstuhl": "Kunstgeschichte", "email": "Professor.Becker@techforwarduniversity.com"},
    "Schulz": {"Lehrstuhl": "Philosophie", "email": "Professor.Schulz@techforwarduniversity.com"},
    "Hoffmann": {"Lehrstuhl": "Ingenieurwissenschaften", "email": "Professor.Hoffmann@techforwarduniversity.com"},
    # Leere Einträge
    "Error1": "Error",
    "Error2": "Error",
    # Eintrag mit einer Flag, die eine API ohne Authentifizierung kennzeichnet
    "Stone": {"Lehrstuhl": "Computer Science", "email": "FLAG{API_WITHOUT_AUTHENTICATION_DETECTED}@techforwarduniversity.com"}
}
#Angriff: curl "http://localhost:1234/api/professorinfo?lastname=Stone"

@app.route('/api/professorinfo', methods=['GET'])
def professor_info():
    lastname = request.args.get('lastname')
    
    if lastname in professors:
        professor_info = professors[lastname]
        # Gibt den kompletten Eintrag aus, einschließlich Lehrstuhl und E-Mail
        return jsonify({"error": "None", "lastname": lastname, **professor_info}), 200
    else:
        # Fehlermeldung
        return jsonify({"error": "Professor not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=1234)
