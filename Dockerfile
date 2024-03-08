# Basis-Image
FROM python:3.8-alpine

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Abhängigkeiten installieren
# Kopiere die requirements.txt Datei in das Arbeitsverzeichnis
COPY requirements.txt /app/
# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Anwendungscode in das Arbeitsverzeichnis im Container
COPY . /app

# Exponiere den Port, auf dem die Anwendung läuft
EXPOSE 1234

ENV FLASK_APP=app.py

# Startbefehl für die Anwendung
CMD ["flask", "run", "--host=0.0.0.0", "--port=1234"]
