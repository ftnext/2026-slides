:ogp_title: ローカルLLMをFirefoxに住まわせる
:ogp_event_name: hannari-local-llm
:ogp_slide_name: llm-lives-in-firefox
:ogp_description: ローカルLLMやってみたLT会！（2026/05）

======================================================================
ローカルLLMをFirefoxに住まわせる
======================================================================

:Event: ローカルLLMやってみたLT会！
:Presented: 2026/05/29 nikkie

.. デモ後に開く想定
.. 5分LT：冒頭2分デモ、残り3分で「今のデモを再現するには」を説明

今のデモで見せたもの
======================================================================

Firefoxのサイドバーに **ローカルLLM** を置きました

* ページ全体を日本語で要約
* 選択範囲にプロンプト

登場人物
======================================================================

* Firefox：`AI制御 (AI controls) <https://blog.mozilla.org/en/firefox/ai-controls/>`__ 機能 (Firefox 148〜)
* `Gemma 4 <https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/>`__
* `Ollama <https://docs.ollama.com/>`__
* `Open WebUI <https://docs.openwebui.com/>`__

構成
--------------------------------------------------

.. mermaid::

    flowchart TD
        A[Firefox<br>AI制御] -->|iframe| B[Open WebUI<br>localhost:8080]
        B -->|Ollama API| C[Ollama<br>localhost:11434]
        C --> D["gemma4:e4b"]

手順1：OllamaでGemmaをサーブ
--------------------------------------------------

.. code-block:: console

    $ ollama --version
    ollama version is 0.22.0

    $ ollama pull gemma4:e4b

.. code-block:: console
    :caption: Ollama API 動作確認

    % curl http://localhost:11434/api/tags

手順2：Open WebUIを起動
--------------------------------------------------

.. code-block:: console

    % uv tool install open-webui
    % DATA_DIR=~/.open-webui open-webui serve

http://localhost:8080/ でOpen WebUIが開きます

手順3：Open WebUIを設定
--------------------------------------------------

* 初回ウィザードで管理者アカウントを作成
* 管理画面でOllamaへの接続を設定

  * ``http://localhost:11434``

* Open WebUI上で ``gemma4:e4b`` が選べればOK

手順4：Firefoxの設定
--------------------------------------------------

* 設定 > AI制御 を有効に（「AI支援をブロックする」false）
* タブで ``about:config`` を開く

.. code-block:: text

    browser.ml.chat.hideLocalhost

これを ``false`` にします

.. Firefoxの設定名からすると「hide localhost」を無効化する、という説明が自然

Firefoxに住まわせた！
======================================================================

* サイドバー > AIチャットボットに **localhost** を選ぶ
* ``http://localhost:8080`` のOpen WebUIが出る
* Firefoxに必要なのはAPIではなく **Web UI**

ボタン1つで要約させ放題！
--------------------------------------------------

TODO 画像

まとめ🌯：ローカルLLMをFirefoxに住まわせる
======================================================================

* Gemma4:e4bをOllamaでAPIにし、Open WebUIでFirefoxに住まわせた
* FirefoxのAI制御機能でlocalhostを設定している
* **呼び出し放題** はいいぞ

ふだんのコマンドはこれだけ
--------------------------------------------------

.. code-block:: console

    % # OllamaはPC起動時に起動する設定
    % DATA_DIR=~/.open-webui open-webui serve

ご清聴ありがとうございました
======================================================================

* nikkie(にっきー) / `@ftnext <https://x.com/ftnext>`__ / `Codex Ambassador (Tokyo) <https://x.com/ftnext/status/2051929099992707217>`__
* 機械学習エンジニア（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A提供 <https://jp.ub-speeda.com/news/20260319/>`__）

.. image:: ../_static/uzabase-white-logo.png

参考資料
======================================================================

* `第902回 FirefoxのAIチャットボットをローカルLLMで使用する <https://gihyo.jp/admin/serial/01/ubuntu-recipe/0902>`__ （llama.cpp構成）
* 拙ブログ `Firefox の AI コントロール機能を設定して、Ollama で動かすローカルの gemma4:e4b を Firefox に住まわせる <https://nikkie-ftnext.hatenablog.com/entry/firefox-ai-control-ollama-local-gemma4-via-open-webui>`__
