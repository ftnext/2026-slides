================================================================================
Pythonの環境構築をすることになったあなたへ（2026年版）
================================================================================

Pythonの環境構築をすることになったあなたへ（2026年版）
================================================================================

:Event: Python環境構築を、もう一度考える
:Presented: 2026/11/4 nikkie （スペース連打 or 矢印キーでめくります）

お集まりいただきありがとうございます
==================================================

* ゴール：今（2026年）の **Python環境構築がつかめる** （入口までお連れします）
* Pythonの経験がない方も踏まえて前提知識補いながらお伝えします📻

お前、誰よ
============================================================

* nikkie（にっきー）・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__・`Devin Ambassador <https://x.com/ftnext/status/2069459222040105357>`__
* 機械学習エンジニア [#uzabase-message]_ ・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__・`Slackbot <https://jp.ub-speeda.com/news/20260910/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#uzabase-message] お詫び申し上げます。`【第二報】NewsPicksのお客様の個人情報漏洩の可能性に関するお詫びとお知らせ <https://corp.newspicks.com/info/20261009>`__

Python歴
------------------------------------------------------------

* 2016〜 ソフトウェアエンジニア
* 2017年11月 Pythonを独学開始
* 2019〜 仕事でもPython（ユーザベース 機械学習エンジニア）
* LT、ブログ、PyCon JP 登壇

興味あれば後ほどどうぞ
------------------------------------------------------------

.. image:: ../_static/findy-ogp-chottowakaru-python.png
    :target: https://findy-code.io/media/articles/chotto-wakaru-python
    :alt: 最近、なぜみんなuvを使っているんですか？ Pythonパッケージ管理の変遷と現在地

興味あれば後ほどどうぞ その2
------------------------------------------------------------

.. raw:: html

    <iframe width="800" height="480" src="https://ftnext.github.io/2026-slides/pyconjp/teach-venv-pip-install-alternatives.html#/1"
        title="Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？"></iframe>

目次：Pythonの環境構築をすることになったあなたへ
================================================================================

1. Pythonのドキュメントの方法（uv以前）
2. uv以後
3. 2026年の話題

.. include:: basic.rst.txt

.. include:: uv-way.rst.txt

小まとめ🥟 uvに任せられること
==================================================

* Pythonの管理
* 仮想環境の管理（サードパーティパッケージ管理）

簡単なので任せていっています

.. include:: uv-usecases.rst.txt

TODO お昼明けからすぐにuvだ！<-そこまで言ってない
------------------------------------------------------------

* 変えるのは新規プロジェクトからでいいと思っています
* ツールの単なる置き換えは、ユーザへの価値をほとんど生み出さないですよね
* uv-migrate

.. include:: topics-2026.rst.txt

TODO One more thing: pnpm
------------------------------------------------------------

.. 未来 PEP 831？

.. チュートリアルにuvを推しますが、私はuvに満足していません。むしろAstralに伝えたいことは山ほどあります（インタビュー記事や廊下でどうぞ）

まとめ🌯 Pythonの環境構築をすることになったあなたへ（2026年版）
================================================================================

* uvを試してみてはいかがでしょうか？
* Pythonの管理、仮想環境管理、``uv tool install``・inline script metadataととっても便利ですよ

仮想環境の管理が簡単になっている
------------------------------------------------------------

* uvは仮想環境を「`正しい使い方を簡単に、誤った使い方を困難に <https://yoshi389111.github.io/kinokobooks/prog_ja/prog053.htm>`__」した（+爆速 & ワンストップ）
* **仮想環境の抽象化・カプセル化**：仕組みを詳しく知らなくても使える
* メッセージ「仮想環境をツールに任せて楽してこーぜ」

参考文献リスト 🏃‍♂️
------------------------------------------------------------

* 『`ハイパーモダンPython <https://www.oreilly.co.jp/books/9784814400928/>`__』
* `PEP 405 – Python Virtual Environments <https://peps.python.org/pep-0405/>`__
* ばんくしさん「`ゼロから作る自作 Python Package Manager 入門 <https://techbookfest.org/product/rpXewXTtekXgNPFBCWLrX4>`__」

.. https://nikkie-ftnext.hatenablog.com/entry/vaaaaanquish-python-package-manager-diy-introduction-is-awesome

ご清聴ありがとうございました
------------------------------------------------------------

EOF
===
