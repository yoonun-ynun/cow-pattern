from info import Info

class Database:
    """
    DB와 상호작용 하기 위한 클래스 입니다.
    """
    def create(self, info: Info) -> bool:
        """
        DB에 새로운 우비와 사용자에 대한 정보를 저장합니다.
        info에는 소의 고유id, 사용자 이름, 특징 백터가 들어갑니다.
        :param info: 사용자에 대한 정보 클래스 입니다. Info 클래스로 정의되어 있습니다.
        :return: 성공유무를 반환합니다.
        """
        pass
    def update(self, cow_id: int, info: Info) -> bool:
        """
        소의 고유id를 받아 해당 소에 대한 정보를 업데이트 합니다.
        :param cow_id: 소의 고유id 값입니다.
        :param info: 사용자에 대한 정보 클래스 입니다. Info 클래스로 정의되어 있습니다.
        :return: 성공유부를 니다.
        """
        pass

    def get_by_user(self, name: str) -> list[Info] | None:
        """
        사용자 이름을 받아서 해당 사용자의 소유한 소의 정보를 반환하니다.
        소를 여러마리 소유하고 있을 수 있으므로 list로 반환합니다.
        :param name: 사용자의 이름입니다.
        :return: 소의 정보를 담은 Info 클래스에 대한 리스트 형식입니다. 없을 시 None을 반환합니다.
        """
        pass

    def get_by_id(self, cow_id: int) -> Info | None:
        """
        소의 고유id를 받아서 해당 소에 대한 정보를 반환합니다.
        :param cow_id: 소의 고유id 입니다.
        :return: 해당 소의 정보를 반환합니다. 없을 시 None을 반환합니다.
        """
        pass

    def delete(self, cow_id: int) -> bool:
        """
        소의 고유id를 받아서 해당 소에 대한 정보 삭제를 진행합니다.
        :param cow_id: 소의 고유id 입니다.
        :return: 성공유무를 반환합니다.
        """
        pass