
import sqlite3

def deleteRecord():
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Deleting single record now
##        sql_delete_query = """DELETE from exam_result_all_question where attempt = 3"""
##        sql_delete_query = """DELETE from exam_result where marks = 0"""
        sql_delete_query = """DELETE from exam_pre_post_result where exam = 2"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

deleteRecord()
