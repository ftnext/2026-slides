============================================================
仮想環境からの脱却：2026年に向けたPythonの新しいパラダイム
============================================================

仮想環境からの脱却：2026年に向けたPythonの新しいパラダイム
============================================================

:Event: PythonAsia 2026
:Presented: 2026/03/22 nikkie

.. 1. 導入（3分）

こんにちは、PythonAsia！（お前、誰よ）
============================================================

* 東京で機械学習エンジニア。`Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`A2A提供開始 <https://jp.ub-speeda.com/news/20260319/>`__） [#uzabase-south-asia-news]_
* `sphinx-new-tab-link <https://github.com/ftnext/sphinx-new-tab-link>`__ はじめOSS開発。`SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ メンテナ

.. image:: ../_static/uzabase-white-logo.png

.. [#uzabase-south-asia-news] `Acquisition of Sealed Network <https://uzabaseglobal.com/press-release/uzabase-expands-southeast-asia-expert-network-with-acquisition-of-sealed-network>`__

昔はいつも管理していたのに、今ではほとんど管理しなくてよいもの、なに？
======================================================================

.. PyCon JPのプロポーザル確認（あと東海、静岡？）

答えは **仮想環境**
------------------------------------------------------------

.. 挙手？ みなさん、仮想環境管理していますか？

仮想環境を開発者が管理する必要はなくなっている
------------------------------------------------------------

.. - このパラダイムシフトの予告

* *一時的な仮想環境* を使ったコマンド実行
* *inline script metadata* (PEP 723)
* Pythonプロジェクト管理ツール

BREAKING NEWS!!
------------------------------------------------------------

.. 今日の結論がいつまで言えるかわからないが、用意してきた内容で話します

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="en" data-align="center" data-dnt="true"><p lang="en" dir="ltr">We&#39;ve reached an agreement to acquire Astral.<br><br>After we close, OpenAI plans for <a href="https://twitter.com/astral_sh?ref_src=twsrc%5Etfw">@astral_sh</a> to join our Codex team, with a continued focus on building great tools and advancing the shared mission of making developers more productive.<a href="https://t.co/V0rDo0G8h9">https://t.co/V0rDo0G8h9</a></p>&mdash; OpenAI Newsroom (@OpenAINewsroom) <a href="https://twitter.com/OpenAINewsroom/status/2034616934671724639?ref_src=twsrc%5Etfw">2026年3月19日</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

仮想環境からの脱却 目次
============================================================

1. 仮想環境の基礎
2. 手動で仮想環境管理のつらさ
3. 解決策の進化（メインパート）

2026年現在可能になった解決策
------------------------------------------------------------

1. *一時的な仮想環境* を使ったコマンド実行
2. *inline script metadata* (PEP 723)

.. 2. 仮想環境の基礎（3分）

1️⃣仮想環境の基礎
============================================================

仮想環境はなぜ私たち（Python開発者）に必要なのか

Pythonチュートリアルより
------------------------------------------------------------

.. 従来のワークフロー: 作成、アクティベート、インストール、利用

.. code-block:: shell

    $ python -m venv .venv --upgrade-deps
    $ source .venv/bin/activate
    (.venv) $ python -m pip install sampleproject

`12.2. Creating Virtual Environments <https://docs.python.org/3.14/tutorial/venv.html#creating-virtual-environments>`__

.. A common directory location for a virtual environment is .venv.
    https://nikkie-ftnext.hatenablog.com/entry/python-venv-directory-name-202404

仮想環境とは **ディレクトリ**
------------------------------------------------------------

.. code-block:: shell

    % python -m venv --help
    usage: venv ENV_DIR [ENV_DIR ...]

.. code-block:: shell
    :caption: :file:`.venv/` というディレクトリができている

    % ls -al
    drwxr-xr-x@  7 nikkie  staff  224 Mar 20 12:42 .venv

.. - 仮想環境とは何か、そしてなぜPythonで必要だったのかを簡単におさらいする

なぜディレクトリを作るのか
------------------------------------------------------------

* **サードパーティライブラリ** のインストール先にするため
* 仮に仮想環境を使わない場合、インストール先はマシンの中に1箇所

.. TODO 図解を考える

:file:`.venv/` には何がある？ [#python314-easter-egg]_
------------------------------------------------------------

.. tree -L 2 .venv を加工

.. code-block:: txt

    .venv
    ├── bin
    │   ├── activate
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.14
    │   ├── python -> python3.14
    │   ├── python3 -> python3.14
    │   ├── python3.14 -> /Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14
    │   └── 𝜋thon -> python3.14
    ├── lib
    │   └── python3.14
    └── pyvenv.cfg

.. [#python314-easter-egg] easter egg: 𝜋thon https://github.com/python/cpython/pull/125035

:file:`.venv/bin/python`
------------------------------------------------------------

* マシンにインストールしたPython処理系への **シンボリックリンク**
* :file:`activate` では環境変数 ``PATH`` を更新して、この処理系が見つかるようにしている
* 処理系と標準ライブラリはこちらを使う

:file:`.venv/lib/python3.14/site-packages`
------------------------------------------------------------

* サードパーティライブラリのインストール先のディレクトリ
* 仮想環境ごとに分かれているので、**バージョン違いが共存** する

.. python -m site で標準ライブラリ + 仮想環境のサードバーティライブラリが確認できる

.. 3. 手動管理のつらさ（4分）

2️⃣俺たちが、仮想環境管理ツールなんだ
============================================================

.. code-block:: shell

    $ python -m venv .venv --upgrade-deps
    $ source .venv/bin/activate
    (.venv) $ python -m pip install sampleproject

人力管理のつらみを挙げていく（全4つ）

.. - こうした問題がなぜ生産性に影響するのか

仮想環境の再現：``pip freeze``
------------------------------------------------------------

.. code-block:: shell

    (.venv) $ python -m pip freeze > requirements.txt

.. code-block:: shell

    $ python -m venv other-env --upgrade-deps
    $ source other-env/bin/activate
    (other-env) $ python -m pip install -r requirements.txt

`12.3. Managing Packages with pip <https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip>`__

依存ライブラリには2種類ある
------------------------------------------------------------

:直接(direct): 例 httpx
:推移的(transitive): httpcore, h11, ...

課題1: ``pip freeze`` の出力は扱いが難しい
------------------------------------------------------------

* directな依存もtransitiveな依存も1つの :file:`requirements.txt` にまとまる
* directな依存にextraを指定していた場合、:file:`requirements.txt` ではextraの情報は失われる

.. そもそも今の仮想環境を正として出力するのではなく、ライブラリの組合せが正ではないか

課題2: 特定のパッケージをアンインストールしづらい
------------------------------------------------------------

* directな依存を消す際、**transitiveな依存の削除** が大変
* 直接の依存1は libA, libB に依存
* 直接の依存2は libA, libC に依存

.. 直接の依存と推移的な依存    
    依存2を消すとき、libCは消せるが、libAは消せない

.. revealjs-break::
    :notitle:

.. image:: ../_static/pythonasia/remove-direct-dependency.drawio.png

課題3: スクリプトごとの仮想環境
------------------------------------------------------------

* 気になるライブラリを試したいだけだが、毎回仮想環境を作ることになる

.. code-block:: txt
    :caption: このようなディレクトリがいくつも

    .
    ├── .venv/
    └── script.py

課題4: リンタやフォーマッタが仮想環境ごとに
------------------------------------------------------------

* 開発中に使うコマンドラインツールを **どの仮想環境にも都度** インストールする
* どのプロジェクトでも最新に保つのが大変

仮想環境管理ツール、俺たちが抱えるペイン
------------------------------------------------------------

1. directもtransitiveも1つにまとまる ``pip freeze``
2. directと一緒にどのtransitiveまでは消していい？
3. たくさんのスクリプトと仮想環境
4. リンタやフォーマッタをどの仮想環境にもインストールして最新化していく

.. 4. 解決策の進化（5分）

3️⃣コミュニティがこれらの課題にどう対応してきたか
============================================================

.. TODO ここはどの課題へのアプローチが伝わるように構成できるとよさそう

1. directもtransitiveも1つにまとまる ``pip freeze``
2. directと一緒にどのtransitiveまでは消していい？
3. たくさんのスクリプトと仮想環境
4. リンタやフォーマッタをどの仮想環境にもインストールして最新化していく

.. _pip-tools: https://github.com/jazzband/pip-tools

`pip-tools`_
------------------------------------------------------------

* ``pip freeze`` に代えて
* 課題1: directもtransitiveもまとまるの解消
* directな依存の指定を変えることで、課題2も解消される

pip-tools のワークフロー
------------------------------------------------------------

:command:`pip-compile` & :command:`pip-sync`

.. image:: ../_static/pythonasia/pip-tools-overview.svg

https://github.com/jazzband/pip-tools/blob/v7.5.3/img/pip-tools-overview.svg

.. revealjs-break::

:pip-compile: :file:`requirements.in` (direct)から :file:`requirements.txt` (direct & transitive)を生成する
:pip-sync: :file:`requirements.txt` に仮想環境を一致させる

.. _Poetry: https://github.com/python-poetry/poetry

`Poetry`_
------------------------------------------------------------

.. - Poetry のアプローチ: プロジェクト単位での仮想環境管理

* :command:`poetry add` に直接の依存を指定（課題1・2へのアプローチ）
* pip-toolsに比べて、**仮想環境をより意識しない** （:command:`poetry run`） [#poetry-uses-project-venv]_
* Pythonプロジェクト開発で受け入れられてきた印象（2020年前後） [#poetry-alternative-pipenv]_

.. [#poetry-uses-project-venv] `use the {project-dir}/.venv directory if one already exists. <https://python-poetry.org/docs/configuration/#virtualenvsin-project>`__

.. [#poetry-alternative-pipenv] `Pipenv <https://github.com/pypa/pipenv>`__ もPythonプロジェクト開発で受け入れられていました

.. _Rye: https://github.com/astral-sh/rye

`Rye`_ [#rye-sunset]_
------------------------------------------------------------

.. - Rye の登場と、それが uv に与えた影響

* Rust製（Python製ツールより高速）
* **Python自体の管理** + 仮想環境管理（pip-tools）
* pipのない仮想環境

.. [#rye-sunset] mitsuhiko-sanが作り、Astralに移管された後、2026年2月にアーカイブされていました。お疲れさまでした

そしてuv
------------------------------------------------------------

* pipのRust実装として登場。`drop-in replacement for pip and pip-tools workflows. <https://astral.sh/blog/uv>`__
* Pythonの管理もプロジェクトの仮想環境の管理もできるように [#uv-unified-python-packaging]_
* 4つの課題にアプローチできている（このあと紹介）

.. [#uv-unified-python-packaging] https://astral.sh/blog/uv-unified-python-packaging

.. * **高速** [#how-uv-got-so-fast]_
    [#how-uv-got-so-fast] https://nesbitt.io/2025/12/26/how-uv-got-so-fast.html

uvへと至る流れ
------------------------------------------------------------

* Poetry（やPipenv）がプロジェクトの仮想環境管理を簡単に
* RyeがPythonの管理やpip-toolsを使った仮想環境管理をするツールとして注目
* さらに *pipx* や *PEP 723* を取り込んだuvへ（このあと紹介）

.. include:: ja/standalone-cli.rst.txt

.. include:: ja/inline-script-metadata.rst.txt

.. 8. ツール選定とまとめ（2分）

最後に、ツール選定
============================================================

Pythonプロジェクト管理も踏まえて

* uv🏅
* Hatch❤️

Poetry
------------------------------------------------------------

.. Poetry の成熟度：最新の仕様に追従できていない

* コマンド実行やスクリプト実行以外をPoetryがだいぶ楽にしてくれて偉大
* `PEP 621 <https://peps.python.org/pep-0621/>`__ (``[project]``)サポートが4年後の `2.0.0 <https://github.com/python-poetry/poetry/releases/tag/2.0.0>`__ のように、最新の仕様に即時追従できていない状況（オススメしづらい）

uv🏅
------------------------------------------------------------

.. `uv` はオールインワンの有力解だが、唯一の選択肢ではない

* Pythonプロジェクト管理もサポート（:file:`pyproject.toml` を強制）

    * :command:`uv add` や :command:`uv sync`

* 1つのツールで ``uvx`` や inline script metadata まで広くサポートするので現時点で **最有力**

Hatch
------------------------------------------------------------

* uvはPythonプロジェクトは1つ仮想環境。この前提が違うツールとして注目している
* **複数の仮想環境** をHatchが管理する！（テスト用、型チェック用、...）
* inline script metadata も使えるが、``uvx`` 相当の機能はない

まとめ🌯 仮想環境からの脱却
============================================================

.. - 未来像: 開発者は手動の仮想環境管理から解放される

* サードパーティライブラリのインストール先として仮想環境の重要性は変わらない
* しかし現在では、仮想環境を **開発者が管理する必要はなくなって** いる

開発者は手動の仮想環境管理から **解放** されている
------------------------------------------------------------

* コマンド実行：ツールが一時的な仮想環境にインストールして
* スクリプト実行：inline script metadata

早速試して楽してこーぜ
------------------------------------------------------------

.. - 行動提案: 今週中に `uvx` か `pipx run` のどちらか1つを試してみる

* uv (``uvx``, ``uv run``)
* pipx (``pipx run``)

仮想環境を作るコマンドは初学者チュートリアルに今もまだ必要か
------------------------------------------------------------

* Pythonチュートリアルなど、これまでは全員が通ってきたが見直すタイミングではないか
* IMO：Pythonで **スクリプトを書きたい初学者にはスキップ** していいのでは（inline script metadata）
* プロのPython開発者には仮想環境を理解を推奨。理解していると解ける問題が増えます

ご清聴ありがとうございました
------------------------------------------------------------

Happy Python Development
