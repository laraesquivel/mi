# Use a imagem base do Python
FROM python:3.12.1-slim

# Define o diretório de trabalho como /app
WORKDIR /app

# Copia o conteúdo da pasta atual (onde o código do VS Code está) para o contêiner
COPY . /app

# Instalação das dependências do seu projeto, se houver
#RUN pip install -r requirements.txt

# Comando para ativar o ambiente virtual, se necessário (substitua pelo seu comando de ativação)
# Se o ambiente virtual já estiver ativado no diretório de trabalho, este comando pode ser omitido
RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"

# Comando para executar o seu aplicativo Python
CMD ["python", "__init__.py"]
