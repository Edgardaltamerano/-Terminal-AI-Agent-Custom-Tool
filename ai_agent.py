import os
import shutil
import re
from pathlib import Path
from colorama import Fore, Style, init
import platform

# Inisialisasi colorama
init(autoreset=True)

class TerminalAIAgent:
    def __init__(self):
        self.alat = {
            'organiser_file_pintar': self.organiser_file_pintar,
            'pemeriksa_sistem': self.pemeriksa_sistem,
            'pencari_file': self.pencari_file
        }
        
    def tampilkan_pesan_berpikir(self, pesan):
        """Menampilkan pesan thinking dengan warna kuning"""
        print(f"\n{Fore.YELLOW}[AI Berpikir]: {pesan}{Style.RESET_ALL}")
    
    def tampilkan_output_alat(self, pesan):
        """Menampilkan output alat dengan warna cyan"""
        print(f"{Fore.CYAN}[Output Alat]: {pesan}{Style.RESET_ALL}")
    
    def tampilkan_jawaban_akhir(self, pesan):
        """Menampilkan jawaban akhir dengan warna putih"""
        print(f"\n{Fore.WHITE}[Jawaban Akhir AI]: {pesan}{Style.RESET_ALL}")
    
    def tampilkan_error(self, pesan):
        """Menampilkan error dengan warna merah"""
        print(f"{Fore.RED}[Error]: {pesan}{Style.RESET_ALL}")
    
    def organiser_file_pintar(self, jalur, ekstensi):
        """
        Custom Tool: Mengorganisir file berdasarkan ekstensi
        
        Args:
            jalur (str): Jalur direktori target
            ekstensi (str): Ekstensi file yang dicari (pdf, jpg, py, dll)
        """
        try:
            jalur = Path(jalur)
            if not jalur.exists():
                return {"berhasil": False, "error": f"Jalur '{jalur}' tidak ditemukan"}
            
            # Normalisasi ekstensi (hapus titik jika ada)
            ekstensi = ekstensi.lower().lstrip('.')
            
            # Buat folder terorganisir
            jalur_terorganisir = jalur / "Terorganisir"
            folder_ekstensi = jalur_terorganisir / ekstensi.upper()
            folder_ekstensi.mkdir(parents=True, exist_ok=True)
            
            # Cari file secara rekursif
            file_yang_dipindahkan = []
            pola = f"*.{ekstensi}"
            
            for jalur_file in jalur.rglob(pola):
                if jalur_file.is_file() and jalur_file.parent != folder_ekstensi:
                    try:
                        # Buat nama file baru untuk menghindari konflik
                        nama_file_baru = jalur_file.name
                        penghitung = 1
                        
                        # Periksa apakah file dengan nama sama sudah ada di tujuan
                        while (folder_ekstensi / nama_file_baru).exists():
                            bagian_nama = jalur_file.stem, penghitung, jalur_file.suffix
                            nama_file_baru = f"{bagian_nama[0]}_{bagian_nama[1]}{bagian_nama[2]}"
                            penghitung += 1
                        
                        # Pindahkan file
                        tujuan = folder_ekstensi / nama_file_baru
                        shutil.move(str(jalur_file), str(tujuan))
                        file_yang_dipindahkan.append(nama_file_baru)
                        
                        self.tampilkan_output_alat(f"Memindahkan: {jalur_file.name} → {nama_file_baru}")
                        
                    except Exception as e:
                        self.tampilkan_error(f"Gagal memindahkan {jalur_file}: {str(e)}")
                        continue  # Lanjut ke file berikutnya meski ada error
            
            return {
                "berhasil": True,
                "jumlah_dipindahkan": len(file_yang_dipindahkan),
                "tujuan": str(folder_ekstensi),
                "file": file_yang_dipindahkan
            }
            
        except Exception as e:
            return {"berhasil": False, "error": str(e)}
    
    def pemeriksa_sistem(self):
        """Custom Tool: Melakukan pemeriksaan sistem"""
        try:
            info_sistem = {
                "platform": platform.system(),
                "rilis_platform": platform.release(),
                "versi_platform": platform.version(),
                "arsitektur": platform.architecture(),
                "prosesor": platform.processor(),
            }
            
            # Dapatkan info memori (bekerja di sebagian besar sistem)
            try:
                import psutil
                memori = psutil.virtual_memory()
                info_sistem["total_memori"] = f"{memori.total // (1024**3)} GB"
                info_sistem["memori_tersedia"] = f"{memori.available // (1024**3)} GB"
                info_sistem["memori_terpakai"] = f"{memori.percent}%"
                
                # Penggunaan CPU
                penggunaan_cpu = psutil.cpu_percent(interval=1)
                info_sistem["penggunaan_cpu"] = f"{penggunaan_cpu}%"
                
            except ImportError:
                info_sistem["info_memori"] = "Install psutil untuk info detail memori"
            
            return {"berhasil": True, "info_sistem": info_sistem}
            
        except Exception as e:
            return {"berhasil": False, "error": str(e)}
    
    def pencari_file(self, jalur, pola):
        """
        Custom Tool: Mencari file berdasarkan pola nama
        
        Args:
            jalur (str): Jalur direktori target
            pola (str): Pola pencarian (bisa menggunakan wildcard)
        """
        try:
            jalur = Path(jalur)
            if not jalur.exists():
                return {"berhasil": False, "error": f"Jalur '{jalur}' tidak ditemukan"}
            
            file_ditemukan = []
            for jalur_file in jalur.rglob(pola):
                if jalur_file.is_file():
                    file_ditemukan.append({
                        "nama": jalur_file.name,
                        "jalur": str(jalur_file),
                        "ukuran": f"{jalur_file.stat().st_size / 1024:.2f} KB"
                    })
            
            return {
                "berhasil": True,
                "jumlah_ditemukan": len(file_ditemukan),
                "file": file_ditemukan
            }
            
        except Exception as e:
            return {"berhasil": False, "error": str(e)}
    
    def parse_input_pengguna(self, input_pengguna):
        """Mengurai input pengguna dan menentukan alat yang sesuai"""
        input_pengguna_lower = input_pengguna.lower()
        
        # Pola untuk organiser file
        pola_organiser = [
            r'(rapikan|organisir|pindahkan|atur|susun).*(file|pdf|jpg|png|docx|txt|py|zip|folder)',
            r'(cari|carikan).*(pdf|jpg|png|docx|txt|py|zip).*(pindahkan|rapikan|atur)',
            r'(file organizer|organize file|rapikan file)',
            r'(semua|semua file).*(zip|pdf|jpg)',
            r'(folder|direktori).*(zip|pdf|jpg)'
        ]
        
        for pola in pola_organiser:
            if re.search(pola, input_pengguna_lower):
                return 'organiser_file_pintar'
        
        # Pola untuk pemeriksa sistem
        if re.search(r'(cek|periksa|check).*(sistem|ram|memory|cpu|laptop|komputer)', input_pengguna_lower):
            return 'pemeriksa_sistem'
        
        # Pola untuk pencari file
        if re.search(r'(cari|carikan|temukan|search|find).*file', input_pengguna_lower):
            return 'pencari_file'
        
        return None
    
    def ekstrak_parameter(self, input_pengguna, nama_alat):
        """Mengekstrak parameter dari input pengguna"""
        input_pengguna_lower = input_pengguna.lower()
        
        if nama_alat == 'organiser_file_pintar':
            # Ekstrak ekstensi
            daftar_ekstensi = ['pdf', 'jpg', 'jpeg', 'png', 'docx', 'txt', 'py', 'zip', 'rar']
            ekstensi = None
            
            # Cari ekstensi dalam input
            for ext in daftar_ekstensi:
                if ext in input_pengguna_lower:
                    ekstensi = ext
                    break
            
            # Jika tidak ditemukan, default ke pdf
            if not ekstensi:
                ekstensi = 'pdf'
            
            # Jalur default adalah direktori saat ini
            jalur = os.getcwd()
            
            # Periksa folder spesifik
            if 'download' in input_pengguna_lower or 'unduh' in input_pengguna_lower:
                jalur = os.path.expanduser('~/Downloads')
            elif 'document' in input_pengguna_lower or 'dokumen' in input_pengguna_lower:
                jalur = os.path.expanduser('~/Documents')
            elif 'desktop' in input_pengguna_lower or 'deskop' in input_pengguna_lower:
                jalur = os.path.expanduser('~/Desktop')
            
            return {'jalur': jalur, 'ekstensi': ekstensi}
        
        elif nama_alat == 'pencari_file':
            jalur = os.getcwd()
            pola = "*"
            
            if 'download' in input_pengguna_lower:
                jalur = os.path.expanduser('~/Downloads')
            elif 'document' in input_pengguna_lower:
                jalur = os.path.expanduser('~/Documents')
            
            # Ekstrak pola pencarian
            if 'pdf' in input_pengguna_lower:
                pola = "*.pdf"
            elif 'jpg' in input_pengguna_lower or 'gambar' in input_pengguna_lower:
                pola = "*.jpg"
            elif 'python' in input_pengguna_lower or '.py' in input_pengguna_lower:
                pola = "*.py"
            elif 'zip' in input_pengguna_lower:
                pola = "*.zip"
            
            return {'jalur': jalur, 'pola': pola}
        
        elif nama_alat == 'pemeriksa_sistem':
            return {}
        
        return {}
    
    def proses_perintah(self, input_pengguna):
        """Memproses perintah dari pengguna"""
        self.tampilkan_pesan_berpikir("Menganalisis permintaan pengguna...")
        
        # Tentukan alat yang akan digunakan
        nama_alat = self.parse_input_pengguna(input_pengguna)
        
        if not nama_alat:
            self.tampilkan_jawaban_akhir("Maaf, saya tidak memahami perintah tersebut. Saya bisa membantu dengan:\n- Organisasi file (contoh: 'rapikan file PDF di folder Downloads')\n- Pemeriksaan sistem (contoh: 'cek sisa RAM di laptop')\n- Pencarian file (contoh: 'cari file Python di Documents')")
            return
        
        # Ekstrak parameter
        self.tampilkan_pesan_berpikir(f"Mengidentifikasi parameter untuk {nama_alat}...")
        parameter = self.ekstrak_parameter(input_pengguna, nama_alat)
        
        # Info debug (opsional)
        self.tampilkan_output_alat(f"Alat: {nama_alat}, Parameter: {parameter}")
        
        # Jalankan alat
        self.tampilkan_pesan_berpikir(f"Menjalankan {nama_alat} dengan parameter: {parameter}")
        fungsi_alat = self.alat[nama_alat]
        hasil = fungsi_alat(**parameter)
        
        # Tampilkan hasil
        self.tampilkan_output_alat("Eksekusi alat selesai")
        
        if hasil['berhasil']:
            if nama_alat == 'organiser_file_pintar':
                pesan = f"Tugas selesai! Berhasil memindahkan {hasil['jumlah_dipindahkan']} file {parameter['ekstensi'].upper()} ke folder {hasil['tujuan']}"
                if hasil['file']:
                    pesan += f"\nFile yang dipindahkan: {', '.join(hasil['file'][:5])}"  # Tampilkan 5 file pertama
                    if len(hasil['file']) > 5:
                        pesan += f" ... dan {len(hasil['file']) - 5} file lainnya"
            elif nama_alat == 'pemeriksa_sistem':
                info = hasil['info_sistem']
                pesan = f"Informasi Sistem:\n- OS: {info['platform']} {info['rilis_platform']}\n- Arsitektur: {info['arsitektur'][0]}"
                if 'memori_tersedia' in info:
                    pesan += f"\n- Memori Tersedia: {info['memori_tersedia']} dari {info['total_memori']}\n- Memori Terpakai: {info['memori_terpakai']}\n- Penggunaan CPU: {info['penggunaan_cpu']}"
            elif nama_alat == 'pencari_file':
                pesan = f"Ditemukan {hasil['jumlah_ditemukan']} file dengan pola '{parameter['pola']}'"
                if hasil['file']:
                    pesan += f"\nFile ditemukan:\n"
                    for file in hasil['file'][:5]:  # Tampilkan 5 file pertama
                        pesan += f"- {file['nama']} ({file['ukuran']})\n"
                    if len(hasil['file']) > 5:
                        pesan += f"... dan {len(hasil['file']) - 5} file lainnya"
            self.tampilkan_jawaban_akhir(pesan)
        else:
            self.tampilkan_error(f"Eksekusi alat gagal: {hasil.get('error', 'Error tidak diketahui')}")
    
    def jalankan(self):
        """Menjalankan AI Agent"""
        print(f"{Fore.GREEN}=== AI Terminal Agent ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}Selamat datang! Saya AI Agent yang siap membantu.{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Perintah yang didukung:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}- Organisasi file (rapikan file PDF di folder Downloads){Style.RESET_ALL}")
        print(f"{Fore.WHITE}- Pemeriksaan sistem (cek sisa RAM di laptop){Style.RESET_ALL}")
        print(f"{Fore.WHITE}- Pencarian file (cari file Python di Documents){Style.RESET_ALL}")
        print(f"{Fore.WHITE}Ketik 'quit' untuk keluar{Style.RESET_ALL}\n")
        
        while True:
            try:
                input_pengguna = input(f"{Fore.GREEN}Anda: {Style.RESET_ALL}").strip()
                
                if input_pengguna.lower() in ['quit', 'exit', 'keluar']:
                    print(f"{Fore.YELLOW}[AI]: Sampai jumpa!{Style.RESET_ALL}")
                    break
                
                if input_pengguna:
                    self.proses_perintah(input_pengguna)
                else:
                    print(f"{Fore.YELLOW}[AI]: Silakan ketik perintah...{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[AI]: Agent dihentikan. Sampai jumpa!{Style.RESET_ALL}")
                break
            except Exception as e:
                self.tampilkan_error(f"Terjadi error: {str(e)}")

# Install package yang diperlukan jika belum ada
def install_kebutuhan():
    try:
        import colorama
        import psutil
        print("✅ Semua dependencies sudah terinstall!")
    except ImportError:
        import subprocess
        import sys
        print("Menginstall dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "psutil"])
        print("✅ Dependencies berhasil diinstall!")

if __name__ == "__main__":
    install_kebutuhan()
    agent = TerminalAIAgent()
    agent.jalankan()
