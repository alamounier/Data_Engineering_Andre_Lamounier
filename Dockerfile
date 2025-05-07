FROM openjdk:17-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libkrb5-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/pip3 /usr/bin/pip

RUN pip install --no-cache-dir pyspark pandas numpy requests delta-spark

RUN mkdir -p /opt/spark/jars
COPY jars/*.jar /opt/spark/jars/

WORKDIR /app

COPY . /app

CMD ["python", "main.py"]


# # Base da imagem com OpenJDK 17 (necessário para o Spark)
# FROM openjdk:17-slim

# # Instala Python, pip e dependências adicionais
# RUN apt-get update && apt-get install -y \
#     python3 \
#     python3-pip \
#     libkrb5-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Cria links simbólicos para garantir compatibilidade entre python3 e pip3
# RUN ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/pip3 /usr/bin/pip

# # Instalando bibliotecas necessárias
# RUN pip install --no-cache-dir pyspark pandas numpy requests delta-spark 

# # Cria a pasta para os JARs e copia os JARs para o container
# RUN mkdir -p /opt/spark/jars
# COPY jars/*.jar /opt/spark/jars/

# # Define o diretório de trabalho
# WORKDIR /app

# # Copia o código-fonte do projeto (incluindo a pasta etl_layers e outros scripts)
# COPY . /app

# # Expõe a porta do Airflow, se necessário (caso você use um servidor web no Airflow)
# # EXPOSE 8080

# # Comando padrão para rodar o script principal
# CMD ["python", "main.py"]








# FROM openjdk:17-slim

# # Instala Python, pip e dependências
# RUN apt-get update && apt-get install -y \
#     python3 \
#     python3-pip \
#     && rm -rf /var/lib/apt/lists/*

# # Cria links simbólicos (forçando se já existirem)
# RUN ln -sf /usr/bin/python3 /usr/bin/python && ln -sf /usr/bin/pip3 /usr/bin/pip

# # Instala bibliotecas necessárias
# RUN pip install --no-cache-dir pyspark pandas numpy requests

# # Cria pasta para os JARs e copia arquivos, se houver
# RUN mkdir -p /opt/spark/jars
# COPY jars/*.jar /opt/spark/jars/

# # Define o diretório de trabalho
# WORKDIR /app

# # Copia o código da aplicação
# COPY app/ /app

# # Comando padrão
# CMD ["python", "main.py"]