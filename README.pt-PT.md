# 🔒 Esteganografia LSB – alphondiny

Aplicação desktop em Python com interface gráfica (Tkinter) para ocultar e extrair mensagens secretas dentro de imagens PNG utilizando a técnica de **Esteganografia LSB** (*Least Significant Bit*).

> **Esteganografia**  
> Desenvolvido por **Alphonsiny Vas**

---

## ✨ Funcionalidades

- **🔒 Ocultar mensagens** – Esconde texto arbitrário dentro de uma imagem PNG sem alterar visualmente a imagem.
- **🔓 Extrair mensagens** – Recupera o texto escondido a partir de uma imagem estego, desde que seja fornecida a palavra-passe correta.
- **🔑 Proteção por palavra-passe** – A mensagem é distribuída pseudoaleatoriamente pelos pixéis da imagem com base numa chave, dificultando a deteção estatística.
- **🌍 Suporte bilíngue** – Interface disponível em Português (PT-PT) e Inglês (EN-US).
- **🖼️ Interface gráfica intuitiva** – Desenvolvida em Tkinter, não requer conhecimentos de linha de comandos.

---

## 🛠️ Requisitos

| Dependência | Versão mínima |
|-------------|---------------|
| Python      | 3.7+          |
| Pillow (PIL)| 9.0+          |
| tkinter     | (incluído na stdlib do Python) |

### Instalação das dependências

```bash
pip install Pillow
```

> O `tkinter` já vem incluído na instalação padrão do Python na maioria dos sistemas operativos. Caso não esteja disponível, instale-o através do gestor de pacotes do seu sistema:
> - **Debian/Ubuntu:** `sudo apt-get install python3-tk`
> - **Fedora/RHEL:** `sudo dnf install python3-tkinter`
> - **macOS:** incluído com a instalação oficial do Python via [python.org](https://python.org)
> - **Windows:** incluído por defeito no instalador do Python

---

## 🚀 Como executar

1. Clone ou descarregue este repositório:
   ```bash
   git clone https://github.com/alphondiny/esteganografia-lsb.git
   cd esteganografia-lsb
   ```

2. Execute a aplicação:
   ```bash
   python esteganografia_bilingue.py
   ```

---

## 📖 Como utilizar

### Alterar idioma

No topo da janela, selecione **PT-PT** ou **EN-US** na caixa de idioma. A interface atualiza instantaneamente sem necessidade de reiniciar a aplicação.

### Ocultar uma mensagem

1. Clique em **"Selecionar imagem original (PNG)"** e escolha uma imagem PNG.
2. Escreva a mensagem que pretende esconder no campo **"Mensagem a esconder"**.
3. Introduza uma **palavra-passe** no campo correspondente.
4. Clique em **"💾 Esconder e guardar como..."** e escolha o nome do ficheiro de saída.
5. A imagem resultante será visualmente idêntica à original, mas conterá a mensagem escondida.

### Extrair uma mensagem

1. Clique em **"Selecionar imagem com mensagem (PNG)"** e escolha a imagem estego.
2. Introduza a **mesma palavra-passe** utilizada na ocultação.
3. Clique em **"🔍 Extrair"**.
4. A mensagem será apresentada no campo de resultado.

> ⚠️ **Nota:** A palavra-passe deve ser exatamente a mesma utilizada na ocultação. Caso contrário, o terminador não será encontrado e a extração falhará.

---

## 🔬 Como funciona

### Técnica LSB (Least Significant Bit)

A aplicação utiliza o canal **azul (B)** de cada pixél RGB para armazenar 1 bit da mensagem, substituindo o bit menos significativo:

```
Pixél original:  (R, G, B) = (120, 200, 255)
Bit a esconder:  0
Pixél alterado:  (R, G, B) = (120, 200, 254)  ← B & 0xFE | bit
```

A alteração de apenas 1 bit no canal azul é praticamente imperceptível ao olho humano, mantendo a integridade visual da imagem.

### Distribuição pseudoaleatória

Para aumentar a segurança, a mensagem **não é escrita sequencialmente** nos pixéis. Em vez disso, gera-se uma permutação pseudoaleatória dos índices dos pixéis com base na palavra-passe fornecida:

```python
semente = sum(ord(c) for c in chave)
random.seed(semente)
random.shuffle(indices)
```

Isto significa que:
- Sem a palavra-passe correta, é impossível saber quais pixéis contêm a mensagem.
- A distribuição aleatória dificulta análises estatísticas que poderiam detetar a presença de dados escondidos.

### Formato da mensagem

A mensagem é convertida para binário (8 bits por caractere UTF-8) e terminada com um byte nulo (`00000000`), que sinaliza o fim da mensagem durante a extração.

---

## 📁 Estrutura do projeto

```
.
├── esteganografia_bilingue.py   # Código fonte principal (bilíngue)
├── README.pt-PT.md              # Documentação em Português
├── README.en-US.md              # Documentation in English
└── .gitignore                   # (opcional) Ficheiros a ignorar pelo Git
```

---

## ⚠️ Limitações e notas

- **Formato de imagem:** Apenas imagens **PNG** são suportadas. O formato PNG utiliza compressão sem perdas, o que garante que os bits LSB não sejam alterados pelo processo de compressão (ao contrário do JPEG).
- **Capacidade:** A capacidade máxima de armazenamento é de aproximadamente **1 byte por pixél** (1 bit por canal azul). Para uma imagem de 800×600, o limite teórico é de ~480 000 caracteres, embora a aplicação verifique o espaço disponível.
- **Segurança:** Embora a distribuição pseudoaleatória dificulte a deteção casual, esta implementação é didática. Para cenários de alta segurança, considere adicionar encriptação da mensagem antes da esteganografia (ex: AES-256) e utilizar geradores de números aleatórios criptograficamente seguros.
- **Palavra-passe:** A chave é utilizada apenas para gerar a sequência de índices. Não encripta o conteúdo da mensagem em si.

---

## 🖼️ Screenshots

> *(Adicionar screenshots da aplicação em funcionamento aqui)*

| Ocultar mensagem | Extrair mensagem |
|------------------|------------------|
| *(screenshot 1)* | *(screenshot 2)* |

---

## 👤 Autor

**Alphonsiny Vas**

- GitHub: [@alphondiny](https://github.com/alphondiny)
- Projeto desenvolvido no âmbito da Esteganografia (junho/2026)

---

## 📄 Licença

Este projeto é open-source e está disponível sob a licença [MIT](LICENSE).

---

## 🤝 Contribuições

Contribuições são bem-vindas! Se encontrar algum bug ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

---

<p align="center">
  <sub>Feito com ❤️ e Python</sub>
</p>
