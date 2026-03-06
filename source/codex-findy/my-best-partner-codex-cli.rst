==================================================
わたしの、最高の相棒、Codex CLI
==================================================

わたしの、最高の **相棒**、Codex CLI
==================================================

:Event: Codexどう使ってる？期待通りにいかない時の向き合い方と工夫
:Presented: 2026/03/06 nikkie

お話しすること🗣️
==================================================

1. Codex自走事例
2. 使った仕組み： **Rules**
3. 裏側の実装にdive

お前、誰よ（Python使いの自己紹介）
==================================================

* nikkie（にっきー）・Python歴8年 [#nikkie-ftnext-blog]_
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-ftnext-blog] `ブログ <https://nikkie-ftnext.hatenablog.com/>`__ 連続1200日突破

Claude CodeやCodex CLIについて発表
--------------------------------------------------

* `Pythonを"理解"しているコーディングエージェントが欲しい！！ <https://ftnext.github.io/2025-slides/yapc-fukuoka/lt-agent-who-understand-python.html#/2>`__ （Claude CodeのHooks）
* `ねぇ、Codex CLI。私だけにあなたのコンテキスト、教えて？ <https://ftnext.github.io/2025-slides/aidd-codex1/codex-rs-telemetry.html#/2>`__
* `Codex CLIで 加速 するコードリーディング <https://ftnext.github.io/2025-slides/lunchwithai-codex2/invincible-code-reading.html>`__

コーディングエージェントについての見解
--------------------------------------------------

:Claude Code: わたしの、最高の **妹** [#claude-code-language-free-input-article]_
:Codex CLI: わたしの、最高の **相棒**

あくまで2026年3月初頭時点です

.. [#claude-code-language-free-input-article] `Claude Code に"自由入力で"言語設定できるようになったと聞きまして <https://nikkie-ftnext.hatenablog.com/entry/claude-code-210-language-setting-free-input-can-be-my-sister#%E7%A7%81%E3%81%AF%E5%A6%B9%E3%81%AB%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99>`__

Codex CLI **自走** 事例
==================================================

「DBをdockerで立てて、APIを別で立てて、curlして、その後DBをdumpして」を20回くらい

🏃‍♂️のスライドはCodex CLIの話ではないため、詳細が理解できなくても大丈夫です

Agent Development Kit 🏃‍♂️
--------------------------------------------------

* https://github.com/google/adk-python
* *簡単* にAIエージェントを開発できる

``adk create`` 🏃‍♂️
--------------------------------------------------

.. code-block:: python
    :caption: :file:`search_agent/agent.py`

    root_agent = Agent(
        model='gemini-3.1-pro-preview',
        name='search_agent',
        instruction="You are a helpful assistant with access to Google Search. (略)",
        tools=[google_search],
    )

``adk web`` 🏃‍♂️
--------------------------------------------------

.. image:: ../_static/codex-findy/adk-web-screenshot.png

.. Agent Engine や Cloud Run にデプロイ容易

マイナーバージョンアップで壊れる 🏃‍♂️
--------------------------------------------------

* adk-python は隔週リリース（現在 1.26.0）
* ADKのバージョンを上げる（:command:`uv sync -P google-adk`）
* Web UIは起動する
* 実行時にエラー

.. revealjs-break::
    :notitle:

.. image:: ../_static/codex-findy/adk-miner-version-up-runtime-error.png

.. code-block:: log
    :caption: 応答がなく、エラーが出ている

    INFO:     127.0.0.1:61263 - "POST /run_sse HTTP/1.1" 500 Internal Server Error

    sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) column events.custom_metadata does not exist

    [SQL: SELECT events.id AS events_id, events.app_name AS events_app_name, events.user_id AS events_user_id, events.session_id AS events_session_id, events.invocation_id AS events_invocation_id, events.author AS events_author, events.actions AS events_actions, events.long_running_tool_ids_json AS events_long_running_tool_ids_json, events.branch AS events_branch, events.timestamp AS events_timestamp, events.content AS events_content, events.grounding_metadata AS events_grounding_metadata, events.custom_metadata AS events_custom_metadata, events.usage_metadata AS events_usage_metadata, events.citation_metadata AS events_citation_metadata, events.partial AS events_partial, events.turn_complete AS events_turn_complete, events.error_code AS events_error_code, events.error_message AS events_error_message, events.interrupted AS events_interrupted 
    FROM events 
    WHERE events.app_name = %(app_name_1)s::VARCHAR AND events.user_id = %(user_id_1)s::VARCHAR AND events.session_id = %(session_id_1)s::VARCHAR ORDER BY events.timestamp DESC]
    [parameters: {'app_name_1': 'search_agent', 'user_id_1': 'user', 'session_id_1': '3e967de9-05aa-4d53-bd07-aad4daf0c25d'}]
    (Background on this error at: https://sqlalche.me/e/20/f405)

なぜマイナーバージョンアップで壊れるのか 🏃‍♂️
--------------------------------------------------

* **ORMの実装が変わっている** （カラム追加）
* 一方DBのテーブル定義は古いまま
* 新しいカラムを ``SELECT`` で指定しているが、テーブルになく、実行時にエラー

.. https://nikkie-ftnext.hatenablog.com/entry/google-adk-python-minor-version-up-break-at-runtime-due-to-table-change-cope-with-sqldef

バージョンごとにテーブル定義を知りたい
--------------------------------------------------

* `sqldef <https://github.com/sqldef/sqldef>`__ というツールを知っていた
* 2つのテーブル定義から **ALTER TABLE を自動で作る**
* 💡ADKのマイナーバージョンアップと合わせて ``ALTER TABLE`` もやれば、実行時エラーなくなるのでは

.. 希望のissue

**テーブル定義** のdump作業
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

:command:`docker` 操作

ADKサーバ起動
--------------------------------------------------

.. code-block:: shell

    $ nohup uvx --from google-adk==1.22.0 adk api_server \
        --session_service_uri postgresql+psycopg://postgres:mysecretpassword@localhost:5432/postgres
    $ lsof -ti :8000
    $ kill <pid>

残りのコマンド
--------------------------------------------------

.. code-block:: shell

    $ curl -X POST http://127.0.0.1:8000/apps/my_agent/users/test_user/sessions \
        -H 'Content-Type: application/json' -d '{}'

    $ psqldef -h localhost -p 5432 -U postgres -W mysecretpassword \
        postgres --export > schemas/v<version>/postgresql.sql

まずペアプロ
--------------------------------------------------

* 対話的に :file:`AGENTS.md` を作成。ここまでのコマンドを列挙した **手順書**
* 1つバージョンを指定して、コマンド実行を都度許可しながら一緒に作業
* :file:`AGENTS.md` 更新や、シェルスクリプトによる自動化を必要に応じて依頼

やや脱線：Codex CLIの作業から **学ぶ** 🏃‍♂️
--------------------------------------------------

* `git status <https://git-scm.com/docs/git-status>`__ **-sb**
* 起動したサーバのログの保存（``nohup uvx adk api_server > server.log 2>&1``）
* ログファイルを見て調査している！

IMO：Codex CLIは **シェル芸人**
--------------------------------------------------

.. raw:: html

    <iframe width="800" height="480" src="https://ftnext.github.io/2025-slides/lunchwithai-codex2/invincible-code-reading.html#/5/4"
        title="Codex CLIで 加速 するコードリーディング"></iframe>

.. https://x.com/ftnext/status/1993526059401461978

Rules
==================================================

* https://developers.openai.com/codex/rules
* コマンド実行を **事前許可** （禁止）する仕組み
* patternへの前方一致

`OpenAI Learning Lab: Codex を使いこなす <https://openai.ondemand.goldcast.io/on-demand/d1544c04-a382-4e1f-9077-01ba81293f44>`__ より
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
    :emphasize-lines: 1

    prefix_rule(pattern=["scripts/export_schema.sh"], decision="allow")
    prefix_rule(pattern=["git", "add"], decision="allow")
    prefix_rule(pattern=["git", "commit"], decision="allow")

スクリプト（抜粋）
--------------------------------------------------

.. code-block:: bash

    api_pid="$(cat "$current_pidfile")"
    kill "$api_pid" >/dev/null 2>&1 || true

    docker rm -f "$current_container" >/dev/null 2>&1 || true

なぜスクリプトにまとめたか
--------------------------------------------------

* ``docker rm -f`` や ``kill`` を任意の引数で実行できちゃうのはリスク（Codexは賢いのでめったになさそうだが）
* スクリプトであれば前方一致だけでなく **引数までコントロールできる**
* 放置して達成！ [#adk-python-db-schema-history-codex-version]_ ：https://github.com/ftnext/adk-python-db-schema-history

.. [#adk-python-db-schema-history-codex-version] gpt-5.2-codex (medium effort?) (後に gpt-5.3-codex)

.. revealjs-break::
    :notitle:

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">Codex でコマンド実行ポリシーをカスタマイズする方法について書きました、Claude Code の permissions(allow/deny) に相当します<a href="https://t.co/JDAJEF7q52">https://t.co/JDAJEF7q52</a></p>&mdash; Yorifuji Mitsunori (@yorifuji) <a href="https://twitter.com/yorifuji/status/2007705314666393967?ref_src=twsrc%5Etfw">2026年1月4日</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

.. comment out
    Rules速習におすすめ記事 [#yorifuji-codex-rules-article]_
    ----------------------------------------------------------------------------------------------------
    .. [#yorifuji-codex-rules-article] yorifujiさん `Codex の Execution policy rules を理解して安全・快適に利用する <https://zenn.dev/yorifuji/articles/3d44ca14ad6b3e>`__

.. OpenAI Developer Docs MCP に聞く

yorifujiさん記事から：Rulesは ``[]`` をネストしても書けます
----------------------------------------------------------------------------------------------------

.. code-block:: starlark
    :emphasize-lines: 5

    # Before
    prefix_rule(pattern=["git", "add"], decision="allow")
    prefix_rule(pattern=["git", "commit"], decision="allow")
    # After
    prefix_rule(pattern=["git", ["add", "commit"]], decision="allow")

`execpolicyのREADME <https://github.com/openai/codex/blob/main/codex-rs/execpolicy/README.md>`__ にあります

まとめ🌯 繰り返し作業を Rules で自走
==================================================

* 「DBをdockerで立てて、APIを別で立てて、curlして、その後DBをdumpして」を20回くらい
* :file:`AGENTS.md` に手順書を作り、自動化スクリプトも書かせていく
* Rules で前方一致でマッチよりもスクリプトに入れたほうがより安全にできた例

Dive：コマンド実行許可の裏側
==================================================

v0.110.0のソースコードリーディングより [#latest-codex-cli-version-20260306]_

.. [#latest-codex-cli-version-20260306] 発表時最新はv0.111.0

.. https://nikkie-ftnext.hatenablog.com/entry/when-codex-cli-shell-command-ask-for-approval-from-source-reading

Codex CLIのセキュリティ
--------------------------------------------------

* Sandbox mode: シェルコマンドを安全に **実行**
* Approval policy: シェルコマンドの実行 **許可を尋ね** させて安全に

https://developers.openai.com/codex/security#sandbox-and-approvals

Codex CLIのオプション
--------------------------------------------------

* Sandbox mode: ``--sandbox``, ``-s``
* Approval policy: ``--ask-for-approval``, ``-a``

https://developers.openai.com/codex/cli/reference#global-flags

``#codex_findy`` より（2025/10）
--------------------------------------------------

.. raw:: html

    <iframe src="https://www.docswell.com/slide/KJQYQM/embed#p25" allowfullscreen="true" class="docswell-iframe" width="620" height="350" style="border: 1px solid #ccc; display: block; margin: 0px auto; padding: 0px; aspect-ratio: 620/350;"></iframe>

:command:`codex` （フラグなし）
--------------------------------------------------

projectを **trust** (*Do you trust the contents of this directory?*)

* Sandbox: workspace-write [#default-sandbox-mode-0.110.0]_
* Approval: OnRequest [#default-approval-policy-0.110.0]_

.. [#default-sandbox-mode-0.110.0] https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/core/src/config/mod.rs#L1456

.. [#default-approval-policy-0.110.0] https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/core/src/config/mod.rs#L1827

シェルコマンドの実行許可
--------------------------------------------------

1. **ルールにあればルールのdecisionとなる**
2. ルールにない場合のフォールバック処理

https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/core/src/exec_policy.rs#L199

SandboxとApprovalに基づくフォールバック
------------------------------------------------------------

* `安全なコマンド <https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/shell-command/src/command_safety/is_safe_command.rs>`__ （``ls``, ``git status``） -> 実行
* `危険かもしれないコマンド <https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/shell-command/src/command_safety/is_dangerous_command.rs>`__ （``rm -rf /``） -> 許可を求める
* 追加の権限を必要とするか -> するなら許可を求め、しないなら実行 [#exec-policy-0.110.0]_

.. [#exec-policy-0.110.0] https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/core/src/exec_policy.rs#L488

コマンドはsandboxで実行
--------------------------------------------------

* Approval: OnRequestでは、コマンドが失敗した時sandboxの外での実行は **しない**
* （コマンドが失敗した時にsandbox外で実行させることもできます。自走tips）

https://github.com/openai/codex/blob/rust-v0.110.0/codex-rs/core/src/tools/orchestrator.rs#L232

小まとめ：コマンド実行許可の裏側
==================================================

* Rulesのpatternやdecisionが優先される
* Rulesに無いコマンドは、sandboxやapprovalに基づいて処理（通常はworkspace-write・OnRequest）

ご清聴ありがとうございました！
--------------------------------------------------

Happy Python Development♪

.. Appendix 最初のプロンプト
