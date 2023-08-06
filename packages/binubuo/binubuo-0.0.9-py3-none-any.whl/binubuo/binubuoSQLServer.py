import pyodbc
import sys
import json
import ast
import time
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

# Remove annoying incompatible warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class binubuoSQLServer:
    def __init__(self, binubuokey, dbserver, dbname, dbfullConnection=None):
        self.binubuokey = binubuokey
        self.dbserver = dbserver
        self.dbname = dbname
        self.dbfullConnection = dbfullConnection
        self.max_sample_size = 100
        self.connected = False
        self.binuObj = binubuo(binubuokey)
        self.show_messages = False

    def m(self, message):
        if self.show_messages:
            print(message)

    def set_message(self, show=False):
        self.show_messages = show
        self.binuObj.set_message(show)

    def connect(self):
        try:
            if self.dbfullConnection is None:
                self.connection = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = self.dbserver , database = self.dbname)
            else:
                self.connection = self.dbfullConnection
            self.connected = True
            #self.connection.autocommit = True
        except:
            self.m("Error: Failed to connect to database. Please make sure you have a connection before using other methods.")
            self.connection = None

    def connectSecondary(self, dbserver, dbname, dbfullConnection=None):
        try:
            if dbfullConnection is None:
                self.secondary_connection = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = dbserver , database = dbname)
            else:
                self.secondary_connection = dbfullConnection
            self.connected_secondary = True
        except:
            self.m("Error: Failed to connect to secondary/alternate database. Please check your connection details and try again.")
            self.secondary_connection = None

    def columnGeneratorComments(self, table_name, comments, override=False):
        if self.connected:
            comment_count_sql = """select
                    count(exp.value)
                from 
                    INFORMATION_SCHEMA.COLUMNS ISC
                    left outer join sys.extended_properties exp on object_id(ISC.table_name) = exp.major_id and isc.ordinal_position = exp.minor_id
                WHERE
                    isc.table_name = ?
                and
                    exp.class_desc = 'OBJECT_OR_COLUMN'
                and
                    exp.name = 'MS_DESCRIPTION';"""
            working_cursor = self.connection.cursor()
            working_cursor.execute(comment_count_sql, (table_name,))
            cursor_result = working_cursor.fetchone()
            print(cursor_result)
            self.m("Comments: " + str(cursor_result[0]))
            if (cursor_result[0] > 0 or not override) or (cursor_result[0] == 0):
                # Let us go ahead and set comment generators as requested.
                if (comments.find('=') > 0):
                    # Named notation
                    for cn in comments.split(","):
                        colname = cn.split("=")[0].strip()
                        colcomment = cn.split("=")[1].strip()
                        col_add_stmt = """EXEC sp_addextendedproperty   
                            @name = N'MS_DESCRIPTION',   
                            @value = ?,  
                            @level0type = N'Schema', @level0name = 'dbo',  
                            @level1type = N'Table',  @level1name = ?,  
                            @level2type = N'Column', @level2name = ?"""
                        working_cursor.execute(col_add_stmt, (colcomment, table_name, colname))
                        self.connection.commit()
                else:
                    # Just split and follow column order. Ignore any column outside of split length
                    ordered_col_cursor = self.connection.cursor()
                    ordered_col_sql = "select ORDINAL_POSITION, COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name = ? order by ORDINAL_POSITION asc;"
                    ordered_col_cursor.execute(ordered_col_sql, (table_name,))
                    comment_cursor = self.connection.cursor()
                    col_row = ordered_col_cursor.fetchone()
                    while col_row:
                        self.m("Working on col: " + col_row[1])
                        try:
                            colcomment = comments.split(",")[col_row[0] - 1]
                            col_add_stmt = """EXEC sp_addextendedproperty   
                                @name = N'MS_DESCRIPTION',   
                                @value = ?,  
                                @level0type = N'Schema', @level0name = 'dbo',  
                                @level1type = N'Table',  @level1name = ?,  
                                @level2type = N'Column', @level2name = ?"""
                            self.m("Comment command: " + col_add_stmt + "\nWith args: " + colcomment + " " + table_name + " " + col_row[1])
                            comment_cursor.execute(col_add_stmt, (colcomment, table_name, col_row[1]))
                        except:
                            # Aint no comment for this column. Just ignore
                            self.m("Soemthing went wrong here")
                        col_row = ordered_col_cursor.fetchone()
                    self.connection.commit()