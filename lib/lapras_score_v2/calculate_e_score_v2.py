from typing import Callable
import numpy
from scipy import stats
from pydantic import BaseModel
from typing_extensions import TypedDict
from lib.lapras_score_v2 import calculate_raw_e_score_v2_detail as public_calculate_raw_e_score_v2_detail

"""技術力スコアのRawスコアから正規化スコアへの変換を行うモジュール

このモジュールでは、以下の2種類のスコアを扱います：

1. Rawスコア:
   - GitHub活動、技術記事、技術イベントなどの各活動から直接計算される未加工のスコア

2. Normalizedスコア(単にスコアとも呼ぶ):
   - Rawスコアをリファレンス集団との比較に基づいて変換した標準化されたスコア
   - 常に1.0から5.0の範囲に収まるように正規化される
   - 3.0を中心とした正規分布に従うように調整される
   - パーセンタイル値（0-100%）も併せて計算され、相対的な位置づけが分かる

正規化の処理では、各Rawスコアをリファレンス集団内での順位情報に基づいて変換します
"""


class RankInfo(BaseModel):
    """ユーザーのスコアに基づくリファレンス集団内での順位情報

    このクラスは、Rawスコアに基づいて、リファレンス集団内での
    相対的な順位情報を表現します。これらの情報は、後続の正規化処理で
    Normalizedスコアを計算する際に使用されます。
    """
    lower_count: int
    """当該スコアよりも低いスコアを持つリファレンスユーザーの数"""
    higher_count: int
    """当該スコアよりも高いスコアを持つリファレンスユーザーの数"""
    same_rank_count: int
    """当該スコアと同じスコアを持つリファレンスユーザーの数"""


class RankInfoWithinReferenceFunctionArgs(BaseModel):
    raw_score: float
    """ランク付けの対象となるRawスコア"""


class RankInfoWithinReferenceFunctions(BaseModel):
    """各スコアカテゴリにおけるランク情報を取得するための関数群

    各カテゴリのRawスコアについて、リファレンス集団内での順位情報を取得するための関数群を提供します
    これらの関数は正規化処理の際に使用されます
    """
    get_e_score_v2_rank_info: Callable[[RankInfoWithinReferenceFunctionArgs], RankInfo]
    """技術力スコアv2のRawスコアに基づくランク情報を取得する関数"""
    get_github_score_rank_info: Callable[[RankInfoWithinReferenceFunctionArgs], RankInfo]
    """GitHubのRawスコアに基づくランク情報を取得する関数"""
    get_tech_article_score_rank_info: Callable[[RankInfoWithinReferenceFunctionArgs], RankInfo]
    """技術記事のRawスコアに基づくランク情報を取得する関数"""
    get_tech_event_score_rank_info: Callable[[RankInfoWithinReferenceFunctionArgs], RankInfo]
    """技術イベントのRawスコアに基づくランク情報を取得する関数"""
    get_tag_count_score_rank_info: Callable[[RankInfoWithinReferenceFunctionArgs], RankInfo]
    """タグカウントのRawスコアに基づくランク情報を取得する関数"""


class EScoreV2Data(BaseModel):
    """技術力スコアv2の正規化された計算結果を保持するクラス

    このクラスは、Rawスコアから変換された正規化スコアとそのパーセンタイル値を保持します。
    全てのスコアは1.0から5.0の範囲に正規化され、3.0を中心とした正規分布に従うように調整されています。

    各スコアはNoneを許容し、正規化処理が実行できない場合
    （例：リファレンスデータが不足している場合など）はNoneが設定されます。
    """
    e_score_v2: float | None
    """技術力スコアv2(Normalized)"""
    e_score_v2_percentile: float | None
    """技術力スコアv2がリファレンス集団の中でどの位置にいるか(Percentile)"""
    github_score: float | None
    """GitHubスコア(Normalized)"""
    github_score_percentile: float | None
    """GitHubがリファレンス集団の中でどの位置にいるか(Percentile)"""
    tech_article_score: float | None
    """技術記事スコア(Normalized)"""
    tech_article_score_percentile: float | None
    """技術記事がリファレンス集団の中でどの位置にいるか(Percentile)"""
    tech_event_score: float | None
    """技術イベントスコア(Normalized)"""
    tech_event_score_percentile: float | None
    """技術イベントがリファレンス集団の中でどの位置にいるか(Percentile)"""
    tag_count_score: float | None
    """タグカウントスコア(Normalized)"""
    tag_count_score_percentile: float | None
    """タグカウントがリファレンス集団の中でどの位置にいるか(Percentile)"""


class CalculateEScoreV2Args(BaseModel):
    """技術力スコアv2を計算するための入力パラメータを定義する
    """
    raw_e_score_v2: float
    """技術力スコア(Raw)"""
    raw_e_score_v2_detail: public_calculate_raw_e_score_v2_detail.RawEScoreV2Detail
    """詳細スコア(Raw): GitHub, 技術記事, 技術イベント, タグカウント"""
    rank_info_within_reference_functions: RankInfoWithinReferenceFunctions
    """リファレンス集団内での順位情報を取得するための関数群"""
    is_reference_person: bool
    """リファレンス集団に属する人物かどうかを示すフラグ"""


class NormalizedScoreWithPercentile(BaseModel):
    """Normalizedスコアとそれがリファレンス集団の中でどの位置にいるかを保持する
    """
    score: float
    """Normalizedスコア"""
    percentile: float
    """リファレンス集団の中での位置(Percentile)"""


def calculate_e_score_v2(args: CalculateEScoreV2Args) -> EScoreV2Data:
    """Raw技術力スコアとRaw詳細スコアから、Normalizedスコアを計算する
    """
    # 共通の引数をTypedDictで定義
    class CommonArgs(TypedDict):
        is_reference_person: bool

    common_kwargs = CommonArgs(
        is_reference_person=args.is_reference_person,
    )

    normalized_score_with_percentile = _normalize_score(
        **common_kwargs,
        raw_score=args.raw_e_score_v2,
        get_rank_info_within_reference=args.rank_info_within_reference_functions.get_e_score_v2_rank_info,
    )

    github_score_with_percentile = _normalize_score(
        **common_kwargs,
        raw_score=args.raw_e_score_v2_detail.github_value,
        get_rank_info_within_reference=args.rank_info_within_reference_functions.get_github_score_rank_info,
    )

    tech_article_score_with_percentile = _normalize_score(
        **common_kwargs,
        raw_score=args.raw_e_score_v2_detail.tech_article_value,
        get_rank_info_within_reference=args.rank_info_within_reference_functions.get_tech_article_score_rank_info,
    )

    tech_event_score_with_percentile = _normalize_score(
        **common_kwargs,
        raw_score=args.raw_e_score_v2_detail.tech_event_value,
        get_rank_info_within_reference=args.rank_info_within_reference_functions.get_tech_event_score_rank_info,
    )

    tag_count_score_with_percentile = _normalize_score(
        **common_kwargs,
        raw_score=args.raw_e_score_v2_detail.tag_count_value,
        get_rank_info_within_reference=args.rank_info_within_reference_functions.get_tag_count_score_rank_info,
    )

    return EScoreV2Data(
        e_score_v2=(normalized_score_with_percentile.score
                    if normalized_score_with_percentile else None),
        e_score_v2_percentile=(normalized_score_with_percentile.percentile
                               if normalized_score_with_percentile else None),
        github_score=(github_score_with_percentile.score
                      if github_score_with_percentile else None),
        github_score_percentile=(github_score_with_percentile.percentile
                                 if github_score_with_percentile else None),
        tech_article_score=(tech_article_score_with_percentile.score
                            if tech_article_score_with_percentile else None),
        tech_article_score_percentile=(tech_article_score_with_percentile.percentile
                                       if tech_article_score_with_percentile else None),
        tech_event_score=(tech_event_score_with_percentile.score
                          if tech_event_score_with_percentile else None),
        tech_event_score_percentile=(tech_event_score_with_percentile.percentile
                                     if tech_event_score_with_percentile else None),
        tag_count_score=(tag_count_score_with_percentile.score
                         if tag_count_score_with_percentile else None),
        tag_count_score_percentile=(tag_count_score_with_percentile.percentile
                                    if tag_count_score_with_percentile else None),
    )


def _normalize_score_from_rank(
    lower_count: int,
    higher_count: int,
    same_rank_count: int,
) -> NormalizedScoreWithPercentile:
    """順位情報からNormalizedスコアを算出する

    Parameters:
    * lower_count: 0以上の整数。自分よりも順位が下の人の数。
    * higher_count: 0以上の整数。自分よりも順位が上の人の数。
    * same_rank_count: 0以上の整数。自分と同率順位の人の数 (自身を除く)。
    """
    # 同率順位の補正値を計算
    # total_count = 全体の人数 (lower + higher + same + 自分)
    total_count = lower_count + higher_count + same_rank_count + 1

    # 補正項 (分布の端のスコアを近似的に補正するための因子)
    # 下記記事の「近似値の計算」における $\varepsilon_N$ の値
    # https://qiita.com/nunukim/items/e4470f984bee85fbb136
    adjustment_factor = 1 - 0.5 / numpy.log(total_count + 1)

    # 同率順位の場合、上位・下位に半分ずつ分配する
    rank_distribution = 0.5 * same_rank_count

    # 補正後の上位・下位カウント
    lower_count_adjusted = lower_count + rank_distribution + adjustment_factor
    higher_count_adjusted = higher_count + rank_distribution + adjustment_factor

    # 標準正規分布に変換
    # ppf(1-x) = -ppf(x) だが、 x=1付近では桁落ちで精度が下がるので、x=0付近を使うようにする。
    z_score = numpy.sign(
        higher_count_adjusted - lower_count_adjusted
    ) * stats.norm.ppf(
        numpy.minimum(lower_count_adjusted, higher_count_adjusted)
        / (lower_count_adjusted + higher_count_adjusted)
    )

    # スコアを3.0を中心とした分布に変換（標準偏差0.5）
    adjusted_score = z_score * 0.5 + 3.0

    # 最終スコアを1-5の範囲に収める
    final_score = numpy.clip(adjusted_score, 1.0, 5.0)

    # パーセンタイルの計算
    # p = 100 × (l + c)/(l + m + c + 自分) %
    # l: lower_count (下位の人数)
    # m: higher_count (上位の人数)
    # c: same_rank_count (同率の人数)
    percentile = 100.0 * (lower_count + same_rank_count) / total_count

    return NormalizedScoreWithPercentile(
        score=final_score,
        percentile=percentile,
    )


def _normalize_score(
    raw_score: float,
    is_reference_person: bool,
    get_rank_info_within_reference: Callable[[RankInfoWithinReferenceFunctionArgs], RankInfo],
) -> NormalizedScoreWithPercentile | None:
    """リファレンス集団の中での順位からスコアを計算する

    Parameters:
    * raw_score: ランク付けの対象となるRawスコア
    * is_reference_person: リファレンス集団に属する人物かどうかを示すフラグ
    * get_rank_info_within_reference: リファレンス集団の中での順位情報を取得するための関数
    """
    # リファレンス集団の中での順位を取得
    rank_info = get_rank_info_within_reference(RankInfoWithinReferenceFunctionArgs(
        raw_score=raw_score,
    ))

    # スコアが低すぎる場合は判定不能
    if raw_score < 0.12:
        return None

    # 自分がreference_personの場合は、自分のスコアがsame_rank_countに含まれるので、-1 する
    same_rank_count = rank_info.same_rank_count
    if is_reference_person:
        same_rank_count = max(0, same_rank_count - 1)

    return _normalize_score_from_rank(
        lower_count=rank_info.lower_count,
        higher_count=rank_info.higher_count,
        same_rank_count=same_rank_count,
    )
