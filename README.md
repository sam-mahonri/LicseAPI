# Licse API
Chatbot API - Robô institucional de conversas com IA colaborativa

### Instalação da API

1. **Configurar Projeto no Firebase:**
   - Crie um projeto no Firebase através do console do Firebase.
   - Adicione um Realtime Database ao seu projeto.
   - Defina as regras do banco de dados como "test mode" para facilitar o desenvolvimento.
   
2. **Clonar Repositório do Aplicativo:**
   - Clone o repositório do aplicativo Flask em sua máquina local, você pode executar ``` git clone urlDoRepositorio.git ``` ou simplesmente faça o download dessa pasta e faça as operações dentro dela.

### Criar e Ativar Ambiente Virtual

#### Windows:

1. **Criar Ambiente Virtual:**
   - Abra o terminal do Windows.
   - Navegue até o diretório onde deseja criar o ambiente virtual.
   - Execute o seguinte comando para criar o ambiente virtual utilizando o módulo `venv`:
     ```shell
     python -m venv venv
     ```

2. **Ativar Ambiente Virtual:**
   - No mesmo terminal, navegue até o diretório onde o ambiente virtual foi criado.
   - Para ativar o ambiente virtual, execute o seguinte comando:
     ```shell
     venv\Scripts\activate
     ```

#### Linux:

1. **Criar Ambiente Virtual:**
   - Abra o terminal do Linux.
   - Navegue até o diretório onde deseja criar o ambiente virtual.
   - Execute o seguinte comando para criar o ambiente virtual utilizando o módulo `venv`:
     ```shell
     python3 -m venv venv
     ```

2. **Ativar Ambiente Virtual:**
   - No mesmo terminal, navegue até o diretório onde o ambiente virtual foi criado.
   - Para ativar o ambiente virtual, execute o seguinte comando:
     ```shell
     source venv/bin/activate
     ```

3. **Instalar dependências:**
   - Abra um terminal na raiz do projeto.
   - Execute o seguinte comando para instalar as dependências listadas no arquivo `requirements.txt`:
     ```
     pip install -r requirements.txt
     ```

5. **Configurar Variáveis de Ambiente:**
   - Configure as variáveis de ambiente necessárias para a conexão com o Firebase. Isso pode incluir credenciais de serviço ou a URL do banco de dados.

6. **Executar o Aplicativo:**
   - No terminal, execute o script Python principal do aplicativo Flask, geralmente chamado `run.py`, com o seguinte comando:
     ```
     python run.py
     ```
   - O aplicativo Flask deverá estar agora em execução localmente e acessível através do navegador.

7. **Testar o Aplicativo:**
   - Abra um navegador da web e vá para o endereço local onde o aplicativo Flask está sendo executado (geralmente `http://localhost:5000`).
   - Interaja com o aplicativo para garantir que esteja funcionando conforme o esperado.


