import os  # Importa a biblioteca os para interações com o sistema operacional
import logging  # Importa a biblioteca logging para logs apropriados
import threading  # Importa a biblioteca threading para trabalhar com threads
import webbrowser  # Importa a biblioteca webbrowser para abrir links no navegador
import sys # Importa a biblioteca sys para obter informações sobre o sistema

import tkinter  # Importa a biblioteca tkinter para criar interfaces gráficas
import customtkinter  # Importa a biblioteca customtkinter para widgets personalizados
from customtkinter.windows.ctk_toplevel import ThemeManager  # Importado para gerenciar temas de cores
import keyboard  # Importa a biblioteca keyboard para capturar eventos de teclado
import pystray  # Importa a biblioteca pystray para criar ícones na bandeja do sistema
from PIL import Image, ImageDraw  # Importa a biblioteca PIL para manipulação de imagens

# Obtém o diretório do script atual ou o diretório temporário do PyInstaller
if getattr(sys, 'frozen', False):
    script_dir = sys._MEIPASS
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho para o arquivo de tema
theme_path = os.path.join(script_dir, "assets", "theme.json")

# Constrói o caminho para o arquivo de tema
theme_dir = os.path.join(script_dir, "assets", "themes")

# Define o tema padrão do customtkinter usando o caminho do arquivo de tema
customtkinter.set_default_color_theme(theme_path)  # Temas: "blue" (padrão), "green", "dark-blue", ("sweetkind?"")

# Constrói o caminho para o diretório de logs
log_dir = os.path.join(script_dir, "log")

# Cria o diretório de logs se não existir
os.makedirs(log_dir, exist_ok=True)

# Configura o logger
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - [%(levelname)s] %(filename)s:%(lineno)d (%(name)s/%(funcName)s) --> %(message)s',
    datefmt='%Y-%m-%d @ %H:%M:%S',
    handlers=[
        logging.FileHandler(f"{log_dir}/main.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

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
    def show_error(self, message):
        """
        Mostra uma mensagem de erro em uma nova janela.
        """
        try:
            logging.error(message)
            error_window = customtkinter.CTkToplevel(self.root)
            error_window.title("Error")
            error_window.geometry((f"{defaultWidth}x{defaultHeight}"))
            error_window.attributes('-topmost', True)
            error_label = customtkinter.CTkLabel(error_window, text=message, text_color="red")
            error_label.pack(pady=20)
            error_button = customtkinter.CTkButton(error_window, text="OK", command=error_window.destroy)
            error_button.pack(pady=10)
            self.root.update_idletasks()
        except Exception as e:
            logging.error(f"Erro ao mostrar a mensagem de erro: {e}")
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

            self.visible = True
            logging.debug(f"Estado inicial de visible: {self.visible}")

            self.commands = {
                "dir": self.open_script_dir
            }
            self.hideWindowAfterCommand = True
            logging.debug(f"Estado inicial de hideWindowAfterCommand: {self.hideWindowAfterCommand}")
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
            logging.debug("Configurando a interface...")
            for widget in self.root.winfo_children():
                widget.destroy()

            self.background_frame = customtkinter.CTkFrame(self.root)#, bg="#646464")
            self.background_frame.pack(fill="both", expand=True, padx=1, pady=1)

            self.content_frame = customtkinter.CTkFrame(self.background_frame)#, bg="#1d1f21")
            self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

            self.content_frame.columnconfigure(0, weight=1)
            self.content_frame.rowconfigure(1, weight=1)

            self.label = customtkinter.CTkLabel(
                self.content_frame,
                text="\u00AF\\_(\u30C4)_/\u00AF",
                font=("Arial", 16)#,
                #text_color="white"
            )
            #if 
            self.label.grid(row=0, column=0, pady=(10, 5), sticky="ew")

            self.entry_frame = customtkinter.CTkFrame(self.content_frame, height=defaultHeight)#, bg="#1d1f21")
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
            logging.debug("Alternando a visibilidade da janela...")
            if self.visible:
                self.hide_window()
            else:
                self.show_window()
            logging.debug(f"Estado de visible alternado: {self.visible}")
        except Exception as e:
            self.show_error(f"Erro ao alternar a visibilidade da janela: {e}")

    def show_window(self):
        """
        Mostra a janela e a centraliza na tela.
        """
        try:
            logging.debug("Mostrando a janela...")
            self.center_window()
            self.root.deiconify()
            self.visible = True
            logging.debug(f"Mostrar janela, estado de visible: {self.visible}")
            self.entry.focus_force()
        except Exception as e:
            self.show_error(f"Erro ao mostrar a janela: {e}")

    def hide_window(self):
        """
        Oculta a janela.
        """
        try:
            logging.debug("Escondendo a janela...")
            self.root.withdraw()
            self.visible = False
            logging.debug(f"Esconder janela, estado de visible: {self.visible}")
        except Exception as e:
            self.show_error(f"Erro ao esconder a janela: {e}")

    def check_exit(self, event):
        """
        Verifica o comando de saída e executa a ação correspondente.
        """
        try:
            command = self.entry.get().strip().lower()
            logging.debug(f"Comando recebido: {command}")
            if command == "exit":
                self.cleanup()
            elif command == "?":
                self.show_commands_tooltip_handler()
                self.entry.delete(0, 'end')
                self.reset_input_placeholder("Digite o comando...", color="lime")
            else:
                if self.execute_command(command):
                    self.entry.delete(0, 'end')
                    self.entry.configure(placeholder_text="Digite o comando...")
                    logging.debug(f"hideWindowAfterCommand em check_exit: {self.hideWindowAfterCommand}")
                    if self.hideWindowAfterCommand:
                        self.hide_window()
                    self.hideWindowAfterCommand = True
        except Exception as e:
            self.show_error(f"Erro ao verificar o comando de saída: {e}")

    def open_link_with_value(self, base_url, value):
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
            logging.debug(f"Estado inicial de hideWindowAfterCommand: {self.hideWindowAfterCommand}")

            if command in self.commands:
                logging.info(f"Executando comando interno: {command}")
                self.commands[command]()
                self.hideWindowAfterCommand = True
                logging.debug(f"Definir estado de hideWindowAfterCommand: {self.hideWindowAfterCommand}")
                return True
            elif command == "in":
                logging.info("Criando nova entrada para comando 'in'")
                self.create_new_entry(
                    "CNPJ",
                    "cyan",
                    lambda value: self.open_link_with_value_and_reset(
                        "https://intranet.lzt.com.br/cliente/pesquisar/REPLACEME",
                        value
                    )
                )
            elif command in {"tema", "temas", "theme", "themes"}:
                self.criar_interface_escolha_tema()
                
                self.adjust_window_size()
                self.hideWindowAfterCommand = False
                logging.debug(f"Definir estado de hideWindowAfterCommand: {self.hideWindowAfterCommand}")
                self.root.update_idletasks()
                return True
            else:
                accepted_extensions = ["py", "txt"]
                command_file = None
                for ext in accepted_extensions:
                    potential_file = os.path.join(commands_dir, f"{command}.{ext}")
                    logging.debug(f"Verificando arquivo: {potential_file}")
                    if os.path.isfile(potential_file):
                        command_file = potential_file
                        break

                if command_file:
                    try:
                        logging.debug(f"Executando arquivo de comando: {command_file}")
                        with open(command_file, "r", encoding="utf-8") as file:
                            exec(file.read().encode().decode('utf-8'))
                        logging.debug(f"hideWindowAfterCommand após exec: {self.hideWindowAfterCommand}")
                        self.setup_interface()
                        return True
                    except Exception as e:
                        self.show_error(f"Erro ao executar comando '{command}': {e}")
                        return False
                else:
                    self.reset_input_placeholder(f"Comando '{command}' não encontrado", "red")
                    return False
        except Exception as e:
            self.show_error(f"Erro ao executar o comando: {e}")
            return False

    def criar_interface_escolha_tema(self):
        """
        Constrói a interface para escolha de tema e mantém a janela ancorada à janela principal.
        """
        try:
            logging.info("Construindo interface de escolha de tema...")

            # Verifica se a janela já existe e está aberta
            if hasattr(self, 'escolha_tema_main_window') and self.escolha_tema_main_window.winfo_exists():
                logging.warning("A janela de escolha de tema já está aberta.")
                return

            # Criação da nova janela
            self.escolha_tema_main_window = customtkinter.CTkToplevel(self.root)
            self.escolha_tema_main_window.overrideredirect(True)
            self.escolha_tema_main_window.title("Escolha de Tema")

            # Frame para os elementos da interface
            escolha_tema_frame = customtkinter.CTkFrame(self.escolha_tema_main_window)
            escolha_tema_frame.pack(fill="both", expand=True, padx=1, pady=1)

            # Adiciona widgets na janela de escolha de temas
            temas_padroes_label = customtkinter.CTkLabel(
                escolha_tema_frame, text="Temas Padrões:", font=("Arial", 12)
            )
            temas_padroes_label.pack(pady=(5, 0))

            # Botão de Tema Padrão
            bt_tema_padrao = customtkinter.CTkButton(
                escolha_tema_frame,
                text="Padrão",
                command=lambda: self.aplicar_novo_tema("theme")
            )
            bt_tema_padrao.pack(pady=(10, 10), padx=(10, 10))

            # Botões de escolha de temas padrões
            temas_padroes = ["Blue", "Dark-Blue", "Green"]
            for tema_padrao in temas_padroes:
                bt_temas_padrao = customtkinter.CTkButton(
                    escolha_tema_frame,
                    text=tema_padrao,
                    command=lambda t=tema_padrao: self.aplicar_novo_tema(t.lower())
                )
                bt_temas_padrao.pack(pady=(0, 5))

            # Verifica e adiciona temas personalizados, se disponíveis
            temas_disponiveis = self.get_available_themes()
            if temas_disponiveis:
                temas_personalizados_label = customtkinter.CTkLabel(
                    escolha_tema_frame, text="Temas Personalizados:", font=("Arial", 12)
                )
                temas_personalizados_label.pack(pady=(15, 5))

                for theme in temas_disponiveis:
                    theme_button = customtkinter.CTkButton(
                        escolha_tema_frame,
                        text=theme.title(),
                        command=lambda t=theme: self.aplicar_novo_tema(t)
                    )
                    theme_button.pack(pady=(0, 5))
            else:
                no_themes_label = customtkinter.CTkLabel(
                    escolha_tema_frame, text="Nenhum tema personalizado disponível."
                )
                no_themes_label.pack(pady=(15, 5))

            # Botão para fechar a janela
            botao_sair_tema = customtkinter.CTkButton(
                escolha_tema_frame,
                text="Fechar",
                command=self.fechar_escolha_tema
            )
            botao_sair_tema.pack(pady=(20, 10))

            # Inicia o processo de ancoragem
            self.ancorar_janela_tema()
            
            self.reset_input_placeholder()

        except Exception as e:
            self.show_error(f"Erro ao construir a interface de escolha de tema: {e}")



    def ancorar_janela_tema(self):
        """
        Mantém a janela de escolha de temas ancorada à janela principal.
        """
        try:
            # Verifica se a janela de escolha de temas ainda existe
            if hasattr(self, 'escolha_tema_main_window') and self.escolha_tema_main_window.winfo_exists():
                # Obtém a posição da janela principal
                x = self.root.winfo_x() - self.root.winfo_width() + 75 # Deslocamento horizontal
                y = self.root.winfo_y()  # Mesma posição vertical
                self.escolha_tema_main_window.geometry(f"+{x}+{y}")

                # Continua atualizando
                self.root.after(100, self.ancorar_janela_tema)
        except Exception as e:
            self.show_error(f"Erro ao ancorar janela de escolha de temas: {e}")

            
    def fechar_escolha_tema(self):
        """
        Fecha a janela de escolha de tema.
        """
        try:
            if hasattr(self, 'escolha_tema_main_window') and self.escolha_tema_main_window.winfo_exists():
                self.escolha_tema_main_window.destroy()
                del self.escolha_tema_main_window
        except Exception as e:
            self.show_error(f"Erro ao fechar a janela de escolha de temas: {e}")



    def get_tema_atual(self):
        """
        Retorna o valor do tema atual.
        """
        tema_atual = ThemeManager._currently_loaded_theme
        return tema_atual            
            
    def get_available_themes(self):
        """
        Retorna a lista de temas disponíveis.
        """
        try:
            logging.debug("Obtendo temas disponíveis...")
            themes = []
            for file in os.listdir(theme_dir):
                if file.endswith(".json"):
                    themes.append(file.split('.')[0])
                    
            return themes
        except Exception as e:
            logging.error(f"Erro ao obter temas disponíveis: {e}")
            self.show_error(f"Erro ao obter temas disponíveis: {e}")
            return []

    def aplicar_novo_tema(self, tema):
        """
        Aplica um novo tema à aplicação.
        """
        try:
            
            self.tema_atual = tema
            logging.debug(f"Aplicando novo tema: {tema}")
            if tema == "theme":
                customtkinter.set_default_color_theme(theme_path)
            elif tema in {"blue", "green", "dark-blue"}:
                customtkinter.set_default_color_theme(tema)
            else:
                customtkinter.set_default_color_theme(f"{theme_dir}/{tema}.json")
                
            self.root.update_idletasks()
            
            self.setup_interface()
            self.criar_interface_escolha_tema()

            logging.debug(f"Tema atual: {ThemeManager._currently_loaded_theme}")
        except Exception as e:
            self.show_error(f"Erro ao aplicar o novo tema: {e}")

    def reset_input_placeholder(self, message="", color=None):
        """
        Reseta o placeholder do campo de entrada com uma mensagem.
        """
        try:
            logging.debug(f"Resetando placeholder do campo de entrada: {message}")
            self.entry.delete(0, 'end')
            if color in {""," ","reset",None}: 
                self.entry.configure(placeholder_text=message)
            else:
                self.entry.configure(placeholder_text=message, placeholder_text_color=color)
            self.entry.bind("<Key>", self.reset_input_handler, add="+")
        except Exception as e:
            self.show_error(f"Erro ao resetar o placeholder: {e}")

    def reset_input_handler(self, event):
        """
        Manipulador para resetar o campo de entrada.
        """
        try:
            logging.debug("Resetando campo de entrada...")
            self.setup_interface()
            self.entry.insert(0, event.char)
        except Exception as e:
            self.show_error(f"Erro ao resetar o campo de entrada: {e}")



    def open_link(self, url="https://www.google.com"):
        """
        Abre o link especificado no navegador padrão.
        """
        try:
            logging.info(f"Abrindo link: {url}")
            webbrowser.open(url)
        except Exception as e:
            self.show_error(f"Erro ao abrir o link: {e}")

    def open_link_with_value_and_reset(self, base_url, value):
        """
        Abre um link no navegador substituindo um valor na URL base e reseta a interface.
        """
        try:
            logging.info(f"Abrindo link com valor e resetando: {value}")
            self.open_link_with_value(base_url, value)
            self.setup_interface()
            self.root.geometry(defaultGeometry)
            self.center_window()
            if self.hideWindowAfterCommand:
                self.hide_window()
            logging.debug(f"hideWindowAfterCommand em open_link_with_value_and_reset: {self.hideWindowAfterCommand}")
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
                self.entry_frame,
                placeholder_text="Digite o valor...",
                fg_color="#282a2e"
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
            logging.debug("Ajustando tamanho da janela...")
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
            icon.visible = False
            icon.stop()
            logging.debug(f"Limpeza da aplicação, estado de visible: {self.visible}")
        except Exception as e:
            logging.error(f"Erro ao limpar a aplicação: {e}")

    def list_commands(self):
        """
        Lista os comandos disponíveis no diretório de comandos.
        """
        try:
            logging.debug("Listando comandos disponíveis...")
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
            logging.debug(f"Obtendo docstring do comando: {file_path}")
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
                return docstring if docstring else "[Sem descrição]"
        except Exception as e:
            logging.error(f"Erro ao obter a docstring dos comandos: {e}")
            self.show_error(f"Erro ao obter a docstring: {e}")
            return "Erro ao obter descrição"

    def show_commands_tooltip_handler(self):
        """
        Mostra um tooltip com a lista de comandos disponíveis.
        """
        try:
            logging.info("Mostrando tooltip de comandos disponíveis...")
            commands = self.list_commands()
            tooltip_text = "Comandos disponíveis:\n\n" + "\n".join(commands)
            self.show_windows_tooltip(tooltip_text)
            self.entry.bind("<Key>", self.hide_tooltip, add="+")
            logging.debug(f"Estado de visibilidade do tooltip: {hasattr(self, 'tooltip')}")
        except Exception as e:
            self.show_error(f"Erro ao mostrar comandos: {e}")

    def show_windows_tooltip(self, text):
        """
        Mostra um tooltip na janela.
        """
        try:
            #logging.info("Mostrando tooltip na janela...")
            self.tooltip = customtkinter.CTkToplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.geometry(f"+0+0")
            label = customtkinter.CTkLabel(self.tooltip, text=text, justify='left')
            label.pack(ipadx=1)
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
            logging.debug(f"Estado de visibilidade do tooltip: {hasattr(self, 'tooltip')}")
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