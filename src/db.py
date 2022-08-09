import sqlite3

#VERSION TWO
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

class DatabaseDriver(object):

    def __init__(self):
        self.conn = sqlite3.connect("list.db", check_same_thread=False)
        self.create_internship_table()
        self.create_subtask_table()
    
    def create_internship_table(self):
        try:
            self.conn.execute(
                """
                    CREATE TABLE internships (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL, 
                        status TEXT,
                        date TEXT
                    );
                """    
            )
        except Exception as e:
            print(e)

    def delete_internship_table(self):
        self.conn.execute("DROP TABLE IF EXISTS internships;")

    def get_all_internships(self):
        cursor = self.conn.execute("SELECT * FROM internships;")
        internships = []
        for row in cursor:
            internships.append({"id": row[0], "name": row[1], "status": row[2], "date": row[3]})
        return internships

    def insert_internship_table(self, name, status, date):
        cursor = self.conn.execute("INSERT INTO internships (name, status, date) VALUES (?, ?, ?);", (name, status, date))
        self.conn.commit()
        return cursor.lastrowid

    def get_internship_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM internships WHERE id = ?;", (id,))

        for row in cursor:
            return {"id": row[0], "name": row[1], "status": row[2], "date": row[3]}

        return None
    
    def update_internship_by_id(self, id, name, status, date):
        self.conn.execute("UPDATE internships SET name=?, status=?, date=? WHERE id=?;", (name, status, date, id))
        self.conn.commit()

    def delete_internship_by_id(self, id):
        self.conn.execute("DELETE FROM internships WHERE id = ?;", (id,))
        self.conn.commit()


    def create_subtask_table(self):
        try: self.conn.execute(
            """
                CREATE TABLE subtasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    date TEXT,
                    internship_id INTEGER NOT NULL,
                    FOREIGN KEY(internship_id) REFERENCES internships(id)
                );
            """
        )
        except Exception as e:
            print(e)

    def insert_subtask(self, title, description, date, internship_id):
        cursor = self.conn.execute("INSERT INTO subtasks (title, description, date, internship_id) VALUES (?, ?, ?, ?);", (title, description, date, internship_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_subtasks(self):
        cursor = self.conn.execute("SELECT * FROM subtasks;")
        subtasks = []
        for row in cursor:
            subtasks.append(
                {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "date": row[3],
                "internship_id": row[4]
                }
            )
        return subtasks
    
    def get_subtask_by_id(self, subtask_id):
        cursor = self.conn.execute("SELECT * FROM subtasks WHERE id = ?", (subtask_id,))
        for row in cursor:
            return {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "date": row[3],
                "internship_id": row[4]
            }
        return None
    
    def get_subtasks_by_internship(self, internship_id):
        cursor = self.conn.execute("SELECT * FROM subtasks WHERE internship_id = ?", (internship_id,))
        subtasks = []
        for row in cursor:
            subtasks.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "date": row[3],
                    "internship_id": row[4]
                }
            )
        return subtasks
    
DatabaseDriver = singleton(DatabaseDriver)


# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# association_table = db.Table(
#     "association",
#     db.Column("Internship_id", db.Integer, db.ForeignKey("internship.id")),
#     db.Column("category_id", db.Integer, db.ForeignKey("categories.id"))
# )

# class Internship(db.Model):
#     __tablename__ = "internships"
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     name = db.Column(db.String, nullable = False)
#     status = db.Column(db.String)
#     date = db.Columns(db.String)
#     subtasks = db.relationship("Subtask", cascades = "delete")
#     categories = db.relationship("Category", secondary = association_table, back_populates="categories")

#     def __init__(self, **kwargs):
#         self.name = kwargs.get("name", "")
#         self.status = kwargs.get("status", "")
#         self.date = kwargs.get("date", "")
    
#     def serialize(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "status": self.status,
#             "date": self.date,
#             "subtasks": [s.serialize() for s in self.subtasks],
#             "categories": [c.simple_serialize() for c in self.categories]
#         }

# class Subtask(db.Model):
#     __tablename__ = "subtasks"
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     date = db.Column(db.String)
#     internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"))

#     def __init__(self, **kwargs):
#         self.title = kwargs.get("description", "")
#         self.description = kwargs.get("done", "")
#         self.date = kwargs.get("date", "")
#         self.internship_id = kwargs.get("internship_id")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "date": self.date,
#             "internship_id": self.internship_id
#         }

# class Category(db.Model):
#     __tablename__="categories"
#     id = db.Column(db.Integer, primary_key = True, autoincrement=True)
#     status = db.Column(db.String)
#     internships = db.relationship("Internship", secondary=association_table, back_populates="internships")

#     def __init__(self, **kwargs):
#         self.status = kwargs.get("status", "")
    
#     def serialize(self):
#         return {
#             "id": self.id,
#             "status": self.status,
#             "internships": [i.serialize() for i in self.categories]
#         }
#     def simple_serialize(self):
#         return{
#             "id": self.id,
#             "status": self.status,
#         }
    


