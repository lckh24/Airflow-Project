# 🚀 Olist E-commerce Data Pipeline & Analysis

## 📌 Project Overview
This project showcases an end-to-end **ETL pipeline** and **data warehouse** built for the Olist Brazilian e-commerce dataset. Using **Apache Airflow**, **PostgreSQL**, and **Power BI**, the pipeline enables analytical reporting and business insights through a structured star schema data model.

---

## ⚙️ Tech Stack

- **ETL Orchestration**: Apache Airflow (with Git-sync auto-deployment)
- **Data Source**: CSV → MySQL (simulated raw layer)
- **Storage & Modeling**: PostgreSQL with star schema design
- **Languages**: Python, SQL
- **Visualization**: Microsoft Power BI
- **Containerization**: Docker

---

## 🧩 Project Goals

- Build a modern data pipeline with clear separation of concerns (bronze, silver, gold layers)
- Design a scalable star schema for analytical queries
- Enable business users to explore key metrics via dashboards

---

## 🏗️ ETL Pipeline Architecture

The pipeline follows a layered architecture inspired by the **Medallion model**:

1. **Bronze (Raw)**: Load CSV data into MySQL → extract into PostgreSQL staging.
2. **Silver (Staging)**: Clean and transform data (resolve nulls, data types, joins).
3. **Gold (Warehouse)**: Load clean data into star schema tables for BI use.

> DAGs are orchestrated with Airflow, and Git-sync ensures CI/CD workflow for DAGs deployment.

### 📉 ETL Pipeline Flow

![ETL Pipeline](https://github.com/user-attachments/assets/54ddca2e-1d2f-49ae-968d-13a939c28fe4)

---

## 🗃️ Data Warehouse Schema

- **Fact Table**: `order_fact`
- **Dimension Tables**: `dim_customers`, `dim_products`, `dim_sellers`, `dim_dates`, `dim_geolocation`

![Star Schema](https://github.com/user-attachments/assets/fed0756b-8c94-4de2-961e-b057e4bd2c67)

---

## ⛓ DAG Snapshots

![Airflow DAG](https://github.com/user-attachments/assets/146f639c-e331-4aa0-8673-60fffc7584fb)

---

## 📊 Power BI Dashboards

Visualizations were created using Power BI to help answer key business questions:

- Top-performing states, categories, sellers
- Delivery performance & review scores
- Monthly revenue trends

![Dashboard 1](https://github.com/user-attachments/assets/bc8078b3-9f92-4ab8-b6f2-b140169dfd54)  
![Dashboard 2](https://github.com/user-attachments/assets/ad46ed3d-cc50-4d95-8084-af6017ec9461)

---

## 🧾 Dataset Info

- **Source**: [Kaggle - Olist Brazilian E-commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Time Period**: 2016–2018
- **Data Volume**: 100K+ orders, 70K+ products, 100K+ customers

---

## 🏢 About Olist

Olist is a Brazil-based platform that connects small merchants with large marketplaces. It simplifies operations by centralizing product listings, logistics, and customer communication.

---

## 📬 Contact

For any questions or collaboration, feel free to reach out!

