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

* 東京で機械学習エンジニア。`Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`A2A提供 <https://jp.ub-speeda.com/news/20260319/>`__） [#uzabase-south-asia-news]_
* :fab:`github` `@ftnext <https://github.com/ftnext>`__ `SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ (9k⭐️)メンテナ

.. 業務やOSSのPython開発で得た知見をPyConで共有しています

.. image:: ../_static/uzabase-white-logo.png

.. [#uzabase-south-asia-news] `Acquisition of Sealed Network <https://uzabaseglobal.com/press-release/uzabase-expands-southeast-asia-expert-network-with-acquisition-of-sealed-network>`__

昔はいつも管理していたのに、今ではほとんど管理しなくてよいもの、なに？
======================================================================

.. PyCon JPのプロポーザル確認（あと東海、静岡？）

答えは **仮想環境**
------------------------------------------------------------

みなさん、自分の手で仮想環境を管理していますか？🙋

.. 私はほとんどしていません。挙手した方は持ち帰るものが多いと思います

仮想環境を開発者が管理する必要はなくなっている
------------------------------------------------------------

.. - このパラダイムシフトの予告

* 種々のPythonプロジェクト管理ツール
* *一時的な仮想環境* を使ったCommand Line Interface (CLI)実行
* *inline script metadata* (PEP 723)

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

1. *一時的な仮想環境* を使ったCLI実行
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

`12.2. Creating Virtual Environments (The Python Tutorial) <https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments>`__

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
    :caption: python.org からmacOSにインストール
    :emphasize-lines: 2,7,11-12

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
    │   └── python3.14/
    └── pyvenv.cfg

.. [#python314-easter-egg] easter egg: 𝜋thon https://github.com/python/cpython/pull/125035

:file:`.venv/bin/python`
------------------------------------------------------------

* マシンにインストールしたPython処理系への **シンボリックリンク**
* :file:`activate` では環境変数 ``PATH`` を更新して、この処理系が見つかるようにしている
* 処理系と標準ライブラリはこちらを使う

:file:`.venv/lib/python3.14/site-packages/`
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

    $ python -m venv recreate-env --upgrade-deps
    $ source recreate-env/bin/activate
    (recreate-env) $ python -m pip install -r requirements.txt

`12.3. Managing Packages with pip (The Python Tutorial) <https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip>`__

依存ライブラリには2種類ある
------------------------------------------------------------

.. code-block:: shell
    :caption: 直接(direct)依存

    (.venv) $ % python -m pip install httpx

.. code-block:: shell
    :caption: 推移的(transitive)依存
    :emphasize-lines: 2-5,7

    (.venv) $ python -m pip freeze
    anyio==4.12.1
    certifi==2026.2.25
    h11==0.16.0
    httpcore==1.0.9
    httpx==0.28.1
    idna==3.11

課題1: ``pip freeze`` の出力は扱いが難しい
------------------------------------------------------------

* directな依存もtransitiveな依存も1つの :file:`requirements.txt` にまとまる
* directな依存にextraを指定 [#specify-extra-install]_ していた場合、:file:`requirements.txt` では **extraの情報は失われる**

.. [#specify-extra-install] 例 ``python -m pip install SpeechRecognition[audio]``

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

課題3: スクリプトごとの仮想環境が増殖
------------------------------------------------------------

* 気になるライブラリをquickstartしたいだけだが、毎回仮想環境を作ることになる

.. code-block:: txt
    :caption: このようなディレクトリがいくつも

    .
    ├── .venv/
    └── script.py

課題4: リンタやフォーマッタが仮想環境ごとに
------------------------------------------------------------

* 開発中に使うCLIを **どの仮想環境にも都度** インストールする
* どのプロジェクトでも最新に保つのが大変

仮想環境管理ツール、俺たちが抱えるペイン
------------------------------------------------------------

1. directもtransitiveも1つにまとまる ``pip freeze``
2. directを消すとき一緒にどのtransitiveも消せる？
3. スクリプト用の仮想環境いくつも
4. CLIを仮想環境に都度インストールして最新化

.. 4. 解決策の進化（5分）

3️⃣コミュニティがこれらの課題にどう対応してきたか
============================================================

.. TODO ここはどの課題へのアプローチが伝わるように構成できるとよさそう

1. directもtransitiveも1つにまとまる ``pip freeze``
2. directを消すとき一緒にどのtransitiveも消せる？
3. スクリプト用の仮想環境いくつも
4. CLIを仮想環境に都度インストールして最新化

.. _pip-tools: https://github.com/jazzband/pip-tools

`pip-tools`_
------------------------------------------------------------

* ``pip freeze`` に代えて :command:`pip-compile` & :command:`pip-sync` [#pip-tools-overview-reference]_

.. image:: ../_static/pythonasia/pip-tools-overview.svg
    
.. [#pip-tools-overview-reference] https://github.com/jazzband/pip-tools/blob/v7.5.3/img/pip-tools-overview.svg

pip-tools のワークフロー
------------------------------------------------------------

.. code-block:: txt
    :caption: directな依存を :file:`requirements.in` に書く

    httpx

課題1: directもtransitiveもまとまるが解消します

.. revealjs-break::

.. code-block:: txt
    :caption: :command:`pip-compile` で :file:`requirements.txt` (direct & transitive)を生成

    anyio==4.12.1
        # via httpx
    certifi==2026.2.25
        # via
        #   httpcore
        #   httpx
    h11==0.16.0
        # via httpcore
    httpcore==1.0.9
        # via httpx
    httpx==0.28.1
        # via -r requirements.in
    idna==3.11
        # via
        #   anyio
        #   httpx

.. revealjs-break::

* :command:`pip-sync` で :file:`requirements.txt` に仮想環境を一致させる
* :file:`requirements.in` の **directな依存の指定を変えて**、:file:`requirements.txt` も仮想環境も変える（課題2も解消）

.. _Poetry: https://github.com/python-poetry/poetry

`Poetry`_
------------------------------------------------------------

.. - Poetry のアプローチ: プロジェクト単位での仮想環境管理

.. code-block:: shell
    :caption: 直接の依存を指定する（＝課題1・2へのアプローチ）

    $ poetry new
    $ poetry add httpx
    $ ls
    poetry.lock     pyproject.toml

仮想環境をより意識しない [#poetry-uses-project-venv]_
------------------------------------------------------------

.. code-block:: shell
    :caption: コマンドの先頭に ``poetry run`` とつけるだけで仮想環境で実行

    $ poetry run python -m pip freeze

* Pythonプロジェクト開発で受け入れられてきた印象（2020年前後） [#poetry-alternative-pipenv]_

.. [#poetry-uses-project-venv] `use the {project-dir}/.venv directory if one already exists. <https://python-poetry.org/docs/configuration/#virtualenvsin-project>`__

.. [#poetry-alternative-pipenv] `Pipenv <https://github.com/pypa/pipenv>`__ もPythonプロジェクト開発で受け入れられていました

.. _Rye: https://github.com/astral-sh/rye

`Rye`_ [#rye-sunset]_
------------------------------------------------------------

.. - Rye の登場と、それが uv に与えた影響

* Rust製（Python製ツールより高速）
* **Python自体の管理** + 仮想環境管理

.. [#rye-sunset] mitsuhiko-sanが作り、Astralに移管された後、2026年2月にアーカイブされていました。お疲れさまでした

.. code-block:: shell
    :caption: https://rye.astral.sh/guide/basics/ [#rye-interesting-point]_

    $ rye init
    $ rye add httpx
    $ rye sync

.. [#rye-interesting-point] pipのない仮想環境をpip-toolsで管理しているのが、技術的に興味深かったです

そしてuv
------------------------------------------------------------

* pipのRust実装として登場。`drop-in replacement for pip and pip-tools workflows. <https://astral.sh/blog/uv>`__
* Pythonもプロジェクトの仮想環境も管理できるように [#uv-unified-python-packaging]_

.. [#uv-unified-python-packaging] https://astral.sh/blog/uv-unified-python-packaging

.. code-block:: shell
    :caption: https://docs.astral.sh/uv/guides/projects/

    $ uv init
    $ uv add httpx
    $ uv sync

.. * **高速** [#how-uv-got-so-fast]_
    [#how-uv-got-so-fast] https://nesbitt.io/2025/12/26/how-uv-got-so-fast.html

uvへと至る流れ
------------------------------------------------------------

* Poetry（やPipenv）が **Pythonプロジェクトの仮想環境管理** を簡単に
* Rust製のRye：**Pythonの管理** も（仮想環境管理はpip-tools）
* Ryeの機能に *pipx* や *PEP 723* を取り込んだuvへ（このあと紹介）

.. include:: ja/standalone-cli.rst.txt

.. include:: ja/inline-script-metadata.rst.txt

.. 8. ツール選定とまとめ（2分）

最後に、ツール選定
============================================================

Poetry以来のPythonプロジェクト管理も踏まえて

* uv🏅
* Hatch❤️

Poetry
------------------------------------------------------------

.. Poetry の成熟度：最新の仕様に追従できていない

* Poetryがだいぶ楽にしてくれた（CLI実行やスクリプト実行の課題が残った）
* 最新の仕様に即時追従できていない状況（オススメしづらい）

    * `PEP 621 <https://peps.python.org/pep-0621/>`__ (``[project]``)サポートが4年後の `2.0.0 <https://github.com/python-poetry/poetry/releases/tag/2.0.0>`__

uv🏅
------------------------------------------------------------

.. `uv` はオールインワンの有力解だが、唯一の選択肢ではない

.. code-block:: shell
    :caption: Pythonプロジェクト管理もサポート（:file:`pyproject.toml` を強制）

    $ uv add httpx
    $ uv sync

* 1つのツールで ``uvx`` や inline script metadata まで **広くサポート** するので現時点で最有力

.. 現在はuvは最新のPEPをいち早く実装する存在だが、OpenAIの買収によりその傾向が変わってしまうかも

Hatch
------------------------------------------------------------

* Pythonプロジェクト管理もサポートするが、**複数の仮想環境** を管理する形式
* inline script metadata も使えるが、``uvx`` 相当の機能はない

Hatchは興味深い❤️
------------------------------------------------------------

.. code-block:: console

    $ hatch env show
    Standalone
    ┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Name    ┃ Type    ┃ Dependencies ┃ Scripts ┃
    ┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━┩
    │ default │ virtual │              │         │
    ├─────────┼─────────┼──────────────┼─────────┤
    │ types   │ virtual │ mypy>=1.0.0  │ check   │
    └─────────┴─────────┴──────────────┴─────────┘

uvはじめ多くはPythonプロジェクトに1つだけの仮想環境

まとめ🌯 仮想環境 **人力管理** からの脱却
============================================================

.. - 未来像: 開発者は手動の仮想環境管理から解放される

* サードパーティライブラリのインストール先として仮想環境の重要性は変わらない
* しかし現在では、仮想環境を **開発者が管理する必要はなくなって** いる

開発者は手動の仮想環境管理から **解放** されている
------------------------------------------------------------

* CLI実行：ツールが一時的な仮想環境にインストールして
* スクリプト実行：inline script metadata

早速試して **楽して** こーぜ
------------------------------------------------------------

.. - 行動提案: 今週中に `uvx` か `pipx run` のどちらか1つを試してみる

* uv (``uvx``, ``uv run``)
* pipx (``pipx run``)

仮想環境を作るコマンドって初学者チュートリアルに必要？
------------------------------------------------------------

* Pythonチュートリアルや入門書は見直すタイミングではないか
* IMO：Pythonで **スクリプトを書きたい初学者にはスキップ** していいのでは（inline script metadata）
* プロのPython開発者には仮想環境を理解するのを推奨

ご清聴ありがとうございました
------------------------------------------------------------

Happy Python Development
