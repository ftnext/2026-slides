:ogp_title: Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
:ogp_event_name: pyconjp
:ogp_slide_name: teach-venv-pip-install-alternatives
:ogp_description: PyCon JP 2026 #pyconjpB

================================================================================
Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
================================================================================

Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
================================================================================

:Event: PyCon JP 2026 ``#pyconjpB``
:Presented: 2026/8/21 nikkie

**意見を集める** 時間です！
--------------------------------------------------

* PyCon JP 2026のプログラムは「`対話と交流 <https://techplay.jp/column/2127>`__」
* `Code of Conduct 行動規範 <https://2026.pycon.jp/ja/coc>`__ を守って楽しく *決闘*
* 各位の技術的な選択に **敬意** を

Python公式チュートリアルより
==================================================

.. code-block:: console
    :caption: `12. 仮想環境とパッケージ <https://docs.python.org/ja/3/tutorial/venv.html>`__

    $ python3.14 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ python -m pip install httpx2

2026年時点でも最適な一歩目？
--------------------------------------------------

* 議論ポイント：最初に教えるときに「venv を作って pip install」を選択しますか？
* `Python Boot Camp <https://pycamp.pycon.jp/textbook/7_scraping.html>`__ でやりたいのは、パッケージ（requests）を使ったWeb API呼び出し
* ``#pyconjpB`` でツイート推奨

お前、誰よ
============================================================

* nikkie（にっきー） [#nikkie-uuid]_ ・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__・`Devin Ambassador <https://x.com/ftnext/status/2069459222040105357>`__ [#coba-hiroshima-iizo]_
* 機械学習エンジニア・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-uuid] UUID `28fb3f96-a221-462c-93bd-567b431715b9 <https://x.com/ftnext/status/2041119610368602138>`__

.. [#coba-hiroshima-iizo] 8/20(木)の `もくもく会 <https://aid.connpass.com/event/401330/>`__ に使わせていただいた、コワーキングスペース `co-ba <https://co-ba.net/hiroshima/>`__ さんよかったです

「venvはもはや必須科目ではない」
------------------------------------------------------------

.. image:: ../_static/findy-ogp-chottowakaru-python.png
    :target: https://findy-code.io/media/articles/chotto-wakaru-python
    :alt: 最近、なぜみんなuvを使っているんですか？ Pythonパッケージ管理の変遷と現在地

IMO：Pythonの こんなチュートリアルはどうだい？
------------------------------------------------------------

* uv導入 [#nikkie-uv-impression]_。 **uvでPythonをインストール**
* Pythonの文法説明
* **仮想環境を省略**。スクリプトは後述する *inline script metadata* で実行（``uv run script.py``）

.. [#nikkie-uv-impression] チュートリアルにuvを推しますが、私はuvに満足していません。むしろAstralに伝えたいことは山ほどあります（インタビュー記事や廊下でどうぞ）

メッセージ「仮想環境を ツールに任せて楽してこーぜ」
------------------------------------------------------------

* Pythonの仮想環境は変わらず必要
* 仮想環境を **どう管理するか** は再考の余地がある
* パッケージを使う最初の一歩をどう案内するか、ここに参加者の皆さんと **集合知**

目次：Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
================================================================================

1. 仮想環境はなぜ必要か
2. 仮想環境の管理方法（人力 or ツール）
3. ひろがる、ツールで仮想環境管理
4. 2026年で考えたいトピック

.. include:: why-virtual-environment-needed.rst.txt

.. include:: virtual-environment-management.rst.txt

.. include:: bye-human-managed-virtual-environments.rst.txt

.. include:: topics-2026.rst.txt

まとめ🌯：Pythonチュートリアル、venv を作って pip install と2026年も教え続けますか？
==========================================================================================

* 私の立場は「**否** （＝教え続けない）」
* uvでPythonを入れ、inline script metadataで仮想環境を初回は飛ばす（ただしcooldownは伝える）

仮想環境の扱い方は **少しずつよくなって** きた
------------------------------------------------------------

* uvは仮想環境を「`正しい使い方を簡単に、誤った使い方を困難に <https://yoshi389111.github.io/kinokobooks/prog_ja/prog053.htm>`__」した（+爆速 & ワンストップ）
* 10年前は人力全盛だったが、ツールが進化した今、人力以外の選択肢がある
* **仮想環境の抽象化・カプセル化**：仕組みを詳しく知らなくても使える

Pythonで仕事をしている方は
------------------------------------------------------------

* どこかの段階で **仮想環境を理解するのをおすすめ** （それは最初でなくていい）
* Python処理系がどう動くのか知っている範囲を広げられる。結果、エンジニアとして解ける課題が広がる
* このトークをきっかけにしてもいいかもしれませんね

参考文献リスト 🏃‍♂️
------------------------------------------------------------

* 『`ハイパーモダンPython`_』
* `PEP 405 – Python Virtual Environments <https://peps.python.org/pep-0405/>`__
* ばんくしさん「`ゼロから作る自作 Python Package Manager 入門 <https://techbookfest.org/product/rpXewXTtekXgNPFBCWLrX4>`__」

.. https://nikkie-ftnext.hatenablog.com/entry/vaaaaanquish-python-package-manager-diy-introduction-is-awesome

ご清聴ありがとうございました
------------------------------------------------------------

あなただったら、venv を作って pip install と教えますか？

このあと15:00〜 stapyコミュニティブースへどうぞ🌸
================================================================================

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">コミュニティブースにみんなのPython勉強会あります〜 <a href="https://x.com/hashtag/stapy?src=hash&amp;ref_src=twsrc%5Etfw">#stapy</a> <a href="https://x.com/hashtag/pyconjp2026?src=hash&amp;ref_src=twsrc%5Etfw">#pyconjp2026</a><br>お好み焼き・宮島stapyステッカーも配布してます <a href="https://t.co/EdmTG5F35q">pic.twitter.com/EdmTG5F35q</a></p>&mdash; nikkie(にっきー) / にっP (@ftnext) <a href="https://x.com/ftnext/status/2090649754258821555?ref_src=twsrc%5Etfw">2026年8月21日</a></blockquote> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>

来週東京でDevinCon！
------------------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">📣 DevinCon Tokyo、8/26（水）開催決定！<br>Cognition初の日本コミュニティイベント。Devinユーザーに限らず、AI駆動開発に取り組むすべてのエンジニアをお待ちしています。Migration / SRE / AI駆動開発組織設計、各社の実践知が集まります。…</p>&mdash; Cognition Japan (@cognition_jp) <a href="https://x.com/cognition_jp/status/2082631076900721116?ref_src=twsrc%5Etfw">2026年7月30日</a></blockquote>

EOF
===
