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

- **Bronze Layer**: Stores raw data from the sources, keeping all versions of the records. By using the Change Data Feed (CDF), any changes to the data over time can be tracked. This provides a complete history of all modifications made to the input data.

- **Silver Layer**: In this layer, the pipeline processes and transforms the data into a more analysis-friendly format. The Silver layer table will be overwritten with each execution, ensuring that only the latest version of the data is retained, thus saving processing resources. There is no need to store the complete history of changes, as the Bronze layer already preserves this information.

- **Gold Layer**: The Gold layer will represent the aggregated table from the Silver layer, ideal for building dashboards and reports for the business area.

**Versioning Advantage**: If there is a need to recover previous versions of the data or perform auditing, the Bronze layer, with Delta versioning, offers this flexibility. The Silver layer focuses only on the latest version, which makes analysis easier and enhances performance.

This architectural model strikes a balance between full history control (in the Bronze layer) and processing efficiency (in the Silver layer), optimizing resources while maintaining flexibility for future adjustments or audits.

---

## ⚙️ Orchestration with Airflow

- Each `DockerOperator` runs a specific Python script for a given pipeline layer inside a Docker container based on the `pyspark_image`.
- Intermediate data is persisted in the `outputs` folder, which is mounted across all containers via the `mounts` parameter.
- Tasks are executed in sequence: `bronze_task → silver_task → gold_task`.
- The use of `docker-socket-proxy` allows Airflow to securely control Docker containers even within another container.

---

## 📌 Results

Below are some analyses on the Gold layer:

<img src="/imgs_png/resultados.png" alt="python" height="400" /> 