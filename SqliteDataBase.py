import re
import sqlite3


class SqliteDataBase:
    '''Set db file name\n
    Example:\n
    db = SqliteDataBase("lite.db")
    '''

    def __init__(self, file_name: str, check_thread: bool = True):
        self.db = sqlite3.connect(file_name, check_same_thread=check_thread)
        self.cursor = self.db.cursor()

    @property
    def tables(self):
        SQL = "SELECT * FROM sqlite_master WHERE type='table'"
        temp = [table for table in self.cursor.execute(SQL).fetchall()]

        tables = {}

        for table in temp:
            tables[table[1]] = list(map(lambda x: x.replace("text", '').strip(), re.findall(r'\w+ text', table[-1])))

        return tables

    def create_table(self, table_name: str, fields: list):
        '''Create a table with your fields\n
        Example:\n
        db = SqliteDataBase("lite.db")\n
        fields = ['user_id', 'call']\n
        db.create_table("log", fields)
        '''
        self.cursor.execute(f"""CREATE TABLE {table_name}({' text, '.join(fields) + ' text'})""")

    def add_record(self, table_name: str, data: dict):
        '''Insert the data record in the table\n
        Example:\n
        db = SqliteDataBase("lite.db")\n
        fields = ['user_id', 'call']\n
        db.create_table("log", fields)\n
        data = {
            "user_id": 123,
            "call": "history",
        }\n
        db.add_record("log", data)
        '''
        self.cursor.execute(f"""INSERT INTO {table_name} VALUES({','.join([f'"{data[key]}"' for key in data])})""")

        self.db.commit()

    def get_records(self, table_name: str, count: int = None, where: str = None,
                    order_by_field: str = None, sort_reverse: bool = False):
        '''Get records from the table\n
        Example:\n
        db = SqliteDataBase("lite.db")\n
        fields = ['user_id', 'call']\n
        db.create_table("log", fields)\n
        data = {
            "user_id": 123,
            "call": "history",
        }\n
        db.add_record("log", data)
        # Get all record from "log" table\n
        db.get_records("log")\n
        # Get 5  records containing a "call" field equal to "help" and sorted by user_id from "log" table\n
        db.get_records("log", 5, where='call="help"', order_by_field='user_id')
        '''

        def tuple_to_dict(table_name, data):
            fields = self.tables[table_name]
            return list(map(lambda x: dict(zip(fields, x)), data))

        sql = f"SELECT * FROM {table_name}"

        if where:
            sql += f" WHERE {' AND'.join(where.split(','))}"

        if order_by_field:
            sql += f" ORDER BY {order_by_field}"

            if sort_reverse:
                sql += " DESC"
            else:
                sql += " ASC"

        self.cursor.execute(sql)
        data = self.cursor.fetchmany(count) if count else self.cursor.fetchall()
        res = tuple_to_dict(table_name, data)

        return res[0] if count == 1 and len(res) else res

    def delete_all_records(self, table_name: str):
        self.cursor.execute(f"DELETE FROM {table_name}")
