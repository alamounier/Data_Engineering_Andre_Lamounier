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

<img src="/imgs_png/estrutura_projeto.png" alt="python" height="50" /> 

## 📁 Como executar

1. Suba os serviços com Docker Compose
Execute o seguinte comando na raiz do projeto (onde está localizado o docker-compose.yml):

- docker-compose up -d

2. Acesse a interface do Airflow
Abra seu navegador e vá para: http://localhost:8080
Use as credenciais padrão:

- Usuário: airflow
- Senha: airflow

3. Ative e execute a DAG
Na interface do Airflow:

- Localize a DAG chamada brewery_etl_dag.
- Habilite a DAG clicando no botão "On/Off".
- Em seguida, clique em Trigger DAG (botão de play) para iniciar o pipeline.

4. Monitore as execuções
Acompanhe o progresso e visualize os logs diretamente na interface do Airflow, clicando em cada task da DAG.
Os resultados processados serão salvos na pasta src/outputs.
