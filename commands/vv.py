import keyboard
import time

def paste_vv(text: str, commands: list):
    """
    Executa uma sequência de comandos de entrada no teclado.
    """
    #Args:
    #    text (str): O texto a ser digitado inicialmente.
    #    commands (list): Lista de comandos em sequência. Cada comando pode ser:
    #        - "write:<texto>" -> Digita o texto especificado.
    #        - "key:<tecla>" -> Envia uma tecla simples.
    #        - "press:<tecla>" -> Pressiona uma tecla sem soltar.
    #        - "release:<tecla>" -> Solta uma tecla previamente pressionada.
    
    # Escreve o texto inicial
    keyboard.write(text)
    time.sleep(0.1)  # Pequeno delay entre texto e comandos

    # Executa os comandos em sequência
    for command in commands:
        if command.startswith("write:"):
            _, text_to_write = command.split(":", 1)
            keyboard.write(text_to_write)
        elif command.startswith("key:"):
            _, key = command.split(":", 1)
            keyboard.send(key)
        elif command.startswith("press:"):
            _, key = command.split(":", 1)
            keyboard.press(key)
        elif command.startswith("release:"):
            _, key = command.split(":", 1)
            keyboard.release(key)
        #time.sleep(0.1)  # Pequeno delay entre os comandos

# Exemplo de uso
text = (f"Visita Virtual ao Cliente.\n\n")
commands = [
    "key:ctrl+u", "key:ctrl+b",  # Ctrl+U e Ctrl+B
    "write:Procedimentos Realizados:\n", # Escreve o texto complementar
    "key:ctrl+u", "key:ctrl+b",  # Ctrl+U e Ctrl+B
    "write:-", "key:space", # Espaço para transformar o - em lista
    "key:down"  # Move o cursor para baixo
]

# Executar o comando com x segundos de delay para o usuário se preparar
time.sleep(0.5)
print("Executando os comandos...")
paste_vv(text, commands)
