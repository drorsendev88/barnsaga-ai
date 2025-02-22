# Använd en mindre basimage för en lättare och snabbare container
FROM python:3.9-slim

# Sätt arbetsmappen i containern
WORKDIR /app

# Kopiera beroenden först för att optimera byggprocessen
COPY requirements.txt .

# Installera beroenden
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera hela projektet
COPY . .

# Exponera port 5000
EXPOSE 5000

# Starta appen med Gunicorn för bättre prestanda
CMD ["python", "run.py"]
