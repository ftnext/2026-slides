============================================================
仮想環境からの脱却：2026年に向けたPythonの新しいパラダイム
============================================================

.. 1. 導入（3分）

お前、誰よ
============================================================

* ユーザベース（Tokyo）でAIエージェント開発
* 日本を中心とするPyConで登壇多数

TODO ロゴ

.. TODO ユーザベース、エキスパートネットワークサービス買収の英語リリース

昔はいつも管理していたのに、今ではほとんど管理しなくてよいもの、なに？
======================================================================

.. PyCon JPのプロポーザル確認（あと東海、静岡？）

答えは **仮想環境**
------------------------------------------------------------

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

    <blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><p lang="en" dir="ltr">We&#39;ve reached an agreement to acquire Astral.<br><br>After we close, OpenAI plans for <a href="https://twitter.com/astral_sh?ref_src=twsrc%5Etfw">@astral_sh</a> to join our Codex team, with a continued focus on building great tools and advancing the shared mission of making developers more productive.<a href="https://t.co/V0rDo0G8h9">https://t.co/V0rDo0G8h9</a></p>&mdash; OpenAI Newsroom (@OpenAINewsroom) <a href="https://twitter.com/OpenAINewsroom/status/2034616934671724639?ref_src=twsrc%5Etfw">2026年3月19日</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

仮想環境からの脱却 目次
============================================================

1. 仮想環境の基礎
2. 手動で仮想環境管理のつらさ
3. 解決策の進化（メインパート）

解決策の進化
------------------------------------------------------------

2026年現在可能な2つの解決策

.. 2. 仮想環境の基礎（3分）

仮想環境の基礎
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

:file:`.venv/` には何がある？
------------------------------------------------------------

.. tree -L 2 .venv を加工

.. code-block:: txt

    .venv
    ├── bin
    │   ├── activate
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.13
    │   ├── python -> python3.13
    │   ├── python3 -> python3.13
    │   └── python3.13 -> /.../.local/share/uv/python/cpython-3.13-macos-aarch64-none/bin/python3.13
    ├── lib
    │   └── python3.13/
    └── pyvenv.cfg

:file:`.venv/bin/python`
------------------------------------------------------------

* マシンにインストールしたPython処理系へのシンボリックリンク
* :file:`activate` では環境変数 ``PATH`` を更新して、この処理系が見つかるようにしている
* 処理系と標準ライブラリはこちらを使う

:file:`.venv/lib/python3.13/site-packages`
------------------------------------------------------------

* サードパーティライブラリのインストール先のディレクトリ
* 仮想環境ごとに分かれているので、**バージョン違いが共存** する

.. python -m site で標準ライブラリ + 仮想環境のサードバーティライブラリが確認できる

.. 3. 手動管理のつらさ（4分）

俺たちが、仮想環境管理ツールなんだ
============================================================

.. 先のコマンド

人力管理のつらみを挙げていく（全4つ）

.. - こうした問題がなぜ生産性に影響するのか

課題1: 特定のパッケージをアンインストールしづらい
------------------------------------------------------------

.. 直接の依存と推移的な依存
    直接の依存1は libA, libB に依存
    直接の依存2は libA, libC に依存
    依存2を消すとき、libCは消せるが、libAは消せない

課題2: ``pip freeze`` の出力順の扱いが難しい
------------------------------------------------------------

.. Pythonチュートリアルでもfreezeが案内される

TODO 意図までは組みきれないという話？（それとも入れたものを出力するって考え方に違和感って話？）

課題3: スクリプトごとの仮想環境
------------------------------------------------------------

* 煩雑さ（ディレクトリの様子で示す？）
* 別の環境へと持ち運びにくい

.. 気になるライブラリ、管理を頑張らずに試したい

課題4: リンタやフォーマッタが仮想環境ごとに
------------------------------------------------------------

* 開発中に使うコマンドラインツールはどの仮想環境にも都度インストールされる
* どのプロジェクトでも最新に保つのが大変

仮想環境管理ツール、俺たちが抱えるペイン
------------------------------------------------------------

.. 4つ再掲

.. 4. 解決策の進化（5分）

コミュニティがこれらの課題にどう対応してきたか
============================================================

.. TODO ここはどの課題へのアプローチが伝わるように構成できるとよさそう

pip-tools
============================================================

``pip freeze`` に代えて

.. 課題1と2へのアプローチになる

pip-tools のワークフロー
------------------------------------------------------------

* :file:`requirements.in` （直接）から :file:`requirements.txt` （直接 & 推移）を生成する
* 仮想環境は :file:`requirements.txt` に一致する
* 2つのコマンドで実現（図）

Poetry
============================================================

.. - Poetry のアプローチ: プロジェクト単位での仮想環境管理

* 直接の依存を指定
* 仮想環境を意識せずともよい

Rye、そしてuv
============================================================

.. - Rye の登場と、それが uv に与えた影響

* Rust製（Python製ツールより高速）
* Python自体の管理 + 仮想環境管理
* **pipのない** 仮想環境

.. uvはpipのRust実装として登場
    仮想環境管理もできるように

.. TODO 解決策1と2ではすべての課題を解決していないことに気づいた
    （本編で触れないがuv syncで解決できた課題をどう扱うか）

- 現世代のツール群への流れを整理する

.. 5. 現代的な解決策1: インストール不要のコマンド実行（5分） + 7の半分（1.5分）

解決策1：仮想環境管理不要のコマンド実行
============================================================

PyPIで公開されている **CLI** に適用可能（例：Ruff）

.. - コード比較: 古い方法 vs 新しい方法

Before：仮想環境にインストールしてからコマンド実行
------------------------------------------------------------

.. code-block:: shell

    $ # python -m venv .venv --upgrade-deps
    $ source .venv/bin/activate  # プロジェクトの仮想環境
    (.venv) $ python -m pip install ruff
    (.venv) $ ruff format

今は一時的な仮想環境を使ったコマンド実行が可能
------------------------------------------------------------

- :command:`uvx ruff format` （:command:`uv tool run ruff format`） [#fyi-uv-format]_
- または :command:`pipx run ruff format`

.. [#fyi-uv-format] experimentalな `uv format <https://docs.astral.sh/uv/reference/cli/#uv-format>`__ もあります （`0.8.13 <https://github.com/astral-sh/uv/releases/tag/0.8.13>`__ で追加）

インストール方法
------------------------------------------------------------

.. code-block:: shell
    :caption: uv (for macOS & Linux) [#uv-installation-doc]_

    curl -LsSf https://astral.sh/uv/install.sh | sh

.. code-block:: shell
    :caption: pipx は ``brew`` など **システムのパッケージマネージャ優先** で [#pipx-installation-doc]_

    python3 -m pip install --user pipx

.. [#uv-installation-doc] https://docs.astral.sh/uv/getting-started/installation/
.. [#pipx-installation-doc] For detail, see https://pipx.pypa.io/stable/how-to/install-pipx/#installing-pipx

ツールが一時的な仮想環境にインストールしている
------------------------------------------------------------

.. - 仕組み: 内部では一時的な仮想環境が使われている

* ツールがコマンドの指定を受け
* パッケージをインストールした一時的な仮想環境を用意して [#uv-doc-cache-tool-environments]_
* コマンド実行 [#pipx-doc-explanation-run]_

.. [#uv-doc-cache-tool-environments] 毎回仮想環境を作るわけでなく、 *キャッシュ* もされる https://docs.astral.sh/uv/concepts/tools/#tool-environments

.. [#pipx-doc-explanation-run] https://pipx.pypa.io/stable/explanation/how-pipx-works/#pipx-run

デモ 手動 venv vs ``uvx``
------------------------------------------------------------

.. 7 フォーマッターの実行: 手動 venv vs `uvx`

.. code-block:: shell
    :caption: Before

    $ python -m venv format-env --upgrade-deps
    $ source format-env/bin/activate
    (format-env) $ python -m pip install ruff
    (format-env) $ ruff format

.. code-block:: shell
    :caption: After

    $ uvx ruff format

``uvx`` や ``pipx run`` のススメ
------------------------------------------------------------

* 私たちが仮想環境を触ることがない（ツールが代わってくれる）
* **管理の手間なく最新バージョン** が使える
* 複数プロジェクトで横断的に使える（課題4）

私はこんなところで使ってます [#awesome-pipx-uvx]_
------------------------------------------------------------

.. - 実際のユースケース
    リンター、フォーマッター（Ruffは紹介済み）

.. code-block:: shell

    $ uvx cookiecutter gh:simonw/llm-plugin

.. code-block:: shell

    $ uvx --from sphinx --with sphinx-new-tab-link \
        sphinx-build -M html source build

.. code-block:: shell
    :caption: GitHub ActionsのUbuntuイメージにはpipxがインストール済み [#github-actions-pipx-python-build]_

    $ pipx run build
    $ pipx run twine check dist/*

.. [#awesome-pipx-uvx] https://github.com/ftnext/awesome-pipx-uvx (WIP)

.. [#github-actions-pipx-python-build] https://github.com/ftnext/sphinx-new-tab-link/blob/v0.8.1/.github/workflows/publish.yml

一時的の代わりにマシンに入れることもできます
------------------------------------------------------------

* :command:`uv tool install`
* :command:`pipx install` (`Installing stand alone command line tools <https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/>`__)

ただし手動でアップグレードが必要（`uv tool upgrade <https://docs.astral.sh/uv/concepts/tools/#upgrading-tools>`__・`pipx upgrade-all <https://pipx.pypa.io/stable/reference/cli/#pipx-upgrade-all>`__）

.. 6. 現代的な解決策2: inline script metadata（5分） + 7の半分（1.5分）

解決策2: inline script metadata
============================================================

Python **スクリプト** に適用可能

https://packaging.python.org/en/latest/specifications/inline-script-metadata/

サードパーティライブラリを使ったスクリプト
------------------------------------------------------------

.. literalinclude:: ../../samplecode/inline-script-metadata/example_like_pep723.py
    :language: python
    :lines: 8-20
    :caption: 最新のPEP 10件のタイトルを取得

Before：仮想環境に依存をインストールしてからスクリプト実行
------------------------------------------------------------

.. code-block:: shell

    $ python -m venv .venv --upgrade-deps
    $ source .venv/bin/activate
    (.venv) $ python -m pip install httpx rich
    (.venv) $ python script.py

.. - 問題: スクリプトにも依存関係が必要なため、使い捨ての venv が増えがち
    先の課題3
    配布が大変

.. _PEP 723: https://peps.python.org/pep-0723/

`PEP 723`_ – Inline script metadata
------------------------------------------------------------

.. literalinclude:: ../../samplecode/inline-script-metadata/example_like_pep723.py
    :language: python
    :lines: 1-7
    :caption: コメントとしてTOML形式のメタデータを書く

inline script metadataをサポートするツールで実行するだけ
------------------------------------------------------------

* uv run script.py
* pipx run script.py
* hatch run script.py [#hatch-installation-doc]_
* pdm run script.py [#pdm-installation-doc]_

.. [#hatch-installation-doc] https://hatch.pypa.io/dev/install/

.. [#pdm-installation-doc] https://pdm-project.org/en/latest/#installation

ツールが依存をインストールした仮想環境を用意して実行
------------------------------------------------------------

* ツールがmetadataを読み
* *requires-python* に沿ったPython処理系で
* *dependencies* をインストールした一時的な仮想環境を用意して、スクリプト実行

uvはinline script metadataを書き込む！ [#alternative-uv-init-script]_
------------------------------------------------------------------------------------------

`uv add --script <https://docs.astral.sh/uv/reference/cli/#uv-add--script>`__ script.py httpx rich [#uv-add-script-write-lower-bound]_

.. code-block:: python

    # /// script
    # requires-python = ">=3.13"
    # dependencies = [
    #     "httpx>=0.28.1",
    #     "rich>=14.3.3",
    # ]
    # ///

.. [#alternative-uv-init-script] `uv init --script <https://docs.astral.sh/uv/reference/cli/#uv-init--script>`__ でinline script metadata付きの空スクリプトができる

.. [#uv-add-script-write-lower-bound] `uv 0.9.16 <https://github.com/astral-sh/uv/releases/tag/0.9.16>`__ からlower boundが書かれるように。ref: https://github.com/astral-sh/uv/issues/15544

デモ 手動 venv vs ``uv run script.py``
------------------------------------------------------------

.. 準備 inline script metadataのないscript.pyを用意しておく

.. code-block:: shell
    :caption: Before

    $ python -m venv script-env --upgrade-deps
    $ source script-env/bin/activate
    (script-env) $ python -m pip install httpx rich
    (script-env) $ python script.py

.. code-block:: shell
    :caption: After [#pip-26-requirements-from-script]_

    $ uv add --script script.py httpx rich
    $ uv run script.py

.. [#pip-26-requirements-from-script] `pip install --requirements-from-script script.py <https://ichard26.github.io/blog/2026/01/whats-new-in-pip-26.0/#installing-from-inline-script-metadata-pep-723>`__

inline script metadataのススメ
------------------------------------------------------------

* 私たちが仮想環境を触ることがない（ツールが代わってくれる）
* スクリプトがポータブルに。別のマシンでも **簡単に再現実行** できる [#execute-from-url-inline-script-metadata]_

.. [#execute-from-url-inline-script-metadata] uv run https://gist.githubusercontent.com/ftnext/d9a2094ca2a54e84d3677217e607c783/raw/5438023012cef1957801b95b6b9685d0a0e01e6f/unlock_pdf.py （信頼できないスクリプトにはオススメしません）

私はこんなところで使ってます
------------------------------------------------------------

* SlackやDiscordでスクリプトを共有する際
* PyPIで配布しているライブラリであればexamplesに提案 [#nikkie-inline-script-metadata-example]_
* コーディングエージェントのフック（シバンで ``uv run``） [#coding-agent-hooks-shebang-uv-run-example]_

.. [#nikkie-inline-script-metadata-example] 例 https://github.com/argilla-io/synthetic-data-generator/pull/23

.. [#coding-agent-hooks-shebang-uv-run-example] with `cchooks <https://github.com/GowayLee/cchooks>`__ https://gist.github.com/ftnext/ccc020832e1d753554428ff520c3ea49

.. 8. ツール選定とまとめ（2分）

Pythonプロジェクト管理
============================================================

* コマンド実行やスクリプト実行以外はPoetryがだいぶ楽にしてくれた

.. Poetry の成熟度：最新の仕様に追従できていない

uv
------------------------------------------------------------

.. `uv` はオールインワンの有力解だが、唯一の選択肢ではない

Hatch
------------------------------------------------------------

* **複数の仮想環境** をHatchが管理する！
* テスト用、型チェック用、...

まとめ🌯 仮想環境からの脱却
============================================================

.. - 未来像: 開発者は手動の仮想環境管理から解放される

* サードパーティライブラリのインストール先として仮想環境の重要性は変わらない
* しかし現在では、仮想環境を開発者が管理する必要はなくなっている

開発者は手動の仮想環境管理から解放されている
------------------------------------------------------------

* コマンド実行：ツールが一時的な仮想環境にインストールして
* スクリプト実行：inline script metadata

早速試して楽してこーぜ
------------------------------------------------------------

.. - 行動提案: 今週中に `uvx` か `pipx run` のどちらか1つを試してみる

* uv (``uvx``, ``uv run``)
* pipx (``pipx run``)

ご清聴ありがとうございました
------------------------------------------------------------

Happy Python Development

.. TODO プロの開発者は仮想環境の理解は必要（あったほうが重宝される）
    一方、スクリプトを書きたいだけなら仮想環境を理解しなくても簡単に結果を利用できる時代が訪れている（チュートリアルの見直し必要では）
