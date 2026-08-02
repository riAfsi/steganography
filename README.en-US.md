# 🔒 LSB Steganography – alphondiny

Desktop application in Python with a graphical interface (Tkinter) for hiding and extracting secret messages inside PNG images using the **LSB Steganography** (*Least Significant Bit*) technique.

> **Steganography**  
> Developed by **Alphonsiny Vas**

---

## ✨ Features

- **🔒 Hide messages** – Conceals arbitrary text inside a PNG image without visually altering it.
- **🔓 Extract messages** – Recovers hidden text from a stego image, provided the correct password is given.
- **🔑 Password protection** – The message is distributed pseudo-randomly across the image pixels based on a key, making statistical detection harder.
- **🌍 Bilingual support** – Interface available in Portuguese (PT-PT) and English (EN-US).
- **🖼️ Intuitive GUI** – Built with Tkinter, no command-line knowledge required.

---

## 🛠️ Requirements

| Dependency  | Minimum version |
|-------------|-----------------|
| Python      | 3.7+            |
| Pillow (PIL)| 9.0+            |
| tkinter     | (included in Python stdlib) |

### Installing dependencies

```bash
pip install Pillow
```

> `tkinter` is included in the standard Python installation on most operating systems. If it is not available, install it through your system's package manager:
> - **Debian/Ubuntu:** `sudo apt-get install python3-tk`
> - **Fedora/RHEL:** `sudo dnf install python3-tkinter`
> - **macOS:** included with the official Python installation from [python.org](https://python.org)
> - **Windows:** included by default in the Python installer

---

## 🚀 How to run

1. Clone or download this repository:
   ```bash
   git clone https://github.com/alphondiny/esteganografia-lsb.git
   cd esteganografia-lsb
   ```

2. Run the application:
   ```bash
   python esteganografia_bilingue.py
   ```

---

## 📖 How to use

### Change language

At the top of the window, select **PT-PT** or **EN-US** from the language box. The interface updates instantly with no need to restart the application.

### Hide a message

1. Click **"Select original image (PNG)"** and choose a PNG image.
2. Type the message you want to hide in the **"Message to hide"** field.
3. Enter a **password** in the corresponding field.
4. Click **"💾 Hide and save as..."** and choose the output filename.
5. The resulting image will be visually identical to the original but will contain the hidden message.

### Extract a message

1. Click **"Select image with hidden message (PNG)"** and choose the stego image.
2. Enter the **same password** used during hiding.
3. Click **"🔍 Extract"**.
4. The message will be displayed in the result field.

> ⚠️ **Note:** The password must be exactly the same as the one used for hiding. Otherwise, the terminator will not be found and extraction will fail.

---

## 🔬 How it works

### LSB Technique (Least Significant Bit)

The application uses the **blue (B)** channel of each RGB pixel to store 1 bit of the message, replacing the least significant bit:

```
Original pixel:  (R, G, B) = (120, 200, 255)
Bit to hide:     0
Altered pixel:   (R, G, B) = (120, 200, 254)  ← B & 0xFE | bit
```

Changing only 1 bit in the blue channel is practically imperceptible to the human eye, preserving the visual integrity of the image.

### Pseudo-random distribution

To increase security, the message is **not written sequentially** across pixels. Instead, a pseudo-random permutation of pixel indices is generated based on the provided password:

```python
seed = sum(ord(c) for c in key)
random.seed(seed)
random.shuffle(indices)
```

This means:
- Without the correct password, it is impossible to know which pixels contain the message.
- The random distribution makes statistical analysis harder, which could otherwise detect the presence of hidden data.

### Message format

The message is converted to binary (8 bits per UTF-8 character) and terminated with a null byte (`00000000`), which signals the end of the message during extraction.

---

## 📁 Project structure

```
.
├── esteganografia_bilingue.py   # Main source code (bilingual)
├── README.pt-PT.md              # Documentação em Português
├── README.en-US.md              # Documentation in English
└── .gitignore                   # (optional) Files to ignore by Git
```

---

## ⚠️ Limitations and notes

- **Image format:** Only **PNG** images are supported. The PNG format uses lossless compression, which ensures that LSB bits are not altered by the compression process (unlike JPEG).
- **Capacity:** The maximum storage capacity is approximately **1 byte per pixel** (1 bit per blue channel). For an 800×600 image, the theoretical limit is ~480,000 characters, although the application checks for available space.
- **Security:** Although the pseudo-random distribution makes casual detection harder, this is an educational implementation. For high-security scenarios, consider adding encryption to the message before steganography (e.g., AES-256) and using cryptographically secure random number generators.
- **Password:** The key is used only to generate the index sequence. It does not encrypt the message content itself.

---

## 🖼️ Screenshots

> *(Add screenshots of the application in use here)*

| Hide message     | Extract message  |
|------------------|------------------|
| *(screenshot 1)* | *(screenshot 2)* |

---

## 👤 Author

**Alphonsiny Vas**

- GitHub: [@alphondiny](https://github.com/alphondiny)
- Project developed as part of Steganography studies (June/2026)

---

## 📄 License

This project is open-source and available under the [MIT](LICENSE) license.

---

## 🤝 Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, feel free to open an *issue* or submit a *pull request*.

---

<p align="center">
  <sub>Made with ❤️ and Python</sub>
</p>
