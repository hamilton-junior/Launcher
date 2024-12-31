"""
Comando de debug para testes de execução de comandos.
"""
app.hideWindowAfterCommand = False  # Define a variável de instância hideWindowAfterCommand como False
logging.info(f"hideWindowAfterCommand set to: {app.hideWindowAfterCommand}")
logging.info(f"Comando {command} executado com sucesso!")