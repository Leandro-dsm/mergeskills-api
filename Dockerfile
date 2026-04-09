FROM python:3.11-slim

WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]