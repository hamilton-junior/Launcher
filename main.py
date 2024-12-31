import os  # Importa a biblioteca os para interações com o sistema operacional
import logging  # Importa a biblioteca logging para logs apropriados
import threading  # Importa a biblioteca threading para trabalhar com threads
import webbrowser  # Importa a biblioteca webbrowser para abrir links no navegador

import tkinter  # Importa a biblioteca tkinter para criar interfaces gráficas
import customtkinter  # Importa a biblioteca customtkinter para widgets personalizados
import keyboard  # Importa a biblioteca keyboard para capturar eventos de teclado
import pystray  # Importa a biblioteca pystray para criar ícones na bandeja do sistema
from PIL import Image, ImageDraw  # Importa a biblioteca PIL para manipulação de imagens

# Configura o logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(name)s/%(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho para o arquivo de tema
theme_path = os.path.join(script_dir, "assets", "theme.json")

# Define o tema padrão do customtkinter usando o caminho do arquivo de tema
customtkinter.set_default_color_theme(theme_path)  # Temas: "blue" (padrão), "green", "dark-blue", "sweetkind"

# Define o diretório de comandos e ícones
commands_dir = os.path.join(script_dir, "commands")
icon_path = os.path.join(script_dir, "assets/icons", "icon.png")
tray_icon_path = os.path.join(script_dir, "assets/icons", "trayicon.png")

# Define a geometria padrão da janela, para ser usada ao redefinir a janela
defaultWidth = 240
defaultHeight = 100
defaultGeometry = f"{defaultWidth}x{defaultHeight}" #Define a geometria padrão da janela em uma única variável, para facilitar o uso do tamanho final

class AlwaysOnTopApp:
    """
    Classe para criar uma aplicação que permanece sempre no topo.
    """
    def __init__(self):
        """
        Inicializa a aplicação, configurando a janela principal e a interface.
        """
        try:
            logging.info("Inicializando a aplicação...")
            self.root = customtkinter.CTk()
            self.root.geometry(defaultGeometry)
            self.root.title("Launcher")
            self.root.attributes('-topmost', True)
            self.root.overrideredirect(True)
            self.root.iconphoto(False, tkinter.PhotoImage(file=icon_path))
            self.center_window()
            self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

            self.setup_interface()

            self.visible = False

            self.commands = {
                "dir": self.open_script_dir
            }
            self.hideWindowAfterCommand = True
            self.entry_count = 0  # Initialize entry count
        except Exception as e:
            self.show_error(f"Erro ao inicializar a aplicação: {e}")

    def center_window(self):
        """
        Centraliza a janela na tela.
        """
        try:
            logging.info("Centralizando a janela...")
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
        except Exception as e:
            self.show_error(f"Erro ao centralizar a janela: {e}")

    def setup_interface(self):
        """
        Configura a interface inicial da aplicação.
        """
        try:
            logging.info("Configurando a interface...")
            for widget in self.root.winfo_children():
                widget.destroy()

            self.background_frame = tkinter.Frame(self.root, bg="#646464")
            self.background_frame.pack(fill="both", expand=True, padx=1, pady=1)

            self.content_frame = tkinter.Frame(self.background_frame, bg="#1d1f21")
            self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

            self.content_frame.columnconfigure(0, weight=1)
            self.content_frame.rowconfigure(1, weight=1)

            self.label = customtkinter.CTkLabel(
                self.content_frame, text="\u00AF\\_(\u30C4)_/\u00AF", font=("Arial", 16), text_color="white"
            )
            self.label.grid(row=0, column=0, pady=(10, 5), sticky="ew")

            self.entry_frame = tkinter.Frame(self.content_frame, bg="#1d1f21", height=defaultHeight)
            self.entry_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
            self.entry_frame.columnconfigure(0, weight=1)

            self.entry = customtkinter.CTkEntry(
                self.entry_frame, placeholder_text="Digite o comando...", fg_color="#282a2e", text_color="white"
            )
            self.entry.grid(row=0, column=0, sticky="nsew")
            self.entry.bind("<Return>", self.check_exit)
            self.entry.focus_set()

            self.entry_count = 0  # Initialize/Reset entry count

            self.root.update_idletasks()
            self.root.geometry(f"{defaultWidth}x{defaultHeight}")
        except Exception as e:
            self.show_error(f"Erro ao configurar a interface: {e}")

    def toggle_window(self):
        """
        Alterna a visibilidade da janela.
        """
        try:
            logging.info("Alternando a visibilidade da janela...")
            if self.visible:
                self.hide_window()
            else:
                self.show_window()
        except Exception as e:
            self.show_error(f"Erro ao alternar a visibilidade da janela: {e}")

    def show_window(self):
        """
        Mostra a janela e a centraliza na tela.
        """
        try:
            logging.info("Mostrando a janela...")
            self.center_window()
            self.root.deiconify()
            self.visible = True
            self.entry.focus_force()
        except Exception as e:
            self.show_error(f"Erro ao mostrar a janela: {e}")

    def hide_window(self):
        """
        Oculta a janela.
        """
        try:
            logging.info("Escondendo a janela...")
            self.root.withdraw()
            self.visible = False
        except Exception as e:
            self.show_error(f"Erro ao esconder a janela: {e}")

    def check_exit(self, event):
        """
        Verifica o comando de saída e executa a ação correspondente.
        """
        try:
            command = self.entry.get().strip().lower()
            logging.info(f"Comando recebido: {command}")
            if command == "exit":
                self.cleanup()
            elif command == "?":
                self.show_commands_tooltip()
                self.entry.delete(0, 'end')
                self.reset_input_placeholder("Digite o comando...", color="lime")
            else:
                if self.execute_command(command):
                    self.entry.delete(0, 'end')
                    self.entry.configure(placeholder_text="Digite o comando...")
                    logging.info(f"hideWindowAfterCommand in check_exit: {self.hideWindowAfterCommand}")
                    if self.hideWindowAfterCommand:
                        self.hide_window()
                    self.hideWindowAfterCommand = True
        except Exception as e:
            self.show_error(f"Erro ao verificar o comando de saída: {e}")

    def open_link_with_value(self, value, base_url):
        """
        Abre um link no navegador substituindo um valor na URL base.
        """
        try:
            logging.info(f"Abrindo link com valor: {value}")
            url = base_url.replace("REPLACEME", value)
            webbrowser.open(url)
        except Exception as e:
            self.show_error(f"Erro ao abrir o link: {e}")

    def execute_command(self, command):
        """
        Executa o comando especificado.
        """
        try:
            logging.info(f"Initial hideWindowAfterCommand: {self.hideWindowAfterCommand}")

            if command in self.commands:
                logging.info(f"Executando comando interno: {command}")
                self.commands[command]()
                self.hideWindowAfterCommand = True
                return True
            elif command == "in":
                logging.info("Criando nova entrada para comando 'in'")
                self.create_new_entry(
                    "CNPJ",
                    labelColor="cyan",
                    command=lambda value: self.open_link_with_value_and_reset(
                        value,
                        "https://intranet.lzt.com.br/cliente/pesquisar/REPLACEME"
                    )
                )
                self.adjust_window_size()
                self.hideWindowAfterCommand = False
                self.root.update_idletasks()
                return True
            else:
                accepted_extensions = ["py", "txt"]
                command_file = None
                for ext in accepted_extensions:
                    potential_file = os.path.join(commands_dir, f"{command}.{ext}")
                    logging.info(f"Checking for file: {potential_file}")
                    if os.path.isfile(potential_file):
                        command_file = potential_file
                        break

                if command_file:
                    try:
                        logging.info(f"Executando arquivo de comando: {command_file}")
                        with open(command_file, "r", encoding="utf-8") as file:
                            exec(file.read().encode().decode('utf-8'))
                        logging.info(f"hideWindowAfterCommand after exec: {self.hideWindowAfterCommand}")
                        self.setup_interface()
                        return True
                    except Exception as e:
                        self.show_error(f"Erro ao executar comando '{command}': {e}")
                        return False
                else:
                    self.reset_input_placeholder(f"Comando '{command}' não encontrado")
                    return False
        except Exception as e:
            self.show_error(f"Erro ao executar o comando: {e}")
            return False

    def reset_input_placeholder(self, message, color="red"):
        """
        Reseta o placeholder do campo de entrada com uma mensagem.
        """
        try:
            logging.info(f"Resetando placeholder do campo de entrada: {message}")
            self.entry.delete(0, 'end')
            self.entry.configure(placeholder_text=message, placeholder_text_color=color)
            self.entry.bind("<Key>", self.reset_input_handler, add="+")
        except Exception as e:
            self.show_error(f"Erro ao resetar o placeholder: {e}")

    def reset_input_handler(self, event):
        """
        Manipulador para resetar o campo de entrada.
        """
        try:
            logging.info("Resetando campo de entrada...")
            self.setup_interface()
            self.entry.insert(0, event.char)
        except Exception as e:
            self.show_error(f"Erro ao resetar o campo de entrada: {e}")

    def show_error(self, message):
        """
        Mostra uma mensagem de erro em uma nova janela.
        """
        try:
            logging.error(message)
            error_window = customtkinter.CTkToplevel(self.root)
            error_window.title("Error")
            error_window.geometry((f"{width}x{height}"))
            error_window.attributes('-topmost', True)
            error_label = customtkinter.CTkLabel(error_window, text=message, text_color="red")
            error_label.pack(pady=20)
            error_button = customtkinter.CTkButton(error_window, text="OK", command=error_window.destroy)
            error_button.pack(pady=10)
            self.root.update_idletasks()
        except Exception as e:
            logging.error(f"Erro ao mostrar a mensagem de erro: {e}")

    def open_link(self, url="https://www.google.com"):
        """
        Abre o link especificado no navegador padrão.
        """
        try:
            logging.info(f"Abrindo link: {url}")
            webbrowser.open(url)
        except Exception as e:
            self.show_error(f"Erro ao abrir o link: {e}")

    def open_link_with_value_and_reset(self, value, base_url):
        """
        Abre um link no navegador substituindo um valor na URL base e reseta a interface.
        """
        try:
            logging.info(f"Abrindo link com valor e resetando: {value}")
            self.open_link_with_value(value, base_url)
            self.setup_interface()
            self.root.geometry(defaultGeometry)
            self.center_window()
            if self.hideWindowAfterCommand:
                self.hide_window()
        except Exception as e:
            self.show_error(f"Erro ao abrir o link e resetar a interface: {e}")

    def open_file(self, file_path=script_dir):
        """
        Abre o arquivo especificado.
        """
        try:
            logging.info(f"Abrindo arquivo: {file_path}")
            os.startfile(file_path)
        except Exception as e:
            self.show_error(f"Erro ao abrir o arquivo: {e}")

    def create_new_entry(self, labelText, labelColor="white", command=None):
        """
        Cria uma nova entrada com um rótulo especificado.
        """
        try:
            logging.info(f"Criando nova entrada: {labelText}")
            # Create a new label for the entry
            new_label = customtkinter.CTkLabel(
                self.entry_frame, text=labelText, font=("Arial", 16), text_color=labelColor
            )
            new_label.grid(row=self.entry_count * 2 + 1, column=0, pady=(10, 5), sticky="ew")

            # Create a new entry field
            new_entry = customtkinter.CTkEntry(
                self.entry_frame, placeholder_text="Digite o valor...", fg_color="#282a2e", text_color="white"
            )
            if command:
                new_entry.bind("<Return>", lambda Event: command(new_entry.get().strip()))
            else:
                new_entry.bind("<Return>", self.check_exit)
            new_entry.grid(row=self.entry_count * 2 + 2, column=0, padx=10, pady=(5, 10), sticky="ew")

            self.entry_count += 1  # Increment entry count
            self.adjust_window_size()
            self.entry_frame.rowconfigure(self.entry_count * 2 + 2, weight=1)  # Ensure new row is configured
            self.root.update_idletasks()
            new_entry.focus_force()
        except Exception as e:
            self.show_error(f"Erro ao criar nova entrada: {e}")

    def adjust_window_size(self):
        """
        Ajusta o tamanho da janela para garantir que todos os campos estejam visíveis.
        """
        try:
            logging.info("Ajustando tamanho da janela...")
            self.root.update_idletasks()
            width = defaultWidth
            height = defaultHeight + (self.entry_count * 70)  # Adjust height based on entry count
            self.root.geometry(f"{width}x{height}")
        except Exception as e:
            self.show_error(f"Erro ao ajustar o tamanho da janela: {e}")

    def open_script_dir(self):
        """
        Abre o diretório do script.
        """
        try:
            logging.info("Abrindo diretório do script...")
            os.startfile(script_dir)
        except Exception as e:
            self.show_error(f"Erro ao abrir o diretório do script: {e}")

    def cleanup(self):
        """
        Limpa e encerra a aplicação.
        """
        try:
            logging.info("Limpando e encerrando a aplicação...")
            self.root.destroy()
            icon.stop()
        except Exception as e:
            logging.error(f"Erro ao limpar a aplicação: {e}")

    def list_commands(self):
        """
        Lista os comandos disponíveis no diretório de comandos.
        """
        try:
            logging.info("Listando comandos disponíveis...")
            commands_list = []
            for file in os.listdir(commands_dir):
                if file.endswith(".py") or file.endswith(".txt"):
                    command_name = file.split('.')[0]
                    docstring = self.get_command_docstring(os.path.join(commands_dir, file))
                    commands_list.append(f"{command_name} - {docstring}")
            return commands_list
        except Exception as e:
            self.show_error(f"Erro ao listar comandos: {e}")
            return []

    def get_command_docstring(self, file_path):
        """
        Extrai a docstring do arquivo de comando especificado.
        """
        try:
            logging.info(f"Obtendo docstring do comando: {file_path}")
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                docstring_started = False
                docstring = ""
                for line in lines:
                    if '"""' in line:
                        if docstring_started:
                            docstring += line.split('"""')[0].strip()
                            break
                        else:
                            docstring_started = True
                            docstring = line.split('"""')[1].strip()
                    elif docstring_started:
                        docstring += " " + line.strip()
                return docstring if docstring else "Sem descrição"
        except Exception as e:
            self.show_error(f"Erro ao obter a docstring: {e}")
            return "Erro ao obter descrição"

    def show_commands_tooltip(self):
        """
        Mostra um tooltip com a lista de comandos disponíveis.
        """
        try:
            logging.info("Mostrando tooltip de comandos disponíveis...")
            commands = self.list_commands()
            tooltip_text = "Comandos disponíveis:\n\n" + "\n".join(commands)
            self.show_windows_tooltip(tooltip_text)
        except Exception as e:
            self.show_error(f"Erro ao mostrar comandos: {e}")

    def show_windows_tooltip(self, text):
        """
        Mostra um tooltip na janela.
        """
        try:
            logging.info("Mostrando tooltip na janela...")
            self.tooltip = tkinter.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.geometry(f"+0+0")
            label = tkinter.Label(self.tooltip, text=text, justify='left', background="#ffffe0", relief='solid', borderwidth=1)
            label.pack(ipadx=1)
            self.entry.bind("<Key>", self.hide_tooltip, add="+")
        except Exception as e:
            self.show_error(f"Erro ao mostrar tooltip: {e}")

    def hide_tooltip(self, event):
        """
        Esconde o tooltip.
        """
        try:
            logging.info("Escondendo tooltip...")
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                del self.tooltip
        except Exception as e:
            self.show_error(f"Erro ao esconder tooltip: {e}")

def create_image(width, height, color1, color2):
    """
    Cria uma imagem para o ícone da bandeja do sistema. (fallback)
    """
    try:
        logging.info("Criando imagem para ícone da bandeja...")
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
            fill=color2
        )
        return image
    except Exception as e:
        logging.error(f"Erro ao criar a imagem: {e}")

def on_exit():
    """
    Função chamada ao sair da aplicação.
    """
    try:
        logging.info("Saindo da aplicação...")
        if 'app' in globals():
            app.cleanup()
    except Exception as e:
        logging.error(f"Erro ao sair da aplicação: {e}")

def tray_thread():
    """
    Thread para criar o ícone da bandeja do sistema.
    """
    try:
        logging.info("Iniciando thread da bandeja do sistema...")
        global icon
        icon_image = Image.open(tray_icon_path)
        icon = pystray.Icon(
            "App", 
            icon_image, 
            menu=pystray.Menu(
                pystray.MenuItem("Exit", lambda: on_exit())
            )   
        )
        icon.run()
    except Exception as e:
        logging.error(f"Erro ao iniciar a thread da bandeja: {e}")

if __name__ == "__main__":
    # Inicializa a aplicação e configura o ícone da bandeja do sistema.
    try:
        logging.info("Iniciando a aplicação...")
        app = AlwaysOnTopApp()

        tray = threading.Thread(target=tray_thread, daemon=True)
        tray.start()

        keyboard.add_hotkey("ctrl+capslock", app.toggle_window)

        app.root.mainloop()
    except Exception as e:
        logging.error(f"Erro ao iniciar a aplicação: {e}")