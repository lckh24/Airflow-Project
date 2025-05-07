from airflow.providers.mysql.hooks.mysql import MySqlHook
from support_processing import TemplateOperatorDB
import logging
from contextlib import closing
import os

class MySQLOperators:
    
    def __init__(self, conn_id="mysql"):
        """
        Initializes a connection to a MySQL database using Airflow's MySqlHook.
        Parameters:
            conn_id (str): The Airflow connection ID for the MySQL database.
        """
        try:
            self.mysqlhook = MySqlHook(mysql_conn_id=conn_id)
            self.mysql_conn = self.mysqlhook.get_conn()
        except:
            logging.error(f"Can't connect to {conn_id} database")
            
    def get_data_to_pd(self, query=None):
        """
        Executes a SQL query and returns the result as a pandas DataFrame.
        Parameters:
            query (str): The SQL query to execute.
        Returns:
            pandas.DataFrame: Query results.
        """
        return self.mysqlhook.get_pandas_df(query)
    
    def get_records(self, query):
        """
        Executes a SQL query and returns the result as a list of tuples.
        Parameters:
            query (str): The SQL query to execute.
        Returns:
            list of tuples: Query results.
        """
        return self.mysqlhook.get_records(query)
    
    def execute_query(self, query):
        """
        Executes a single SQL query (e.g., INSERT, UPDATE, DELETE).

        Parameters:
            query (str): The SQL query to execute.
        """
        try:
            cur = self.mysql_conn.cursor()
            cur.execute(query)
            self.mysql_conn.commit()
        except:
            logging.ERROR(f"Can not execute query: {query}")
            
    def insert_dataframe_into_table(self, table_name, dataframe, data, chunk_size=100000):
        """
        Inserts data into a MySQL table in chunks using batch processing.
        Parameters:
            table_name (str): The target table name.
            dataframe (pd.DataFrame): The DataFrame used to infer table structure.
            data (list of tuples): The data to be inserted.
            chunk_size (int): Number of records per batch insert (default is 100,000).
        """
        query = TemplateOperatorDB(table_name).createQueryInsertInto(dataframe)
        try:
            with closing(self.mysql_conn) as conn:
                if self.mysqlhook.supports_autocommit:
                    self.mysqlhook.set_autocommit(conn, False)
                conn.commit()
                with closing(conn.cursor()) as cur:
                    for i in range(0, len(data), chunk_size):
                        partitioned_data = data[i:i+chunk_size]
                        lst = []
                        for row in partitioned_data:
                            sub_lst = []
                            for cell in row:
                                sub_lst.append(self.mysqlhook._serialize_cell(cell, conn))
                            lst.append(sub_lst)
                        values = tuple(lst)
                        num_records = len(values)
                        cur.executemany(query, values)
                        print(f"Merged/updated {num_records} records")
                        conn.commit()
                conn.commit()  
        except:
            logging.ERROR(f"Can not execute {query}")
            
    def delete_records_in_table(self, table_name, key_field, values):
        """
        Deletes records from a table based on a list of key field values.
        Parameters:
            table_name (str): The name of the table to delete from.
            key_field (str): The name of the key field.
            values (list): List of key field values to delete.
        """
        query = TemplateOperatorDB(table_name).create_delete_query(key_field, values)
        
        try:
            with closing(self.mysql_conn) as conn:
                if self.mysqlhook.supports_autocommit:
                    self.mysqlhook.set_autocommit(conn, False)
                conn.commit()
                with closing(conn.cursor()) as cur:
                    lst = []
                    for cell in values:
                        lst.append(self.mysqlhook._serialize_cell(cell,conn))
                    del_values = tuple(lst)
                    cur.execute(query, del_values)
                    num_records = len(values)
                    print(f"Deleted {num_records} records")
                    conn.commit()
            conn.commit()
        except:
            logging.ERROR(f"Can not execute {query}")
        
    def insert_data_into_table(self, table_name, data, create_table_like=""):
        """
        Inserts rows into a MySQL table. Optionally creates the table if it doesn't exist.
        Parameters:
            table_name (str): The target table name.
            data (list of tuples): The data to be inserted.
            create_table_like (str): Optional. If provided, creates the table based on this template table.
        """
        if create_table_like != "":
            create_tbl_query = f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {create_table_like};"
            conn = self.mysql_conn
            cur = conn.cursor()
            cur.execute(create_tbl_query)
            conn.commit()
        try:
            self.mysqlhook.insert_rows(table_name, data)  
        except:
            logging.ERROR(f"Can not insert data into {table_name}")
            
    def remove_table_if_exists(self, table_name):
        """
        Drops a table if it exists.
        Parameters:
            table_name (str): The name of the table to remove.
        """
        try:
            remove_table_query = f"DROP TABLE IF EXISTS {table_name}"
            cur = self.mysql_conn.cursor()
            cur.execute(remove_table_query)
            self.mysql_conn.commit()                     
        except:
            logging.ERROR(f"Can not remove table: {table_name}")    
            
    def truncate_all_data_from_table(self, table_name):
        """
        Removes all records from a table without deleting the table itself.
        Parameters:
            table_name (str): The name of the table to truncate.
        """
        try:
            truncate_table = f"TRUNCATE TABLE {table_name};"
            cur = self.mysql_conn.cursor()
            cur.execute(truncate_table)
            self.mysql_conn.commit()
        except:
            logging.ERROR(f"Can not truncate table: {table_name}")
    
    def dump_table_into_path(self, table_name):
        """
        Exports a table's data to a .txt file located in MySQL's secure_file_priv directory.
        Parameters:
            table_name (list or str): The name (or list containing the name) of the table to export.
        """
        try:
            priv = self.mysqlhook.get_first("SELECT @@global.secure_file_priv")
            if priv and priv[0]:
                tbl_name = list(table_name)[0]
                file_name = tbl_name.replace(".", "__")
                self.mysqlhook.bulk_dump(table_name=tbl_name, output_file=os.path.join(priv[0], f"{file_name}.txt"))
            else:
                logging.ERROR("Missing privilege")
        except:
            logging.ERROR(f"Can not dump {table_name}")
            
    def load_data_into_table(self, table_name):
        """
        Loads data from 'TABLES.txt' into the specified MySQL table.
        Assumes the file is located in MySQL's secure_file_priv directory.
        Parameters:
            table_name (str): The name of the target table to load data into.
        """
        try:
            priv = self.mysql_hook.get_first("SELECT @@global.secure_file_priv")
            if priv and priv[0]:
                file_path = os.path.join(priv[0], "TABLES.txt")
                load_data_into_tbl = f"LOAD DATA INFILE '{file_path}' INTO TABLE {table_name};"
                cur = self.mysql_conn.cursor()
                cur.execute(load_data_into_tbl)
                self.mysql_conn.commit()
            else:
                logging.ERROR("Missing privilege")
        except:
            logging.ERROR(f"Can not load {table_name}")
