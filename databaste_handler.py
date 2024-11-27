import mysql.connector


class DataBaseHandler:
    def __init__(self):
        self.db = mysql.connector.connect(
          host="jfraszczak.mysql.pythonanywhere-services.com",
          user="jfraszczak",
          password="Bazka12345",
          database="jfraszczak$kodland_quiz"
        )
        self.cursor = self.db.cursor()

    def select(self, query: str, values: tuple | None = None) -> list:
        if values is not None:
           self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self, query: str, values: tuple | None = None):
        if values is not None:
           self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.db.commit()

    def user_exists(self, user_name: str) -> bool:
        query = "SELECT * FROM best_scores WHERE user_name = %s"
        result: list = self.select(query=query, values=(user_name,))
        return len(result) > 0

    def get_best_score(self, user_name: str) -> int:
        if self.user_exists(user_name=user_name):
            query = "SELECT best_score FROM best_scores WHERE user_name = %s"
            return self.select(query=query, values=(user_name,))[0][0]
        return 0
    
    def set_user(self, user_name: str) -> None:
        if not self.user_exists(user_name=user_name):
            query = "INSERT INTO best_scores VALUES (%s, %s)"
            self.commit(query=query, values=(user_name, 0))

    def update_best_score(self, user_name: str, score: int) -> None:
        if self.user_exists(user_name=user_name):
            best_score: int = self.get_best_score(user_name=user_name)
            if score > best_score:
                query = "UPDATE best_scores SET best_score = %s WHERE user_name = %s"
                self.commit(query=query, values=(score, user_name))
