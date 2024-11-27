
class DataBaseHandlerMock:

    data: dict[str, int] = {}

    def get_best_score(self, user_name: str) -> int:
        if user_name in self.data:
            return self.data[user_name]
        return 0
    
    def set_user(self, user_name: str) -> None:
        if user_name not in self.data:
            self.data[user_name] = 0
    
    def update_best_score(self, user_name: str, score: int) -> None:
        if user_name in self.data:
            if score > self.data[user_name]:
                self.data[user_name] = score
