import cx_Oracle
import sys
import json
import ast
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

class binubuoOracle:
    def __init__(self, binubuokey, dbuser, dbpwd, dbdsn, dbconfig=None, dbfullConnection=None):
        self.binubuokey = binubuokey
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.dbdsn = dbdsn
        self.dbconfig = dbconfig
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
                if self.dbconfig is not None:   
                    cx_Oracle.init_oracle_client(config_dir=self.dbconfig)
                self.connection = cx_Oracle.connect(user=self.dbuser, password=self.dbpwd, dsn=self.dbdsn)
            else:
                self.connection = self.dbfullConnection
            self.connected = True
            # Set defaults
            working_cursor = self.connection.cursor()
            stmt = "alter session set nls_date_format='YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"'"
            self.m(stmt)
            working_cursor.execute(stmt)
            stmt = "alter session set nls_timestamp_format='YYYY-MM-DD\"T\"HH24:MI:SSXFF'"
            self.m(stmt)
            working_cursor.execute(stmt)
            stmt = "alter session set nls_timestamp_tz_format='YYYY-MM-DD\"T\"HH24:MI:SSXFFTZH:TZM'"
            self.m(stmt)
            working_cursor.execute(stmt)
        except:
            self.m("Error: Failed to connect to database. Please make sure you have a connection before using other methods.")
            self.connection = None

    def connectSecondary(self, dbuser, dbpwd, dbdsn, dbconfig=None, dbfullConnection=None):
        try:
            if dbfullConnection is None:
                if dbconfig is not None:
                    try: 
                        cx_Oracle.init_oracle_client(config_dir=dbconfig)
                    except:
                        # If Client Library already loaded (with the primary connection) ignore the error here
                        pass
                self.secondary_connection = cx_Oracle.connect(user=dbuser, password=dbpwd, dsn=dbdsn)
            else:
                self.secondary_connection = dbfullConnection
            self.connected_secondary = True
            working_cursor = self.secondary_connection.cursor()
            stmt = "alter session set nls_date_format='YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"'"
            self.m(stmt)
            working_cursor.execute(stmt)
            stmt = "alter session set nls_timestamp_format='YYYY-MM-DD\"T\"HH24:MI:SSXFF'"
            self.m(stmt)
            working_cursor.execute(stmt)
            stmt = "alter session set nls_timestamp_tz_format='YYYY-MM-DD\"T\"HH24:MI:SSXFFTZH:TZM'"
            self.m(stmt)
            working_cursor.execute(stmt)
        except:
            self.m("Error: Failed to connect to secondary/alternate database. Please check your connection details and try again.")
            self.secondary_connection = None

    def calculateSampleSize(self, table_name):
        sub_sample_cursor = self.connection.cursor()
        sub_sample_size_stmt = "select nvl(num_rows, 0) from user_tables where table_name = :tabname"
        sub_sample_cursor.execute(sub_sample_size_stmt, tabname = table_name.upper())
        sub_sample_size_cal = sub_sample_cursor.fetchone()
        # Calculate the real sample size in percent
        if (int(sub_sample_size_cal[0]) > 0 and int(sub_sample_size_cal[0]) < self.max_sample_size):
            sub_sample_size_cal_cust = 99.99
        elif (int(sub_sample_size_cal[0]) > self.max_sample_size):
            # Calculate rough percentage of max sample size
            sub_sample_size_cal_cust = round((self.max_sample_size/int(sub_sample_size_cal[0])*100), 8)
        else:
            # In case of zero rows, we read all of nothing :)
            sub_sample_size_cal_cust = 99.99
        self.m("Sample size of " + str(sub_sample_size_cal_cust) + " calculated for " + str(sub_sample_size_cal[0]) + " rows.")
        return sub_sample_size_cal_cust

    def templateFromTable(self, table_name, use_comments=True, use_infer=False, use_sample_data=False):
        self.template = BinubuoTemplate()
        # Let us validate the table name before we continue.
        assert_table_sql = "select dbms_assert.sql_object_name(:tabname) from dual"
        assert_table_cursor = self.connection.cursor()
        table_exist = False
        try:
            assert_table_cursor.execute(assert_table_sql, tabname = table_name.upper())
            self.templateTable = table_name.upper()
            table_exist = True
        except:
            self.m("Table name entered does not exist. templateFromTable can only be used on existing tables.")
        # We know the table exists.
        # There are a number of different ways to branch out and do the template.
        # 1. Just use generic defaults for datatype.
        # 2. Use comments if available, and fall back to defaults if a column does not have a comment.
        # 3. Call the webservice with _only_ metadata to infer the generator
        # 4. Call the webservice with metadata _and_ sample data to infer the generator.
        if table_exist:
            if not use_infer:
                # No webservice call to generate template.
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = """select
                    utc.column_name
                    , case utc.data_type
                        when 'NUMBER' then 'number'
                        when 'VARCHAR2' then 'string'
                        when 'NVARCHAR2' then 'string'
                        when 'DATE' then 'date'
                        when 'TIMESTAMP' then 'time'
                        when 'TIMESTAMP(6)' then 'time'
                        else 'string'
                    end as column_data_type
                    , case
                        when utc.data_type = 'NUMBER' and utc.avg_col_len = 3 and utc.num_distinct <=2 then 'numeric_on_off'
                        when utc.data_type = 'NUMBER' and utc.avg_col_len < 4 then 'small_number'
                        when utc.data_type = 'NUMBER' and utc.avg_col_len < 6 then 'medium_number'
                        when utc.data_type = 'NUMBER' and utc.avg_col_len > 5 then 'large_number'
                        when utc.data_type = 'FLOAT' and utc.avg_col_len < 4 then 'small_amount'
                        when utc.data_type = 'FLOAT' and utc.avg_col_len < 6 then 'medium_amount'
                        when utc.data_type = 'FLOAT' and utc.avg_col_len > 5 then 'large_amount'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 10 and utc.num_distinct <=5 then 'flow_status'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 30 and utc.num_distinct > round(ut.num_rows*0.7) then 'full_name'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 10 then 'medium_word'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len > 20 then 'large_word'
                        when utc.data_type = 'DATE' then 'date'
                        when utc.data_type = 'TIMESTAMP' then 'timestamp'
                        when utc.data_type = 'TIMESTAMP(6)' then 'timestamp'
                        else 'word'
                    end as column_def_generator
                    , ucc.comments 
                    , ut.num_rows
                    , utc.num_nulls
                    , utc.num_distinct
                    , utc.nullable
                    , utc.avg_col_len
                from
                    user_tab_columns utc
                    inner join user_tables ut on ut.table_name = utc.table_name
                    left outer join user_col_comments ucc on utc.table_name = ucc.table_name and utc.column_name = ucc.column_name 
                where
                    utc.table_name = :tabname
                order by 
                    utc.column_id asc"""
                working_cursor.execute(generic_column_meta_sql, tabname = table_name.upper())
                for cname, cdtype, cdgenerator, ccomment, crows, cnumnulls, cnumdist, cnullable, cavglen in working_cursor:
                    self.template.init_column(column_name=cname, column_type="generated", column_datatype=cdtype)
                    if ccomment is not None and use_comments:
                        self.template.set_column_attribute(cname, "generator", ccomment)
                    else:
                        self.template.set_column_attribute(cname, "generator", cdgenerator)
                # Once we are done, we can validate the template and return it.
                self.template.validate_template()
                self.template.complete_template()
                return self.template.template_JSON
            else:
                # Placeholder to run the infer code.
                if use_sample_data:
                    sub_sample_size_cal_cust = self.calculateSampleSize(table_name)
                working_cursor = self.connection.cursor()
                if use_sample_data:
                    columns_meta_stmt = """with foreign_references as (
                        select a.table_name, a.column_name, a.constraint_name, c.owner, 
                        -- referenced pk
                        c.r_owner, c_pk.table_name r_table_name, c2.column_name r_column_name
                        from user_cons_columns a
                        join user_constraints c on a.constraint_name = c.constraint_name
                        join user_constraints c_pk on c.r_constraint_name = c_pk.constraint_name
                        join user_cons_columns c2 on c_pk.constraint_name = c2.constraint_name
                        where c.constraint_type = 'R'
                        and a.table_name = :tabname
                    )
                    select utc.column_name, json_object(
                        key 'column_name' value utc.column_name
                        , key 'table_name' value ut.table_name
                        , key 'column_datatype' value case utc.data_type
                            when 'CLOB' then 'text'
                            when 'NUMBER' then 'number'
                            when 'VARCHAR2' then 'string'
                            when 'VARCHAR' then 'string'
                            when 'NVARCHAR2' then 'string'
                            when 'CHAR' then 'string'
                            when 'DATE' then 'date'
                            when 'TIMESTAMP(6)' then 'time'
                            when 'TIMESTAMP' then 'time'
                            else 'string'
                        end 
                        , key 'table_level_rowcount' value nvl(ut.num_rows, 0) 
                        , key 'table_level_avg_row_length' value nvl(ut.avg_row_len, 0)
                        , key 'column_level_avg_col_length' value nvl(utc.avg_col_len, 0)
                        , key 'column_data_length' value utc.data_length
                        , key 'column_number_precision' value utc.data_precision
                        , key 'column_number_decimals' value utc.data_scale
                        , key 'column_nullable' value utc.nullable
                        , key 'column_nulls' value utc.num_nulls
                        , key 'column_distinct_count' value utc.num_distinct
                        , key 'column_low_value' value case
                            when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'VARCHAR', 'CHAR') then utl_raw.cast_to_varchar2(utc.low_value)
                            when utc.data_type = 'CLOB' then substr(utl_raw.cast_to_varchar2(utc.low_value), 1, 200)
                            when utc.data_type = 'NUMBER' then to_char(utl_raw.cast_to_number(utc.low_value))
                            when utc.data_type = 'DATE' then to_char(to_date(rtrim(to_char(100*(to_number(substr(utc.low_value,1,2),'XX')-100)
                                        + (to_number(substr(utc.low_value,3,2),'XX')-100),'fm0000')||'-'||
                                        to_char(to_number(substr(utc.low_value,5,2),'XX'),'fm00')||'-'||
                                        to_char(to_number(substr(utc.low_value,7,2),'XX'),'fm00')||' '||
                                        to_char(to_number(substr(utc.low_value,9,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.low_value,11,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.low_value,13,2),'XX')-1,'fm00')), 'YYYY-MM-DD HH24:MI:SS'))
                            when utc.data_type in ('TIMESTAMP', 'TIMESTAMP(6)') then to_char(to_timestamp(rtrim(to_char(100*(to_number(substr(utc.low_value,1,2),'XX')-100)
                                        + (to_number(substr(utc.low_value,3,2),'XX')-100),'fm0000')||'-'||
                                        to_char(to_number(substr(utc.low_value,5,2),'XX'),'fm00')||'-'||
                                        to_char(to_number(substr(utc.low_value,7,2),'XX'),'fm00')||' '||
                                        to_char(to_number(substr(utc.low_value,9,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.low_value,11,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.low_value,13,2),'XX')-1,'fm00')), 'YYYY-MM-DD HH24:MI:SS'))
                            else 'Not extractable'
                        end 
                        , key 'column_high_value' value case
                            when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'VARCHAR', 'CHAR') then utl_raw.cast_to_varchar2(utc.high_value)
                            when utc.data_type = 'CLOB' then utl_raw.cast_to_varchar2(utc.high_value)
                            when utc.data_type = 'NUMBER' then to_char(utl_raw.cast_to_number(utc.high_value))
                            when utc.data_type = 'DATE' then to_char(to_date(rtrim(to_char(100*(to_number(substr(utc.high_value,1,2),'XX')-100)
                                        + (to_number(substr(utc.high_value,3,2),'XX')-100),'fm0000')||'-'||
                                        to_char(to_number(substr(utc.high_value,5,2),'XX'),'fm00')||'-'||
                                        to_char(to_number(substr(utc.high_value,7,2),'XX'),'fm00')||' '||
                                        to_char(to_number(substr(utc.high_value,9,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.high_value,11,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.high_value,13,2),'XX')-1,'fm00')), 'YYYY-MM-DD HH24:MI:SS'))
                            when utc.data_type in ('TIMESTAMP', 'TIMESTAMP(6)') then to_char(to_timestamp(rtrim(to_char(100*(to_number(substr(utc.high_value,1,2),'XX')-100)
                                        + (to_number(substr(utc.high_value,3,2),'XX')-100),'fm0000')||'-'||
                                        to_char(to_number(substr(utc.high_value,5,2),'XX'),'fm00')||'-'||
                                        to_char(to_number(substr(utc.high_value,7,2),'XX'),'fm00')||' '||
                                        to_char(to_number(substr(utc.high_value,9,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.high_value,11,2),'XX')-1,'fm00')||':'||
                                        to_char(to_number(substr(utc.high_value,13,2),'XX')-1,'fm00')), 'YYYY-MM-DD HH24:MI:SS'))
                            else 'Not extractable'
                        end
                        , key 'column_is_reference' value case
                            when fr.column_name is not null then 1
                            else 0
                        end
                        , key 'reference_table' value fr.r_table_name
                        , key 'reference_column' value fr.r_column_name
                         absent on null) col_infer_meta
                    from
                        user_tab_cols utc
                        inner join user_tables ut on ut.table_name = utc.table_name
                        left outer join foreign_references fr on fr.table_name = utc.table_name and fr.column_name = utc.column_name
                    where
                        utc.table_name = :tabname
                    order by 
                        utc.column_id asc"""
                else:
                    columns_meta_stmt = """with foreign_references as (
                        select a.table_name, a.column_name, a.constraint_name, c.owner, 
                        -- referenced pk
                        c.r_owner, c_pk.table_name r_table_name, c2.column_name r_column_name
                        from user_cons_columns a
                        join user_constraints c on a.constraint_name = c.constraint_name
                        join user_constraints c_pk on c.r_constraint_name = c_pk.constraint_name
                        join user_cons_columns c2 on c_pk.constraint_name = c2.constraint_name
                        where c.constraint_type = 'R'
                        and a.table_name = :tabname
                    )
                    select utc.column_name, json_object(
                        key 'column_name' value utc.column_name
                        , key 'table_name' value ut.table_name
                        , key 'column_datatype' value case utc.data_type
                            when 'CLOB' then 'text'
                            when 'NUMBER' then 'number'
                            when 'VARCHAR2' then 'string'
                            when 'VARCHAR' then 'string'
                            when 'NVARCHAR2' then 'string'
                            when 'CHAR' then 'string'
                            when 'DATE' then 'date'
                            when 'TIMESTAMP(6)' then 'time'
                            when 'TIMESTAMP' then 'time'
                            else 'string'
                        end 
                        , key 'table_level_rowcount' value nvl(ut.num_rows, 0) 
                        , key 'table_level_avg_row_length' value nvl(ut.avg_row_len, 0)
                        , key 'column_level_avg_col_length' value nvl(utc.avg_col_len, 0)
                        , key 'column_data_length' value utc.data_length
                        , key 'column_number_precision' value utc.data_precision
                        , key 'column_number_decimals' value utc.data_scale
                        , key 'column_nullable' value utc.nullable
                        , key 'column_nulls' value utc.num_nulls
                        , key 'column_distinct_count' value utc.num_distinct
                        , key 'column_low_value' value 'Not given'
                        , key 'column_high_value' value 'Not given'
                        , key 'column_is_reference' value case
                            when fr.column_name is not null then 1
                            else 0
                        end
                        , key 'reference_table' value fr.r_table_name
                        , key 'reference_column' value fr.r_column_name
                         absent on null) col_infer_meta
                    from
                        user_tab_cols utc
                        inner join user_tables ut on ut.table_name = utc.table_name
                        left outer join foreign_references fr on fr.table_name = utc.table_name and fr.column_name = utc.column_name
                    where
                        utc.table_name = :tabname
                    order by 
                        utc.column_id asc"""
                self.m("Statement to get column data: " + columns_meta_stmt)
                #self.m("Bind value for stmt: " + table_name.upper())
                working_cursor.execute(columns_meta_stmt, tabname = table_name.upper())
                for col_name, col_infer_meta in working_cursor:
                    self.m("Column to infer: " + col_name)
                    # If we are allowed sample data. Now is the time to fetch individual samples
                    if use_sample_data:
                        sub_sample_cursor = self.connection.cursor()
                        # Merge the sample data.
                        # First parse the main column metadata
                        main_meta = json.loads(col_infer_meta)
                        sub_sample_stmt = "select json_arrayagg(" + str(col_name) + " returning clob) from " + str(table_name) + " sample (" + str(sub_sample_size_cal_cust) +") order by rowid"
                        sub_sample_cursor.execute(sub_sample_stmt)
                        sample_data = sub_sample_cursor.fetchone()
                        # First we get the sample data as a clob string
                        sample_data_clob_str = sample_data[0].read()
                        # Convert to a list so we can add for real.
                        sample_data_clob_str = ast.literal_eval(sample_data_clob_str)
                        # Now add the sample data as a real array.
                        main_meta["sample_values"] = sample_data_clob_str
                        if main_meta["column_is_reference"] == 1:
                            rel_sample_size_cal_cust = self.calculateSampleSize(main_meta["reference_table"])
                            rel_sample_cursor = self.connection.cursor()
                            rel_sample_stmt = """with base_histograms as (select
                                    json_object(
                                        key 'hkv' value {ref_col_name} 
                                        , key 'fcnt' value fcnt
                                        , key 'low_cnt' value first_value(fcnt) ignore nulls over (order by fcnt)
                                        , key 'high_cnt' value last_value(fcnt) ignore nulls over (order by fcnt rows between unbounded preceding and unbounded following)
                                    ) jsobj
                                from (
                                    select
                                    ora_hash(a.{ref_col_name}) {ref_col_name}
                                    , count(b.{col_name}) fcnt
                                    from {ref_tab_name} a
                                    , {tab_name} b
                                    where
                                    a.{ref_col_name} = b.{col_name}
                                    and
                                    a.{ref_col_name} in (
                                        select 
                                        {ref_col_name}
                                        from
                                        {ref_tab_name} sample({ref_sample})
                                    )
                                    group by
                                    a.{ref_col_name}
                                ))
                            select
                                json_arrayagg(jsobj returning clob)
                            from
                                base_histograms""".format(col_name = main_meta["column_name"], tab_name = table_name, ref_col_name = main_meta["reference_column"], ref_tab_name = main_meta["reference_table"], ref_sample = rel_sample_size_cal_cust)
                            self.m("Column is a foreign key. Build relation histogram")
                            self.m("Relation histogram query: " + rel_sample_stmt)
                            rel_sample_cursor.execute(rel_sample_stmt)
                            rel_sample_data = rel_sample_cursor.fetchone()
                            self.m("Foreign key histogram: ")
                            self.m(rel_sample_data)
                            rel_sample_data_clob_str = rel_sample_data[0].read()
                            rel_sample_data_clob_str = ast.literal_eval(rel_sample_data_clob_str)
                            main_meta["reference_histogram"] = rel_sample_data_clob_str
                    else:
                        main_meta = json.loads(col_infer_meta)
                    # We now have every column and its metadata. Send to API endpoint to do intelligent infer.
                    # We get back the entire json of inferred column
                    # Init column
                    self.template.init_column(column_name=col_name)
                    # Try calling infer endpoint
                    self.m("Infer: " + json.dumps(main_meta))
                    x_response = self.binuObj.infer_generator(json.dumps(main_meta))
                    self.m(x_response)
                    # The response is the column json as a string format. Call replace_column_from_json
                    self.template.replace_column_from_json(col_name, json.dumps(x_response))
                # Once we are done, we can validate the template and return it.
                self.template.validate_template()
                self.template.complete_template()
                return self.template.template_JSON

    def columnGeneratorComments(self, table_name, comments, override=False):
        if self.connected:
            comment_count_sql = "select count(*) from user_col_comments where table_name = :tabname"
            working_cursor = self.connection.cursor()
            working_cursor.execute(comment_count_sql, tabname = table_name.upper())
            cursor_result = working_cursor.fetchone()
            if (cursor_result[0] > 0 or not override) or (cursor_result[0] == 0):
                # Let us go ahead and set comment generators as requested.
                if (comments.find('=') > 0):
                    # Named notation
                    for cn in comments.split(","):
                        colname = cn.split("=")[0].strip()
                        colcomment = cn.split("=")[1].strip()
                        col_add_stmt = "comment on column " + table_name + "." + colname + " is '" + colcomment + "'"
                        working_cursor.execute(col_add_stmt)
                else:
                    # Just split and follow column order. Ignore any column outside of split length
                    ordered_col_cursor = self.connection.cursor()
                    ordered_col_sql = "select column_id, column_name from user_tab_cols where table_name = :tabname order by column_id asc"
                    ordered_col_cursor.execute(ordered_col_sql, tabname = table_name.upper())
                    for cid, cname in ordered_col_cursor:
                        try:
                            colcomment = comments.split(",")[cid - 1]
                            col_add_stmt = "comment on column " + table_name + "." + cname + " is '" + colcomment + "'"
                            working_cursor.execute(col_add_stmt)
                        except:
                            # Aint no comment for this column. Just ignore
                            pass

    def quick_fetch_table(self
            , table_name, use_comments=True, use_infer=False
            , use_sample_data=False, use_tuple_return=False
            , output_csv=False, output_type="screen", output_name="same"
            , rows="same"):
        self.template = BinubuoTemplate()
        assert_table_sql = "select dbms_assert.sql_object_name(:tabname) from dual"
        assert_table_cursor = self.connection.cursor()
        table_exist = False
        try:
            assert_table_cursor.execute(assert_table_sql, tabname = table_name.upper())
            self.templateTable = table_name.upper()
            table_exist = True
        except:
            self.m("Table name entered does not exist. templateFromTable can only be used on existing tables.")
        # Table exists
        if table_exist:
            quick_fetch_columns_array = []
            if not use_infer:
                # No webservice call to generate template.
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = """select
                        utc.column_name
                        , case utc.data_type
                            when 'NUMBER' then 'number'
                            when 'VARCHAR2' then 'string'
                            when 'NVARCHAR2' then 'string'
                            when 'DATE' then 'date'
                            when 'TIMESTAMP' then 'time'
                            when 'TIMESTAMP(6)' then 'time'
                            else 'string'
                        end as column_data_type
                        , case
                            when utc.data_type = 'NUMBER' and utc.avg_col_len = 3 and utc.num_distinct <=2 then 'numeric_on_off'
                            when utc.data_type = 'NUMBER' and utc.avg_col_len < 4 then 'small_number'
                            when utc.data_type = 'NUMBER' and utc.avg_col_len < 6 then 'medium_number'
                            when utc.data_type = 'NUMBER' and utc.avg_col_len > 5 then 'large_number'
                            when utc.data_type = 'FLOAT' and utc.avg_col_len < 4 then 'small_amount'
                            when utc.data_type = 'FLOAT' and utc.avg_col_len < 6 then 'medium_amount'
                            when utc.data_type = 'FLOAT' and utc.avg_col_len > 5 then 'large_amount'
                            when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 10 and utc.num_distinct <=5 and ut.num_rows > 100 then 'flow_status'
                            when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 30 and utc.num_distinct > round(ut.num_rows*0.7) then 'full_name'
                            when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 10 then 'medium_word'
                            when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len > 20 then 'large_word'
                            when utc.data_type = 'DATE' then 'date'
                            when utc.data_type = 'TIMESTAMP' then 'timestamp'
                            when utc.data_type = 'TIMESTAMP(6)' then 'timestamp'
                            else 'word'
                        end as column_def_generator
                        , ucc.comments 
                        , ut.num_rows
                        , utc.num_nulls
                        , utc.num_distinct
                        , utc.nullable
                        , utc.avg_col_len
                    from
                        user_tab_columns utc
                        inner join user_tables ut on ut.table_name = utc.table_name
                        left outer join user_col_comments ucc on utc.table_name = ucc.table_name and utc.column_name = ucc.column_name 
                    where
                        utc.table_name = :tabname
                    order by 
                        utc.column_id asc"""
                working_cursor.execute(generic_column_meta_sql, tabname = table_name.upper())
                for cname, cdtype, cdgenerator, ccomment, crows, cnumnulls, cnumdist, cnullable, cavglen in working_cursor:
                    self.template.init_column(column_name=cname, column_type="generated", column_datatype=cdtype)
                    if ccomment is not None and use_comments:
                        quick_fetch_columns_array.append(ccomment)
                    else:
                        quick_fetch_columns_array.append(cdgenerator)
                # Once we are done, we can call the quick fetch.
                quick_fetch_columns = ",".join(quick_fetch_columns_array)
                # Before fetching, set rows if needed.
                if rows == "same":
                    # TODO: Set to current rowcount
                    self.binuObj.drows(10)
                else:
                    try:
                        self.binuObj.drows(int(rows))
                    except:
                        self.binuObj.drows()
                if use_tuple_return or output_type.lower() == "table":
                    tuple_value = "tuple"
                else:
                    tuple_value = "list"
                if output_csv:
                    self.binuObj.csv(1)
                if output_name == "same":
                    output_name_real = table_name
                else:
                    output_name_real = output_name
                if output_type.lower() == "screen" or output_type.lower() == "table":
                    resp_cols = self.binuObj.quick_fetch(quick_fetch_columns, tuple_value)
                    self.m("Length is: " + str(len(resp_cols)))
                    self.m(resp_cols)
                    if output_type.lower() == "screen":
                        return resp_cols
                    else:
                        # We need to insert.
                        quick_insert_stmt = self.build_insert_statement(table_name, output_name_real)
                        quick_insert_cursor = self.connection.cursor()
                        quick_insert_cursor.executemany(quick_insert_stmt, resp_cols)
                        self.connection.commit()
                elif output_type.lower() == "file":
                    self.binuObj.quick_fetch_to_file(quick_fetch_columns, output_name_real)
                # Reset required vals
                self.binuObj.csv()
                self.binuObj.drows()

    def dataset_from_table(self, table_name, use_comments=True, use_infer=False, use_sample_data=False):
        dset_template = self.templateFromTable(table_name, use_comments, use_infer, use_sample_data)
        # Create or replace the dataset
        self.binuObj.create_dataset(table_name, dset_template)

    def build_insert_statement(self, source_table, target_table=None):
        insert_stmt_cursor = self.connection.cursor()
        build_insert_stmt = """select 
                    '(' || listagg(column_name, ',') within group (order by column_id asc) || ') values (' || listagg(':c' ||rownum, ',') within group (order by column_id asc) || ')'
                from user_tab_cols
                where table_name = :tabname
                order by
                    column_id"""
        insert_stmt_cursor.execute(build_insert_stmt, tabname=source_table.upper())
        cursor_result = insert_stmt_cursor.fetchone()
        if target_table is not None:
            insert_stmt = "insert into " + target_table.lower() + " " + cursor_result[0]
        else:
            insert_stmt = "insert into " + source_table.lower() + " " + cursor_result[0]
        self.m("Insert stmt: " + insert_stmt)
        return insert_stmt

    def ddl_from_table(self, table_name):
        ddl_cursor = self.connection.cursor()
        ddl_stmt = """begin
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'SQLTERMINATOR', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'PRETTY', true);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'SEGMENT_ATTRIBUTES', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'STORAGE', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'CONSTRAINTS', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'REF_CONSTRAINTS', false);
            dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'EMIT_SCHEMA', false);
        end;"""
        # Set the transformation rules for DDL extraction.
        ddl_cursor.execute(ddl_stmt)
        # Extract DDL
        ddl_stmt = """select dbms_metadata.get_ddl('TABLE', :tabname)
            from dual"""
        ddl_cursor.execute(ddl_stmt, tabname = table_name.upper())
        ddl_out_str = ddl_cursor.fetchone()
        ddl_out_str = ddl_out_str[0].read()
        return ddl_out_str

    def copy_table(self, source_table, target_table=None, copy_method="quickfetch"
            , drop_target_if_exist=False, alternate_dataset_name=False
            , use_comments=True, use_infer=False, use_sample_data=False
            , data_rows="source", target_db=None):
        assert_table_sql = "select dbms_assert.sql_object_name(:tabname) from dual"
        # SOURCE work
        assert_table_cursor = self.connection.cursor()
        working_cursor = self.connection.cursor()
        if target_db is None:
            target_assert_cursor = self.connection.cursor()
            target_work_cursor = self.connection.cursor()
        else:
            target_assert_cursor = self.secondary_connection.cursor()
            target_work_cursor = self.secondary_connection.cursor()
        source_table_exist = False
        target_table_exist = True
        try:
            assert_table_cursor.execute(assert_table_sql, tabname = source_table.upper())
            source_table_exist = True
        except:
            self.m("Source table does not exist.")
        # TARGET work
        # If target_table is none, we will create a copy with same name plus '_copy' appended to it.
        if target_table is None:
            loc_target_table = source_table + "_copy"
        else:
            loc_target_table = target_table
        try:
            target_assert_cursor.execute(assert_table_sql, tabname = loc_target_table.upper())
            target_table_exist = True
            if drop_target_if_exist:
                remove_target_stmt = "drop table " + loc_target_table.lower() + " purge"
                self.m("Dropping target with stmt: " + remove_target_stmt)
                target_work_cursor.execute(remove_target_stmt)
            else:
                self.m("Target table exist cannot create.")
        except:
            target_table_exist = False
        if source_table_exist and not target_table_exist:
            # Source is there and target is not there. Good to go.
            # First we create an empty copy table
            # If local database we can use create as select ...
            # If secondary database, we do extract DDL
            if target_db is None:
                table_ddl = "create table " + loc_target_table.lower() + " as select * from " + source_table.lower() + " where 1=2"
            else:
                # We need to extract from primary the stmt to build in secondary
                table_ddl = self.ddl_from_table(source_table.upper())
                # Now we just need to replace tablename, since the DDL will be source table name
                table_ddl = table_ddl.replace('"' + source_table.upper() + '"', '"' + loc_target_table.upper() + '"')
            self.m("Create table stmt: " + table_ddl)
            target_work_cursor.execute(table_ddl)
            # Table created. Build insert stmt
            insert_stmt = self.build_insert_statement(source_table, loc_target_table)
            self.m("Insert stmt: " + insert_stmt)
            # Set the rows
            if data_rows == "source":
                # Get the rowcount in the source table.
                pass
            else:
                try:
                    self.binuObj.drows(int(data_rows))
                except:
                    self.binuObj.drows(int(10))
            # Get new rows.
            if copy_method == "quickfetch":
                rows_bind = self.quick_fetch_table(table_name=source_table, use_tuple_return=True)
                self.m("Rows returned for insert: " + str(len(rows_bind)))
                target_work_cursor.executemany(insert_stmt, rows_bind)
            elif copy_method == "dataset":
                if not alternate_dataset_name:
                    # Expect dataset name to be same as source table.
                    dset_name = source_table
                else:
                    dset_name = alternate_dataset_name
                # Create the dataset, if it does not exist
                # TODO: Check if it exists
                self.dataset_from_table(dset_name, use_comments, use_infer, use_sample_data)
                # Call the dataset for the rows.
                rows_bind = self.binuObj.dataset(dataset_name=dset_name, response_type="tuple")
                self.m("Rows returned for insert: " + str(len(rows_bind)))
                target_work_cursor.executemany(insert_stmt, rows_bind)
            if target_db is None:
                self.connection.commit()
            else:
                self.secondary_connection.commit()

