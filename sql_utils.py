from typing import Dict, List
import sqlite3
import os
import sys
import csv

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

        #print(query_string)

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
        return None

    conn.close()
    print("The SQLite connection is closed")

    return result

def populate_questions(file):
    '''

    populate the questions database with all questions in the csv

    '''
    # clears database
    query = 'DELETE FROM Questions'
    sqliteExecute(query)

    q_list = []

    # populates database from csv
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = 0
        for row in reader:

            # don't input header
            if header == 0:
                header = 1
                continue

            question_filename = "'" + row[2] + "'"
            level = "'" + row[3] + "'"
            subject = "'" + row[4] + "'"
            topics = "'" + row[5] + "'"

            q_dict = {"'level'":level, "'subject'":subject, "'topics'":topics, "'question_filename'":question_filename}
            q_list.append(q_dict)

            insertRow('Questions', q_dict)

    return q_list

def get_topics_from_subject(subject, level=None):
    
    sub = "subject=" + "'" + subject + "'"
    lev = "level=" + "'" + level + "'"
    if level == None:
        query = 'SELECT DISTINCT topics FROM Questions WHERE subject = ?'
    else:
        query = 'SELECT DISTINCT topics FROM Questions WHERE'
        query = query + " " + sub + " AND " + lev
    result = sqliteExecute(query)

    topic_list = []

    if result != None and len(result) != 0:
        for i, result in enumerate(result):
            if result[0] == 'unknown':
                continue
            topic_list.append(result[0])

    return topic_list

def get_questions_from_topic(level, topic):
    
    lev = "level=" + "'" + level + "'"
    top = "topics=" + "'" + topic.lower() + "'"

    query = 'SELECT DISTINCT question_id, question_filename FROM Questions WHERE'
    query = query + " " + lev + " AND " + top
    print(query)
    result = sqliteExecute(query)

    q_list = []

    if result != None and len(result) != 0:
        for i, result in enumerate(result):
            q_list.append((result[0], result[1]))

    return q_list

#print(get_topics_from_subject('Maths', 'GCSE'))
#print(get_questions_from_topic('GCSE', 'algebra'))

# populate_questions('data_2.csv')[3]

#q_dict = {"'level'":"'GCSE'", "'subject'":"'maths'", "'topics'":"'simultaneous'", "'question_filename'":"'simultaneous1.png'"}
#insertRow('Questions', q_dict)

#u_dict = {"'user_name'":"'bob'", "'hash'":"'hi'"}
#insertRow('Users', u_dict)

'''def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertQuestion(subject, topic, question):
    try:
        sqliteConnection = sqlite3.connect(database_dir)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Questions
                                  (subject, topic, question) VALUES (?, ?, ?)"""

        empQuestion = convertToBinaryData(question)
        # Convert data into tuple format
        data_tuple = (subject, topic, question)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(question_id):
    try:
        sqliteConnection = sqlite3.connect(database_dir)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from Questions where question_id = ?"""
        cursor.execute(sql_fetch_blob_query, (question_id,))
        record = cursor.fetchall()
        for row in record:
            print(row[:2])
            #print("question_id = ", row[0], "subject = ", row[1], "topic = ", row[2])
            topic = row[1]
            question = row[3]
            #resumeFile = row[3]

            #print("Storing employee image and resume on disk \n")
            photoPath = sys.path[0] + "question" + str(row[0]) + ".txt"
            print(photoPath)
            #resumePath = "E:\pynative\Python\photos\db_data\\" + name + "_resume.txt"
            writeTofile(question, photoPath)
            #writeTofile(resumeFile, resumePath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

#print(convertToBinaryData('download2.png'))
insertQuestion('maths', 'algebra', 'download2.png')
#readBlobData(1)'''