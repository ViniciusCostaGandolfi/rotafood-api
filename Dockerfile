# Use a imagem oficial do Python 3.11
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o diretório de trabalho
COPY . .

# Expõe a porta 80 para o acesso externo
EXPOSE 80

# Comando para executar o aplicativo FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
