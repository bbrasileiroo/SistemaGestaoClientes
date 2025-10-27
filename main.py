import tkinter as tk
from tkinter import messagebox  # Usado para mostrar pop-ups de sucesso
import sqlite3
import pandas as pd
import os # Usado para encontrar o caminho do script
import matplotlib.pyplot as plt # plt é o "desenhista"
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # a "ponte" que conecta o Matplotlib com o Tkinter
# --- NOVO IMPORT ---
from matplotlib.ticker import MaxNLocator

class AppCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema de Gestão de Clientes') # Título atualizado
        
        # --- Caminho do Banco de Dados ---
        # Garante que o DB seja criado na mesma pasta do script
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_path, 'clientes.db')
        
        # Garante que a tabela exista
        self.criar_tabela_se_nao_existir()

        # --- Divisão da Janela em "Frames" ---
        self.frame_esq = tk.Frame(root)
        self.frame_esq.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        # side=tk.LEFT "gruda" este frame na esquerda.

        self.frame_dir = tk.Frame(root, width=400, height=300)
        self.frame_dir.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        # fill=tk.BOTH e expand=True fazem o gráfico ocupar o espaço disponível.

        # --- Uma variável para "lembrar" do widget do gráfico ---
        self.canvas_widget = None

        # --- Widgets da Interface (Agora dentro do self.frame_esq) ---
        
        # Labels
        tk.Label(self.frame_esq, text='Nome').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.frame_esq, text='Sobrenome').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.frame_esq, text='Idade').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.frame_esq, text='E-mail').grid(row=3, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.frame_esq, text='Telefone').grid(row=4, column=0, padx=10, pady=5, sticky='w')
        # sticky='w' alinha o texto à esquerda (West)

        # Entrys (Campos de entrada)
        self.entry_nome = tk.Entry(self.frame_esq, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        self.entry_sobrenome = tk.Entry(self.frame_esq, width=30)
        self.entry_sobrenome.grid(row=1, column=1, padx=10, pady=5)

        self.entry_idade = tk.Entry(self.frame_esq, width=30)
        self.entry_idade.grid(row=2, column=1, padx=10, pady=5)

        self.entry_email = tk.Entry(self.frame_esq, width=30)
        self.entry_email.grid(row=3, column=1, padx=10, pady=5)

        self.entry_telefone = tk.Entry(self.frame_esq, width=30)
        self.entry_telefone.grid(row=4, column=1, padx=10, pady=5)

        # Botões
        self.botao_cadastrar = tk.Button(self.frame_esq, text='Cadastrar Cliente', command=self.cadastrar_cliente_e_atualizar)
        self.botao_cadastrar.grid(row=5, column=0, padx=10, pady=10, columnspan=2, ipadx=80)

        self.botao_exportar = tk.Button(self.frame_esq, text='Exportar Base (Excel)', command=self.exportar_clientes)
        self.botao_exportar.grid(row=6, column=0, padx=10, pady=10, columnspan=2, ipadx=80)

        # --- Botão de Relatório ---
        self.botao_relatorio = tk.Button(self.frame_esq, text='Atualizar Relatório', command=self.mostrar_relatorio)
        # Este botão chama a nova função de gráfico
        self.botao_relatorio.grid(row=7, column=0, padx=10, pady=10, columnspan=2, ipadx=80)

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

    # --- Função "Wrapper" ---
    def cadastrar_cliente_e_atualizar(self):
        # Esta função existe para fazer duas coisas com um só clique:
        # 1. Cadastrar o cliente
        self.cadastrar_cliente()
        # 2. Atualizar o gráfico com o novo cliente
        self.mostrar_relatorio()

    def cadastrar_cliente(self):
        """Validação de dados"""
        idade_val = self.entry_idade.get()
        email_val = self.entry_email.get()
        if not idade_val.isdigit():
            messagebox.showerror("Erro de Dados", "O campo 'Idade' deve ser um número.")
            return
        if "@" not in email_val or "." not in email_val:
            messagebox.showerror("Erro de Dados", "O campo 'E-mail' parece ser inválido.")
            return
        
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

    # --- Função inteira para o Dashboard ---
    def mostrar_relatorio(self):
        """Puxa os dados e exibe um gráfico de barras no frame_dir."""

        # Limpa o gráfico anterior (se existir)
        # Isso é VITAL para que os gráficos não se sobreponham
        if self.canvas_widget:
            self.canvas_widget.destroy()

        try:
            # Puxa os dados com Pandas
            with self.conectar_db() as conn:
                # Vamos precisar apenas da coluna 'idade'
                df = pd.read_sql_query("SELECT idade FROM clientes", conn)

            # 3. A Análise
            if df.empty:
                # Se não há dados, não faz nada
                return 
            
            # Garante que a coluna 'idade' seja numérica, caso algo passe
            df['idade'] = pd.to_numeric(df['idade'])
            
            # "Agrupe por idade" e "Conte o tamanho" de cada grupo
            analise_idade = df.groupby('idade').size().reset_index(name='contagem')
            
            # 4. Criar o Gráfico
            fig, ax = plt.subplots(figsize=(5, 4))
            
            # Cria o gráfico de barras
            ax.bar(analise_idade['idade'], analise_idade['contagem'])
            
            # Adiciona títulos
            ax.set_title('Contagem de Clientes por Idade')
            ax.set_ylabel('Nº de Clientes')
            ax.set_xlabel('Idade')

            # --- NOVO: Correção dos Eixos ---
            
            # 1. Força o eixo Y (Nº de Clientes) a usar apenas números inteiros
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))

            # 2. Força o eixo X (Idade) a usar apenas as idades do nosso dataFrame
            # Isso remove os decimais estranhos no eixo X
            ax.set_xticks(analise_idade['idade'])
            
            plt.tight_layout() # Ajusta para caber tudo

            # 5. A "Ponte" (Carregar no Tkinter)
            # Conecta a 'fig' (figura) do Matplotlib ao 'self.frame_dir'
            canvas = FigureCanvasTkAgg(fig, master=self.frame_dir)
            
            # Pega o "widget" do Tkinter e o salva
            self.canvas_widget = canvas.get_tk_widget()
            
            # Exibe o gráfico na tela
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Erro no Gráfico", f"Não foi possível gerar o relatório: {e}")

# --- Ponto de Entrada da Aplicação ---
def main():
    """Função principal que inicia a aplicação."""
    root = tk.Tk()
    app = AppCadastro(root)
    root.mainloop()

if __name__ == "__main__":
    main()