import tkinter
import threading
import customtkinter
import keyboard
import pystray
from PIL import Image, ImageDraw
import os

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho para o arquivo de tema
theme_path = os.path.join(script_dir, "data", "theme.json")

# Define o tema padrão do customtkinter usando o caminho do arquivo de tema
customtkinter.set_default_color_theme(theme_path)  # Temas: "blue" (padrão), "green", "dark-blue", "sweetkind"


class AlwaysOnTopApp:  # Define a classe AlwaysOnTopApp
    def __init__(self):  # Define o método inicializador __init__
        self.root = customtkinter.CTk()  # Cria uma janela customtkinter
        self.root.geometry("240x100")  # Define o tamanho inicial da janela
        self.root.title("Launcher")  # Define o título da janela
        self.root.attributes('-topmost', True)  # Mantém a janela sempre no topo de outras janelas
        self.root.overrideredirect(True)  # Remove as decorações da janela (barra de tarefas e botão de fechar)
        self.center_window()  # Centraliza a janela na tela
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)  # Esconde a janela em vez de fechá-la

        # Cria um frame de fundo com uma cor de borda
        self.background_frame = tkinter.Frame(self.root, bg="#646464")  # Cor da borda
        self.background_frame.pack(fill="both", expand=True, padx=1, pady=1)  # Adiciona uma borda fina

        # Cria um frame de conteúdo com uma cor de fundo
        self.content_frame = tkinter.Frame(self.background_frame, bg="#1d1f21")  # Cor de fundo
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)  # Preenche toda a janela

        # Cria um layout de grade
        self.content_frame.columnconfigure(0, weight=1)  # Expande horizontalmente
        self.content_frame.rowconfigure(1, weight=1)  # Expande verticalmente
        
        # Cria um rótulo e uma entrada de texto
        self.label = customtkinter.CTkLabel(  # Cria um rótulo personalizado
            self.content_frame, text="\u00AF\\_(\u30C4)_/\u00AF", font=("Arial", 16), text_color="white"
        )
        self.label.grid(row=0, column=0, pady=(10, 5), sticky="nsew")  # Posiciona o rótulo na grade

        self.entry = customtkinter.CTkEntry(  # Cria uma entrada de texto personalizada
            self.content_frame, placeholder_text="Digite o comando...", fg_color="#282a2e", text_color="white"
        )
        self.entry.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")  # Posiciona a entrada de texto na grade
        self.entry.bind("<Return>", self.check_exit)  # Associa o evento de pressionar a tecla Enter à função check_exit

        self.visible = False  # Inicializa a variável visible como False

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_window(self):
        if self.visible:
            self.hide_window()
        else:
            self.show_window()

    def show_window(self):
        self.center_window()
        self.root.deiconify()
        self.visible = True

    def hide_window(self):
        self.root.withdraw()
        self.visible = False

    def check_exit(self, event):
        if self.entry.get().strip().lower() == "exit":
            self.cleanup()

    def cleanup(self):
        self.root.destroy()
        icon.stop()

# Cria um ícone na bandeja do sistema

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
        fill=color2
    )
    return image

def on_exit():
    app.cleanup()

def tray_thread():
    global icon
    icon = pystray.Icon(
        "App", 
        create_image(64, 64, "purple", "green"), 
        menu=pystray.Menu(
            pystray.MenuItem("Exit", lambda: on_exit())
        )
    )
    icon.run()

if __name__ == "__main__":
    # Inicializa o aplicativo
    app = AlwaysOnTopApp()

    # Inicia o ícone da bandeja do sistema em uma thread separada
    tray = threading.Thread(target=tray_thread, daemon=True)
    tray.start()

    # Configura a tecla de atalho para alternar a visibilidade da janela
    keyboard.add_hotkey("ctrl+capslock", app.toggle_window)

    # Executa o mainloop
    app.root.mainloop()
