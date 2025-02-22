from app import create_app  # Hämta create_app från app-mappen

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")