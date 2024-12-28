import tkinter  # Importa a biblioteca tkinter para criar interfaces gráficas
import threading  # Importa a biblioteca threading para trabalhar com threads
import customtkinter  # Importa a biblioteca customtkinter para widgets personalizados
import keyboard  # Importa a biblioteca keyboard para capturar eventos de teclado
import pystray  # Importa a biblioteca pystray para criar ícones na bandeja do sistema
from PIL import Image, ImageDraw  # Importa a biblioteca PIL para manipulação de imagens
import os  # Importa a biblioteca os para interações com o sistema operacional
import webbrowser  # Importa a biblioteca webbrowser para abrir links no navegador

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho para o arquivo de tema
theme_path = os.path.join(script_dir, "data", "theme.json")

# Define o tema padrão do customtkinter usando o caminho do arquivo de tema
customtkinter.set_default_color_theme(theme_path)  # Temas: "blue" (padrão), "green", "dark-blue", "sweetkind"

# Define o diretório de comandos e ícones
commands_dir = os.path.join(script_dir, "commands")
icon_path = os.path.join(script_dir, "data", "icon.png")
tray_icon_path = os.path.join(script_dir, "data", "trayicon.png")

# Define a geometria padrão da janela, para ser usada ao redefinir a janela
defaultGeometry = "240x100"

class AlwaysOnTopApp:  # Define a classe AlwaysOnTopApp
    def __init__(self):  # Define o método inicializador __init__
        try:
            self.root = customtkinter.CTk()  # Cria uma janela customtkinter
            self.root.geometry(defaultGeometry)  # Define o tamanho inicial da janela
            self.root.title("Launcher")  # Define o título da janela
            self.root.attributes('-topmost', True)  # Mantém a janela sempre no topo de outras janelas
            self.root.overrideredirect(True)  # Remove as decorações da janela (barra de tarefas e botão de fechar)
            self.root.iconphoto(False, tkinter.PhotoImage(file=icon_path))  # Define o ícone da janela
            self.center_window()  # Centraliza a janela na tela
            self.root.protocol("WM_DELETE_WINDOW", self.hide_window)  # Esconde a janela em vez de fechá-la

            self.setup_interface()  # Configura a interface inicial

            self.visible = False  # Inicializa a variável visible como False

            # Define os comandos padrão disponíveis
            self.commands = {
                "dir": self.open_script_dir  # Adiciona o comando "dir"
            }
            self.hideWindowAfterCommand = True  # Variável de instância para controlar se a janela deve ser escondida após a execução de comandos
        except Exception as e:
            self.show_error(f"Erro ao inicializar a aplicação: {e}")

    def center_window(self):
        try:
            self.root.update_idletasks()  # Atualiza as tarefas pendentes da janela
            width = self.root.winfo_width()  # Obtém a largura da janela
            height = self.root.winfo_height()  # Obtém a altura da janela
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)  # Calcula a posição x para centralizar a janela
            y = (self.root.winfo_screenheight() // 2) - (height // 2)  # Calcula a posição y para centralizar a janela
            self.root.geometry(f"{width}x{height}+{x}+{y}")  # Define a posição da janela
        except Exception as e:
            self.show_error(f"Erro ao centralizar a janela: {e}")

    def setup_interface(self):
        try:
            # Remove widgets existentes
            for widget in self.root.winfo_children():
                widget.destroy()

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
            self.entry.focus_set()  # Define o foco no campo de entrada

            # Ajusta a altura da janela para acomodar os widgets
            self.root.update_idletasks()
            self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")
        except Exception as e:
            self.show_error(f"Erro ao configurar a interface: {e}")

    def toggle_window(self):
        try:
            if self.visible:
                self.hide_window()  # Esconde a janela se estiver visível
            else:
                self.show_window()  # Mostra a janela se estiver oculta
        except Exception as e:
            self.show_error(f"Erro ao alternar a visibilidade da janela: {e}")

    def show_window(self):
        try:
            self.center_window()  # Centraliza a janela
            self.root.deiconify()  # Mostra a janela
            self.visible = True  # Define a variável visible como True
            self.entry.focus_force()  # Define o foco no campo de entrada
        except Exception as e:
            self.show_error(f"Erro ao mostrar a janela: {e}")

    def hide_window(self):
        try:
            self.root.withdraw()  # Oculta a janela
            self.visible = False  # Define a variável visible como False
        except Exception as e:
            self.show_error(f"Erro ao esconder a janela: {e}")

    def check_exit(self, event):
        try:
            command = self.entry.get().strip().lower()  # Obtém o comando digitado e converte para minúsculas
            if command == "exit":
                self.cleanup()  # Encerra o aplicativo se o comando for "exit"
            else:
                if self.execute_command(command):  # Executa o comando e verifica se foi bem-sucedido
                    self.entry.delete(0, 'end')  # Limpa o campo de entrada
                    self.entry.configure(placeholder_text="Digite o comando...")  # Reseta o placeholder para o padrão
                    print(f"hideWindowAfterCommand in check_exit: {self.hideWindowAfterCommand}")  # Depuração
                    if self.hideWindowAfterCommand:
                        self.hide_window()  # Esconde a janela se a variável de instância estiver True
                    self.hideWindowAfterCommand = True  # Reseta a variável para True após a execução do comando
        except Exception as e:
            self.show_error(f"Erro ao verificar o comando de saída: {e}")

    def open_link_with_value(self, value, base_url):
        try:
            url = base_url.replace("REPLACEME", value)
            webbrowser.open(url)
        except Exception as e:
            self.show_error(f"Erro ao abrir o link: {e}")

    def execute_command(self, command):
        try:
            print(f"Initial hideWindowAfterCommand: {self.hideWindowAfterCommand}")  # Depuração

            if command in self.commands:
                self.commands[command]()  # Executa o comando se estiver na lista de comandos
                self.hideWindowAfterCommand = True  # Reseta a variável para True após a execução do comando
                return True
            elif command == "in":
                self.expand_app(labelText="Informe o CNPJ", command=lambda value: self.open_link_with_value_and_reset(value, "http://intranet.lzt.com.br/cliente/pesquisar/REPLACEME"))
                self.hideWindowAfterCommand = True  # Reseta a variável para True após a execução do comando
                return True
            else:
                accepted_extensions = ["py", "txt"]  # Extensões de arquivos aceitas
                command_file = None
                for ext in accepted_extensions:
                    potential_file = os.path.join(commands_dir, f"{command}.{ext}")
                    print(f"Checking for file: {potential_file}")  # Depuração
                    if os.path.isfile(potential_file):
                        command_file = potential_file
                        break

                if command_file:
                    try:
                        with open(command_file, "r", encoding="utf-8") as file:
                            exec(file.read().encode().decode('utf-8'))  # Executa o arquivo de comando
                        print(f"hideWindowAfterCommand after exec: {self.hideWindowAfterCommand}")  # Depuração
                        self.hideWindowAfterCommand = True  # Reseta a variável para True após a execução do comando
                        print(f"hideWindowAfterCommand after exec and set to true: {self.hideWindowAfterCommand}")  # Depuração

                        return True
                    except Exception as e:
                        self.show_error(f"Erro ao executar comando '{command}': {e}")  # Mostra erro se ocorrer
                        return False
                else:
                    self.reset_input_placeholder(f"Comando '{command}' não encontrado")  # Reseta o placeholder se o comando não for encontrado
                    return False
        except Exception as e:
            self.show_error(f"Erro ao executar o comando: {e}")
            return False

    def reset_input_placeholder(self, error_message):
        try:
            self.entry.delete(0, 'end')  # Limpa o campo de entrada
            self.entry.configure(placeholder_text=error_message, placeholder_text_color="red")  # Configura o placeholder com mensagem de erro
            self.entry.bind("<Key>", self.reset_input_handler, add="+")  # Associa o evento de pressionar qualquer tecla à função reset_input_handler
        except Exception as e:
            self.show_error(f"Erro ao resetar o placeholder: {e}")

    def reset_input_handler(self, event):
        try:
            self.setup_interface()  # Reinicia a interface
            self.entry.insert(0, event.char)  # Insere o caractere pressionado
        except Exception as e:
            self.show_error(f"Erro ao resetar o campo de entrada: {e}")

    def show_error(self, message):
        try:
            error_window = customtkinter.CTkToplevel(self.root)  # Cria uma nova janela de erro
            error_window.title("Error")  # Define o título da janela de erro
            error_window.geometry("300x100")  # Define o tamanho da janela de erro
            error_window.attributes('-topmost', True)  # Mantém a janela de erro no topo
            error_label = customtkinter.CTkLabel(error_window, text=message, text_color="red")  # Cria um rótulo de erro
            error_label.pack(pady=20)  # Adiciona o rótulo à janela de erro
            error_button = customtkinter.CTkButton(error_window, text="OK", command=error_window.destroy)  # Cria um botão para fechar a janela de erro
            error_button.pack(pady=10)  # Adiciona o botão à janela de erro
            self.root.update_idletasks()
        except Exception as e:
            print(f"Erro ao mostrar a mensagem de erro: {e}")

    def open_link(self, url="https://www.google.com"):  # Define o link padrão como o Google
        try:
            webbrowser.open(url)  # Abre o link no navegador padrão
        except Exception as e:
            self.show_error(f"Erro ao abrir o link: {e}")

    def open_link_with_value_and_reset(self, value, base_url):
        try:
            self.open_link_with_value(value, base_url)
            self.setup_interface()  # Refaça a interface após abrir o link
            self.root.geometry(defaultGeometry)  # Volta ao tamanho original
            self.center_window()  # Recentraliza a janela
            if self.hideWindowAfterCommand:
                self.hide_window()  # Esconde a janela se a variável de instância estiver True
        except Exception as e:
            self.show_error(f"Erro ao abrir o link e resetar a interface: {e}")

    def open_file(self, file_path=script_dir):  # Define o caminho padrão do arquivo como o diretório atual
        try:
            os.startfile(file_path)  # Abre o arquivo especificado
        except Exception as e:
            self.show_error(f"Erro ao abrir o arquivo: {e}")

    def expand_app(self, labelText="Novo Valor:", command=None):  # Adicione o parâmetro command
        try:
            # Adiciona um novo rótulo
            new_label = customtkinter.CTkLabel(
                self.content_frame, text=labelText, font=("Arial", 16), text_color="white"
            )
            new_label.grid(row=self.content_frame.grid_size()[1], column=0, pady=(10, 5), sticky="nsew")  # Adiciona um novo rótulo

            # Adiciona uma nova entrada de texto
            entry_name = f"new_entry_{labelText.replace(' ', '_').lower()}"
            setattr(self, entry_name, customtkinter.CTkEntry(
                self.content_frame, placeholder_text="Digite o valor...", fg_color="#282a2e", text_color="white"
            ))
            new_entry = getattr(self, entry_name)
            if command:
                new_entry.bind("<Return>", lambda event: command(new_entry.get().strip()))
            else:
                new_entry.bind("<Return>", self.check_exit)
            new_entry.grid(row=self.content_frame.grid_size()[1], column=0, padx=10, pady=(5, 10), sticky="ew")  # Adiciona uma nova entrada de texto

            # Ajusta a altura da janela para acomodar os widgets
            self.root.update_idletasks()
            self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height() + 50}")

            # Reposiciona o campo principal entry para não ficar distorcido
            self.entry.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
            self.root.update_idletasks()
        except Exception as e:
            self.show_error(f"Erro ao expandir a aplicação: {e}")

    def open_script_dir(self):
        try:
            os.startfile(script_dir)  # Abre o diretório do script
        except Exception as e:
            self.show_error(f"Erro ao abrir o diretório do script: {e}")

    def cleanup(self):
        try:
            self.root.destroy()  # Destroi a janela principal
            icon.stop()  # Para o ícone da bandeja do sistema
        except Exception as e:
            print(f"Erro ao limpar a aplicação: {e}")

# Função para criar um ícone para a bandeja do sistema  caso trayicon.png não exista
def create_image(width, height, color1, color2):
    try:
        image = Image.new('RGB', (width, height), color1)  # Cria uma nova imagem
        dc = ImageDraw.Draw(image)  # Cria um objeto de desenho
        dc.rectangle(
            (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
            fill=color2  # Desenha um retângulo na imagem
        )
        return image
    except Exception as e:
        print(f"Erro ao criar a imagem: {e}")

def on_exit():
    try:
        if 'app' in globals():
            app.cleanup()  # Encerra o aplicativo
    except Exception as e:
        print(f"Erro ao sair da aplicação: {e}")

def tray_thread():
    try:
        global icon
        icon_image = Image.open(tray_icon_path)  # Abre a imagem do ícone da bandeja
        icon = pystray.Icon(
            "App", 
            icon_image, 
            menu=pystray.Menu(
                pystray.MenuItem("Exit", lambda: on_exit())  # Adiciona um item de menu para sair
            )   
        )
        icon.run()  # Executa o ícone da bandeja
    except Exception as e:
        print(f"Erro ao iniciar a thread da bandeja: {e}")

if __name__ == "__main__":
    try:
        # Inicializa o aplicativo
        app = AlwaysOnTopApp()

        # Inicia o ícone da bandeja do sistema em uma thread separada
        tray = threading.Thread(target=tray_thread, daemon=True)
        tray.start()

        # Configura a tecla de atalho para alternar a visibilidade da janela
        keyboard.add_hotkey("ctrl+capslock", app.toggle_window)

        # Executa o mainloop
        app.root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")