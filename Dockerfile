# Använd en officiell Python-image
FROM python:3.9

# Sätt arbetsmappen i containern
WORKDIR /app

# Kopiera projektfiler till containern
COPY . /app

# Installera beroenden från requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponera port 5000
EXPOSE 5000

# Starta applikationen
CMD ["python", "app.py"]        