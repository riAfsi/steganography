import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image
import random
import os

# ============================================================
# DICIONÁRIOS DE TRADUÇÃO
# ============================================================
TRANSLATIONS = {
    "pt-PT": {
        "title": "Esteganografia LSB – alphondiny",
        "header": "Ferramenta de Esteganografia LSB",
        "lang_label": "Idioma:",

        # Ocultar
        "hide_frame": "🔒 Ocultar Mensagem",
        "select_original": "Selecionar imagem original (PNG)",
        "no_image": "Nenhuma imagem selecionada",
        "message_label": "Mensagem a esconder:",
        "password_label": "Palavra‑passe:",
        "hide_save": "💾 Esconder e guardar como...",

        # Extrair
        "extract_frame": "🔓 Extrair Mensagem",
        "select_hidden": "Selecionar imagem com mensagem (PNG)",
        "password_extract_label": "Palavra‑passe:",
        "extract_btn": "🔍 Extrair",
        "result_label": "Resultado:",

        # Erros
        "err_select_image": "Selecione uma imagem PNG.",
        "err_write_message": "Escreva a mensagem.",
        "err_set_password": "Defina uma palavra‑passe.",
        "err_message_too_big": "Mensagem grande de mais. Máx. {} caracteres.",
        "err_enter_password": "Introduza a palavra‑passe.",
        "err_terminator": "❌ Terminador não encontrado.\nVerifica a palavra‑passe ou a imagem.",

        # Sucessos
        "success_saved": "Guardada em:\n{}",

        # About
        "about_title": "Sobre",
        "about_text": "AfVa Esteganografia\n\nCriado por:\nAlphonsiny Vas\n\njunho/26",
        "about_btn": "ℹ️ About",
        "footer_text": "Esteganografia",
    },
    "en-US": {
        "title": "LSB Steganography – alphondiny",
        "header": "LSB Steganography Tool",
        "lang_label": "Language:",

        # Ocultar
        "hide_frame": "🔒 Hide Message",
        "select_original": "Select original image (PNG)",
        "no_image": "No image selected",
        "message_label": "Message to hide:",
        "password_label": "Password:",
        "hide_save": "💾 Hide and save as...",

        # Extrair
        "extract_frame": "🔓 Extract Message",
        "select_hidden": "Select image with hidden message (PNG)",
        "password_extract_label": "Password:",
        "extract_btn": "🔍 Extract",
        "result_label": "Result:",

        # Erros
        "err_select_image": "Please select a PNG image.",
        "err_write_message": "Please write a message.",
        "err_set_password": "Please set a password.",
        "err_message_too_big": "Message too large. Max {} characters.",
        "err_enter_password": "Please enter the password.",
        "err_terminator": "❌ Terminator not found.\nCheck the password or the image.",

        # Sucessos
        "success_saved": "Saved to:\n{}",

        # About
        "about_title": "About",
        "about_text": "AfVa Steganography\n\nCreated by:\nAlphonsiny Vas\n\nJune/26",
        "about_btn": "ℹ️ About",
        "footer_text": "Steganography",
    }
}


class EstegoApp:
    def __init__(self, root):
        self.root = root
        self.lang = "pt-PT"  # idioma padrão

        self.root.title(self.t("title"))
        self.root.geometry("750x680")
        self.root.resizable(True, True)

        self.imagem_original = ""
        self.imagem_oculta = ""

        # ---------- Barra de idioma ----------
        frame_lang = tk.Frame(root)
        frame_lang.pack(pady=(5, 0), fill="x", padx=20)

        tk.Label(frame_lang, text=self.t("lang_label"), font=("Arial", 10)).pack(side="left")
        self.combo_lang = ttk.Combobox(frame_lang, values=["PT-PT", "EN-US"], state="readonly", width=10)
        self.combo_lang.set("PT-PT")
        self.combo_lang.pack(side="left", padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.mudar_idioma)

        # ---------- Cabeçalho ----------
        self.lbl_header = tk.Label(root, text=self.t("header"), font=("Arial", 14, "bold"))
        self.lbl_header.pack(pady=10)

        # ---------- Frame OCULTAR ----------
        self.frame_ocultar = tk.LabelFrame(root, text=self.t("hide_frame"), padx=10, pady=10)
        self.frame_ocultar.pack(padx=20, pady=5, fill="x")

        self.btn_select_original = tk.Button(self.frame_ocultar, text=self.t("select_original"), command=self.selecionar_original)
        self.btn_select_original.pack(fill="x", pady=3)

        self.lbl_original = tk.Label(self.frame_ocultar, text=self.t("no_image"), fg="gray")
        self.lbl_original.pack()

        self.lbl_message = tk.Label(self.frame_ocultar, text=self.t("message_label"))
        self.lbl_message.pack(anchor="w")

        self.txt_mensagem = scrolledtext.ScrolledText(self.frame_ocultar, height=3, width=70)
        self.txt_mensagem.pack(pady=3)

        self.lbl_pass_hide = tk.Label(self.frame_ocultar, text=self.t("password_label"))
        self.lbl_pass_hide.pack(anchor="w")

        self.entry_chave_ocultar = tk.Entry(self.frame_ocultar, show="*", width=30)
        self.entry_chave_ocultar.pack(pady=2)

        self.btn_hide = tk.Button(self.frame_ocultar, text=self.t("hide_save"), command=self.esconder)
        self.btn_hide.pack(pady=5)

        # ---------- Frame EXTRAIR ----------
        self.frame_extrair = tk.LabelFrame(root, text=self.t("extract_frame"), padx=10, pady=10)
        self.frame_extrair.pack(padx=20, pady=5, fill="both", expand=True)

        self.btn_select_hidden = tk.Button(self.frame_extrair, text=self.t("select_hidden"), command=self.selecionar_oculta)
        self.btn_select_hidden.pack(fill="x", pady=3)

        self.lbl_oculta = tk.Label(self.frame_extrair, text=self.t("no_image"), fg="gray")
        self.lbl_oculta.pack()

        self.lbl_pass_extract = tk.Label(self.frame_extrair, text=self.t("password_extract_label"))
        self.lbl_pass_extract.pack(anchor="w")

        self.entry_chave_extrair = tk.Entry(self.frame_extrair, show="*", width=30)
        self.entry_chave_extrair.pack(pady=2)

        self.btn_extract = tk.Button(self.frame_extrair, text=self.t("extract_btn"), command=self.extrair)
        self.btn_extract.pack(pady=5)

        self.lbl_result = tk.Label(self.frame_extrair, text=self.t("result_label"))
        self.lbl_result.pack(anchor="w")

        self.txt_resultado = scrolledtext.ScrolledText(self.frame_extrair, height=8, width=70, state="disabled")
        self.txt_resultado.pack(pady=5, fill="both", expand=True)

        # ---------- RODAPÉ ----------
        self.frame_rodape = tk.Frame(root)
        self.frame_rodape.pack(side="bottom", fill="x", pady=5)

        self.btn_about = tk.Button(self.frame_rodape, text=self.t("about_btn"), command=self.mostrar_about)
        self.btn_about.pack(side="left", padx=20)

        self.lbl_footer = tk.Label(self.frame_rodape, text=self.t("footer_text"), font=("Arial", 8))
        self.lbl_footer.pack(side="right", padx=20)

    # ---------- Função de tradução ----------
    def t(self, key):
        """Retorna o texto traduzido para o idioma atual."""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["pt-PT"]).get(key, key)

    # ---------- Mudar idioma ----------
    def mudar_idioma(self, event=None):
        escolha = self.combo_lang.get()
        if escolha == "PT-PT":
            self.lang = "pt-PT"
        else:
            self.lang = "en-US"

        self.atualizar_interface()

    def atualizar_interface(self):
        """Atualiza todos os textos da interface para o idioma selecionado."""
        self.root.title(self.t("title"))
        self.lbl_header.config(text=self.t("header"))

        self.frame_ocultar.config(text=self.t("hide_frame"))
        self.btn_select_original.config(text=self.t("select_original"))
        if not self.imagem_original:
            self.lbl_original.config(text=self.t("no_image"))
        self.lbl_message.config(text=self.t("message_label"))
        self.lbl_pass_hide.config(text=self.t("password_label"))
        self.btn_hide.config(text=self.t("hide_save"))

        self.frame_extrair.config(text=self.t("extract_frame"))
        self.btn_select_hidden.config(text=self.t("select_hidden"))
        if not self.imagem_oculta:
            self.lbl_oculta.config(text=self.t("no_image"))
        self.lbl_pass_extract.config(text=self.t("password_extract_label"))
        self.btn_extract.config(text=self.t("extract_btn"))
        self.lbl_result.config(text=self.t("result_label"))

        self.btn_about.config(text=self.t("about_btn"))
        self.lbl_footer.config(text=self.t("footer_text"))

    # ---------- Funções de seleção ----------
    def selecionar_original(self):
        f = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if f:
            self.imagem_original = f
            self.lbl_original.config(text=os.path.basename(f), fg="black")

    def selecionar_oculta(self):
        f = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
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
            messagebox.showerror("Error", self.t("err_select_image"))
            return
        msg = self.txt_mensagem.get("1.0", "end-1c")
        if not msg:
            messagebox.showerror("Error", self.t("err_write_message"))
            return
        chave = self.entry_chave_ocultar.get()
        if not chave:
            messagebox.showerror("Error", self.t("err_set_password"))
            return

        try:
            img = Image.open(self.imagem_original).convert('RGB')
            pixels = list(img.getdata())
            total = len(pixels)
            bits = ''.join(format(ord(c), '08b') for c in msg) + '00000000'
            if len(bits) > total:
                messagebox.showerror("Error", self.t("err_message_too_big").format(total))
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
                messagebox.showinfo("Success", self.t("success_saved").format(destino))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- EXTRAIR ----------
    def extrair(self):
        if not self.imagem_oculta:
            messagebox.showerror("Error", self.t("err_select_image"))
            return
        chave = self.entry_chave_extrair.get()
        if not chave:
            messagebox.showerror("Error", self.t("err_enter_password"))
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
                self.txt_resultado.insert("1.0", self.t("err_terminator"))
            self.txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- About ----------
    def mostrar_about(self):
        messagebox.showinfo(self.t("about_title"), self.t("about_text"))


# ---------- Executar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = EstegoApp(root)
    root.mainloop()