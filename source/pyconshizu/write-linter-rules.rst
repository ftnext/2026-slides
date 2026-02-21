:ogp_title: Pythonのリンタを作ろう
:ogp_event_name: pyconshizu
:ogp_slide_name: write-linter-rules
:ogp_description: PyCon mini Shizuoka 2026
:ogp_image_name: pyconshizu

==================================================
Pythonのリンタを作ろう
==================================================

:Event: PyCon mini Shizuoka 2026
:Presented: 2026/02/21 nikkie

訂正：リンタの **ルール** を作ろう
==================================================

* プロポーザルのタイトルが本文を反映していませんでした。ごめんなさい [#build-python-linter-first-step]_
* 主張：Pythonのリンタの **ルールを書ける** ようになって、より使いこなしていきましょう（:fab:`github` `サンプルコード <https://github.com/ftnext/2026-slides/tree/main/samplecode/write-python-linter-rules>`__）

.. [#build-python-linter-first-step] せめてものお詫びとして拙ブログ `flake8 を観察して作る、小さな Python リンタ（一歩目）  <https://nikkie-ftnext.hatenablog.com/entry/my-first-python-linter-based-on-flake8-observation-first-step>`__

皆さまお使いのリンタは？
--------------------------------------------------

* Ruff
* flake8
* pylint

対象：仕組みは分からないが、1つでも **動かしたことがある**

お前、誰よ
==================================================

* nikkie（にっきー）・Python歴8年・`ブログ <https://nikkie-ftnext.hatenablog.com/>`__ 連続1100日突破
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png

.. _flake8-kotoha: https://pypi.org/project/flake8-kotoha/

**拡張** できるものが好き
--------------------------------------------------

* 公開している flake8 プラグイン :fab:`github` `@ftnext <https://github.com/ftnext>`__

  * `flake8-kotoha`_
  * `happy-python-logging <https://pypi.org/project/happy-python-logging/>`__

* Ruff 使ってます（速さ & 簡単さ）

導入：あなたはリンタのルールを書きたくなる
==================================================

.. _PEP 8: https://peps.python.org/pep-0008/

スタイルガイド `PEP 8`_
--------------------------------------------------

* 見た目について（例：演算子と半角スペース） [#formatter]_
* このようなPythonを **書いてはいけません** （代わりにこう書きましょう）

    * このトークでリンタが指しているのはこちら

.. [#formatter] フォーマッタと呼ばれるツールの出番ですね

例「このように書いてはいけません」 [#B012]_
--------------------------------------------------

.. code-block:: python
    :caption: ぶっぶーですわ🙅‍♀️

    def foo():
        try:
            1 / 0
        finally:
            return 42

.. [#B012] `jump-statement-in-finally (B012) <https://docs.astral.sh/ruff/rules/jump-statement-in-finally/>`__ （拙ブログ `「What's new in Python 3.14」より finally 節での return（や continue・break）は SyntaxWarning で警告されるようになりました（PEP 765） <https://nikkie-ftnext.hatenablog.com/entry/whatsnew-python-314-pep-765-syntaxwarning-finally-return>`__）

PEP 8 以外の例：ログメッセージにf-stringはいけません [#G004]_
----------------------------------------------------------------------

.. code-block:: python
    :caption: ぶっぶーですわ🙅‍♀️

    logger.info(f"{user} - Something happened")

.. code-block:: python
    :caption: ロギングでは **%演算子による書式化**

    logger.info("%s - Something happened", user)

.. （ロギングって中で%してるのか！）

.. [#G004] `logging-f-string (G004) <https://docs.astral.sh/ruff/rules/logging-f-string/>`__ （拙ブログ `Pythonのログメッセージにf-stringはいけません。そこのClaude、私はあなたに言っているんですよ <https://nikkie-ftnext.hatenablog.com/entry/hey-claude-dont-use-f-string-in-logging-messages>`__）

スタイルガイドはリンタにチェックさせよう
--------------------------------------------------

* 人間は全てのルールを覚えていられない
* 書いてはいけないPythonの **指摘をリンタに任せる**
* 効能：コードレビューの焦点がスタイルから本質的なロジックへ

.. 人間が勉強のためにルールを確認するのは大事
    https://nikkie-ftnext.hatenablog.com/entry/write-python-following-pep8-opportunity-to-understand#%E6%80%9D%E3%81%88%E3%81%B0Flake8%E3%81%AB%E5%8F%B1%E3%81%A3%E3%81%A6%E3%82%82%E3%82%89%E3%81%A3%E3%81%A6%E3%81%8D%E3%81%9F

コーディングエージェントにリンタを持たせる
--------------------------------------------------

* IMO：LLMは（性能向上は甚だしいが）Pythonを十分には理解していない

    * 例：先のログメッセージのf-string

* **フック機能でリンタを組み込み** スタイルガイドを強制する [#yapc-fukuoka-lt]_

.. [#yapc-fukuoka-lt] YAPCでのLT🏅 `Pythonを"理解"しているコーディングエージェントが欲しい！！ <https://ftnext.github.io/2025-slides/yapc-fukuoka/lt-agent-who-understand-python.html#/2>`__

「指摘したいルールが誰にも公開されていない」問題
------------------------------------------------

* リントルールは 800 以上あるが、自分が欲しいルールが存在しないことがある

.. code-block:: python
    :caption: この型ヒントには伸びしろがある

    def plus_one_ng(numbers: list[int]) -> list[int]:
        return [n + 1 for n in numbers]

.. _typing.List: https://docs.python.org/ja/3/library/typing.html#typing.List

引数の型ヒントをlistにしてはいけません
--------------------------------------------------

.. code-block:: python
    :caption: list以外を渡しても動きます

    plus_one_ng((1, 2, 3))  # collections.abc.Sequence
    plus_one_ng(range(3))   # collections.abc.Iterable

`typing.List`_ のドキュメントより
--------------------------------------------------

    Note that to annotate arguments, it is preferred to use an abstract collection type such as ``Sequence`` or ``Iterable`` rather than to use ``list`` or ``typing.List``.

``collections.abc.Sequence`` や ``collections.abc.Iterable`` などの **抽象** 型が好ましい

`flake8-kotoha`_ を自作しました
--------------------------------------------------

.. code-block:: console

    $ uvx --with flake8-kotoha flake8 lint-targets/use_iterable.py
    lint-targets/use_iterable.py:6:17: KTH101 Type hint with abstract type `collections.abc.Iterable` or `collections.abc.Sequence`, instead of concrete type `list`

.. code-block:: python
    :caption: こうしましょう

    def plus_one_ok(numbers: Iterable[int]) -> list[int]:
        return [n + 1 for n in numbers]

ルールを書きたくなってきましたよね？
--------------------------------------------------

「引数の型ヒントをlistにしてはいけません」を例に

:1. Pythonで書く: 例として **flake8プラグイン**
:2. Ruff では？: **意見** を伝えるので考えるきっかけに

.. include:: flake8.rst.txt

.. include:: rust-tools.rst.txt

まとめ🌯 Pythonのリンタのルールを作ろう
==================================================

* Pythonコードのスタイルの指摘はリンタに任せよう
* 自分が欲しいルールが見つからないときは **自分で書こう**

Pythonでリンタのルールを書く
--------------------------------------------------

* 標準ライブラリastで抽象構文木を見ながら **指摘したいPythonノードの処理をvisitorに追加**
* 既存のリンタのプラグインにしてルール追加
* 💡ルールが書けたら、CLIからのファイルの読み込みなどを足していけばリンタが作れるじゃん！

Ruff + カスタムルール
--------------------------------------------------

* ast-grep（**YAML** でルールを書く）
* この機会にRustを書いちゃおう🌟
* Astralはさすがにそろそろプラグインを追加してください🙏（私も挑みます）

ご清聴ありがとうございました！
--------------------------------------------------

Happy Python Development♪
