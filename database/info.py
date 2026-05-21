class Info:
    """
    소에 대한 정보를 저장하는 클래스 입니다.
    """
    id: int
    name: str
    vector: list[float]

    def __init__(self, cow_id: int, name: str, vector: list[float]) -> None:
        """
        소에 대한 정보를 지정합니다.
        :param cow_id: 소의 고유id 입니다.
        :param name: 소 소유자의 이름입니다.
        :param vector: 소의 특징에 대한 벡터값입니다. list[float] 자료형을 사용합니다.
        """
        self.id = cow_id
        self.name = name
        self.vector = vector