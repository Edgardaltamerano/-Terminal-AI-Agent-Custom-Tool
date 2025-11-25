# -Terminal-AI-Agent-Custom-Tool
# 🤖 AI Terminal Agent - Asisten Cerdas di Command Line

AI Agent berbasis terminal yang dapat memahami perintah bahasa Indonesia dan menjalankan tugas otomatis seperti manajemen file, monitoring sistem, dan pencarian file.

## ✨ Fitur Utama

- **💬 Natural Language Interface** - Berinteraksi dengan bahasa Indonesia sehari-hari
- **🎨 Terminal Berwarna** - Interface yang menarik dan mudah dibaca
- **📁 Smart File Organizer** - Otomatis mengorganisir file berdasarkan ekstensi
- **🖥️ System Monitoring** - Cek RAM, CPU, dan info sistem lainnya
- **🔍 File Search** - Pencarian file yang powerful
- **🛡️ Aman & Terjamin** - Error handling yang robust

## 🚀 Instalasi Cepat

### Prerequisites
- Python 3.7 atau lebih tinggi
- pip (Python package manager)

### Langkah 1: Clone Repository
```bash
git clone https://github.com/username/ai-terminal-agent.git
cd ai-terminal-agent
```
### Langkah 2: Jalankan AI Agent
python ai_agent.py

Dependencies akan otomatis terinstall!

<img width="763" height="218" alt="image" src="https://github.com/user-attachments/assets/2a46f1dd-d76a-4bf6-a6f2-7d0766cf6b78" />

## 🎯 Contoh Perintah yang Didukung
## 📁 File Management
```bash
"rapikan file PDF di folder Downloads"
"organisir file JPG di Desktop" 
"pindahkan file Python di Documents"
"atur file ZIP di folder Downloads"
"susun semua file DOCX"
```
## 🖥️ System Monitoring
```bash
"cek sisa RAM di laptop saya"
"periksa kondisi sistem"
"berapa penggunaan CPU sekarang"
"cek memory laptop"
```
## 🔍 File Search
```bash
"cari file PDF di folder Documents"
"carikan file gambar JPG di Pictures"
"temukan file Python di project folder"
```
## 🎨 Contoh Output
File Organization
```text
You: rapikan file pdf di downloads

[AI Thinking]: Menganalisis permintaan user...
[AI Thinking]: Mengidentifikasi parameter untuk smart_file_organizer...
[Tool Output]: Tool: smart_file_organizer, Parameters: {'path': 'C:/Users/User/Downloads', 'extension': 'pdf'}
[AI Thinking]: Menjalankan smart_file_organizer dengan parameter: {'path': 'C:/Users/User/Downloads', 'extension': 'pdf'}

[Tool Output]: Memindahkan: laporan.pdf → laporan.pdf
[Tool Output]: Memindahkan: tutorial.pdf → tutorial.pdf
[Tool Output]: Tool execution completed

[AI Final Answer]: Tugas selesai! Berhasil memindahkan 2 file PDF ke folder C:/Users/User/Downloads/Organized/PDF
File yang dipindahkan: laporan.pdf, tutorial.pdf
```

## System Check
```text
You: cek sisa RAM di laptop

[AI Thinking]: Menganalisis permintaan user...
[AI Thinking]: Mengidentifikasi parameter untuk system_check...
[AI Thinking]: Menjalankan system_check dengan parameter: {}
[Tool Output]: Tool execution completed

[AI Final Answer]: Informasi Sistem:
- OS: Windows 10.0.19045
- Architecture: 64bit
- Memory Available: 6.2 GB dari 16.0 GB
- Memory Used: 61.5%
- CPU Usage: 23.8%
```
## 🔧 Technical Details
Dependencies
colorama - Untuk warna di terminal

psutil - Untuk system monitoring

pathlib - Untuk manipulasi path yang aman

Supported Platforms
✅ Windows

✅ macOS

✅ Linux

File Structure Created
``` text
Downloads/
├── Organized/
│   ├── PDF/
│   │   ├── file1.pdf
│   │   └── file2.pdf
│   └── JPG/
│       ├── image1.jpg
│       └── image2.jpg
```

## 🎪 Fitur Keren
### 🧠 Natural Language Processing
AI memahami berbagai variasi perintah:

"rapikan file PDF" = "organisir file pdf" = "pindahkan file pdf"

"cek RAM" = "periksa memory" = "lihat sisa memory"

### 📂 Smart File Detection
Mendeteksi otomatis:

Ekstensi file: PDF, JPG, PNG, DOCX, TXT, PY, ZIP, RAR

Folder target: Downloads, Documents, Desktop

Bahasa: Indonesia sehari-hari

### 🛡️ Safety Features
Validasi path sebelum operasi

Penanganan error yang graceful

Duplicate file handling dengan penamaan otomatis

### ❓ Troubleshooting
Problem: ModuleNotFoundError
Solution:

```bash
pip install colorama psutil
Problem: Permission Error
Solution: Jalankan sebagai administrator (Windows) atau sudo (Linux/Mac)

Problem: Folder tidak ditemukan
Solution: Pastikan folder target ada dan dapat diakses
```

### 🤝 Kontribusi
Contributions are welcome!

Fork repository

Buat feature branch

Commit changes

Push ke branch

Buat Pull Request

### 📄 License
MIT License - bebas digunakan untuk personal maupun komersial.

##💡 Tips Penggunaan
Gunakan bahasa natural - AI memahami percakapan sehari-hari

Spesifik lebih baik - "rapikan file PDF di Downloads"

Cek available memory sebelum operasi file besar

Backup data penting sebelum menggunakan file organizer

Dibuat dengan ❤️ untuk developer dan system administrator Indonesia

"Membuat pekerjaan sehari-hari lebih mudah dengan AI"

``` text

## 📋 **File-file yang Perlu Disertakan:**
```
**1. `requirements.txt`**
```txt
colorama>=0.4.6
psutil>=5.9.0
```
2. .gitignore

gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.DS_Store
Organized/  # Folder hasil organisasi
3. Struktur Repository yang Disarankan:

text
ai-terminal-agent/
├── ai_agent.py          # File utama
├── requirements.txt     # Dependencies
├── README.md           # Dokumentasi ini
├── .gitignore          # Git ignore rules
└── images/             # Screenshots (jika ada)
    ├── demo1.png
    └── demo2.png
🚀 Cara Deploy ke GitHub:
bash
# Inisialisasi git
git init

# Tambahkan semua file
git add .

# Commit pertama
git commit -m "feat: AI Terminal Agent dengan natural language Indonesia"

# Hubungkan ke GitHub (ganti dengan URL repo Anda)
git remote add origin https://github.com/username/ai-terminal-agent.git

# Push ke main branch
git branch -M main
git push -u origin main
