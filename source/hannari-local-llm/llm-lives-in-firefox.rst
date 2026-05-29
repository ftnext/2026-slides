:ogp_title: LLMはFirefoxに住める
:ogp_event_name: hannari-local-llm
:ogp_slide_name: llm-lives-in-firefox
:ogp_description: FirefoxのサイドバーからOllamaのローカルLLMを使う

======================================================================
LLMはFirefoxに住める
======================================================================

:Event: はんなりローカルLLM
:Presented: 2026/05/29 nikkie

.. デモ後に開く想定
.. 5分LT：冒頭2分デモ、残り3分で「今のデモを再現するには」を説明

今のデモで見せたもの
======================================================================

Firefoxのサイドバーに **ローカルLLM** を置きました

* ページ全体を要約
* 選択範囲にプロンプト
* 英語記事を日本語で読んでいく

構成
======================================================================

.. mermaid::

    flowchart TD
        A[Firefox<br>AI コントロール] -->|iframe| B[Open WebUI<br>localhost:8080]
        B -->|Ollama API| C[Ollama<br>localhost:11434]
        C --> D["gemma4:e4b"]

ポイント：Firefoxが見るのは **Web UI**
------------------------------------------------------------

* Firefoxのサイドバーには iframe で表示される
* Ollama単体はAPIを返すだけ
* そこで **Open WebUI** を前段に置く

登場人物
======================================================================

* Firefox：AI コントロール機能
* Open WebUI：OllamaのWeb UI（``localhost:8080``）
* Ollama：``gemma4:e4b`` を動かす（``localhost:11434``）

手順1：Ollamaでモデルを用意
======================================================================

.. code-block:: console

    $ ollama --version
    ollama version is 0.22.0

    $ ollama pull gemma4:e4b

``localhost:11434`` でOllama APIが動きます

手順2：Open WebUIを起動
======================================================================

ブログ記事からのアップデート： **uvで入れるだけ**

.. code-block:: console

    % uv tool install open-webui
    % DATA_DIR=~/.open-webui open-webui serve

http://localhost:8080/ でOpen WebUIが開きます

うれしいポイント
------------------------------------------------------------

* ネットワーク設定で悩まない
* Open WebUIからOllamaへは ``localhost:11434`` で届く
* Pythonツールとして入るので、LTで説明する手順が短い

.. code-block:: console

    % curl http://localhost:11434/api/tags

手順3：Open WebUIを設定
======================================================================

http://localhost:8080/

* 初回ウィザードで管理者アカウントを作成
* 管理画面でOllamaへの接続を設定

  * ``http://localhost:11434``

* Open WebUI上で ``gemma4:e4b`` が選べればOK

手順4：Firefoxでlocalhostを選べるようにする
======================================================================

``about:config`` を開く

.. code-block:: text

    browser.ml.chat.hideLocalhost

これを ``false`` にします

.. Firefoxの設定名からすると「hide localhost」を無効化する、という説明が自然

FirefoxのAIコントロール設定
======================================================================

* サイドバーを開く
* AIチャットボットに **localhost** を選ぶ
* ``http://localhost:8080`` のOpen WebUIが出る

つまり、FirefoxにLLMが住んでいるように見えて、
実体は **Firefox → Open WebUI → Ollama → ローカルモデル** です

ハマりどころ
======================================================================

* Firefoxに必要なのは **APIではなくWeb UI**
* ``open-webui serve`` とOllamaの両方を起動しておく
* モデルが見えない時は ``curl localhost:11434/api/tags``
* 初回はOpen WebUIの管理者アカウント作成が必要

なぜうれしい？
======================================================================

* ブラウザから離れずに要約・翻訳できる
* ローカルLLMなので呼び出し放題
* ページ全体だけでなく、選択範囲に対して質問できる
* 「記事を読む」体験にLLMが自然に混ざる

まとめ
======================================================================

* FirefoxのAIコントロールはサイドバーにWeb UIを出せる
* Ollama単体ではなく、Open WebUIを挟むとFirefoxから使いやすい
* ``about:config`` でlocalhostを有効化すれば、ローカルLLMがFirefoxに住む

参考
======================================================================

* `Firefox の AI コントロール機能を設定して、Ollama で動かすローカルの gemma4:e4b を Firefox に住まわせる <https://nikkie-ftnext.hatenablog.com/entry/firefox-ai-control-ollama-local-gemma4-via-open-webui>`__
* `第902回 FirefoxのAIチャットボットをローカルLLMで使用する <https://gihyo.jp/admin/serial/01/ubuntu-recipe/0902>`__
* `Open WebUI <https://openwebui.com/>`__
* `Ollama <https://ollama.com/>`__

ご清聴ありがとうございました
======================================================================

nikkie(にっきー) / `@ftnext <https://x.com/ftnext>`__
