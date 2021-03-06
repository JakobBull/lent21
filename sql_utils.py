from typing import Dict, List
import sqlite3
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
database_dir = os.path.join(app_dir, "db.sqlite")

def updateRow(
        table: str,
        new_columns: Dict[str, str],
        old_columns: Dict[str, str],
    ):
    
    try:
        sqliteConnection = sqlite3.connect(database_dir)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        update_string = ",".join(
            [
                str(k) + "=" + str(v) for k, v in new_columns.items()
            ]
        )

        identify_string = ",".join(
            [
                str(k) + "=" + str(v) for k, v in old_columns.items()
            ]
        )

        query_string = f"""
            UPDATE {table}
            SET {update_string}
            WHERE {identify_string};
        """

        cursor.execute(query_string)
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def insertRow(table: str, values: Dict[str, str]):
    
    try:
        sqliteConnection = sqlite3.connect(database_dir)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        column_string = "(" + ", ".join([str(a) for a in values.keys()]) + ")"
        values_string = "(" + ", ".join([str(a) for a in values.values()]) + ")"

        query_string = f"""
            INSERT INTO {table} {column_string}
            VALUES {values_string};
        """

        cursor.execute(query_string)
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        import pdb; pdb.set_trace()
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def sqliteExecute(instruction, params = ()):
    try:
        conn = sqlite3.connect(database_dir)
        cursor = conn.cursor()
        print("Connected to SQLite")

        cursor.execute(instruction, params)
        print("Instruction executed successfully")

        # Produces a list of tuples where tuple elements are row elements given by instruction
        result = cursor.fetchall()

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite database", error)

    conn.close()
    print("The SQLite connection is closed")

    return result