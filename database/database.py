from info import Info

class Database:
    def create(self, info: Info) -> bool:
        pass
    def update(self, cow_id: int, info: Info) -> bool:
        pass

    def get_by_user(self, name: str) -> list[Info]:
        pass

    def get_by_id(self, cow_id: int) -> Info:
        pass

    def delete(self, cow_id: int) -> bool:
        pass