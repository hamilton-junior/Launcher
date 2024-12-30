# Launcher

Launcher é um aplicativo Python que fornece uma interface gráfica (GUI) para executar comandos personalizados. Ele utiliza a biblioteca `customtkinter` para uma aparência moderna e inclui recursos como janela sempre no topo, integração com a bandeja do sistema e atalhos de teclado.

## Funcionalidades

- **Sempre no Topo**: A janela do aplicativo permanece no topo de todas as outras janelas.
- **Comandos Personalizados**: Execute comandos ou scripts predefinidos localizados no diretório `commands`.
- **Ícone na Bandeja do Sistema**: Minimize o aplicativo para a bandeja do sistema e restaure-o com um clique.
- **Atalhos de Teclado**: Use `Ctrl + CapsLock` para alternar a visibilidade da janela do aplicativo.
- **Interface Dinâmica**: A interface pode se expandir para incluir campos de entrada adicionais conforme necessário.
- **Tratamento de Erros**: Exibe mensagens de erro de forma amigável.

## Instalação

1. Clone o repositório.
2. Instale as dependências necessárias:
    ```sh
    pip install tkinter customtkinter keyboard pystray pillow
    ```
3. Execute o aplicativo:
    ```sh
    python Launcher.py
    ```

## Uso

- **Alternar Janela**: Pressione `Ctrl + CapsLock` para mostrar ou esconder a janela do aplicativo.
- **Executar Comandos**: Digite um comando no campo de entrada e pressione `Enter`.
- **Sair do Aplicativo**: Digite `exit` no campo de entrada ou use o ícone da bandeja do sistema para fechar o aplicativo.

## Comandos Personalizados

Coloque seus scripts de comando personalizados no diretório `commands`. As extensões de arquivo suportadas são `.py` e `.txt`. Cada script de comando pode incluir uma docstring para descrever sua funcionalidade, que será exibida na dica de ferramenta do comando.

## Licença

Este projeto está licenciado sob a Licença MIT.
# Launcher

Launcher é um aplicativo Python que fornece uma interface gráfica (GUI) para executar comandos personalizados. Ele utiliza a biblioteca `customtkinter` para uma aparência moderna e inclui recursos como janela sempre no topo, integração com a bandeja do sistema e atalhos de teclado.

## Funcionalidades

- **Sempre no Topo**: A janela do aplicativo permanece no topo de todas as outras janelas.
- **Comandos Personalizados**: Execute comandos ou scripts predefinidos localizados no diretório `commands`.
- **Ícone na Bandeja do Sistema**: Minimize o aplicativo para a bandeja do sistema e restaure-o com um clique.
- **Atalhos de Teclado**: Use `Ctrl + CapsLock` para alternar a visibilidade da janela do aplicativo.
- **Interface Dinâmica**: A interface pode se expandir para incluir campos de entrada adicionais conforme necessário.
- **Tratamento de Erros**: Exibe mensagens de erro de forma amigável.

## Instalação

1. Clone o repositório.
2. Instale as dependências necessárias:
    ```sh
    pip install tkinter customtkinter keyboard pystray pillow
    ```
3. Execute o aplicativo:
    ```sh
    python Launcher.py
    ```

## Uso

- **Alternar Janela**: Pressione `Ctrl + CapsLock` para mostrar ou esconder a janela do aplicativo.
- **Executar Comandos**: Digite um comando no campo de entrada e pressione `Enter`.
- **Sair do Aplicativo**: Digite `exit` no campo de entrada ou use o ícone da bandeja do sistema para fechar o aplicativo.

## Comandos Personalizados

Coloque seus scripts de comando personalizados no diretório `commands`. As extensões de arquivo suportadas são `.py` e `.txt`. Cada script de comando pode incluir uma docstring para descrever sua funcionalidade, que será exibida na dica de ferramenta do comando.

## Licença

Este projeto está licenciado sob a Licença MIT.