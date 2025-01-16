import math
from typing import Callable

import numpy
from pydantic import BaseModel

"""技術力スコアv2のRawスコアを計算するモジュール

このモジュールでは、以下の4つのカテゴリのRawスコアを計算します：

1. RawGitHubスコア:
   - コントリビューション数
   - リポジトリの評価（スター数、コントリビューター数など）

2. Raw技術記事スコア:
   - Qiitaの記事のストック数
   - Zennの記事のいいね数

3. Raw技術イベントスコア:
   - 参加したイベント数

4. Rawタグカウントスコア:
   - 保有するスキルタグの数

各カテゴリのRawスコアは、それぞれの活動量や評価に基づいて計算され、
後続の正規化処理によってNormalizedスコアに変換されます。
"""


class GitHubRepo(BaseModel):
    """GitHubリポジトリの情報を保持する

    リポジトリのスター数、コントリビューター数、およびコントリビューション情報を保持します。
    Forkされたリポジトリの場合は、オリジナルリポジトリの情報も含みます。
    """
    class Contributor(BaseModel):
        """リポジトリのコントリビューター情報
        """
        contributions: int | None
        """コントリビューション数"""
        login: str | None
        """GitHubのログイン名"""

    contributors_count: int
    """リポジトリの全コントリビューター数"""
    stargazers_count: int
    """リポジトリの獲得スター数"""
    original_repo_contributions: int
    """Forkされたリポジトリの場合の、オリジナルリポジトリへのコントリビューション数"""
    original_stars_count: int
    """Forkされたリポジトリの場合の、オリジナルリポジトリのスター数"""
    contributors: list[Contributor] = []
    """通常のAPIから取得したコントリビューター情報"""
    contributors_from_commits: list[Contributor] = []
    """コミット履歴から取得したコントリビューター情報"""


class ZennArticle(BaseModel):
    """Zenn記事の情報を保持する
    """
    liked: int
    """記事のいいね数"""


class QiitaPost(BaseModel):
    """Qiita記事の情報を保持する
    """
    stockers_count: int
    """記事のストック数"""


class Logger(BaseModel):
    """ロギング関数のDI用

    各ログレベルに対応するCallableを保持します。
    """
    debug: Callable
    info: Callable
    warning: Callable
    error: Callable
    critical: Callable


class RawEScoreV2DetailArgs(BaseModel):
    """Rawスコア計算に必要なパラメータ定義
    """
    github_identifier: str
    """GitHub Identifier"""
    github_contribution_count_list: list[int]
    """日別のGitHubコントリビューション数"""
    tag_count: float
    """保有するスキルタグの数"""
    tech_event_count: float
    """参加した技術イベントの数"""
    qiita_popular_posts: list[QiitaPost]
    """Qiitaの人気記事リスト"""
    zenn_popular_articles: list[ZennArticle]
    """Zennの人気記事リスト"""
    github_popular_repos: list[GitHubRepo]
    """GitHubの人気リポジトリリスト"""
    logger: Logger
    """ロギング関数"""


class RawEScoreV2Detail(BaseModel):
    """各カテゴリのRawスコアを保持する
    """
    github_value: float
    """GitHubのRawスコア（コントリビューションとリポジトリの評価を含む）"""
    tech_article_value: float
    """技術記事のRawスコア（QiitaとZennの記事評価を含む）"""
    tech_event_value: float
    """技術イベントのRawスコア"""
    tag_count_value: float
    """タグカウントのRawスコア"""


def calculate_raw_e_score_v2_detail(args: RawEScoreV2DetailArgs) -> RawEScoreV2Detail:
    """各カテゴリのRawスコアを計算する

    GitHubの活動、技術記事の評価、技術イベントへの参加、保有スキルタグから
    それぞれのRawスコアを計算します。

    Args:
        args (RawEScoreV2DetailArgs): 各プラットフォームからの活動データ

    Returns:
        RawEScoreV2Detail: 計算された各カテゴリのRawスコア
    """
    # GitHub
    github_contribution_value = _get_github_contribution_value(args.github_contribution_count_list)
    github_repo_value = _get_github_repo_value(args.github_popular_repos, args.github_identifier, args.logger)
    github_value = github_contribution_value * 0.1 + github_repo_value

    # Tech Article
    tech_article_value = _get_tech_article_value(args.qiita_popular_posts, args.zenn_popular_articles)

    # Tech Event
    tech_event_value = args.tech_event_count

    # Tag Count
    tag_count_value = args.tag_count

    return RawEScoreV2Detail(
        github_value=github_value,
        tech_article_value=tech_article_value,
        tech_event_value=tech_event_value,
        tag_count_value=tag_count_value,
    )


def _get_github_repo_value(repos: list[GitHubRepo], github_identifier: str, logger: Logger) -> float:
    """GitHubリポジトリの値を計算する

    Args:
        repos (list[GitHubRepo]): 評価対象のリポジトリリスト
        github_identifier (str): 評価対象ユーザーのGitHub ID
        logger (Logger): ロギング機能(DI)

    Returns:
        float: 計算された値
    """
    def _get_contributions_count(repo: GitHubRepo, github_identifier: str) -> int:
        """リポジトリにおける特定ユーザーのコントリビューション数を取得

        通常のAPIとコミット履歴の両方からコントリビューション情報を収集します。

        Args:
            repo (GitHubRepo): 対象リポジトリ
            github_identifier (str): GitHub Identifier

        Returns:
            int: コントリビューション数
        """
        try:
            contributions_count = 0
            # /commits 経由のコントリビューターも考慮して返却する
            contributors = repo.contributors + repo.contributors_from_commits

            for contributor in contributors:
                if contributor.login is None:
                    raise ValueError('contributor is None')
                if contributor.contributions is None:
                    raise ValueError('contributor.contributions is None')
                if contributor.login.casefold() == github_identifier.casefold():
                    contributions_count = contributor.contributions
                    break

            return contributions_count
        except (AttributeError, KeyError, TypeError) as e:
            logger.error(e)
            return 0

    def _get_repo_stats_score(repo: GitHubRepo, github_identifier: str) -> float:
        """リポジトリの統計情報に基づいて値を計算

        コントリビューター数、コントリビューション数、スター数を考慮して
        対数スケールでスコアを計算します。Forkされたリポジトリの場合は
        オリジナルリポジトリとの比較も行います。

        Args:
            repo (GitHubRepo): 対象リポジトリ
            github_identifier (str): GitHub Identifier

        Returns:
            float: 計算された値
        """
        try:
            contributions = _get_contributions_count(repo, github_identifier)
            local_repo_score = float(math.log(repo.contributors_count + 2, 10)) \
                * ((math.log((float(min(contributions, 300)) ** 1.2) + 10) ** 1.7)
                   * math.log(float(min(repo.stargazers_count, 300) / 4) ** 1.3 + 2, 10)) ** 1.2

            if repo.original_repo_contributions > 0:
                original_repo_score = float(math.log(repo.contributors_count + 2, 10)) \
                    * ((math.log((float(min(repo.original_repo_contributions, 300)) ** 1.2) + 10) ** 1.7)
                       * math.log(float(min(repo.original_stars_count, 300) / 4) ** 1.3 + 2, 10)) ** 1.2
            else:
                original_repo_score = 0

            return max(local_repo_score, original_repo_score)

        except TypeError as e:
            logger.error(e)
            return 0

    if not repos:
        return 0

    return float(numpy.prod([math.log(_get_repo_stats_score(repo, github_identifier) + 1) for repo in repos]))


def _get_tech_article_value(qiita_popular_posts: list[QiitaPost], zenn_popular_articles: list[ZennArticle]) -> float:
    """技術記事のRawスコアを計算

    Args:
        qiita_popular_posts (list[QiitaPost]): Qiitaの人気記事リスト
        zenn_popular_articles (list[ZennArticle]): Zennの人気記事リスト

    Returns:
        float: 計算された技術記事スコア
    """
    like_count_list = []
    if qiita_popular_posts:
        like_count_list += [
            post.stockers_count for post in qiita_popular_posts[:3]
        ]

    if zenn_popular_articles:
        like_count_list += [article.liked for article in zenn_popular_articles[:3]]

    if len(like_count_list) == 0:
        return 0

    return float(numpy.prod(
        [
            math.log1p(liked_count)
            # Like数が0の記事を除外した上位3記事を対象とする
            for liked_count in sorted(like_count_list, reverse=True)[:3]
            if liked_count > 0
        ]
    ))


def _get_github_contribution_value(github_contribution_count_list: list[int]) -> float:
    """GitHubコントリビューションの値を計算


    Args:
        github_contribution_count_list (list[int]): 日別のコントリビューション数リスト

    Returns:
        float: 計算された値
    """
    if not github_contribution_count_list:
        return 0

    return numpy.sum(numpy.log1p(github_contribution_count_list))
