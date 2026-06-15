======================================================================
Claude Codeに実装を任せてのgood & more
======================================================================

Claude Code に実装を任せての good & more
======================================================================

:Event: Claude Code、どこまで任せられる？失敗事例から任せ方を学ぶLT会
:Presented: 2026/06/16 nikkie

お前、誰よ？（**Python使い** の自己紹介）
======================================================================

* nikkie（にっきー）・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__
* 機械学習エンジニア（`サマーインターン募集中 <https://hrmos.co/pages/uzabase/jobs/Newgrads28_002>`__）・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A提供 <https://jp.ub-speeda.com/news/20260319/>`__）

.. image:: ../_static/uzabase-white-logo.png

.. _cdcasasagi: https://github.com/ftnext/cdcasasagi

`cdcasasagi`_ （鵲）
======================================================================

* 自作したPython製CLIツール
* Claude Desktopの設定ファイル :file:`claude_desktop_config.json` を簡単に生成
* Opus(4.8 high)で実装、GPT(5.5)でレビュー 

mcp-proxy [#mcp-proxy-diagram]_
--------------------------------------------------

StreamableHTTP（やSSE）のMCPサーバをstdioとして見せられる

.. mermaid::

    graph LR
        A["Claude Desktop"] <--> |stdio| B["mcp-proxy"]
        B <--> |SSE| C["External MCP Server"]

        style A fill:#ffe6f9,stroke:#333,color:black,stroke-width:2px
        style B fill:#e6e6ff,stroke:#333,color:black,stroke-width:2px
        style C fill:#e6ffe6,stroke:#333,color:black,stroke-width:2px

.. [#mcp-proxy-diagram] https://github.com/sparfenyuk/mcp-proxy/tree/v0.12.0?tab=readme-ov-file#1-stdio-to-ssestreamablehttp

mcp-proxyを使う :file:`claude_desktop_config.json`
------------------------------------------------------------

.. code-block:: json
    :caption: commandは環境ごとのパス

    {
      "mcpServers": {
        "openai-developer-docs": {
          "command": "/Users/nikkie/.local/bin/mcp-proxy",
          "args": [
            "--transport",
            "streamablehttp",
            "https://developers.openai.com/mcp"
          ]
        }
      }
    }

cdcasasagiで設定を簡単に
------------------------------------------------------------

.. code-block:: console

    $ cdcasasagi add https://developers.openai.com/mcp --name openai-developer-docs --write

.. code-block:: json

    {
      "mcpServers": {
        "openai-developer-docs": {
          "command": "/Users/nikkie/.local/bin/mcp-proxy",
          "args": [
            "--transport",
            "streamablehttp",
            "https://developers.openai.com/mcp"
          ]
        }
      }
    }

cdcasasagiの開発
======================================================================

* 実装はClaude、レビューはGPT
* **33本** のプルリクエストをOpusに出させた
* 私（人間）は細かいところは見ずにコマンドを動作確認して検収

はじまりのissue
--------------------------------------------------

* `v0.1: cdcasasagi add #1 <https://github.com/ftnext/cdcasasagi/issues/1>`__
* ここからコマンドは増えていった：``import``, ``delete``, ``eject`` e.t.c.

実装はClaude
--------------------------------------------------

* 半分以上は **通勤中** に開発
* webでplan。実装後、プルリクエストの面倒を（人力交え）見させる
* ローカルで開発した後、 ``/autofix-pr`` でwebに面倒見させる

レビューはGPT
--------------------------------------------------

* `Codex plugin for Claude Code <https://github.com/openai/codex-plugin-cc>`__ を使い、Stop hookでCodexレビュー発火
* GitHubのPRへのpushをトリガーに `Codex cloudがレビュー <https://developers.openai.com/codex/integrations/github>`__ するように設定

私に **簡単** だったのでこの形
--------------------------------------------------

* Claude ``/autofix-pr``
* GPT レビュー設定が簡単（特にcloud）

.. ``/loop`` ``/goal``

実装をClaudeに任せてみて
======================================================================

* Opus **単体には任せられない** なあ
* 序列：Opus < 私 < GPT

※今回のPython製小さなCLIに限った話（私の使いこなし不足もあるかと）

Opusのplan
--------------------------------------------------

* planは一通りレビュー。「その設計判断はあかんでしょ」がたまにある

    * 複雑に考えすぎて設計を汚くしている

* 私の持っている知見を実装するClaudeに伝えていく余地を多分に残す

数値で見るGPTレビュー（※GPTによる集計）
--------------------------------------------------

* 全33PR
* P1（重大）コメントあり **6PR（18%）**
* P2コメントあり 24PR

事例：Opusはセキュリティへの意識低め
--------------------------------------------------

    P1 Avoid persisting GitHub token in remote URL

.. code-block:: md
    :caption: CLAUDE.md中の手順

    git remote set-url origin "https://ftnext:$(gh auth token)@github.com/ftnext/cdcasasagi.git

GPTのレビュー雑感
--------------------------------------------------

* Opusは実装する際の指示やplanから、そこにない要素（例：セキュリティ面）に注意を払っていない可能性
* GPTのレビューはめちゃめちゃ細かいところを拾う（融通が効かないので :file:`AGENTS.md` で調整）

.. ペアプロのドライバー（動くコードを書くのは難しい）とナビゲーター（設計判断などができる）？

Fabel？
======================================================================

* GPTのポジションが要らなくなる期待（モドテコイ！）
* Fabelが監督し、OpusやSonnet（やGPT）に実装させる

なぜかGPT-5.5がFabelにもっともな指摘
--------------------------------------------------

.. ただ不思議なことにGPTからツッコミが入ったんですよね...

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">これはFable 5、使いこなせてないってことですかね（裏で弱いモデルに差し代わった？）<br><br>リポジトリ全体にリファクタリングを計画させてみたところ、Codexのレビューループが設定されてて、「Codexの指摘はもっともだったわ…悔しいけど。」とのこと <a href="https://t.co/uD1OQLwoul">pic.twitter.com/uD1OQLwoul</a></p>&mdash; nikkie(にっきー) / にっP (@ftnext) <a href="https://x.com/ftnext/status/2064722440224432132?ref_src=twsrc%5Etfw">2026年6月10日</a></blockquote> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>

まとめ🌯：Claude Codeに実装を任せてのgood & more
======================================================================

:good: 小さなCLIは作れる！（通勤中に出来上がる開館）
:more: Opus単体には任せられない感触。人やGPTのレビューがいる

ご清聴ありがとうございました
------------------------------------------------------------

Happy Development ❤️🤖

OSSサポートに感謝申し上げます
------------------------------------------------------------

* `SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ (9k star) メンテナ
* `Claude for Open Source <https://claude.com/contact-sales/claude-for-oss>`__
* `Codex for Open Source <https://openai.com/ja-JP/form/codex-for-oss/>`__

EOF
===
