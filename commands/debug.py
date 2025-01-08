"""
Comando de debug para testes de execução de comandos.
"""
app.hideWindowAfterCommand = False  # Define a variável de instância hideWindowAfterCommand como False
logging.debug(f"hideWindowAfterCommand set to: {app.hideWindowAfterCommand}")
logging.debug(f"Comando {command} executado com sucesso!")