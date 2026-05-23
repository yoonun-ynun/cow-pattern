from database.database import Database
import numpy as np


def get_similarity_probability(vector1: list[float], vector2: list[float]) -> float:
    """
    두 특징 벡터를 비교하여 동일한 소일 확률(%)을 반환합니다.

    :param vector1: 첫 번째 소의 특징 벡터
    :param vector2: 두 번째 소의 특징 벡터
    :return: 0.0 ~ 100.0 사이의 일치 확률 (%)
    """
    v1 = np.array(vector1, dtype=float)
    v2 = np.array(vector2, dtype=float)

    # 비교가 불가능한 입력은 일치하지 않는 것으로 간주합니다.
    if v1.ndim != 1 or v2.ndim != 1:
        return 0.0
    if v1.size == 0 or v2.size == 0:
        return 0.0
    if v1.shape[0] != v2.shape[0]:
        return 0.0
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 <= 0.0 or norm_v2 <= 0.0:
        return 0.0


    # 1. 코사인 유사도 계산 (결과는 -1.0 ~ 1.0)
    cosine_sim = np.dot(v1, v2) / (norm_v1 * norm_v2)

    # 2. 확률(%)로 변환
    # 유사도가 음수면 아예 패턴이 반대라는 뜻이므로 0%로 간주합니다.
    # 양수(0.0 ~ 1.0)인 경우에만 100을 곱해 퍼센트로 만듭니다.
    probability = max(0.0, float(cosine_sim)) * 100

    # 소수점 둘째 자리까지만 깔끔하게 잘라서 반환
    return round(probability, 2)

class Compare:
    def __init__(self):
        self.db = Database()

    def check(self, vector: list[float]) -> int | None:
        """
        DB에 해당 우비가 있는지 검사합니다.
        :param vector: 검사할 소의 특징 백터입니다.
        :return: 있을경우 소의 고유id, 없을경우 None을 반환합니다.
        """
        vector_list = self.db.get_all_vectors()
        best_id = None
        highest_percent = 0.0

        for item in vector_list:
            percent = get_similarity_probability(vector, item["vector"])

            if percent > highest_percent:
                highest_percent = percent
                best_id = item["id"]

        if highest_percent >= 90.0:
            return best_id

        return None