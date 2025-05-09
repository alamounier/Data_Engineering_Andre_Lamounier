# 🏗️ Projeto de ETL com Airflow, Docker, Delta Lake e Arquitetura Medalhão

Este projeto implementa um pipeline de ETL utilizando Apache Airflow, PySpark, Docker e Delta Lake, estruturado em uma arquitetura de dados em camadas (Bronze, Silver e Gold). O objetivo é orquestrar o processamento de dados da API Open Brewery em contêineres separados para cada etapa do pipeline.

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


