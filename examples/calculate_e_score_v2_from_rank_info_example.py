"""
ランク情報を使用した技術力スコア(E Score)の計算例

このスクリプトは、以下の要素を考慮して技術力スコア(E Score)を計算する例を示します：
- Raw技術力スコアとその詳細値
- 各スコアにおけるユーザーの順位情報（上位・同位・下位の人数）
- リファレンス対象者かどうかの情報
"""

from lib.lapras_score_v2.calculate_e_score_v2 import (
    calculate_e_score_v2,
    CalculateEScoreV2Args,
    RankInfoWithinReferenceFunctions,
    RankInfo,
)
from lib.lapras_score_v2.calculate_raw_e_score_v2_detail import RawEScoreV2Detail


def main():
    # 1. スコア計算に必要な入力データの準備
    score_data = calculate_e_score_v2(
        args=CalculateEScoreV2Args(
            # リファレンス対象者かどうか
            is_reference_person=True,
            # Raw技術力スコア
            raw_e_score_v2=100.0,
            # 各カテゴリーのRawスコア詳細
            raw_e_score_v2_detail=RawEScoreV2Detail(
                github_value=100.0,        # GitHubスコア
                tech_article_value=50.0,   # 技術記事スコア
                tech_event_value=30.0,     # 技術イベントスコア
                tag_count_value=20.0,      # 技術タグスコア
            ),
            # 各スコアにおけるランク情報を取得する関数群
            rank_info_within_reference_functions=RankInfoWithinReferenceFunctions(
                # 総合技術力スコアのランク情報
                get_e_score_v2_rank_info=lambda args: RankInfo(
                    lower_count=10,        # 自分より下位の人数
                    higher_count=20,       # 自分より上位の人数
                    same_rank_count=5,     # 同じランクの人数
                ),
                # GitHubスコアのランク情報
                get_github_score_rank_info=lambda args: RankInfo(
                    lower_count=10,
                    higher_count=20,
                    same_rank_count=5,
                ),
                # 技術記事スコアのランク情報
                get_tech_article_score_rank_info=lambda args: RankInfo(
                    lower_count=10,
                    higher_count=20,
                    same_rank_count=5,
                ),
                # 技術イベントスコアのランク情報
                get_tech_event_score_rank_info=lambda args: RankInfo(
                    lower_count=10,
                    higher_count=20,
                    same_rank_count=5,
                ),
                # 技術タグスコアのランク情報
                get_tag_count_score_rank_info=lambda args: RankInfo(
                    lower_count=10,
                    higher_count=20,
                    same_rank_count=5,
                ),
            ),
        )
    )

    # 2. 結果の表示
    print("\n=== 正規化スコア ===")
    print(f"  GitHubスコア: {score_data.github_score:.2f}")
    print(f"  技術記事スコア: {score_data.tech_article_score:.2f}")
    print(f"  技術イベントスコア: {score_data.tech_event_score:.2f}")
    print(f"  技術タグスコア: {score_data.tag_count_score:.2f}")

    print("\n=== パーセンタイル情報 ===")
    print(f"  GitHub: {score_data.github_score_percentile:.1f}%")
    print(f"  技術記事: {score_data.tech_article_score_percentile:.1f}%")
    print(f"  技術イベント: {score_data.tech_event_score_percentile:.1f}%")
    print(f"  技術タグ: {score_data.tag_count_score_percentile:.1f}%")

    print("\n=== 最終結果 ===")
    print(f"技術力スコア(E Score): {score_data.e_score_v2:.2f}")
    print(f"パーセンタイル: {score_data.e_score_v2_percentile:.1f}%")


if __name__ == "__main__":
    main()
