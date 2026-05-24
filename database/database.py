import pymongo
from pymongo.errors import PyMongoError, CollectionInvalid

from .info import Info
from pymongo import MongoClient


def _create_collection(db: pymongo.database.Database):
    try:
        db.create_collection(
            "cows",
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["id", "name", "vector"],
                    "properties": {
                        "id": {
                            "bsonType": ["int", "long"],
                            "description": "소 고유 ID"
                        },
                        "name": {
                            "bsonType": "string",
                            "description": "소유자 이름"
                        },
                        "vector": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "double"
                            },
                            "description": "특징 벡터"
                        }
                    }
                }
            }
        )
    except CollectionInvalid:
        pass


class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["cow_pattern"]
        _create_collection(self.db)
        self.collection = self.db["cows"]
        try:
            self.collection.create_index("id", unique=True)
        except PyMongoError as exc:
            raise RuntimeError(
                "Failed to initialize database index for cows.id"
            ) from exc

    def create(self, info: Info) -> bool:
        """
        DB에 새로운 우비와 사용자에 대한 정보를 저장합니다.
        info에는 소의 고유id, 사용자 이름, 특징 백터가 들어갑니다.
        :param info: 사용자에 대한 정보 클래스 입니다. Info 클래스로 정의되어 있습니다.
        :return: 성공유무를 반환합니다.
        """
        data = {
            "id": info.id,
            "name": info.name,
            "vector": info.vector,
        }
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        # id가 겹쳐서 DB 등록에 실패하였을 경우
        except PyMongoError:
            return False

    def update(self, cow_id: int, info: Info) -> bool:
        """
        소의 고유id를 받아 해당 소에 대한 정보를 업데이트 합니다.
        :param cow_id: 소의 고유id 값입니다.
        :param info: 사용자에 대한 정보 클래스 입니다. Info 클래스로 정의되어 있습니다.
        :return: 성공유부를 반환합니다.
        """

        try:
            result = self.collection.update_one(
                {"id": cow_id},
                {
                    "$set": {
                        "name": info.name,
                        "vector": info.vector,
                    }
                },
            )
        except PyMongoError:
            return False

        # 승인되었는지가 아닌 실제로 처리된 결과가 있는지 확인 필요
        return result.matched_count > 0

    def get_by_user(self, name: str) -> list[Info] | None:
        """
        사용자 이름을 받아서 해당 사용자의 소유한 소의 정보를 반환합니다.
        소를 여러마리 소유하고 있을 수 있으므로 list로 반환합니다.
        :param name: 사용자의 이름입니다.
        :return: 소의 정보를 담은 Info 클래스에 대한 리스트 형식입니다. 없을 시 None을 반환합니다.
        """

        result = self.collection.find({"name": name})
        list_ = [
            Info(info["id"], info["name"], info["vector"])
            for info in result
        ]

        return list_ if list_ else None

    def get_by_id(self, cow_id: int) -> Info | None:
        """
        소의 고유id를 받아서 해당 소에 대한 정보를 반환합니다.
        :param cow_id: 소의 고유id 입니다.
        :return: 해당 소의 정보를 반환합니다. 없을 시 None을 반환합니다.
        """
        result = self.collection.find_one({"id": cow_id})

        return Info(result["id"], result["name"], result["vector"]) if result else None

    def delete(self, cow_id: int) -> bool:
        """
        소의 고유id를 받아서 해당 소에 대한 정보 삭제를 진행합니다.
        :param cow_id: 소의 고유id 입니다.
        :return: 성공유무를 반환합니다.
        """

        result = self.collection.delete_one({"id": cow_id})
        # 승인되었는지가 아닌 실제로 처리된 결과가 있는지 확인 필요
        return result.deleted_count > 0

    def get_all_vectors(self) -> list[dict]:
        """
        DB에 저장된 모든 소의 id와 특징 벡터를 리스트 형태로 반환합니다.
        :return: [{"id": 1, "vector": [0.1, 0.2]}, ...]
        """
        cursor = self.collection.find({}, {"vector": 1, "id": 1, "_id": 0})

        # 딕셔너리 형태({"vector": [...]})에서 실제 배열 값만 추출하여 리스트로 만듦
        vectors = [{"id": doc["id"], "vector": doc["vector"]} for doc in cursor]

        return vectors

    def get_next_id(self) -> int:
        """
        다음으로 사용할 소 고유 ID를 가져옵니다.
        :return: 다음으로 사용할 소 고유 ID
        """
        result = self.db["counters"].find_one_and_update(
            {"_id": "cow_id"},  # 카운터의 식별자
            {"$inc": {"sequence_value": 1}},  # 값을 1 증가 ($inc)
            upsert=True,  # 문서가 없으면 새로 생성 (초기화)
            return_document=pymongo.ReturnDocument.AFTER,  # 증가된 후의 값을 반환
            projection = {"id": 1, "_id": 0},
        )
        return result["sequence_value"]