:ogp_title: Pythonから使うCodex CLI
:ogp_event_name: stapy-may
:ogp_slide_name: codex-python-sdk
:ogp_description: みんなのPython勉強会#121 LT
:ogp_image_name: stapy-may

.. Wake pet してデモの準備

======================================================================
Pythonから使うCodex CLI
======================================================================

:Event: みんなのPython勉強会#121
:Presented: 2026/05/21 nikkie

祝11周年！
======================================================================

ご参加いただいた方々に深く感謝

Codex [#codex-jp-page]_
======================================================================

* powered by ChatGPT (OpenAI)
* 知ってますか？🙋‍♂️ 使ってますか？🙋
* ChatGPT **無料版でも** 使えます

.. [#codex-jp-page] https://openai.com/ja-JP/codex/

.. （Claude Code書籍）

多様な形態 [#codex-quickstart]_
---------------------------------------------------

* App
* CLI
* IDE拡張
* Web

.. [#codex-quickstart] https://developers.openai.com/codex/quickstart#setup

nikkieとCodex
---------------------------------------------------

* CLIで使い出す
* いまは **Appおすすめ**。``git worktree`` が簡単！
* 鋭いレビューに開発中たびたび救われてきた [#codex-almost-everything]_

.. [#codex-almost-everything] 利用シーンはソフトウェア開発に **限りません**！ `（ほぼ）あらゆる作業に対応する Codex <https://openai.com/ja-JP/index/codex-for-almost-everything/>`__

Appには **pet** を [#codex-hatch-pet]_
---------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-conversation="none" data-lang="ja" data-align="center" data-dnt="true"><p lang="en" dir="ltr">Customize your Codex pet with /hatch <a href="https://t.co/6TUwiQJv8w">pic.twitter.com/6TUwiQJv8w</a></p>&mdash; OpenAI Developers (@OpenAIDevs) <a href="https://twitter.com/OpenAIDevs/status/2050275779452588309?ref_src=twsrc%5Etfw">2026年5月1日</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

.. [#codex-hatch-pet] https://developers.openai.com/codex/app/settings#codex-pets

多様な形態を支える **App Server**
======================================================================

* `Codex ハーネスの解放：App Server を構築した方法 <https://openai.com/ja-JP/index/unlocking-the-codex-harness/>`__
* JSON-RPC プロトコル
* 異なるクライアント（CLI、App、IDE拡張、...）が同じCodexハーネスを使用できる

TypeScript SDK
---------------------------------------------------

* https://developers.openai.com/codex/sdk#typescript-library
* https://www.npmjs.com/package/@openai/codex-sdk
* 利用例：`nrslib/takt <https://github.com/nrslib/takt>`__

実は **Python SDK** も
======================================================================

* https://developers.openai.com/codex/sdk#python-library
* まだPyPIにはありません
* 今日の内容はリリースされてから触るでも十分間に合います

環境構築
---------------------------------------------------

.. code-block:: console

    gh repo clone openai/codex
    cd codex/sdk/python
    uv sync --python 3.13

Hello world
---------------------------------------------------

.. code-block:: python

    >>> from shutil import which
    >>> codex_path = which("codex")
    >>> from openai_codex import AppServerConfig, Codex
    >>> with Codex(AppServerConfig(codex_bin=codex_path)) as codex:
    ...     thread = codex.thread_start(model="gpt-5.5")
    ...     result = thread.run("みんなのPython勉強会11周年の祝辞を述べて")
    ...     print(result.final_response)

豊富な例
---------------------------------------------------

* `Getting Started <https://github.com/openai/codex/blob/main/sdk/python/docs/getting-started.md>`__
* `examples <https://github.com/openai/codex/tree/main/sdk/python/examples>`__

.. _11_cli_mini_app: https://github.com/openai/codex/blob/main/sdk/python/examples/11_cli_mini_app/sync.py

11_cli_mini_app
---------------------------------------------------

.. code-block:: console
    :caption: 自分用ミニCLI！

    % .venv/bin/python examples/11_cli_mini_app/sync.py
    Codex mini CLI. Type /exit to quit.
    Thread: 019e4898-8563-7c62-b3f1-fa3cc112c6f1
    you> こんにちは
    assistant> こんにちは。何を進めますか？
    assistant.status> completed
    usage>
    last: input=19259 output=53 reasoning=38 total=19312 cached=3456
    total: input=19259 output=53 reasoning=38 total=19312 cached=3456

裏の仕組み：直接JSON-RPC
---------------------------------------------------

.. code-block:: json
    :caption: ``codex app-server`` して1行ずつ入力していきます

    {"id":"CBDA577B-6280-4C3E-8C00-523BA5033C2D","method":"initialize","params":{"clientInfo":{"name":"codex_python_sdk","title":"Codex Python SDK","version":"1.131.0"},"capabilities":{"experimentalApi":true}}}
    {"method":"initialized"}
    {"id":"1CA55CCA-DBAB-4048-93FF-C5EC22DCE350","method":"thread/start","params":{"approvalPolicy":"on-request","approvalsReviewer":"auto_review","model":"gpt-5.5"}}
    {"id":"42DDE51B-6FD6-40F0-BCBF-C701AF5BE6C0","method":"turn/start","params":{"threadId":"019e49b5-5261-7993-b82e-2058d951b9de","input":[{"type":"text","text":"みんなのPython勉強会11周年の祝辞を述べて"}]}}

まとめ🌯：Pythonから使うCodex CLI
======================================================================

* OpenAIがCodexを多様な形態で提供できるヒミツ： **App Server**
* リポジトリには **Python SDK** がある
* 環境構築してPythonからCodexを操作できた！

ご清聴ありがとうございました！
---------------------------------------------------

* nikkie(にっきー) `Codex Ambassador (Tokyo) <https://x.com/ftnext/status/2051929099992707217>`__
* 機械学習エンジニア（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A提供 <https://jp.ub-speeda.com/news/20260319/>`__）

.. image:: ../_static/uzabase-white-logo.png
