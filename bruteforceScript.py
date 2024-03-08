import requests
from bs4 import BeautifulSoup
# pip install beautifulsoup4

# URL und Anmeldedaten an Ihre Flask-App anpassen
url = "http://localhost:1234/login"
data = {"username": "fakeuser", "password": "fakepass"}

# Starten Sie eine Session, um Cookies zu behalten (wichtig für Flash-Nachrichten)
with requests.Session() as session:
    for i in range(11):
        # Senden Sie die POST-Anfrage
        response = session.post(url, data=data)

        # Nutzen Sie BeautifulSoup, um das HTML zu parsen
        soup = BeautifulSoup(response.text, 'html.parser')

        # Suchen Sie nach dem Div, das die Flash-Nachrichten enthält
        # (Passen Sie die Klasse an das an, was Sie in Ihren HTML-Templates verwenden)
        flash_messages = soup.find_all('div', class_='alert-danger')

        print(f"Anfrage {i+1}, Status-Code: {response.status_code}")

        # Wenn Flash-Nachrichten gefunden wurden, drucken Sie sie aus
        for message in flash_messages:
            print(message.text.strip())

        # Optional: kurze Pause zwischen Anfragen, um das Timing realistischer zu gestalten
        # time.sleep(1)
