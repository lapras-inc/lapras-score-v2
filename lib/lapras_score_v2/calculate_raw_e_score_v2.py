from lib.lapras_score_v2.calculate_raw_e_score_v2_detail import RawEScoreV2Detail
import numpy
from pydantic import BaseModel


"""技術力スコア(Raw)を計算するモジュール

各カテゴリの詳細スコア(Raw)を重み付けして、総合スコアとなる技術力スコア(Raw)を計算する。
"""


def calculate_raw_e_score_v2(detail: RawEScoreV2Detail) -> float:
    """
    RawEScoreV2Detailの各スコアを重み付けして総合スコアを計算する

    Args:
        detail: 計算対象のRawEScoreV2Detail

    Returns:
        float: 重み付けされた総合スコア(Raw技術力スコア)
    """

    class WeightMap(BaseModel):
        a: float
        b: float

    PARAMS = {
        'github_value': WeightMap(a=0.32, b=1.17),
        'tech_article_value': WeightMap(a=0.21, b=0.31),
        'tech_event_value': WeightMap(a=0.30, b=0.27),
        'tag_count_value': WeightMap(a=0.10, b=0.79),
    }
    # detail の property をループさせて、それぞれの値を計算して合計する
    # 詳細RAWスコアを追加したのに重み付けを忘れていた時にエラーになるようにする
    result = 0
    for key in detail.model_fields.keys():
        weight_map = PARAMS.get(key, None)
        if weight_map is None:
            raise ValueError(f'weight_map is not defined: {key}')
        detail_value = getattr(detail, key)
        if detail_value is None:
            raise ValueError(f'detail_value is None: {key}')
        key_result = weight_map.a * numpy.log1p(weight_map.b * detail_value)
        result += key_result
    return result
