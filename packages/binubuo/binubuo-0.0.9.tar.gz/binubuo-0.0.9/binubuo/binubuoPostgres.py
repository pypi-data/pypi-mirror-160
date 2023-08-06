import psycopg2
import sys
import json
import ast
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

class binubuoPostgres:
    def __init__(self, binubuokey, dbname=None, dbuser=None, dbpwd=None, dbfullConnection=None):
        self.binubuokey = binubuokey
        self.dbuser = dbuser
        self.dbpwd = dbpwd
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
                if self.dbpwd is None:
                    self.connection = psycopg2.connect(dbname=self.dbname, user=self.dbuser)
                else:
                    self.connection = psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpwd)
            else:
                self.connection = self.dbfullConnection
            self.connected = True
        except:
            self.m("Error: Failed to connect to database. Please make sure you have a connection before using other methods.")
            self.connection = None

    def connectSecondary(self, dbname, dbuser, dbpwd=None, dbfullConnection=None):
        try:
            if dbfullConnection is None:
                if dbpwd is None:
                    self.secondary_connection = psycopg2.connect(dbname=dbname, user=dbuser)
                else:
                    self.secondary_connection = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpwd)
            else:
                self.secondary_connection = dbfullConnection
            self.connected_secondary = True
        except:
            self.m("Error: Failed to connect to secondary/alternate database. Please check your connection details and try again.")
            self.secondary_connection = None

    def columnGeneratorComments(self, table_name, comments, override=False):
        if self.connected:
            comment_count_sql = """SELECT
                    count(
                    (
                        SELECT
                            pg_catalog.col_description(c.oid, cols.ordinal_position::int)
                        FROM pg_catalog.pg_class c
                        WHERE
                            c.oid     = (SELECT cols.table_name::regclass::oid) AND
                            c.relname = cols.table_name
                    ))

                FROM information_schema.columns cols
                WHERE
                    cols.table_name = %s"""
            working_cursor = self.connection.cursor()
            working_cursor.execute(comment_count_sql, (table_name,))
            cursor_result = working_cursor.fetchone()
            self.m("Comments: " + str(cursor_result[0]))
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
                    ordered_col_sql = "select ordinal_position, column_name from information_schema.columns cols where cols.table_name = %s order by ordinal_position asc"
                    ordered_col_cursor.execute(ordered_col_sql, (table_name,))
                    for cid, cname in ordered_col_cursor:
                        self.m("Working on col: " + cname)
                        try:
                            colcomment = comments.split(",")[cid - 1]
                            col_add_stmt = "comment on column " + table_name + "." + cname + " is '" + colcomment + "';"
                            self.m("Comment command: " + col_add_stmt)
                            working_cursor.execute(col_add_stmt)
                        except:
                            # Aint no comment for this column. Just ignore
                            pass
                self.connection.commit()

    def calculateSampleSize(self, table_name):
        sub_sample_cursor = self.connection.cursor()
        sub_sample_size_stmt = "select n_live_tup from pg_stat_user_tables where relname = %s"
        sub_sample_cursor.execute(sub_sample_size_stmt, (table_name,))
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
        assert_table_sql = "select exists (select from information_schema.tables where table_name = %s)"
        assert_table_cursor = self.connection.cursor()
        table_exist = False
        assert_table_cursor.execute(assert_table_sql, (table_name,))
        cursor_result = assert_table_cursor.fetchone()
        if cursor_result[0]:
            self.template = BinubuoTemplate()
            self.templateTable = table_name
            table_exist = True
        else:
            self.m("Table name entered does not exist. templateFromTable can only be used on existing tables.")
            quit()
        # Table exists
        if table_exist:
            if not use_infer:
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = """select
                        cols.column_name
                        , case cols.data_type
                            when 'integer' then 'number'
                            when 'double precision' then 'number'
                            when 'character varying' then 'string'
                            when 'character' then 'string'
                            when 'text' then 'text'
                            when 'money' then 'number'
                            when 'date' then 'date'
                            when 'timestamp without time zone' then 'time'
                            when 'timestamp with time zone' then 'time'
                            when 'time without time zone' then 'time'
                            when 'time with time zone' then 'time'
                            when 'bigint' then 'number'
                            when 'real' then 'number'
                            when 'smallint' then 'number'
                            else 'string'
                        end column_data_type
                        , case
                            when cols.data_type = 'integer' and cstats.n_distinct between 1 and 2 then 'numeric_on_off'
                            when cols.data_type = 'integer' then 'small_number'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 10 and cstats.n_distinct between 1 and 5 then 'flow_status'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 30 and (case when cstats.n_distinct <= -.9 then sut.n_live_tup else cstats.n_distinct end) > round(sut.n_live_tup*0.7) then 'full_name'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 10 then 'medium_word'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width > 20 then 'large_word'
                            when cols.data_type = 'money' then 'medium_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width < 4 then 'small_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width < 6 then 'medium_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width > 5 then 'large_amount'
                            when cols.data_type = 'date' then 'date'
                            when cols.data_type in ('timestamp without time zone', 'timestamp with time zone') then 'timestamp'
                            when cols.data_type in ('time without time zone', 'time with time zone') then 'time'
                            when cols.data_type in ('bigint', 'real', 'smallint') then 'small_number'
                            when cols.data_type = 'boolean' then 'boolean'
                            else 'word'
                        end column_def_generator
                        , (
                            select
                                pg_catalog.col_description(c.oid, cols.ordinal_position::int)
                            from 
                                pg_catalog.pg_class c
                            where
                                c.oid = (select cols.table_name::regclass::oid) 
                            and
                                c.relname = cols.table_name
                        ) as column_comment
                        , sut.n_live_tup as num_rows
                        , case
                            when cstats.null_frac > 0 then greatest(round(sut.n_live_tup*cstats.null_frac), 1)
                            else 0
                        end num_nulls
                        , case
                            when cstats.n_distinct <= -.9 then sut.n_live_tup
                            when cstats.n_distinct < 0 and cstats.n_distinct > -.9 then round(sut.n_live_tup*0.9)
                            else cstats.n_distinct
                        end num_distinct
                        , cols.is_nullable
                        , cstats.avg_width
                    from
                        information_schema.columns cols
                        inner join pg_stat_user_tables sut on sut.relname = cols.table_name
                        left outer join pg_stats cstats on cstats.attname = cols.column_name and cstats.tablename = cols.table_name
                    where
                        cols.table_name = %s
                    order by
                        cols.ordinal_position asc;"""
                working_cursor.execute(generic_column_meta_sql, (table_name,))
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
                if use_sample_data:
                    sub_sample_size_cal_cust = self.calculateSampleSize(table_name)
                working_cursor = self.connection.cursor()
                if use_sample_data:
                    columns_meta_stmt = """with foreign_references as (SELECT
                            tc.table_schema,
                            tc.constraint_name,
                            tc.table_name,
                            kcu.column_name,
                            ccu.table_schema AS foreign_table_schema,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM
                            information_schema.table_constraints AS tc     
                            JOIN information_schema.key_column_usage AS kcu      ON tc.constraint_name = kcu.constraint_name      AND tc.table_schema = kcu.table_schema    
                            JOIN information_schema.constraint_column_usage AS ccu      ON ccu.constraint_name = tc.constraint_name      AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY' 
                        AND tc.table_name = %s
                        )
                    select
                        cols.column_name
                        , json_strip_nulls(json_build_object(
                            'column_name'
                            , cols.column_name
                            , 'table_name'
                            , cols.table_name
                            , 'column_datatype'
                            , case cols.data_type
                                when 'integer' then 'number'
                                when 'double precision' then 'number'
                                when 'character varying' then 'string'
                                when 'character' then 'string'
                                when 'text' then 'text'
                                when 'money' then 'number'
                                when 'date' then 'date'
                                when 'timestamp without time zone' then 'time'
                                when 'timestamp with time zone' then 'time'
                                when 'time without time zone' then 'time'
                                when 'time with time zone' then 'time'
                                when 'bigint' then 'number'
                                when 'real' then 'number'
                                when 'smallint' then 'number'
                                else 'string'
                            end
                            , 'table_level_rowcount'
                            , coalesce(sut.n_live_tup, 0)
                            , 'table_level_avg_row_length'
                            , 0
                            , 'column_level_avg_col_length'
                            , coalesce(cstats.avg_width, 0)
                            , 'column_data_length'
                            , case
                                when cols.character_maximum_length is not null then cols.character_maximum_length
                                else null
                            end 
                            , 'column_number_precision'
                            , cols.numeric_precision 
                            , 'column_number_decimals'
                            , cols.numeric_scale 
                            , 'column_nullable'
                            , cols.is_nullable
                            , 'column_nulls'
                            , case
                                when cstats.null_frac > 0 then greatest(round(sut.n_live_tup*cstats.null_frac), 1)
                                else 0
                            end
                            , 'column_distinct_count'
                            , case
                                when cstats.n_distinct <= -.9 then sut.n_live_tup
                                when cstats.n_distinct < 0 and cstats.n_distinct > -.9 then round(sut.n_live_tup*0.9)
                                else cstats.n_distinct
                            end
                            , 'column_low_value'
                            , 'Not extractable'
                            , 'column_high_value'
                            , 'Not extractable'
                            , 'column_is_reference'
                            , case
                                when fr.column_name is not null then 1
                                else 0
                            end
                            , 'reference_table'
                            , fr.foreign_table_name
                            , 'reference_column'
                            , fr.foreign_column_name
                        ))
                    from
                        information_schema.columns cols
                        inner join pg_stat_user_tables sut on sut.relname = cols.table_name
                        left outer join pg_stats cstats on cstats.attname = cols.column_name and cstats.tablename = cols.table_name
                        left outer join foreign_references fr on fr.table_name = cols.table_name and fr.column_name = cols.column_name
                    where
                        cols.table_name = %s
                    order by
                        cols.ordinal_position asc"""
                else:
                    columns_meta_stmt = """with foreign_references as (SELECT
                            tc.table_schema,
                            tc.constraint_name,
                            tc.table_name,
                            kcu.column_name,
                            ccu.table_schema AS foreign_table_schema,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM
                            information_schema.table_constraints AS tc     
                            JOIN information_schema.key_column_usage AS kcu      ON tc.constraint_name = kcu.constraint_name      AND tc.table_schema = kcu.table_schema    
                            JOIN information_schema.constraint_column_usage AS ccu      ON ccu.constraint_name = tc.constraint_name      AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY' 
                        AND tc.table_name = %s
                        )
                    select
                        cols.column_name
                        , json_strip_nulls(json_build_object(
                            'column_name'
                            , cols.column_name
                            , 'table_name'
                            , cols.table_name
                            , 'column_datatype'
                            , case cols.data_type
                                when 'integer' then 'number'
                                when 'double precision' then 'number'
                                when 'character varying' then 'string'
                                when 'character' then 'string'
                                when 'text' then 'text'
                                when 'money' then 'number'
                                when 'date' then 'date'
                                when 'timestamp without time zone' then 'time'
                                when 'timestamp with time zone' then 'time'
                                when 'time without time zone' then 'time'
                                when 'time with time zone' then 'time'
                                when 'bigint' then 'number'
                                when 'real' then 'number'
                                when 'smallint' then 'number'
                                else 'string'
                            end
                            , 'table_level_rowcount'
                            , coalesce(sut.n_live_tup, 0)
                            , 'table_level_avg_row_length'
                            , 0
                            , 'column_level_avg_col_length'
                            , coalesce(cstats.avg_width, 0)
                            , 'column_data_length'
                            , case
                                when cols.character_maximum_length is not null then cols.character_maximum_length
                                else null
                            end 
                            , 'column_number_precision'
                            , cols.numeric_precision 
                            , 'column_number_decimals'
                            , cols.numeric_scale 
                            , 'column_nullable'
                            , cols.is_nullable
                            , 'column_nulls'
                            , case
                                when cstats.null_frac > 0 then greatest(round(sut.n_live_tup*cstats.null_frac), 1)
                                else 0
                            end
                            , 'column_distinct_count'
                            , case
                                when cstats.n_distinct <= -.9 then sut.n_live_tup
                                when cstats.n_distinct < 0 and cstats.n_distinct > -.9 then round(sut.n_live_tup*0.9)
                                else cstats.n_distinct
                            end
                            , 'column_low_value'
                            , 'Not given'
                            , 'column_high_value'
                            , 'Not given'
                            , 'column_is_reference'
                            , case
                                when fr.column_name is not null then 1
                                else 0
                            end
                            , 'reference_table'
                            , fr.foreign_table_name
                            , 'reference_column'
                            , fr.foreign_column_name
                        )) col_infer_meta
                    from
                        information_schema.columns cols
                        inner join pg_stat_user_tables sut on sut.relname = cols.table_name
                        left outer join pg_stats cstats on cstats.attname = cols.column_name and cstats.tablename = cols.table_name
                        left outer join foreign_references fr on fr.table_name = cols.table_name and fr.column_name = cols.column_name
                    where
                        cols.table_name = %s
                    order by
                        cols.ordinal_position asc;"""
                working_cursor.execute(columns_meta_stmt, (table_name, table_name,))
                for col_name, col_infer_meta in working_cursor:
                    self.m("Column to infer: " + col_name)
                    self.m("Infer: " + col_infer_meta["table_name"])
                    main_meta = col_infer_meta
                    if use_sample_data:
                        sub_sample_cursor = self.connection.cursor()
                        # Merge the sample data.
                        sub_sample_stmt = "select json_agg(" + str(col_name) + " order by o_idr asc)  from (select cast(xmin::text as integer) as o_idr, " + str(col_name) + " from " + str(table_name) + "  tablesample system (" + str(sub_sample_size_cal_cust) +") where " + str(col_name) + " is not null order by cast(xmin::text as integer) asc) as ctid_ordr;"
                        sub_sample_cursor.execute(sub_sample_stmt)
                        for sample_data_array in sub_sample_cursor:
                            # Now add the sample data as a real array.
                            if sample_data_array[0] is not None:
                                main_meta["sample_values"] = sample_data_array[0]
                        if main_meta["column_is_reference"] == 1:
                            rel_sample_size_cal_cust = self.calculateSampleSize(main_meta["reference_table"])
                            rel_sample_cursor = self.connection.cursor()
                            rel_sample_stmt = """with base_histograms as (select
                                    json_strip_nulls(json_build_object(
                                        'hashed_key'
                                        , {ref_col_name}
                                        , 'fcnt'
                                        , fcnt
                                        , 'low_cnt'
                                        , first_value(fcnt) over (order by fcnt)
                                        , 'high_cnt'
                                        , last_value(fcnt) over (order by fcnt rows between unbounded preceding and unbounded following)
                                    )) jsobj
                                  from (
                                    select
                                      md5(cast(a.{ref_col_name} as text)) {ref_col_name}
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
                                          {ref_tab_name} tablesample system ({ref_sample})
                                      )
                                    group by
                                      a.{ref_col_name}
                                  ) sq2
                                )
                                select
                                    json_agg(jsobj)
                                from
                                    base_histograms;""".format(col_name = main_meta["column_name"], tab_name = table_name, ref_col_name = main_meta["reference_column"], ref_tab_name = main_meta["reference_table"], ref_sample = rel_sample_size_cal_cust)
                            # Fill in the histogram data
                            self.m("Column is a foreign key. Build relation histogram")
                            self.m("Relation histogram query: " + rel_sample_stmt)
                            rel_sample_cursor.execute(rel_sample_stmt)
                            for ref_sample_data_array in rel_sample_cursor:
                                if ref_sample_data_array[0] is not None:
                                    self.m("Foreign key histogram: ")
                                    self.m(ref_sample_data_array[0])
                                    main_meta["reference_histogram"] = ref_sample_data_array[0]
                    # We get back the entire json of inferred column
                    # Init column and call infer endpoint
                    self.template.init_column(column_name=col_name)
                    self.m("Infer: " + json.dumps(main_meta))
                    x_response = self.binuObj.infer_generator(json.dumps(main_meta))
                    self.m(x_response)
                    # The response is the column json as a string format. Call replace_column_from_json
                    self.template.replace_column_from_json(col_name, json.dumps(x_response))
                # Once we are done, we can validate the template and return it.
                self.template.validate_template()
                self.template.complete_template()
                return self.template.template_JSON


    def quick_fetch_table(self
            , table_name, use_comments=True, use_infer=False
            , use_sample_data=False, use_tuple_return=False
            , output_csv=False, output_type="screen", output_name="same"
            , rows="same"):
        assert_table_sql = "select exists (select from information_schema.tables where table_name = %s)"
        assert_table_cursor = self.connection.cursor()
        table_exist = False
        assert_table_cursor.execute(assert_table_sql, (table_name,))
        cursor_result = assert_table_cursor.fetchone()
        if cursor_result[0]:
            self.template = BinubuoTemplate()
            self.templateTable = table_name
            table_exist = True
        else:
            self.m("Table name entered does not exist. templateFromTable can only be used on existing tables.")
            quit()
        # Table exists
        if table_exist:
            quick_fetch_columns_array = []
            if not use_infer:
                # No webservice call to generate template.
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = """select
                        cols.column_name
                        , case cols.data_type
                            when 'integer' then 'number'
                            when 'double precision' then 'number'
                            when 'character varying' then 'string'
                            when 'character' then 'string'
                            when 'text' then 'text'
                            when 'money' then 'number'
                            when 'date' then 'date'
                            when 'timestamp without time zone' then 'time'
                            when 'timestamp with time zone' then 'time'
                            when 'time without time zone' then 'time'
                            when 'time with time zone' then 'time'
                            when 'bigint' then 'number'
                            when 'real' then 'number'
                            when 'smallint' then 'number'
                            else 'string'
                        end column_data_type
                        , case
                            when cols.data_type = 'integer' and cstats.n_distinct between 1 and 2 then 'numeric_on_off'
                            when cols.data_type = 'integer' then 'small_number'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 10 and cstats.n_distinct between 1 and 5 then 'flow_status'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 30 and (case when cstats.n_distinct <= -.9 then sut.n_live_tup else cstats.n_distinct end) > round(sut.n_live_tup*0.7) then 'full_name'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 10 then 'medium_word'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width > 20 then 'large_word'
                            when cols.data_type = 'money' then 'medium_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width < 4 then 'small_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width < 6 then 'medium_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width > 5 then 'large_amount'
                            when cols.data_type = 'date' then 'date'
                            when cols.data_type in ('timestamp without time zone', 'timestamp with time zone') then 'timestamp'
                            when cols.data_type in ('time without time zone', 'time with time zone') then 'time'
                            when cols.data_type in ('bigint', 'real', 'smallint') then 'small_number'
                            when cols.data_type = 'boolean' then 'boolean'
                            else 'word'
                        end column_def_generator
                        , (
                            select
                                pg_catalog.col_description(c.oid, cols.ordinal_position::int)
                            from 
                                pg_catalog.pg_class c
                            where
                                c.oid = (select cols.table_name::regclass::oid) 
                            and
                                c.relname = cols.table_name
                        ) as column_comment
                        , sut.n_live_tup as num_rows
                        , case
                            when cstats.null_frac > 0 then greatest(round(sut.n_live_tup*cstats.null_frac), 1)
                            else 0
                        end num_nulls
                        , case
                            when cstats.n_distinct <= -.9 then sut.n_live_tup
                            when cstats.n_distinct < 0 and cstats.n_distinct > -.9 then round(sut.n_live_tup*0.9)
                            else cstats.n_distinct
                        end num_distinct
                        , cols.is_nullable
                        , cstats.avg_width
                    from
                        information_schema.columns cols
                        inner join pg_stat_user_tables sut on sut.relname = cols.table_name
                        left outer join pg_stats cstats on cstats.attname = cols.column_name and cstats.tablename = cols.table_name
                    where
                        cols.table_name = %s
                    order by
                        cols.ordinal_position asc;"""
                working_cursor.execute(generic_column_meta_sql, (table_name,))
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
                table_name
                , '(' || string_agg(column_name, ',' ORDER BY ordinal_position) || ') values (' || string_agg('d_d_s_r', ',' ORDER BY ordinal_position) || ')' as ins_stmt
            from information_schema.columns 
            where table_name = %s
            group by table_name"""
        insert_stmt_cursor.execute(build_insert_stmt, (source_table,))
        cursor_result = insert_stmt_cursor.fetchone()
        if target_table is not None:
            insert_stmt = "insert into " + target_table + " " + cursor_result[1]
        else:
            insert_stmt = "insert into " + source_table + " " + cursor_result[1]
        insert_stmt = insert_stmt.replace("d_d_s_r", "%s")
        self.m("Insert stmt: " + insert_stmt)
        return insert_stmt

    def copy_table(self, source_table, target_table=None, copy_method="quickfetch"
            , drop_target_if_exist=False, alternate_dataset_name=False
            , use_comments=True, use_infer=False, use_sample_data=False
            , data_rows="source"):
        assert_table_sql = "select exists (select from information_schema.tables where table_name = %s)"
        assert_table_cursor = self.connection.cursor()
        source_table_exist = False
        target_table_exist = True
        self.m("Before cursor check source")
        working_cursor = self.connection.cursor()
        assert_table_cursor.execute(assert_table_sql, (source_table,))
        cursor_result = assert_table_cursor.fetchone()
        if cursor_result[0]:
            self.template = BinubuoTemplate()
            self.templateTable = source_table
            source_table_exist = True
            self.m("Source exists")
        else:
            self.m("Source table name entered does not exist. copy_table can only be used on existing tables.")
            quit()
        # If target_table is none, we will create a copy with same name plus '_copy' appended to it.
        if target_table is None:
            loc_target_table = source_table + "_copy"
        else:
            loc_target_table = target_table
        try:
            assert_table_cursor.execute(assert_table_sql, (loc_target_table,))
            if cursor_result[0]:
                self.m("Target table exist cannot create:")
                target_table_exist = True
                if drop_target_if_exist:
                    remove_target_stmt = "drop table " + loc_target_table.lower()
                    self.m("Dropping target with stmt: " + remove_target_stmt)
                    working_cursor.execute(remove_target_stmt)
                    self.connection.commit()
                    target_table_exist = False
            else:
                self.m("Target table does not exist.")
                target_table_exist = False
        except:
            target_table_exist = False
        self.m("Just before main continue check")
        if source_table_exist and not target_table_exist:
            # Source is there and target is not there. Good to go.
            # First we create an empty copy table
            copy_stmt = "create table " + loc_target_table.lower() + " as select * from " + source_table.lower() + " where 1=2"
            self.m("Create table stmt: " + copy_stmt)
            working_cursor.execute(copy_stmt)
            self.connection.commit()
            # Table created. Build insert stmt
            insert_stmt = self.build_insert_statement(source_table, loc_target_table)
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
                working_cursor.executemany(insert_stmt, rows_bind)
                self.connection.commit()
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
                working_cursor.executemany(insert_stmt, rows_bind)
                self.connection.commit()