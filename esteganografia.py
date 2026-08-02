import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import random
import os

class EstegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Esteganografia LSB – alphondiny")
        self.root.geometry("700x650")       # mais altura para o rodapé
        self.root.resizable(True, True)

        self.imagem_original = ""
        self.imagem_oculta = ""

        # ---------- Cabeçalho ----------
        tk.Label(root, text="Ferramenta de Esteganografia LSB", font=("Arial", 14, "bold")).pack(pady=10)

        # ---------- Frame OCULTAR ----------
        frame_ocultar = tk.LabelFrame(root, text="🔒 Ocultar Mensagem", padx=10, pady=10)
        frame_ocultar.pack(padx=20, pady=5, fill="x")

        tk.Button(frame_ocultar, text="Selecionar imagem original (PNG)", command=self.selecionar_original).pack(fill="x", pady=3)
        self.lbl_original = tk.Label(frame_ocultar, text="Nenhuma imagem selecionada", fg="gray")
        self.lbl_original.pack()

        tk.Label(frame_ocultar, text="Mensagem a esconder:").pack(anchor="w")
        self.txt_mensagem = scrolledtext.ScrolledText(frame_ocultar, height=3, width=70)
        self.txt_mensagem.pack(pady=3)

        tk.Label(frame_ocultar, text="Palavra‑passe:").pack(anchor="w")
        self.entry_chave_ocultar = tk.Entry(frame_ocultar, show="*", width=30)
        self.entry_chave_ocultar.pack(pady=2)

        tk.Button(frame_ocultar, text="💾 Esconder e guardar como...", command=self.esconder).pack(pady=5)

        # ---------- Frame EXTRAIR ----------
        frame_extrair = tk.LabelFrame(root, text="🔓 Extrair Mensagem", padx=10, pady=10)
        frame_extrair.pack(padx=20, pady=5, fill="both", expand=True)

        tk.Button(frame_extrair, text="Selecionar imagem com mensagem (PNG)", command=self.selecionar_oculta).pack(fill="x", pady=3)
        self.lbl_oculta = tk.Label(frame_extrair, text="Nenhuma imagem selecionada", fg="gray")
        self.lbl_oculta.pack()

        tk.Label(frame_extrair, text="Palavra‑passe:").pack(anchor="w")
        self.entry_chave_extrair = tk.Entry(frame_extrair, show="*", width=30)
        self.entry_chave_extrair.pack(pady=2)

        tk.Button(frame_extrair, text="🔍 Extrair", command=self.extrair).pack(pady=5)

        tk.Label(frame_extrair, text="Resultado:").pack(anchor="w")
        self.txt_resultado = scrolledtext.ScrolledText(frame_extrair, height=8, width=70, state="disabled")
        self.txt_resultado.pack(pady=5, fill="both", expand=True)

        # ---------- RODAPÉ (About + Versão) ----------
        frame_rodape = tk.Frame(root)
        frame_rodape.pack(side="bottom", fill="x", pady=5)

        tk.Button(frame_rodape, text="ℹ️ About", command=self.mostrar_about).pack(side="left", padx=20)
        tk.Label(frame_rodape, text="Esteganografia", font=("Arial", 8)).pack(side="right", padx=20)

    # ---------- Funções de seleção ----------
    def selecionar_original(self):
        f = filedialog.askopenfilename(filetypes=[("Imagens PNG", "*.png")])
        if f:
            self.imagem_original = f
            self.lbl_original.config(text=os.path.basename(f), fg="black")

    def selecionar_oculta(self):
        f = filedialog.askopenfilename(filetypes=[("Imagens PNG", "*.png")])
        if f:
            self.imagem_oculta = f
            self.lbl_oculta.config(text=os.path.basename(f), fg="black")

    # ---------- Sequência pseudoaleatória ----------
    def gerar_sequencia(self, chave, total):
        semente = sum(ord(c) for c in chave)
        random.seed(semente)
        indices = list(range(total))
        random.shuffle(indices)
        return indices

    # ---------- ESCONDER ----------
    def esconder(self):
        if not self.imagem_original:
            messagebox.showerror("Erro", "Selecione uma imagem PNG.")
            return
        msg = self.txt_mensagem.get("1.0", "end-1c")
        if not msg:
            messagebox.showerror("Erro", "Escreva a mensagem.")
            return
        chave = self.entry_chave_ocultar.get()
        if not chave:
            messagebox.showerror("Erro", "Defina uma palavra‑passe.")
            return

        try:
            img = Image.open(self.imagem_original).convert('RGB')
            pixels = list(img.getdata())
            total = len(pixels)
            bits = ''.join(format(ord(c), '08b') for c in msg) + '00000000'
            if len(bits) > total:
                messagebox.showerror("Erro", f"Mensagem grande de mais. Máx. {total} caracteres.")
                return

            ordem = self.gerar_sequencia(chave, total)
            novos = list(pixels)
            for i, bit in enumerate(bits):
                idx = ordem[i]
                r, g, b = novos[idx]
                novos[idx] = (r, g, (b & 0xFE) | int(bit))

            destino = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if destino:
                img.putdata(novos)
                img.save(destino, 'PNG')
                messagebox.showinfo("Sucesso", f"Guardada em:\n{destino}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ---------- EXTRAIR ----------
    def extrair(self):
        if not self.imagem_oculta:
            messagebox.showerror("Erro", "Selecione uma imagem PNG com mensagem.")
            return
        chave = self.entry_chave_extrair.get()
        if not chave:
            messagebox.showerror("Erro", "Introduza a palavra‑passe.")
            return

        try:
            img = Image.open(self.imagem_oculta).convert('RGB')
            pixels = list(img.getdata())
            total = len(pixels)
            ordem = self.gerar_sequencia(chave, total)

            bits = []
            max_bits = min(total, 10000)
            for idx in ordem[:max_bits]:
                _, _, b = pixels[idx]
                bits.append(str(b & 1))

            mensagem = ""
            terminador = False
            for i in range(0, len(bits)-7, 8):
                byte = ''.join(bits[i:i+8])
                if byte == '00000000':
                    terminador = True
                    break
                mensagem += chr(int(byte, 2))

            self.txt_resultado.config(state="normal")
            self.txt_resultado.delete("1.0", "end")
            if terminador:
                self.txt_resultado.insert("1.0", mensagem)
            else:
                self.txt_resultado.insert("1.0", "❌ Terminador não encontrado.\nVerifica a palavra‑passe ou a imagem.")
            self.txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ---------- About ----------
    def mostrar_about(self):
        messagebox.showinfo(
            "Sobre",
            "AfVa Esteganografia\n\n"
            "Criado por: \n"
            "Alphonsiny Vas\n\n"
            "junho/26\n\n"
            
        )

# ---------- Executar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = EstegoApp(root)
    root.mainloop()