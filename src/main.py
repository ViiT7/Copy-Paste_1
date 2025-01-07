# src/main.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class ConsolidadorDeArquivosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consolidador de Arquivos")
        self.root.geometry("600x300")
        self.root.resizable(False, False)

        # Variáveis
        self.pasta_selecionada = tk.StringVar()
        self.nome_arquivo = tk.StringVar(value="consolidado.txt")

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Seletor de Pasta
        frame_pasta = tk.Frame(self.root, padx=10, pady=10)
        frame_pasta.pack(fill='x')

        lbl_pasta = tk.Label(frame_pasta, text="Pasta a ser consolidada:")
        lbl_pasta.pack(side='left')

        entry_pasta = tk.Entry(frame_pasta, textvariable=self.pasta_selecionada, width=50)
        entry_pasta.pack(side='left', padx=5)

        btn_pasta = tk.Button(frame_pasta, text="Selecionar Pasta", command=self.selecionar_pasta)
        btn_pasta.pack(side='left')

        # Nome do Arquivo de Saída
        frame_nome = tk.Frame(self.root, padx=10, pady=10)
        frame_nome.pack(fill='x')

        lbl_nome = tk.Label(frame_nome, text="Nome do arquivo de saída (.txt):")
        lbl_nome.pack(side='left')

        entry_nome = tk.Entry(frame_nome, textvariable=self.nome_arquivo, width=30)
        entry_nome.pack(side='left', padx=5)

        # Botão de Consolidação
        frame_consolidar = tk.Frame(self.root, padx=10, pady=20)
        frame_consolidar.pack()

        btn_consolidar = tk.Button(frame_consolidar, text="Consolidar Arquivos", command=self.consolidar_arquivos, bg="#4CAF50", fg="white", width=20, height=2)
        btn_consolidar.pack()

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_selecionada.set(pasta)

    def consolidar_arquivos(self):
        pasta = self.pasta_selecionada.get()
        nome_arquivo = self.nome_arquivo.get()

        if not pasta:
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta.")
            return

        if not nome_arquivo.endswith(".txt"):
            nome_arquivo += ".txt"

        output_path = os.path.join(os.path.dirname(pasta), "output")
        os.makedirs(output_path, exist_ok=True)
        arquivo_saida = os.path.join(output_path, nome_arquivo)

        try:
            with open(arquivo_saida, "w", encoding="utf-8") as outfile:
                # Cabeçalho
                data_hora = datetime.now().strftime("%d/%m/%y AS %H:%M")
                outfile.write(f"ARQUIVOS DO PROJETO EM SEU ESTADO ATUAL ({data_hora}):\n\n")
                outfile.write("-----------------\n\n")

                # Percorrer arquivos
                for root_dir, dirs, files in os.walk(pasta):
                    for file in files:
                        caminho_completo = os.path.join(root_dir, file)
                        caminho_relativo = os.path.relpath(caminho_completo, pasta)
                        caminho_relativo = caminho_relativo.replace("\\", "/")  # Para consistência

                        outfile.write(f"{caminho_relativo} ->\n\n")

                        try:
                            with open(caminho_completo, "r", encoding="utf-8") as infile:
                                conteudo = infile.read()
                                outfile.write(conteudo + "\n\n")
                        except Exception as e:
                            outfile.write(f"Erro ao ler o arquivo: {e}\n\n")

                        outfile.write("-----------------\n\n")

            messagebox.showinfo("Sucesso", f"Arquivo consolidado criado em:\n{arquivo_saida}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao consolidar os arquivos:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConsolidadorDeArquivosApp(root)
    root.mainloop()
