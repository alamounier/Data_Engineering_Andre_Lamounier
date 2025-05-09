ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.9.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /code

COPY /src/ /code/

# FROM bitnami/spark:3.5.0

# # Define o diretório de trabalho
# WORKDIR /code

# # Copia os JARs extras para o diretório do Spark
# COPY ./src/jars/*.jar /opt/bitnami/spark/jars/

# # Copia e instala as dependências Python
# COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt

# # Copia o código-fonte
# COPY ./src/ /code/
