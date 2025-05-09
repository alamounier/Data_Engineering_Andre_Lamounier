# 🏗️ Projeto de ETL com Airflow, Docker, Delta Lake e Arquitetura Medalhão

Este projeto implementa um pipeline de ETL utilizando Apache Airflow, PySpark, Docker e Delta Lake, estruturado em uma arquitetura de dados em camadas (Bronze, Silver e Gold). O objetivo é orquestrar o processamento de dados da API Open Brewery em contêineres separados para cada etapa do pipeline.

<div align="center">
  <img src="/imgs_png/arquitetura_projeto.png" alt="python" height="200">
</div>

---

## 🔧 Pré Requisitos

- **Docker instalado na máquina local** 

---

## 🔧 Tecnologias Utilizadas

- **Apache Airflow** (orquestração de workflows)
- **Apache Spark com Delta Lake** (processamento de dados com transações ACID)
- **Docker** (ambiente isolado para cada etapa de processamento)
- **Docker Compose** (gerenciamento de múltiplos serviços)
- **Python 3**

---

## 🧱 Arquitetura Medalhão

A arquitetura é dividida em três camadas:

- **Bronze**: coleta dados crus da API Open Brewery.
- **Silver**: limpa, transforma e particiona os dados por localização.
- **Gold**: agrega dados para análises, como a contagem de cervejarias por tipo e localidade.

---

## 📁 Estrutura do Projeto

<img src="/imgs_png/estrutura_projeto.png" alt="python" height="300" /> 

## (colocar engrenagem) Como executar

Siga os passos abaixo para rodar este projeto:

1. Copie o diretório do projeto para uma pasta local em seu computador.

2. Abra o terminal do seu computador e mova até o diretório do projeto.

3. Entra na pasta src/jars e baixa o conector do pypsark no seguinte link https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar e salve nesta mesma pasta, retorne a pasta do projeto raiz novamente pelo terminal.

4. Crie a imagem do container do PySpark executando o seguinte comando: `docker build -t pyspark_image .`

5. Navegue até a pasta do Airflow no terminal, aguarde a execução do container do PySpark e, em seguida, crie o container do Airflow com o seguinte comando: `docker-compose up -d`


## 🧠 Lógica

O objetivo deste pipeline é aproveitar as vantagens da engine Delta e da arquitetura Medalhão para garantir um processamento eficiente, mantendo o controle sobre o histórico de dados e a versão mais recente para análises.

Camada Bronze: Armazena os dados brutos provenientes das fontes, mantendo todas as versões dos registros. Utilizando o Change Data Feed (CDF), é possível rastrear qualquer alteração nos dados ao longo do tempo. Isso oferece um histórico completo de todas as mudanças feitas nos dados de entrada.

Camada Silver: A partir dessa camada, o pipeline processa e transforma os dados para um formato mais adequado para análise. A tabela da camada Silver será sobrescrita a cada execução, garantindo que apenas a versão mais recente dos dados seja mantida, o que economiza recursos de processamento. Não há necessidade de armazenar o histórico completo das alterações, já que a camada Bronze já preserva essa informação.

Camada Gold: A camada Gold será a tabela da camada silver em formato agregado, ideal para construção de dashboards e relatórios para área de negócios.

Vantagem do Versionamento: Caso seja necessário recuperar versões anteriores dos dados ou realizar auditoria, a camada Bronze com versionamento via Delta oferece essa flexibilidade. A camada Silver foca apenas na versão mais atual, o que facilita a análise e melhora a performance.

Esse modelo de arquitetura permite um equilíbrio entre o controle total do histórico (na camada Bronze) e a eficiência de processamento (na camada Silver), otimizando recursos e mantendo a flexibilidade para futuros ajustes ou auditorias.


