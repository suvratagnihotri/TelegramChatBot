import sqlite3


class TeleDB:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS details(chat_id integer PRIMARY KEY, Name text, College text, Source text, Programming_language text, Framework text, Projects text, Skill_level text, Github text)"
        self.conn.execute(tblstmt)
        self.conn.commit()


    def add_item(self,col_name, item_text, owner):
        stmt = "INSERT INTO details(chat_id) SELECT (?) WHERE NOT EXISTS(SELECT 1 FROM details WHERE chat_id = (?))"
        args = (owner, owner)
        self.conn.execute(stmt, args)
        
        stmt = f"UPDATE details SET  {col_name} = (?) WHERE chat_id = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()


    def get_items(self, owner):
        try:
            stmt = "SELECT * FROM details WHERE Chat_id = (?)"
            args = (owner,)
            return [x[1:] for x in self.conn.execute(stmt, args)][0]
        except:
            return 'error'

