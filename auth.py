# Logik für die Loginseite
from datetime import datetime, timedelta
import re


# Funktion zur Erkennung von SQL-Injektionen
# Liste der bekannten Payloads für SQL-Injektionen
sql_injection_payloads = ["' OR '1'='1", "--", ";--", "' OR 1=1 --", "admin' --"]
def detect_sql_injection(username, password):
    for payload in sql_injection_payloads:
        if payload in username or payload in password:
            return True
    return False
# Hier speichern wir die Anmeldeversuche der letzten Zeit.
login_attempts = {}

def detect_brute_force(ip_address):
    global login_attempts  # Diese Zeile ist eigentlich nur nötig, wenn du login_attempts neu zuweisen würdest.
    current_time = datetime.now()
    window_time = timedelta(minutes=1)  # Zeitfenster von 5 Minuten für die Überwachung
    max_attempts = 10  # Maximale Versuche innerhalb des Zeitfensters

    # Bereinigen alter Anmeldeversuche
    # Entferne Einträge direkt aus login_attempts, ohne Neuzuweisung
    for ip in list(login_attempts.keys()):
        if (current_time - login_attempts[ip]['first_attempt_time']) > window_time:
            del login_attempts[ip]

    # Überprüfen, ob die IP-Adresse bereits Anmeldeversuche hat
    if ip_address in login_attempts:
        login_attempts[ip_address]['attempts'] += 1
        login_attempts[ip_address]['last_attempt_time'] = current_time
    else:
        # Beginnen Sie die Überwachung einer neuen IP-Adresse
        login_attempts[ip_address] = {'first_attempt_time': current_time, 'last_attempt_time': current_time, 'attempts': 1}

    # Überprüfen, ob die Anzahl der Versuche das Limit überschreitet
    if ip_address in login_attempts and login_attempts[ip_address]['attempts'] > max_attempts:
        return True

    return False

# Funktion zur Erkennung potenzieller XSS-Angriffe in Benutzereingaben
def detect_xss_attack(input_string):
    # Regex, um gängige XSS-Angriffsmuster zu erkennen
    xss_pattern = re.compile(r'<script.*?>.*?</script>|<.*?javascript:.*?>|<.*?on\w+.*?=.*?>', re.IGNORECASE)
    return xss_pattern.search(input_string) is not None

def detect_directory_traversal(input_string):
    # Muster, die auf Directory Traversal hinweisen könnten
    traversal_patterns = ['../', '..\\', '/etc/passwd', 'c:\\windows']
    
    # Überprüfen der Eingabe gegen jedes Muster
    for pattern in traversal_patterns:
        if pattern in input_string:
            return True
    return False
def detect_command_injection(input_string):
    # Liste gefährlicher Zeichen und Befehlssequenzen
    dangerous_patterns = [';', '|', '&', '$', '`', '||', '&&']
    
    # Überprüfen der Eingabe gegen jedes gefährliche Muster
    for pattern in dangerous_patterns:
        if pattern in input_string:
            return True
    return False
