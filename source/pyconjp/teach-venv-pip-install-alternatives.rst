================================================================================
Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
================================================================================

Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
================================================================================

:Event: PyCon JP 2026 ``#pyconjpB``
:Presented: 2026/8/21 nikkie

**議論** の時間です！
==================================================

* `Code of Conduct 行動規範 <https://2026.pycon.jp/ja/coc>`__
* 各位の技術的な選択に **敬意** を払いましょう
* ルールを守って楽しく *決闘*

Pythonチュートリアルより
==================================================

.. code-block:: console
    :caption: `12. 仮想環境とパッケージ <https://docs.python.org/ja/3/tutorial/venv.html>`__

    $ python3.14 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ python -m pip install httpx2

2026年時点でも最適な一歩目？
--------------------------------------------------

* パッケージを使って例えばWeb API呼び出し（`Python Boot Camp <https://pycamp.pycon.jp/textbook/7_scraping.html>`__）
* 最初に教えるとしたら、「venv を作って pip install」を選択しますか？（議論ポイント）
* ``#pyconjpB`` でツイート推奨

.. TODO Sites作る余地がある

「venv を作って pip install」以外の選択肢（Takeaway）
------------------------------------------------------------

.. TODO 考える材料を提供

* Pythonをも管理する環境管理ツールの登場（代表例：uv）
* CLIツール向け（一時的）仮想環境自動管理
* PEP 723 (inline script metadata)

メッセージ
------------------------------------------------------------

* Pythonの仮想環境は変わらず必要
* 仮想環境を **どう作るか** は再考の余地がある
* 環境構築一歩目をどう案内するか、ここに参加者の皆さんと集合知

お前、誰よ
============================================================

* nikkie（にっきー） [#nikkie-uuid]_ ・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__・`Devin Ambassador <https://x.com/ftnext/status/2069459222040105357>`__
* 機械学習エンジニア・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-uuid] UUID `28fb3f96-a221-462c-93bd-567b431715b9 <https://x.com/ftnext/status/2041119610368602138>`__

Findyさんインタビュー
------------------------------------------------------------

.. TODO 画像にする余地あり

`最近、なぜみんなuvを使っているんですか？ Pythonパッケージ管理の変遷と現在地 <https://findy-code.io/media/articles/chotto-wakaru-python>`__

インタビューより「最初にvenvを教える、その必要はもうないわ」
------------------------------------------------------------

* **一歩目には uv** を推します [#nikkie-uv-impression]_
* venv（仮想環境）を理解していなくても、間違えず簡単にPythonを使える
* Web API呼び出しの例は、*inline script metadata* （後述）

.. [#nikkie-uv-impression] uvを推しますが、私はuvに満足していません。むしろAstralに伝えたいことは山ほどあります（廊下でどうぞ）

.. 【53】正しい使い方を簡単に、誤った使い方を困難に
    https://yoshi389111.github.io/kinokobooks/prog_ja/prog053.htm
    IMO：シンプルを好むが、シンプルは理解が必要で、あまり簡単にはならない。多数で使うならeasyな方ではないか

.. TODO 目次

.. include:: why-virtual-environment-needed.rst.txt

.. include:: virtual-environment-management.rst.txt

.. include:: topics-2026.rst.txt

まとめ🌯：Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
==========================================================================================

* 仮想環境は入門時に必須でないと考えます（inline script metadata）
* 知っている範囲を増やしていけば、スクリプトからプロジェクトへと移行容易なuv
* 最新版のインストールはリスクです。cooldownの設定推奨

.. Pythonの理解を深めたい方（開発者）には、仮想環境の理解を推奨

ご清聴ありがとうございました
------------------------------------------------------------
