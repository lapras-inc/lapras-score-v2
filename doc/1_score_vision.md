# 1.LAPRASが目指すスコアの形

[LAPRAS](https://lapras.com)では、エンジニアのスキルの指標としてLARPASスコアを提供してきました。
ここでは、LAPRASが考えるスコアのあるべき姿を再定義し公開することで、スコアのあり方について広くご意見をいただくことを目的としています。


## Web上のアウトプットから、その人の隠れたスキルや経験を炙り出す

LAPRASでは「人は可能性に満ちた存在である」というコアバリューをもとに、「すべての人に最善の選択肢をマッチング」することをミッションとしてサービス運営を行ってきました。

サービス開始当初のLAPRAS(当時の scouty)は、エンジニアのWeb上でのアウトプットに着目しました。
GitHubでのOSS活動や、技術記事の投稿など、意欲があるエンジニアが頻繁に行アウトプットを見るだけで、そのエンジニアのスキルや経験がいかに優れているかをうかがい知ることができると考えました。
しかし実際には、そうしたアウトプット活動が現職や転職先で適切に評価されていないケースが少なくありません。また本人も、自身のアウトプットをうまく可視化・定量化できずにアピールしきれていない場合もあります。
LAPRASはこのような、潜在能力と意欲の高いエンジニアに最適な機会を提供するため、Web上のアウトプットからその人の隠れたスキルを明らかにする指標としてLAPRASスコアを転職マッチングに活用してきました。

## エンジニアの成長・貢献という「善行」を応援する

加えてLAPRASが目指したいのは、エンジニアのアウトプット活動そのものを積極的に評価することです。
IT業界では学習した技術をブログや登壇、OSSへのコミットなどで還元する文化が昔から根付いています。
ITエンジニアは、各人が所属する企業やクライアントのために働く労働者であると同時に、所属の枠を超えた大きな「エンジニアコミュニティ」の一員でもあります。エンジニアはOSSや技術情報などのコミュニティの恩恵を受けて成長するとともに、自分なりの形でアウトプットすることでコミュニティに貢献します。
これは業界全体の底上げにつながるとともに、エンジニアという職業そのものの在り方に根ざす「善行」であり、LAPRASはそうした活動を行うエンジニアを応援したいと考えます。

LAPRASのサービス開始以来、技術力スコアがアウトプットへの励みになっているという声も多数いただいており、微力ながらそうした文化を後押しできていればと思っています。

## エンジニアの能力を、公平に、多角的に、数値化する

上記の「エンジニアの隠れた能力を可視化する」「エンジニアの成長・貢献を応援する」という視点を達成するためには、LAPRASのスコアは公平で、多角的なものである必要があります。

### 公平なスコア
公平なスコアを実現するためには、以下の観点が重要であると考えています。

* 客観性: 事実に基づいており、判断基準が揺らがないこと
* 透明性: 算出ロジックや基準が明確にされていること
* ハックしづらさ: 恣意的な操作が入りづらい信頼性の高い指標であること

これまでも客観性や透明性には注意を払い、ロジックや統計情報はなるべく開示するように努めてきましたが、まだまだ足りない部分だと考えています。

また、ハックしづらさに関して、実は以前のLAPRASの技術力スコアには「GitHub Star」という軸がありましたが、これはGitHubのリポジトリをスター「した」数（された数ではない）をもとにした評価軸でした。GitHubでスターするだけでスコアが増えてしまうという今考えるとおかしな指標ですが、GitHubでスターしている人は情報感度が高く、実は年収などと意外なほど相関がありました。これはLAPRASのエンジニア向けページができる前から存在したもので、ロジックの公開によってハックのしやすさが問題となり削除しました。

### 多角的なスコア

スコアが多角的であるとは、以下の2つを意味します。

* 入力の多様性: 多様な情報源をもとにスコアを計算すること
* 出力の多様性: 多様な観点や軸で評価し、スコアとして表現すること

入力の多様性が低いと、特定のサービス上でのアウトプットは評価されるけれども、他のサービスでのアウトプットが評価されないということが起こってしまい、公平なスコアとは言い難くなってしまいます。また、エンジニアの一部の活動しか評価しないことは、そのエンジニアのスキルを最大限引き出す上での障害となります。
この点、LAPRASは Zenn の記事や GitHub の非公開活動など、スコアの算出元となる情報を増やしてきましたが、まだまだ足りない部分であると考えています。

また、エンジニアのスキルは決して「つよい」「よわい」の1つの軸で決まるわけではありません。
「すべての人に最善の選択肢」をマッチングするためには、多様なスキルや価値観を適切に表現する必要があります。


### 能力の数値化

公平で多角的なスコアであることに加え、エンジニアの「能力」を表した指標であることも重要な観点です。
最終的にスコアが「最善のマッチング」の助けとなるためには、採用活動を行う企業にとっても意味のある指標でなければなりません。
また、スコアがエンジニアのアウトプット活動を応援するものであっても、それがエンジニアの成長や貢献に向いていなければ質の悪いアウトプットの乱造を助長するものになってしまいます。
このように、スコアが意味のある指標として使えるようにするためには、エンジニアのスキルや経験を何らかの形で反映したものである必要があります。

また、多くのLAPRASユーザーの方から、LAPRASスコアは「世の中のエンジニアの中での自分の立ち位置を知れる」ことに価値があるというご意見をいただきます。
エンジニアとしてのスキルや経験を客観的に測るという観点では「全体の中での自分の立ち位置」という相対的な指標であるという点も重要な要素であると考えられます。
ユーザーの統計情報をもとに、全体の中での相対的なスコアを提供することができるのも、LAPRASのようなプラットフォームが介在することの価値の1つであるとも考えられます。

