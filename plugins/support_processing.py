import pandas as pd 

class TemplateOperatorDB:
    def __init__(self, tableName):
        self.tableName = tableName
        
    #INSERT INTO tableName (column1, column2, ...)
    #VALUES (value1, value2, ...)
    #ON DUPLICATE KEY UPDATE
    #column1 = VALUES(column1),
    #column2 = VALUES(column2);    
    def createQueryInsertInto(self, dataframe):
        self.column = ""
        self.values = ""
        self.odku = ""
        
        endCol = dataframe.columns[-1]
        for col in dataframe.columns:
            if col != endCol:
                self.columns += col + ", "
                self.values += "%s, "
                self.odku += col + "=" + "VALUES(" + col + ")," 
            else:
                self.column += col
                self.values += "%s"
                self.odku += col + "=" + "VALUES(" + col + ")" 
                
        createQuery = \
            f"INSERT INTO {self.tableName}" + \
            f"({self.columns}) " + \
            f"VALUES ({self.values}) " + \
            f"ON DUPLICATE KEY UPDATE {self.odku}"
        
        return createQuery
            
    # DELETE FROM tableName
    # WHERE column IN (%s, %s, %s)
    def create_delete_query(self, key_field, values):
        self.key_field = key_field
        self.values = values 
        self.placeHolder = ""
        
        i = 0
        while i < len(self.values):
            if i != len(self.values) - 1:
                self.placeHolder += "%s, "
            else:
                self.placeHolder += "%s"
            i += 1
        
        createQuery = f"""
            DELETE FROM {self.tableName}
            WHERE {self.key_field} IN ({self.placeHolder})       
        """
        
        return createQuery