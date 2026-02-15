==================================================
Pythonのリンタを作ろう
==================================================

:Event: PyCon mini Shizuoka 2026
:Presented: 2026/02/21 nikkie

訂正：リンタの **ルール** を作ろう
==================================================

* プロポーザルのタイトルが本文を反映していませんでした。ごめんなさい
* 主張：Pythonのリンタの **ルールを書ける** ようになって、より使いこなしていきましょう

皆さまお使いのリンタは？
--------------------------------------------------

* Ruff
* flake8
* pylint

対象：仕組みは分からないが、1つでも **動かしたことがある**

.. TODO どのツールも初見の方向けに一言説明があったほうがよいだろう

お前、誰よ
==================================================

* nikkie（にっきー） ／ :fab:`github` `@ftnext <https://github.com/ftnext>`__ / Python歴8年
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png

.. _flake8-kotoha: https://pypi.org/project/flake8-kotoha/

**拡張** できるものが好き
--------------------------------------------------

* 公開している flake8 プラグイン

  * `flake8-kotoha`_
  * `happy-python-logging <https://pypi.org/project/happy-python-logging/>`__

* Ruff 使ってます（速さ & 簡単さ）

導入：あなたはリンタのルールを書きたくなる
==================================================

.. _PEP 8: https://peps.python.org/pep-0008/

スタイルガイド `PEP 8`_
--------------------------------------------------

「このように書いてはいけません（代わりにこう書きましょう）」

.. code-block:: python
    :caption: ぶっぶーですわ🙅‍♀️

    def foo():
        try:
            1 / 0
        finally:
            return 42

.. https://nikkie-ftnext.hatenablog.com/entry/whatsnew-python-314-pep-765-syntaxwarning-finally-return

PEP 8 以外の「このように書いてはいけません」
--------------------------------------------------

ログメッセージにf-stringはいけません

.. code-block:: python
    :caption: ぶっぶーですわ🙅‍♀️

    logger.info(f"{user} - Something happened")

.. code-block:: python
    :caption: ロギングでは **%-format**

    logger.info("%s - Something happened", user)

.. https://nikkie-ftnext.hatenablog.com/entry/hey-claude-dont-use-f-string-in-logging-messages

スタイルガイドはリンタにチェックさせよう
--------------------------------------------------

* 人間は全てのルールを覚えていられない
* **スタイルの指摘をリンタに任せる**
* 効能：コードレビューの焦点がスタイルから本質的なロジックへ

.. 人間が勉強のためにルールを確認するのは大事
    https://nikkie-ftnext.hatenablog.com/entry/write-python-following-pep8-opportunity-to-understand#%E6%80%9D%E3%81%88%E3%81%B0Flake8%E3%81%AB%E5%8F%B1%E3%81%A3%E3%81%A6%E3%82%82%E3%82%89%E3%81%A3%E3%81%A6%E3%81%8D%E3%81%9F

コーディングエージェントにリンタを持たせる
--------------------------------------------------

* IMO：コーディングエージェントは（性能向上は甚だしいが）Pythonを十分には理解していない（例：先のログメッセージのf-string）
* **フック機能でリンタを組み込み** スタイルガイドを強制する

.. YAPCスライド

「指摘したいルールが誰にも公開されていない」問題
------------------------------------------------

* リントルールは 800 以上あるが、自分が欲しいルールが存在しないことがある

.. code-block:: python
    :caption: 引数の型ヒントをlistにしてはいけません

    def plus_one_ng(numbers: list[int]) -> list[int]:
        return [n + 1 for n in numbers]

`flake8-kotoha`_ 自作
--------------------------------------------------

    Note that to annotate arguments, it is preferred to use an abstract collection type such as ``Sequence`` or ``Iterable`` rather than to use ``list`` or ``typing.List``. [#typing_List]_

代わりに ``collections.abc.Iterable`` や ``collections.abc.Sequence`` を使いましょう

TODO 指摘しているエラーメッセージ

.. [#typing_List] https://docs.python.org/ja/3/library/typing.html#typing.List

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
* 自分が欲しいルールが見つからないときは自分で書こう

Pythonでリンタのルールを書く
--------------------------------------------------

* 標準ライブラリ ast + Visitor パターン
* 既存のリンタのプラグインにしてルール追加
* サードパーティにはもっと楽ができるライブラリがあるそうです

Ruff + カスタムルール
--------------------------------------------------

* ast-grep（YAMLでルールを書く）
* この機会にRustを書いちゃおう！
* Astralはさすがにそろそろプラグインを追加してください

ご清聴ありがとうございました！
--------------------------------------------------

Happy Python Development♪
