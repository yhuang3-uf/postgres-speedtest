import csv
import os
import pathlib
import random
import sys
import time
import typing

import psycopg

def rand_str(identifiers_list: list[str]) -> str:
    """
    Generates a random string between 3 and 12 characters.
    The string will only contain lowercase ASCII symbols.

    The string will be appended to identifiers_list

    :param identifiers_list: A list of identifiers.
    :return: A string with length in [5, 12].
    """
    out_bytearray: bytearray = bytearray()
    for _ in range(random.randint(5, 12)):
        out_bytearray.append(random.randint(0x61, 0x7a))
    out_str: str = out_bytearray.decode("ascii")
    identifiers_list.append(out_str)
    return out_str

def create_test_queries() -> list[str]:
    """
    Creates the test queries
    """
    valid_types: tuple[str, ...] = ("INTEGER", "VARCHAR(50)")
    created_strs: list[str] = []
    output_queries: list[str] = []

    # The number of tables to create and the number of entries to
    # insert into each table.
    num_tables: int = 3
    num_inserts_per_table: int = 5
    num_queries: int = int(os.environ["PGTEST_QUERYCOUNT"].strip())

    sql_tables: dict[str, dict[str, str]] = {}

    def rand_col_value(col_type: str) -> str:
        """
        Gets a random column value

        :param col_type: The type of the column
        :return: A random value for the column
        """
        nonlocal created_strs
        if col_type == "INTEGER":
            return str(random.randint(1,200))
        elif col_type == "VARCHAR(50)":
            return "'" + rand_str(created_strs) + "'"
        raise ValueError("Invalid value for col_type \"" + str(col_type) + "\"")

    for _ in range(num_tables):
        sql_table: dict[str, str] = {}
        for _ in range(random.randint(2, 8)):
            sql_table[rand_str([])] = random.choice(valid_types)
        sql_tables[rand_str([])] = sql_table

    for sql_table_name, sql_table_columns in sql_tables.items():
        primary_key_name: str = rand_str([])
        create_table_stmt: str = "CREATE TABLE " + sql_table_name + "("
        for sql_column_name, sql_column_type in sql_table_columns.items():
            create_table_stmt += sql_column_name + " " + sql_column_type + ", "
        create_table_stmt += primary_key_name + " SERIAL PRIMARY KEY);"
        output_queries.append(create_table_stmt)
        for _ in range(num_inserts_per_table):
            table_insert_cols: list[str] = []
            table_insert_vals: list[str] = []
            for sql_column_name, sql_column_type in sql_table_columns.items():
                table_insert_cols.append(sql_column_name)
                table_insert_vals.append(rand_col_value(sql_column_type))
            output_queries.append("INSERT INTO " + sql_table_name + " (" + 
                    ",".join(table_insert_cols) + ") VALUES (" + 
                    ",".join(table_insert_vals) + ");")

    def where(sql_table_name: str) -> str:
        """
        :param sql_table_name: Name of the SQL table to get the WHERE clause
        for
        :return: The WHERE clause
        """
        nonlocal sql_tables
        sql_table_cols: dict[str, str] = sql_tables[sql_table_name]
        out_where_clause: str = ""
        where_clause_col: str = random.choice(list(sql_table_cols))
        where_clause_val: str = " = '" + random.choice(created_strs) + "'"
        if sql_table_cols[where_clause_col] == "INTEGER":
            where_clause_val = random.choice("<=>") + str(random.randint(1, 200))
        out_where_clause += where_clause_col + where_clause_val + \
                random.choice((" OR ", " AND "))

        where_clause_col = random.choice(list(sql_table_cols))
        where_clause_val = " = '" + random.choice(created_strs) + "'"
        if sql_table_cols[where_clause_col] == "INTEGER":
            where_clause_val = random.choice("<=>") + str(random.randint(1, 200))
        out_where_clause += where_clause_col + where_clause_val
        return out_where_clause

    def select() -> None:
        nonlocal sql_tables
        nonlocal output_queries
        sql_table_name: str = random.choice(list(sql_tables))
        sql_table_cols: dict[str, str] = sql_tables[sql_table_name]
        select_cols: list[str] = random.sample(list(sql_table_cols), 
                k=random.randint(1, len(sql_table_cols)))
        output_queries.append("SELECT " + ", ".join(select_cols) + " FROM " + 
                sql_table_name + " WHERE " + where(sql_table_name) + ";")

    def insert() -> None:
        nonlocal sql_tables
        nonlocal output_queries
        sql_table_name: str = random.choice(list(sql_tables))
        sql_table_cols: dict[str, str] = sql_tables[sql_table_name]
        table_insert_cols: list[str] = []
        table_insert_vals: list[str] = []
        for sql_column_name, sql_column_type in sql_table_cols.items():
            table_insert_cols.append(sql_column_name)
            table_insert_vals.append(rand_col_value(sql_column_type))
        output_queries.append("INSERT INTO " + sql_table_name + " (" + 
                ",".join(table_insert_cols) + ") VALUES (" + 
                ",".join(table_insert_vals) + ");")

    def update() -> None:
        nonlocal sql_tables
        nonlocal output_queries
        sql_table_name: str = random.choice(list(sql_tables))
        sql_table_cols: dict[str, str] = sql_tables[sql_table_name]
        update_stmt: str = "UPDATE " + sql_table_name + " SET "
        update_cols: list[str] = random.sample(list(sql_table_cols), 
                k=random.randint(1, len(sql_table_cols)))
        for update_col in update_cols:
            update_stmt += update_col + " = " + \
                    rand_col_value(sql_table_cols[update_col]) + ", "
        update_stmt = update_stmt[:-2] + " WHERE " + where(sql_table_name) + ";"
        output_queries.append(update_stmt)

    def delete() -> None:
        nonlocal sql_tables
        nonlocal output_queries
        sql_table_name: str = random.choice(list(sql_tables))
        sql_table_cols: dict[str, str] = sql_tables[sql_table_name]
        output_queries.append("DELETE FROM " + sql_table_name + " WHERE " +
                where(sql_table_name) + ";")

    for _ in range(num_queries):
        query_type: int = random.randint(1, 4)
        match query_type:
            case 1:
                select()
            case 2:
                insert()
            case 3:
                update()
            case 4:
                delete()

    for sql_table_name in sql_tables:
        output_queries.append("DROP TABLE " + sql_table_name + ";")

    return output_queries


def runsqltest(sql_queries: list[str]) -> None:
    """
    :param sql_queries: The SQL queries to run.
    """
    connection_url_tpl: str = "postgresql://{user}:{pwd}@{host}:{port}/{db}"
    connection_url: str = connection_url_tpl.format(
        user=os.environ["PG_USERNAME"],
        pwd=os.environ["PG_PASSWORD"],
        host=os.environ["PG_HOST"],
        port=os.environ["PG_PORT"],
        db=os.environ["PG_DATABASE"],
    )
    pg_connection: psycopg.Connection
    with psycopg.connect(connection_url) as pg_connection:
        with pg_connection.cursor() as pg_cursor:
            for sql_query in sql_queries:
                pg_cursor.execute(sql_query)
                pg_connection.commit()

def main(argv: list[str]) -> int:
    test_trial_count: int = 30
    """The number of trials to perform."""

    with open(pathlib.Path(os.environ["PGTEST_OUTFILE"]), 'w') as output_file:
        for i in range(test_trial_count):
            print(i, "generating queries")

            # Create the queries
            trial_queries_list: list[str] = create_test_queries()

            print(i, "running queries")
            # Time how long it takes to run the queries
            test_start_time: float = time.time()
            runsqltest(trial_queries_list)
            test_duration: float = time.time() - test_start_time

            # Write the amount of time taken to a file
            output_file.write(str(round(test_duration, 3)) + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
