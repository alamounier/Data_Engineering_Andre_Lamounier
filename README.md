# 🏗️ ETL Project with Airflow, Docker, Delta Lake, and Medallion Architecture

This project implements an ETL pipeline using Apache Airflow, PySpark, Docker, and Delta Lake, structured within a layered data architecture (Bronze, Silver, and Gold). The goal is to orchestrate the processing of data from the Open Brewery API in separate containers for each pipeline stage.

<div align="center">
  <img src="/imgs_png/arquitetura_projeto.png" alt="python" height="200">
</div>

---

## 🔧 Prerequisites

- **Docker installed on your local machine**  
- 👉 [Download the JAR aws-java-sdk-bundle](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar) — save the file in the `src/jars` folder

---

## 🔧 Technologies Used

- **Apache Airflow** (workflow orchestration)
- **Apache Spark with Delta Lake** (data processing with ACID transactions)
- **Docker** (isolated environment for each processing stage)
- **Docker Compose** (management of multiple services)
- **Python 3**

---

## 🧱 Medallion Architecture

The architecture is divided into three layers:

- **Bronze**: collects raw data from the Open Brewery API.
- **Silver**: cleans, transforms, and partitions the data by location.
- **Gold**: aggregates data for analysis, such as the count of breweries by type and location.

---

## 📁 Project Structure

<img src="/imgs_png/estrutura_projeto.png" alt="python" height="300" /> 

## ⚙️ How to Run

Follow the steps below to run this project:

1. Copy the project directory to a local folder on your computer.

2. Ensure the file `aws-java-sdk-bundle-1.11.1026.jar` is located in the `src/jars` folder.

3. Open the terminal and navigate to the project directory.

4. In the project directory, build the PySpark container image by running the following command: `docker build -t pyspark_image .`

5. After step 4 completes, navigate to the `Airflow/dags/` folder and open the `brewery_etl_dag.py` file. Modify the "sources" for the task mount parameters as follows:
    
    - From: source=r"C:\Users\andre-lamounier\Desktop\airflow-docker\meu-projeto\src\outputs"
    - To: source=r"[path to your outputs folder]"
    
    **Note:** If you use the backslash \ in the file path, prepend the string with `r`. If you use the forward slash /, simply remove the `r`.

6. Now, access the `Airflow` folder in the terminal and create the Airflow container with the following command: `docker-compose up -d`

---

## 🧠 Logic

The objective of this pipeline is to leverage the Delta engine and Medallion architecture to ensure efficient processing while maintaining control over the data history and the most recent version for analysis.

**🥉 Bronze Layer**
This layer stores raw data from the sources, preserving all historical versions of the records using Delta Change Data Feed (CDF). Additionally, the schema is explicitly defined during DataFrame creation, and the .write() step does not allow schema evolution. If new columns are added at the source level, the process fails explicitly, providing developers full control and visibility over changes in the structure. This avoids silent schema drift and enforces strong contracts for data ingestion.

✅ Benefits:
- Full data history with versioning (Delta + CDF).
- Schema enforcement with validation — raises an error on unexpected fields.
- Adds technical columns like line_created_at and line_updated_at for traceability.

**🥈 Silver Layer**
In this layer, the data is cleaned, transformed, and made more analysis-friendly. The Silver table is overwritten on each execution, retaining only the latest version of each record, which reduces storage costs and improves performance. However, additional data quality controls are applied:

- Validates critical fields such as id and name, raising errors for nulls or invalid values.
- Replaces nulls in partitioning fields (country, state, city) with "unknown" to prevent partitioning issues.
- Duplicates and invalid rows are filtered out to ensure high-quality output for downstream consumers.

✅ Benefits:
- Enforced data quality rules before data is made available for consumption.
- Maintains clean, deduplicated data optimized for analysis and partitioned for performance.
- Errors raised during validation allow early detection of data anomalies.

**🥇 Gold Layer**
The Gold layer aggregates the clean data from Silver, producing curated tables for dashboards and business reports. This layer focuses on usability and performance, delivering business metrics and KPIs.

**Versioning Advantage**
If there's a need to recover previous versions or perform audits, the Bronze layer offers full history through Delta versioning and CDF. The Silver layer focuses on delivering only the latest valid version, reducing complexity and storage costs while ensuring analytical efficiency.



---

## ⚙️ Orchestration with Airflow

- Each `DockerOperator` runs a specific Python script for a given pipeline layer inside a Docker container based on the `pyspark_image`.
- Intermediate data is persisted in the `outputs` folder, which is mounted across all containers via the `mounts` parameter.
- Tasks are executed in sequence: `bronze_task → silver_task → gold_task`.
- The use of `docker-socket-proxy` allows Airflow to securely control Docker containers even within another container.

---

## 📌 Results

- Below are some analyses on the Gold layer:

<img src="/imgs_png/resultados.png" alt="python" height="400" /> 
