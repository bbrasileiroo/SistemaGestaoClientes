# Cadastro de Clientes com Banco de Dados

Este é um projeto simples em Python para fins de estudo, que cria uma interface gráfica para cadastrar clientes em um banco de dados local SQLite e permite a exportação desses dados para uma planilha Excel.

## Funcionalidades

* Formulário para inserir Nome, Sobrenome, Idade, E-mail e Telefone.
* Botão para **Cadastrar** o cliente no banco de dados SQLite (`clientes.db`).
* Botão para **Exportar** todos os clientes cadastrados para um arquivo Excel (`banco_clientes.xlsx`).

## Tecnologias Utilizadas

* **Python 3**
* **Tkinter:** Para a interface gráfica (GUI).
* **SQLite3:** Para o armazenamento dos dados.
* **Pandas:** Para a exportação dos dados para Excel.
* **OpenPyXL:** (Dependência do Pandas) Motor para escrita de arquivos `.xlsx`.

## Como Executar

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/bbrasileiroo/Cadastro-de-Clientes---BD.git](https://github.com/bbrasileiroo/Cadastro-de-Clientes---BD.git)
    cd Cadastro-de-Clientes---BD
    ```

2.  (Recomendado) Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  Execute a aplicação:
    ```bash
    python main.py
    ```