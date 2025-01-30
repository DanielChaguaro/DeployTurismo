from app.__init__ import create_app

app = create_app()

@app.route('/')
def home():
    return "¡Hola, Render!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)