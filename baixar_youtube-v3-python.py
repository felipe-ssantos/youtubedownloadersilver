import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
from pathlib import Path
import subprocess

class YouTubeDownloader:
    def __init__(self):
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("YouTube Downloader Silver")
        self.root.geometry("700x680") # Largura x Altura
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a1a')
        
        # Pasta padrão
        self.dest = os.path.join(os.environ['USERPROFILE'], 'Videos', 'YouTube')
        os.makedirs(self.dest, exist_ok=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Container principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # ========== CABEÇALHO ==========
        header = tk.Frame(main_frame, bg='#0066cc', relief='flat')
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            header,
            text="🎬 YouTube Downloader Silver",
            font=('Segoe UI', 22, 'bold'),
            bg='#0066cc',
            fg='#ffffff'
        ).pack(pady=(12, 8))
        
        tk.Label(
            header,
            text="Baixe vídeos e áudios facilmente",
            font=('Segoe UI', 10),
            bg='#0066cc',
            fg='#e6f2ff'
        ).pack(pady=(0, 12))
        
        # ========== LINK ==========
        tk.Label(
            main_frame,
            text="🔗 Link do YouTube:",
            font=('Segoe UI', 11, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        ).pack(fill="x", pady=(0, 5))
        
        # Frame para link e botões
        link_frame = tk.Frame(main_frame, bg='#1a1a1a')
        link_frame.pack(fill="x", pady=(0, 15))
        
        # Entry do link
        self.link_entry = tk.Entry(
            link_frame,
            font=('Segoe UI', 11),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#0066cc',
            relief='solid',
            bd=2
        )
        self.link_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.link_entry.insert(0, "https://www.youtube.com/watch?v=...")
        self.link_entry.config(fg='#666666')
        self.link_entry.bind('<FocusIn>', self.clear_placeholder)
        self.link_entry.bind('<FocusOut>', self.restore_placeholder)
        
        # Frame para botões à direita
        buttons_frame = tk.Frame(link_frame, bg='#1a1a1a')
        buttons_frame.pack(side="left")
        
        # Botão Colar
        self.paste_btn = tk.Button(
            buttons_frame,
            text="📋 Colar",
            font=('Segoe UI', 9, 'bold'),
            bg='#444444',
            fg='#ffffff',
            activebackground='#555555',
            activeforeground='#ffffff',
            relief='raised',
            bd=2,
            cursor='hand2',
            command=self.paste_url,
            width=8
        )
        self.paste_btn.pack(side="left", ipady=7, padx=(0, 5))
        
        # Efeito hover no botão Colar
        self.paste_btn.bind('<Enter>', lambda e: self.paste_btn.config(bg='#555555'))
        self.paste_btn.bind('<Leave>', lambda e: self.paste_btn.config(bg='#444444'))
        
        # ========== BOTÃO INICIAR DOWNLOAD ==========
        self.download_btn = tk.Button(
            buttons_frame,
            text="⬇️ BAIXAR",
            font=('Segoe UI', 10, 'bold'),
            bg='#00aa44',
            fg='#ffffff',
            activebackground='#008833',
            activeforeground='#ffffff',
            relief='raised',
            bd=2,
            cursor='hand2',
            command=self.start_download,
            width=12
        )
        self.download_btn.pack(side="left", ipady=7)
        
        # Efeito hover
        self.download_btn.bind('<Enter>', lambda e: self.download_btn.config(bg='#00cc55'))
        self.download_btn.bind('<Leave>', lambda e: self.download_btn.config(bg='#00aa44'))
        
        # ========== FORMATO E QUALIDADE EM LINHA ==========
        options_frame = tk.Frame(main_frame, bg='#1a1a1a')
        options_frame.pack(fill="x", pady=(0, 15))
        
        # Coluna 1: Formato
        format_col = tk.Frame(options_frame, bg='#2d2d2d', relief='solid', bd=1)
        format_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(
            format_col,
            text="📁 Formato",
            font=('Segoe UI', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(pady=(10, 8))
        
        self.format_var = tk.StringVar(value="video")
        
        tk.Radiobutton(
            format_col,
            text="🎥 Vídeo (MP4)",
            variable=self.format_var,
            value="video",
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#0066cc',
            activebackground='#2d2d2d',
            activeforeground='#ffffff',
            command=self.toggle_resolution
        ).pack(anchor='w', padx=15, pady=2)
        
        tk.Radiobutton(
            format_col,
            text="🎵 Áudio (MP3)",
            variable=self.format_var,
            value="audio",
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#0066cc',
            activebackground='#2d2d2d',
            activeforeground='#ffffff',
            command=self.toggle_resolution
        ).pack(anchor='w', padx=15, pady=(2, 10))
        
        # Coluna 2: Qualidade
        self.quality_col = tk.Frame(options_frame, bg='#2d2d2d', relief='solid', bd=1)
        self.quality_col.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            self.quality_col,
            text="📺 Qualidade",
            font=('Segoe UI', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(pady=(10, 8))
        
        self.resolution_var = tk.StringVar(value="best")
        
        self.res_1080 = tk.Radiobutton(
            self.quality_col,
            text="1080p (Full HD)",
            variable=self.resolution_var,
            value="1080",
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#0066cc',
            activebackground='#2d2d2d',
            activeforeground='#ffffff'
        )
        self.res_1080.pack(anchor='w', padx=15, pady=2)
        
        self.res_720 = tk.Radiobutton(
            self.quality_col,
            text="720p (HD)",
            variable=self.resolution_var,
            value="720",
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#0066cc',
            activebackground='#2d2d2d',
            activeforeground='#ffffff'
        )
        self.res_720.pack(anchor='w', padx=15, pady=2)
        
        self.res_best = tk.Radiobutton(
            self.quality_col,
            text="Melhor disponível",
            variable=self.resolution_var,
            value="best",
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectcolor='#0066cc',
            activebackground='#2d2d2d',
            activeforeground='#ffffff'
        )
        self.res_best.pack(anchor='w', padx=15, pady=(2, 10))
        
        # ========== PASTA DESTINO ==========
        tk.Label(
            main_frame,
            text="💾 Pasta de destino:",
            font=('Segoe UI', 11, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        ).pack(fill="x", pady=(0, 5))
        
        dest_frame = tk.Frame(main_frame, bg='#1a1a1a')
        dest_frame.pack(fill="x", pady=(0, 15))
        
        self.dest_entry = tk.Entry(
            dest_frame,
            font=('Segoe UI', 9),
            bg='#2d2d2d',
            fg='#aaaaaa',
            relief='solid',
            bd=2
        )
        self.dest_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.dest_entry.insert(0, self.dest)
        
        dest_buttons_frame = tk.Frame(dest_frame, bg='#1a1a1a')
        dest_buttons_frame.pack(side="left")
        
        tk.Button(
            dest_buttons_frame,
            text="📂 Alterar",
            font=('Segoe UI', 9, 'bold'),
            bg='#444444',
            fg='#ffffff',
            activebackground='#555555',
            activeforeground='#ffffff',
            relief='raised',
            cursor='hand2',
            command=self.choose_destination,
            bd=2
        ).pack(side="left", ipady=8, ipadx=15, padx=(0, 5))
        
        # Botão para abrir pasta
        self.open_folder_btn = tk.Button(
            dest_buttons_frame,
            text="📁 Abrir Pasta",
            font=('Segoe UI', 9, 'bold'),
            bg='#0066cc',
            fg='#ffffff',
            activebackground='#0088ff',
            activeforeground='#ffffff',
            relief='raised',
            cursor='hand2',
            command=self.open_download_folder,
            bd=2
        )
        self.open_folder_btn.pack(side="left", ipady=8, ipadx=15)
        
        # ========== PROGRESSO ==========
        tk.Label(
            main_frame,
            text="📊 Progresso:",
            font=('Segoe UI', 11, 'bold'),
            bg='#1a1a1a',
            fg='#ffffff',
            anchor='w'
        ).pack(fill="x", pady=(0, 5))
        
        progress_bg = tk.Frame(main_frame, bg='#2d2d2d', relief='solid', bd=1)
        progress_bg.pack(fill="x", pady=(0, 15))
        
        progress_inner = tk.Frame(progress_bg, bg='#2d2d2d')
        progress_inner.pack(fill="x", padx=10, pady=10)
        
        # Estilo da progressbar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#1a1a1a',
            background='#0066cc',
            bordercolor='#444444',
            lightcolor='#0088ff',
            darkcolor='#0044aa',
            thickness=20
        )
        
        self.progress = ttk.Progressbar(
            progress_inner,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", pady=(0, 8))
        self.progress['value'] = 0
        
        self.status_label = tk.Label(
            progress_inner,
            text="⏳ Aguardando...",
            font=('Segoe UI', 10, 'bold'),
            bg='#2d2d2d',
            fg='#aaaaaa'
        )
        self.status_label.pack()
         
        # ========== ESPAÇO FLEXÍVEL ==========
        spacer = tk.Frame(main_frame, bg='#1a1a1a', height=10)
        spacer.pack(fill="x", expand=True)
        
        # ========== RODAPÉ ==========
        footer_frame = tk.Frame(main_frame, bg='#1a1a1a')
        footer_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            footer_frame,
            text="Desenvolvido com Python, por Nelson Felipe. | Versão 1.1",
            font=('Segoe UI', 9),
            bg='#1a1a1a',
            fg='#666666'
        ).pack()
    
    def paste_url(self):
        """Cola a URL da área de transferência"""
        try:
            # Limpa o campo
            self.link_entry.delete(0, tk.END)
            # Cola o conteúdo da área de transferência
            clipboard_content = self.root.clipboard_get()
            self.link_entry.insert(0, clipboard_content)
            self.link_entry.config(fg='#ffffff')
        except:
            messagebox.showwarning("Aviso", "Nenhum conteúdo válido na área de transferência!")
    
    def clear_placeholder(self, event):
        if self.link_entry.get() == "https://www.youtube.com/watch?v=...":
            self.link_entry.delete(0, tk.END)
            self.link_entry.config(fg='#ffffff')
    
    def restore_placeholder(self, event):
        if not self.link_entry.get().strip():
            self.link_entry.insert(0, "https://www.youtube.com/watch?v=...")
            self.link_entry.config(fg='#666666')
    
    def toggle_resolution(self):
        if self.format_var.get() == "video":
            self.res_1080.config(state="normal", fg='#ffffff')
            self.res_720.config(state="normal", fg='#ffffff')
            self.res_best.config(state="normal", fg='#ffffff')
        else:
            self.res_1080.config(state="disabled", fg='#666666')
            self.res_720.config(state="disabled", fg='#666666')
            self.res_best.config(state="disabled", fg='#666666')
    
    def choose_destination(self):
        # Salva o link atual antes de abrir o diálogo
        current_link = self.link_entry.get()
        
        folder = filedialog.askdirectory(initialdir=self.dest, title="Escolha a pasta")
        if folder:
            self.dest = folder
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)
        
        # Restaura o link após selecionar a pasta
        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, current_link)
        if current_link != "https://www.youtube.com/watch?v=...":
            self.link_entry.config(fg='#ffffff')
    
    def open_download_folder(self):
        """Abre a pasta de downloads no explorador de arquivos"""
        if os.path.exists(self.dest):
            try:
                if sys.platform == "win32":
                    os.startfile(self.dest)
                elif sys.platform == "darwin":  # macOS
                    subprocess.Popen(["open", self.dest])
                else:  # Linux
                    subprocess.Popen(["xdg-open", self.dest])
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{str(e)}")
        else:
            messagebox.showwarning("Aviso", "A pasta de destino não existe!")
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
                self.progress['value'] = percent * 100
                self.status_label.config(
                    text=f"📥 Baixando... {int(percent * 100)}%",
                    fg='#00aaff'
                )
                self.root.update_idletasks()
            except:
                self.status_label.config(text="📥 Baixando...", fg='#00aaff')
                self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.progress['value'] = 100
            self.status_label.config(text="⚙️ Processando...", fg='#ffaa00')
            self.root.update_idletasks()
    
    def download_video(self):
        link = self.link_entry.get().strip()
        
        if not link or link == "https://www.youtube.com/watch?v=..." or not link.startswith('http'):
            messagebox.showerror("Erro", "Insira um link válido!")
            self.download_btn.config(state="normal", text="⬇️ BAIXAR", bg='#00aa44')
            return
        
        self.download_btn.config(state="disabled", text="⏳ BAIXANDO...", bg='#666666')
        self.progress['value'] = 0
        self.status_label.config(text="🚀 Iniciando...", fg='#ffaa00')
        
        try:
            fmt = self.format_var.get()
            
            # Opções base SEM cookies - solução mais robusta
            base_opts = {
                'outtmpl': os.path.join(self.dest, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                # Configurações para evitar erro 403
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['dash', 'hls']
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                },
                'quiet': False,
                'no_warnings': False,
            }
            
            if fmt == "video":
                res = self.resolution_var.get()
                if res == "1080":
                    f = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                elif res == "720":
                    f = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]"
                else:
                    f = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                
                base_opts['format'] = f
                base_opts['merge_output_format'] = 'mp4'
            else:
                base_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
                base_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            with yt_dlp.YoutubeDL(base_opts) as ydl:
                ydl.download([link])
            
            self.status_label.config(text="✅ Concluído!", fg='#00ff00')
            self.progress['value'] = 100
            messagebox.showinfo("Sucesso", f"Download concluído!\n\nSalvo em:\n{self.dest}")
            
        except Exception as e:
            self.status_label.config(text="❌ Erro", fg='#ff0000')
            error_msg = str(e)
            if "403" in error_msg or "Forbidden" in error_msg:
                error_msg = "Erro 403: Acesso bloqueado pelo YouTube.\n\n"
                error_msg += "Soluções:\n"
                error_msg += "1. Atualize o yt-dlp: pip install --upgrade yt-dlp\n"
                error_msg += "2. Verifique se o vídeo não é privado/restrito\n"
                error_msg += "3. Tente novamente em alguns minutos"
            messagebox.showerror("Erro", f"Falha no download:\n\n{error_msg}")
        
        finally:
            self.download_btn.config(state="normal", text="⬇️ BAIXAR", bg='#00aa44')
            self.progress['value'] = 0
            self.status_label.config(text="⏳ Aguardando...", fg='#aaaaaa')
    
    def start_download(self):
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()
    
    def run(self):
        # Centralizar janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = YouTubeDownloader()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar: {e}")
        messagebox.showerror("Erro Fatal", f"Não foi possível iniciar:\n{e}")
        input("Pressione Enter para sair...")