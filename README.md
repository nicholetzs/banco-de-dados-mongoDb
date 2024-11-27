Projeto de Carros - Aplicação Flask com MongoDB

Este é um projeto que implementa uma aplicação web para gerenciar carros, com funcionalidades de adicionar, editar e listar carros. A aplicação utiliza Flask como framework web e MongoDB como banco de dados.

Dependências
O projeto usa o Flask para o framework web e o pymongo para a integração com MongoDB. As dependências podem ser instaladas através do arquivo requirements.txt.


Como Rodar o Projeto
Passo 1: Clonar o Repositório
Primeiro, clone o repositório para a sua máquina local:

bash
Copiar código
git clone <URL do repositório>
cd my_project

Passo 2: Criar e Ativar o Ambiente Virtual
É altamente recomendado usar um ambiente virtual para evitar conflitos de dependências. Para criar e ativar o ambiente virtual, execute os seguintes comandos:

No Windows:
python -m venv venv
.\venv\Scripts\activate

No macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Passo 3: Instalar as Dependências
Instale as dependências do projeto listadas no arquivo requirements.txt:
pip install -r requirements.txt

Passo 4: Configurar o MongoDB
Certifique-se de que o MongoDB está instalado e em execução em sua máquina local ou em um servidor remoto. Se estiver usando o MongoDB Atlas ou outro serviço de banco de dados em nuvem, crie uma instância e obtenha a string de conexão.

Se você estiver utilizando MongoDB localmente, o URI de conexão será algo como:

mongodb://localhost:27017

Passo 5: Configurar as Variáveis de Ambiente
No arquivo app/config.py, altere a configuração para conectar com o seu banco de dados MongoDB. Exemplo de configuração:


# app/config.py
class Config:
    SECRET_KEY = 'mysecretkey'  # Para sessões e CSRF
    MONGO_URI = "mongodb://localhost:27017/carros_db"  # Substitua pelo seu URI do MongoDB
    
Passo 6: Rodar o Servidor
Depois de configurar o banco de dados, você pode rodar a aplicação com o seguinte comando:
python run.py
O servidor Flask estará disponível em http://127.0.0.1:5000/ ou http://localhost:5000/ no seu navegador.

Passo 7: Interagir com a Aplicação
Você pode acessar as funcionalidades da aplicação por meio das seguintes rotas:
Ou você pode navegar normalmente pela aplicação! :)

Página principal: http://localhost:5000/
Adicionar carro: http://localhost:5000/add_carro
Editar carro: http://localhost:5000/edit_carro/<carro_id>
Deletar carro: http://localhost:5000/delete_carro/<carro_id>
Funcionalidades
Adicionar Carro: Permite adicionar um novo carro ao banco de dados.
Editar Carro: Permite editar as informações de um carro existente.
Listar Carros: Exibe todos os carros cadastrados.
Deletar Carro: Exclui um carro da base de dados, caso ele não esteja vinculado a um cliente.

