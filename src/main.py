# src/main.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class ConsolidadorDeArquivosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consolidador de Arquivos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Variáveis
        self.pasta_selecionada = tk.StringVar()
        self.nome_arquivo = tk.StringVar(value="consolidado.txt")
        self.exclusoes = []  # Lista para armazenar caminhos relativos a serem ignorados

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Seletor de Pasta
        frame_pasta = tk.Frame(self.root, padx=10, pady=10)
        frame_pasta.pack(fill='x')

        lbl_pasta = tk.Label(frame_pasta, text="Pasta a ser consolidada:")
        lbl_pasta.pack(side='left')

        entry_pasta = tk.Entry(frame_pasta, textvariable=self.pasta_selecionada, width=60)
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

        # Seção de Exclusões
        frame_exclusao = tk.LabelFrame(self.root, text="Excluir Arquivos/Subpastas", padx=10, pady=10)
        frame_exclusao.pack(fill='both', padx=10, pady=10, expand=True)

        # Frame para Botões de Exclusão
        frame_botoes_exclusao = tk.Frame(frame_exclusao)
        frame_botoes_exclusao.pack(fill='x', pady=5)

        btn_adicionar_arquivo = tk.Button(frame_botoes_exclusao, text="Adicionar Arquivo", command=self.adicionar_arquivo, bg="#0275d8", fg="white")
        btn_adicionar_arquivo.pack(side='left', padx=5)

        btn_adicionar_pasta = tk.Button(frame_botoes_exclusao, text="Adicionar Pasta", command=self.adicionar_pasta, bg="#5cb85c", fg="white")
        btn_adicionar_pasta.pack(side='left', padx=5)

        btn_remover_exclusao = tk.Button(frame_botoes_exclusao, text="Remover Seleção", command=self.remover_exclusao, bg="#d9534f", fg="white")
        btn_remover_exclusao.pack(side='left', padx=5)

        # Listbox para mostrar exclusões
        self.listbox_exclusao = tk.Listbox(frame_exclusao, selectmode=tk.SINGLE, width=100, height=20)
        self.listbox_exclusao.pack(side='left', padx=(0,5), fill='y')

        # Scrollbar para a Listbox
        scrollbar = tk.Scrollbar(frame_exclusao, orient="vertical")
        scrollbar.config(command=self.listbox_exclusao.yview)
        scrollbar.pack(side='left', fill='y')

        self.listbox_exclusao.config(yscrollcommand=scrollbar.set)

        # Botão de Consolidação
        frame_consolidar = tk.Frame(self.root, padx=10, pady=20)
        frame_consolidar.pack()

        btn_consolidar = tk.Button(frame_consolidar, text="Consolidar Arquivos", command=self.consolidar_arquivos, bg="#4CAF50", fg="white", width=25, height=2)
        btn_consolidar.pack()

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_selecionada.set(pasta)
            self.exclusoes.clear()
            self.listbox_exclusao.delete(0, tk.END)

    def adicionar_arquivo(self):
        if not self.pasta_selecionada.get():
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            return

        caminho = filedialog.askopenfilename(initialdir=self.pasta_selecionada.get())
        if caminho:
            caminho_relativo = os.path.relpath(caminho, self.pasta_selecionada.get())
            caminho_relativo = caminho_relativo.replace("\\", "/")
            # Verifica se já está na lista
            if caminho_relativo not in self.exclusoes:
                self.exclusoes.append(caminho_relativo)
                self.listbox_exclusao.insert(tk.END, f"Arquivo: {caminho_relativo}")
            else:
                messagebox.showinfo("Informação", "Este arquivo já está na lista de exclusões.")

    def adicionar_pasta(self):
        if not self.pasta_selecionada.get():
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta primeiro.")
            return

        caminho = filedialog.askdirectory(initialdir=self.pasta_selecionada.get())
        if caminho:
            caminho_relativo = os.path.relpath(caminho, self.pasta_selecionada.get())
            caminho_relativo = caminho_relativo.replace("\\", "/")
            # Verifica se já está na lista
            if caminho_relativo not in self.exclusoes:
                self.exclusoes.append(caminho_relativo)
                self.listbox_exclusao.insert(tk.END, f"Pasta: {caminho_relativo}")
            else:
                messagebox.showinfo("Informação", "Esta pasta já está na lista de exclusões.")

    def remover_exclusao(self):
        selecionado = self.listbox_exclusao.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um item para remover.")
            return
        index = selecionado[0]
        exclusao = self.listbox_exclusao.get(index)
        # Extrair o caminho relativo sem o prefixo "Arquivo: " ou "Pasta: "
        caminho_relativo = exclusao.split(": ", 1)[1]
        self.exclusoes.remove(caminho_relativo)
        self.listbox_exclusao.delete(index)

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
                    # Calcular o caminho relativo da pasta atual
                    caminho_relativo_pasta = os.path.relpath(root_dir, pasta)
                    caminho_relativo_pasta = caminho_relativo_pasta.replace("\\", "/")

                    # Verificar se a pasta atual está na lista de exclusões
                    if caminho_relativo_pasta != '.' and caminho_relativo_pasta in self.exclusoes:
                        dirs[:] = []  # Não desce nas subpastas
                        continue

                    # Remover subpastas da lista de exclusões
                    dirs[:] = [d for d in dirs if os.path.join(caminho_relativo_pasta, d).replace("\\", "/") not in self.exclusoes]

                    for file in files:
                        caminho_completo = os.path.join(root_dir, file)
                        caminho_relativo = os.path.relpath(caminho_completo, pasta)
                        caminho_relativo = caminho_relativo.replace("\\", "/")

                        # Verificar se o arquivo está na lista de exclusões
                        if caminho_relativo in self.exclusoes:
                            continue

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
