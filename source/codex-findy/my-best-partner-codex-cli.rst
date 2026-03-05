==================================================
わたしの、最高の相棒、Codex CLI
==================================================

わたしの、最高の相棒、Codex CLI
==================================================

:Event: Codexどう使ってる？期待通りにいかない時の向き合い方と工夫
:Presented: 2026/03/06 nikkie

お話しすること🗣️
==================================================

1. Codex自走事例
2. 使った仕組み： **Rules**
3. dive（裏側の実装）

お前、誰よ（Python使いの自己紹介）
==================================================

* nikkie（にっきー）・Python歴8年 [#nikkie-ftnext-blog]_
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-ftnext-blog] `ブログ <https://nikkie-ftnext.hatenablog.com/>`__ 連続1200日突破

.. 過去の発表（コーディングエージェント）

コーディングエージェントについての見解
--------------------------------------------------

:Claude Code: わたしの、最高の **妹** [#claude-code-language-free-input-article]_
:Codex CLI: わたしの、最高の **相棒**

あくまで2026年3月初頭時点です

.. [#claude-code-language-free-input-article] `Claude Code に"自由入力で"言語設定できるようになったと聞きまして <https://nikkie-ftnext.hatenablog.com/entry/claude-code-210-language-setting-free-input-can-be-my-sister#%E7%A7%81%E3%81%AF%E5%A6%B9%E3%81%AB%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99>`__

Codex CLI自走事例
==================================================

「DBをdockerで立てて、APIを別で立てて、curlして、その後DBをdumpして」を何回も

Agent Development Kit 🏃‍♂️
--------------------------------------------------

* https://github.com/google/adk-python
* *簡単* にAIエージェントを開発できる

``adk create`` 🏃‍♂️
--------------------------------------------------

.. code-block:: python
    :caption: :file:`search_agent/agent.py`

    root_agent = Agent(
        model='gemini-2.5-pro',
        name='search_agent',
        instruction="You are a helpful assistant with access to Google Search. (略)",
        tools=[google_search],
    )

``adk web`` 🏃‍♂️
--------------------------------------------------

.. TODO web UI

.. Agent Engine や Cloud Run にデプロイ容易

マイナーバージョンアップで壊れる 🏃‍♂️
--------------------------------------------------

* ADKのバージョンを上げる（:command:`uv sync -P google-adk`）
* Web UIは起動する
* 実行時にエラー

.. TODO エラーメッセージ

なぜマイナーバージョンアップで壊れるのか 🏃‍♂️
--------------------------------------------------

* ADKのマイナーバージョンアップで **ORMの実装が変わっている** （カラム追加）
* 一方DBのテーブル定義は古いまま
* ``SELECT`` で指定した新カラムがテーブルになく、実行時にエラー

.. https://nikkie-ftnext.hatenablog.com/entry/google-adk-python-minor-version-up-break-at-runtime-due-to-table-change-cope-with-sqldef

バージョンごとにテーブル定義を知りたい
--------------------------------------------------

* `sqldef <https://github.com/sqldef/sqldef>`__ というツールを知っていた
* 2つのテーブル定義から **ALTER TABLE を自動で作る**
* 💡ADKのマイナーバージョンアップと合わせて ``ALTER TABLE`` もやれば、実行時エラーなくなるのでは

テーブル定義のdump作業
==================================================

1. DB起動
2. ADKサーバ起動
3. HTTPリクエスト（＝空のテーブル作成）
4. テーブル定義のdump

DB起動・終了
--------------------------------------------------

.. code-block:: shell

    $ docker ps
    $ docker run --name adk-pg -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:18
    $ docker rm -f adk-pg

ADKサーバ起動
--------------------------------------------------

.. code-block:: shell

    $ uvx --from google-adk==1.22.0 adk api_server \
        --session_service_uri postgresql+psycopg://postgres:mysecretpassword@localhost:5432/postgres
    $ lsof -ti :8000
    $ kill <pid>

残りのコマンド
--------------------------------------------------

.. code-block:: shell

    $ curl -X POST http://127.0.0.1:8000/apps/my_agent/users/test_user/sessions -H 'Content-Type: application/json' -d '{}'

    $ psqldef -h localhost -p 5432 -U postgres -W mysecretpassword postgres --export > schemas/v<version>/postgresql.sql

まずペアプロ
--------------------------------------------------

* 対話的に :file:`AGENTS.md` を作成。ここまでのコマンドを列挙した手順書
* 1つバージョンを指定して、許可しながら一緒に作業
* :file:`AGENTS.md` 更新や、シェルスクリプトによる自動化を必要に応じて依頼

やや脱線：Codex CLIの作業から **学ぶ** 🏃‍♂️
--------------------------------------------------

* `git status <https://git-scm.com/docs/git-status>`__ **-sb**
* 起動したサーバのログの保存（``nohup uvx adk api_server > "$log" 2>&1``）
* ログファイルを見て調査している！

IMO：Codex CLIは **シェル芸人**
--------------------------------------------------

Rules
==================================================

* https://developers.openai.com/codex/rules
* コマンド実行を **事前許可** する仕組み

`OpenAI Learning Lab: Codex を使いこなす <https://openai.ondemand.goldcast.io/on-demand/d1544c04-a382-4e1f-9077-01ba81293f44>`__
------------------------------------------------------------------------------------------------------------------------------------------------------

* 「Codexがいちいち承認を求めてきてテンポが悪い -> Rules で事前承認」（40:30〜）
* :file:`~/.codex/rules/` やプロジェクトの :file:`.codex/rules/` に置く
* `codex execpolicy check <https://developers.openai.com/codex/cli/reference#codex-execpolicy>`__

Rules（途中の状態）
--------------------------------------------------

.. code-block:: starlark

    prefix_rule(pattern=["docker", "ps"], decision="allow")
    prefix_rule(pattern=["scripts/export_schema.sh"], decision="allow")
    prefix_rule(pattern=["docker", "rm", "-f"], decision="allow")
    prefix_rule(pattern=["git", "add"], decision="allow")
    prefix_rule(pattern=["git", "commit"], decision="allow")
    prefix_rule(pattern=["kill"], decision="allow")

手順書に従って Codex CLI が実行するコマンドを **事前許可**

🌟 **スクリプト** にさらにまとめればいいじゃん！
==================================================

.. code-block:: starlark

    prefix_rule(pattern=["scripts/export_schema.sh"], decision="allow")
    prefix_rule(pattern=["git", "add"], decision="allow")
    prefix_rule(pattern=["git", "commit"], decision="allow")

スクリプト（抜粋）
--------------------------------------------------

.. code-block:: shell

    api_pid="$(cat "$current_pidfile")"
    kill "$api_pid" >/dev/null 2>&1 || true

    docker rm -f "$current_container" >/dev/null 2>&1 || true

なぜスクリプトにまとめたか
--------------------------------------------------

* docker rm -f や kill を任意の引数で実行できちゃうのはリスク（Codexは賢いのでめったになさそうだが）
* スクリプトであれば **引数までコントロールできる**

Rules速習におすすめ記事 [#yorifuji-codex-rules-article]_
----------------------------------------------------------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">Codex でコマンド実行ポリシーをカスタマイズする方法について書きました、Claude Code の permissions(allow/deny) に相当します<a href="https://t.co/JDAJEF7q52">https://t.co/JDAJEF7q52</a></p>&mdash; Yorifuji Mitsunori (@yorifuji) <a href="https://twitter.com/yorifuji/status/2007705314666393967?ref_src=twsrc%5Etfw">2026年1月4日</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

.. [#yorifuji-codex-rules-article] yorifujiさん `Codex の Execution policy rules を理解して安全・快適に利用する <https://zenn.dev/yorifuji/articles/3d44ca14ad6b3e>`__

学び：Rulesは ``[]`` をネストしても書けます
--------------------------------------------------

.. code-block:: starlark
    :emphasize-lines: 5

    # Before
    prefix_rule(pattern=["git", "add"], decision="allow")
    prefix_rule(pattern=["git", "commit"], decision="allow")
    # After
    prefix_rule(pattern=["git", ["add", "commit"]], decision="allow")

`execpolicyのREADME <https://github.com/openai/codex/blob/main/codex-rs/execpolicy/README.md>`__ にあります

Dive：コマンド実行許可の裏側
==================================================

.. Appendix 最初のプロンプト
