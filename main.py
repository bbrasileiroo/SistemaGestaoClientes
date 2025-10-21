import tkinter as tk
from tkinter import messagebox  # Usado para mostrar pop-ups de sucesso
import sqlite3
import pandas as pd
import os # Usado para encontrar o caminho do script

class AppCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title('Cadastro de Clientes')
        
        # --- Caminho do Banco de Dados ---
        # Garante que o DB seja criado na mesma pasta do script
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_path, 'clientes.db')
        
        # Garante que a tabela exista
        self.criar_tabela_se_nao_existir()

        # --- Widgets da Interface ---
        
        # Labels
        tk.Label(root, text='Nome').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(root, text='Sobrenome').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(root, text='Idade').grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(root, text='E-mail').grid(row=3, column=0, padx=10, pady=10, sticky='w')
        tk.Label(root, text='Telefone').grid(row=4, column=0, padx=10, pady=10, sticky='w')

        # Entrys (Campos de entrada)
        self.entry_nome = tk.Entry(root, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)

        self.entry_sobrenome = tk.Entry(root, width=30)
        self.entry_sobrenome.grid(row=1, column=1, padx=10, pady=10)

        self.entry_idade = tk.Entry(root, width=30)
        self.entry_idade.grid(row=2, column=1, padx=10, pady=10)

        self.entry_email = tk.Entry(root, width=30)
        self.entry_email.grid(row=3, column=1, padx=10, pady=10)

        self.entry_telefone = tk.Entry(root, width=30)
        self.entry_telefone.grid(row=4, column=1, padx=10, pady=10)

        # Botões
        self.botao_cadastrar = tk.Button(root, text='Cadastrar Cliente', command=self.cadastrar_cliente)
        self.botao_cadastrar.grid(row=5, column=0, padx=10, pady=10, columnspan=2, ipadx=80)

        self.botao_exportar = tk.Button(root, text='Exportar Base', command=self.exportar_clientes)
        self.botao_exportar.grid(row=6, column=0, padx=10, pady=10, columnspan=2, ipadx=80)

    def conectar_db(self):
        """Retorna uma conexão."""
        conexao = sqlite3.connect(self.db_path)
        return conexao

    def criar_tabela_se_nao_existir(self):
        """Cria a tabela 'clientes' caso ela não exista."""
        comando = '''
        CREATE TABLE IF NOT EXISTS clientes (
            nome text,
            sobrenome text,
            idade integer,
            email text,
            telefone text
        )
        '''
        with self.conectar_db() as conn:
            conn.execute(comando)
            # 'with' faz o commit automático

    def cadastrar_cliente(self):
        """Insere os dados dos entrys no banco de dados."""
        comando = '''
        INSERT INTO clientes (nome, sobrenome, idade, email, telefone)
        VALUES (:nome, :sobrenome, :idade, :email, :telefone)
        '''
        dados = {
            'nome': self.entry_nome.get(),
            'sobrenome': self.entry_sobrenome.get(),
            'idade': self.entry_idade.get(),
            'email': self.entry_email.get(),
            'telefone': self.entry_telefone.get()
        }
        
        try:
            with self.conectar_db() as conn:
                conn.execute(comando, dados)
            
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar: {e}")

    def limpar_campos(self):
        """Limpa todos os campos de entrada."""
        self.entry_nome.delete(0, "end")
        self.entry_sobrenome.delete(0, "end")
        self.entry_idade.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefone.delete(0, "end")

    def exportar_clientes(self):
        """Exporta os dados do banco para um arquivo Excel."""
        arquivo_saida = 'banco_clientes.xlsx'
        try:
            with self.conectar_db() as conn:
                query = 'SELECT *, oid FROM clientes'
                colunas = ['nome', 'sobrenome', 'idade', 'email', 'telefone', 'id_banco']
                
                clientes_cadastrados = pd.read_sql_query(query, conn, index_col=None)
                clientes_cadastrados.columns = colunas

            clientes_cadastrados.to_excel(arquivo_saida, index=False)
            messagebox.showinfo("Sucesso", f"Base exportada para {arquivo_saida}!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao exportar: {e}")

# --- Ponto de Entrada da Aplicação ---
def main():
    """Função principal que inicia a aplicação."""
    root = tk.Tk()
    app = AppCadastro(root)
    root.mainloop()

if __name__ == "__main__":
    main()