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
        self.tools = {
            'smart_file_organizer': self.smart_file_organizer,
            'system_check': self.system_check,
            'search_files': self.search_files
        }
        
    def print_thinking(self, message):
        """Menampilkan pesan thinking dengan warna kuning"""
        print(f"\n{Fore.YELLOW}[AI Thinking]: {message}{Style.RESET_ALL}")
    
    def print_tool_output(self, message):
        """Menampilkan output tool dengan warna cyan"""
        print(f"{Fore.CYAN}[Tool Output]: {message}{Style.RESET_ALL}")
    
    def print_final_answer(self, message):
        """Menampilkan jawaban akhir dengan warna putih"""
        print(f"\n{Fore.WHITE}[AI Final Answer]: {message}{Style.RESET_ALL}")
    
    def print_error(self, message):
        """Menampilkan error dengan warna merah"""
        print(f"{Fore.RED}[Error]: {message}{Style.RESET_ALL}")
    
    def smart_file_organizer(self, path, extension):
        """
        Tool Kustom: Mengorganisir file berdasarkan ekstensi
        
        Args:
            path (str): Path direktori target
            extension (str): Ekstensi file yang dicari (pdf, jpg, py, dll)
        """
        try:
            path = Path(path)
            if not path.exists():
                return {"success": False, "error": f"Path '{path}' tidak ditemukan"}
            
            # Normalisasi ekstensi (hapus titik jika ada)
            extension = extension.lower().lstrip('.')
            
            # Buat folder terorganisir
            organized_path = path / "Organized"
            extension_folder = organized_path / extension.upper()
            extension_folder.mkdir(parents=True, exist_ok=True)
            
            # Cari file secara rekursif
            moved_files = []
            pattern = f"*.{extension}"
            
            for file_path in path.rglob(pattern):
                if file_path.is_file() and file_path.parent != extension_folder:
                    try:
                        # Buat nama file baru untuk menghindari konflik
                        new_filename = file_path.name
                        counter = 1
                        
                        # Periksa apakah file dengan nama sama sudah ada di tujuan
                        while (extension_folder / new_filename).exists():
                            name_parts = file_path.stem, counter, file_path.suffix
                            new_filename = f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                            counter += 1
                        
                        # Pindahkan file
                        destination = extension_folder / new_filename
                        shutil.move(str(file_path), str(destination))
                        moved_files.append(new_filename)
                        
                        self.print_tool_output(f"Memindahkan: {file_path.name} → {new_filename}")
                        
                    except Exception as e:
                        self.print_error(f"Gagal memindahkan {file_path}: {str(e)}")
                        continue  # Lanjut ke file berikutnya meski ada error
            
            return {
                "success": True,
                "moved_count": len(moved_files),
                "destination": str(extension_folder),
                "files": moved_files
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def system_check(self):
        """Tool Kustom: Melakukan pemeriksaan sistem"""
        try:
            system_info = {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.architecture(),
                "processor": platform.processor(),
            }
            
            # Dapatkan info memori (bekerja di sebagian besar sistem)
            try:
                import psutil
                memory = psutil.virtual_memory()
                system_info["memory_total"] = f"{memory.total // (1024**3)} GB"
                system_info["memory_available"] = f"{memory.available // (1024**3)} GB"
                system_info["memory_used"] = f"{memory.percent}%"
                
                # Penggunaan CPU
                cpu_usage = psutil.cpu_percent(interval=1)
                system_info["cpu_usage"] = f"{cpu_usage}%"
                
            except ImportError:
                system_info["memory_info"] = "Install psutil untuk info detail memory"
            
            return {"success": True, "system_info": system_info}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_files(self, path, pattern):
        """
        Tool Kustom: Mencari file berdasarkan pola nama
        
        Args:
            path (str): Path direktori target
            pattern (str): Pola pencarian (bisa menggunakan wildcard)
        """
        try:
            path = Path(path)
            if not path.exists():
                return {"success": False, "error": f"Path '{path}' tidak ditemukan"}
            
            found_files = []
            for file_path in path.rglob(pattern):
                if file_path.is_file():
                    found_files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": f"{file_path.stat().st_size / 1024:.2f} KB"
                    })
            
            return {
                "success": True,
                "found_count": len(found_files),
                "files": found_files
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def parse_user_input(self, user_input):
        """Mengurai input user dan menentukan tool yang sesuai"""
        user_input_lower = user_input.lower()
        
        # Pola untuk file organizer
        organizer_patterns = [
            r'(rapikan|organisir|pindahkan|atur|susun).*(file|pdf|jpg|png|docx|txt|py|zip|folder)',
            r'(cari|carikan).*(pdf|jpg|png|docx|txt|py|zip).*(pindahkan|rapikan|atur)',
            r'(file organizer|organize file|rapikan file)',
            r'(semua|semua file).*(zip|pdf|jpg)',
            r'(folder|direktori).*(zip|pdf|jpg)'
        ]
        
        for pattern in organizer_patterns:
            if re.search(pattern, user_input_lower):
                return 'smart_file_organizer'
        
        # Pola untuk system check
        if re.search(r'(cek|periksa|check).*(sistem|ram|memory|cpu|laptop|komputer)', user_input_lower):
            return 'system_check'
        
        # Pola untuk search files
        if re.search(r'(cari|carikan|temukan|search|find).*file', user_input_lower):
            return 'search_files'
        
        return None
    
    def extract_parameters(self, user_input, tool_name):
        """Mengekstrak parameter dari input user"""
        user_input_lower = user_input.lower()
        
        if tool_name == 'smart_file_organizer':
            # Ekstrak ekstensi
            extensions = ['pdf', 'jpg', 'jpeg', 'png', 'docx', 'txt', 'py', 'zip', 'rar']
            extension = None
            
            # Cari ekstensi dalam input user
            for ext in extensions:
                if ext in user_input_lower:
                    extension = ext
                    break
            
            # Jika tidak ditemukan, default ke pdf
            if not extension:
                extension = 'pdf'
            
            # Path default adalah direktori saat ini
            path = os.getcwd()
            
            # Periksa folder spesifik
            if 'download' in user_input_lower or 'unduh' in user_input_lower:
                path = os.path.expanduser('~/Downloads')
            elif 'document' in user_input_lower or 'dokumen' in user_input_lower:
                path = os.path.expanduser('~/Documents')
            elif 'desktop' in user_input_lower or 'deskop' in user_input_lower:
                path = os.path.expanduser('~/Desktop')
            
            return {'path': path, 'extension': extension}
        
        elif tool_name == 'search_files':
            path = os.getcwd()
            pattern = "*"
            
            if 'download' in user_input_lower:
                path = os.path.expanduser('~/Downloads')
            elif 'document' in user_input_lower:
                path = os.path.expanduser('~/Documents')
            
            # Ekstrak pola pencarian
            if 'pdf' in user_input_lower:
                pattern = "*.pdf"
            elif 'jpg' in user_input_lower or 'gambar' in user_input_lower:
                pattern = "*.jpg"
            elif 'python' in user_input_lower or '.py' in user_input_lower:
                pattern = "*.py"
            elif 'zip' in user_input_lower:
                pattern = "*.zip"
            
            return {'path': path, 'pattern': pattern}
        
        elif tool_name == 'system_check':
            return {}
        
        return {}
    
    def process_command(self, user_input):
        """Memproses perintah dari user"""
        self.print_thinking("Menganalisis permintaan user...")
        
        # Tentukan tool yang akan digunakan
        tool_name = self.parse_user_input(user_input)
        
        if not tool_name:
            self.print_final_answer("Maaf, saya tidak memahami perintah tersebut. Saya bisa membantu dengan:\n- File organization (contoh: 'rapikan file PDF di folder Downloads')\n- System check (contoh: 'cek sisa RAM di laptop')\n- File search (contoh: 'cari file Python di Documents')")
            return
        
        # Ekstrak parameter
        self.print_thinking(f"Mengidentifikasi parameter untuk {tool_name}...")
        parameters = self.extract_parameters(user_input, tool_name)
        
        # Info debug (opsional)
        self.print_tool_output(f"Tool: {tool_name}, Parameters: {parameters}")
        
        # Jalankan tool
        self.print_thinking(f"Menjalankan {tool_name} dengan parameter: {parameters}")
        tool_function = self.tools[tool_name]
        result = tool_function(**parameters)
        
        # Tampilkan hasil
        self.print_tool_output("Eksekusi tool selesai")
        
        if result['success']:
            if tool_name == 'smart_file_organizer':
                message = f"Tugas selesai! Berhasil memindahkan {result['moved_count']} file {parameters['extension'].upper()} ke folder {result['destination']}"
                if result['files']:
                    message += f"\nFile yang dipindahkan: {', '.join(result['files'][:5])}"  # Tampilkan 5 file pertama
                    if len(result['files']) > 5:
                        message += f" ... dan {len(result['files']) - 5} file lainnya"
            elif tool_name == 'system_check':
                info = result['system_info']
                message = f"Informasi Sistem:\n- OS: {info['platform']} {info['platform_release']}\n- Architecture: {info['architecture'][0]}"
                if 'memory_available' in info:
                    message += f"\n- Memory Available: {info['memory_available']} dari {info['memory_total']}\n- Memory Used: {info['memory_used']}\n- CPU Usage: {info['cpu_usage']}"
            elif tool_name == 'search_files':
                message = f"Ditemukan {result['found_count']} file matching pattern '{parameters['pattern']}'"
                if result['files']:
                    message += f"\nFile ditemukan:\n"
                    for file in result['files'][:5]:  # Tampilkan 5 file pertama
                        message += f"- {file['name']} ({file['size']})\n"
                    if len(result['files']) > 5:
                        message += f"... dan {len(result['files']) - 5} file lainnya"
            self.print_final_answer(message)
        else:
            self.print_error(f"Eksekusi tool gagal: {result.get('error', 'Error tidak diketahui')}")
    
    def run(self):
        """Menjalankan AI Agent"""
        print(f"{Fore.GREEN}=== AI Terminal Agent ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}Selamat datang! Saya AI Agent yang siap membantu.{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Perintah yang didukung:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}- File organization (rapikan file PDF di folder Downloads){Style.RESET_ALL}")
        print(f"{Fore.WHITE}- System check (cek sisa RAM di laptop){Style.RESET_ALL}")
        print(f"{Fore.WHITE}- File search (cari file Python di Documents){Style.RESET_ALL}")
        print(f"{Fore.WHITE}Ketik 'quit' untuk keluar{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
                
                if user_input.lower() in ['quit', 'exit', 'keluar']:
                    print(f"{Fore.YELLOW}[AI]: Sampai jumpa!{Style.RESET_ALL}")
                    break
                
                if user_input:
                    self.process_command(user_input)
                else:
                    print(f"{Fore.YELLOW}[AI]: Silakan ketik perintah...{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[AI]: Agent dihentikan. Sampai jumpa!{Style.RESET_ALL}")
                break
            except Exception as e:
                self.print_error(f"Terjadi error: {str(e)}")

# Install package yang diperlukan jika belum ada
def install_requirements():
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
    install_requirements()
    agent = TerminalAIAgent()
    agent.run()
