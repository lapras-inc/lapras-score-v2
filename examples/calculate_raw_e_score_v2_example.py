"""
技術力スコア(Raw)の計算例

このスクリプトは、以下の要素を考慮して技術力スコア(Raw)を計算する例を示します：
- GitHubの活動（コントリビューション数、人気リポジトリ情報）
- 技術記事（QiitaとZennの人気記事）
- 技術イベントへの参加
- 保有している技術タグの数
"""

from lib.lapras_score_v2.calculate_raw_e_score_v2 import (
    calculate_raw_e_score_v2,
)
from lib.lapras_score_v2.calculate_raw_e_score_v2_detail import (
    QiitaPost,
    ZennArticle,
    Event,
    calculate_raw_e_score_v2_detail,
    RawEScoreV2DetailArgs,
    GitHubRepo,
    Logger,
)


def main():
    # 1. スコア計算に必要な入力データの準備
    args = RawEScoreV2DetailArgs(
        # GitHubの情報
        github_identifier="user1",
        github_contribution_count_list=[10, 20, 30],  # 過去3ヶ月のコントリビューション数
        github_repos=[
            GitHubRepo(
                full_name="user1/repo1",  # リポジトリのフルネーム
                parent_repo_full_name=None,  # オリジナルリポジトリのフルネーム
                contributors_count=5,      # コントリビューター数
                stargazers_count=100,      # スター数
                parent_repo_contributions=0,  # オリジナルリポジトリへのコントリビューション数
                parent_stars_count=0         # オリジナルリポジトリのスター数
            ),
            GitHubRepo(
                full_name="user1/repo2",
                parent_repo_full_name=None,
                contributors_count=10,
                stargazers_count=200,
                parent_repo_contributions=0,
                parent_stars_count=0
            ),
            GitHubRepo(
                full_name="user1/repo3",
                parent_repo_full_name=None,
                contributors_count=10,
                stargazers_count=10,
                parent_repo_contributions=0,
                parent_stars_count=0
            ),
            GitHubRepo(
                full_name="user1/repo4",
                parent_repo_full_name=None,
                contributors_count=3,
                stargazers_count=3,
                parent_repo_contributions=0,
                parent_stars_count=0
            ),
            GitHubRepo(
                full_name="user1/oss-repo1",  # forkしたリポジトリ
                parent_repo_full_name="parent/oss-repo1",
                contributors_count=15,
                stargazers_count=0,
                parent_repo_contributions=20,
                parent_stars_count=20,
                contributors=[
                    GitHubRepo.Contributor(login="user1", contributions=20),
                ],  # コントリビューター
            ),
            GitHubRepo(
                full_name="parent/oss-repo1",  # fork元のリポジトリ
                parent_repo_full_name=None,
                contributors_count=15,
                stargazers_count=20,
                parent_repo_contributions=0,
                parent_stars_count=0,
                contributors_from_commits=[
                    GitHubRepo.Contributor(login="user1", contributions=20),
                ]  # コミットからのコントリビューター
            ),
        ],
        # 技術記事の情報
        qiita_popular_posts=[
            QiitaPost(stockers_count=100),  # ストック数100の記事
            QiitaPost(stockers_count=200)   # ストック数200の記事
        ],
        zenn_popular_articles=[
            ZennArticle(liked=100)  # いいね数100の記事
        ],
        # その他の技術活動情報
        tag_count=10.0,           # 保有している技術タグの数
        events=[
            Event(
                is_tech_event=True,
                is_presenter=True
            ),
            Event(
                is_tech_event=False,
                is_presenter=False
            ),
            Event(
                is_tech_event=True,
                is_presenter=False
            )
        ],
        # AIレビューの情報
        ai_reviews=[4.0, 1.0, 2.0],
        # ロガーの設定
        logger=Logger(
            debug=print,
            info=print,
            warning=print,
            error=print,
            critical=print,
        )
    )

    # 2. 詳細スコアの計算
    detail = calculate_raw_e_score_v2_detail(args)

    # 3. 総合スコアの計算
    score = calculate_raw_e_score_v2(detail)

    # 4. 結果の表示
    print("\n=== 入力値の詳細 ===")
    print(f"GitHubスコア: {detail.github_value:.2f}")
    print(f"技術記事スコア: {detail.tech_article_value:.2f}")
    print(f"技術イベントスコア: {detail.tech_event_value:.2f}")
    print(f"技術タグスコア: {detail.tag_count_value:.2f}")

    print("\n=== 計算結果 ===")
    print(f"総合技術力スコア(Raw): {score:.2f}")


if __name__ == "__main__":
    main()
