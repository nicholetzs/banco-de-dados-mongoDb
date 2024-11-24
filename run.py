# run.py
from app import create_app  # Importa a função create_app do arquivo app.py

if __name__ == '__main__':
    app = create_app()  # Cria a aplicação
    app.run(debug=False)  # Roda a aplicação, sem o modo de debug
