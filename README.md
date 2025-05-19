# **Olist-E-commerce-Data-Analysis**
![image](https://github.com/user-attachments/assets/f90a074e-020a-4ba8-baa4-e24f104abf35)
--  

## **Summary**:  
In this project, i built a data warehouse using a sales dataset from Olist, a Brazilian e-commerce platform. I designed and implemented a complete ETL pipeline orchestrated by Apache Airflow, with data stored and modeled in PostgreSQL following a star schema. For visualization, we used Microsoft Power BI to create interactive dashboards and reports, allowing users to explore the sales data and uncover business insights.  

## **About the company**:
Olist is an e-commerce company based in São Paulo, Brazil. It serves as a centralized platform that connects numerous small businesses with customers who want to purchase their products.  

## **About the dataset**:  
The dataset is publicly available and contains information on over 100,000 orders placed between 2016 and 2018 across multiple marketplaces in Brazil. It is hosted on Kaggle: [](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
![image](https://github.com/user-attachments/assets/f72cd1a5-7044-4f28-93a2-070390c4e8e7)

## **Data Warehouse schema:**  
We have the order_fact table as our Fact table and it dimensional tables:  
![image](https://github.com/user-attachments/assets/fed0756b-8c94-4de2-961e-b057e4bd2c67)  

## **The ETL pipeline**:  
To create the Data Warehouse schema, we will execute the following pipeline stages:  
 1. Create MySQL database, load data from csv to database.   
 2. Extract data from MySQL to staging stage in Postgres.  
 3. Clean and Transform the data in staging stage.  
 4. Load data to Warehouse stage in Postgres.

![image](https://github.com/user-attachments/assets/54ddca2e-1d2f-49ae-968d-13a939c28fe4)  

I also integrated git-sync with Apache Airflow to automate DAG deployments directly from a Git repository. This setup ensures that any updates to the pipeline code are automatically synchronized with the Airflow DAGs folder, streamlining development and deployment across environments.  

![image](https://github.com/user-attachments/assets/d07bf9ee-34c0-4621-9cc9-032811e622a3)

## **Snapshot DAGs process**:  
![image](https://github.com/user-attachments/assets/146f639c-e331-4aa0-8673-60fffc7584fb)


## **Visualizations**:
![image](https://github.com/user-attachments/assets/bc8078b3-9f92-4ab8-b6f2-b140169dfd54)  
![image](https://github.com/user-attachments/assets/ad46ed3d-cc50-4d95-8084-af6017ec9461)


   








