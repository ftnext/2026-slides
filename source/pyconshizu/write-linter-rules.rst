==============================
Pythonのリンタを作ろう
==============================

nikkie

リンタの **ルール** を作ろう
============================

自己紹介
========

* Pythonが好き
* 公開している flake8 プラグイン

  * `flake8-kotoha <https://pypi.org/project/flake8-kotoha/>`_
  * `happy-python-logging <https://pypi.org/project/happy-python-logging/>`_

イントロダクション
==================

「こう書くべき」ルールがたくさんある
-------------------------------------

* 「このように書いてはいけません（代わりにこう書きましょう）」

  * スタイルガイド PEP 8
  * PEP 8 以外にも「こう書くべき」ルールがたくさんある

リンタの出番
------------

* 人間が全ルール覚えるのは無理
* スタイルの指摘をリンタに任せることで本質的なコードレビューに注力できる
* コーディングエージェントにリンタを持たせて、スタイルガイドを強制する

「指摘したいルールが誰にも公開されていない」問題
------------------------------------------------

* 既存のリントルールの中に、自分が欲しいルールが存在しないことがある
* 例：「引数の型ヒントをlistにしてはいけません」

  * 代わりに ``collections.abc.Iterable`` や ``collections.abc.Sequence`` を使いましょう

スタイルを適用したいコード例
----------------------------

.. code-block:: python

    def plus_one_ng(numbers: list[int]) -> list[int]:
        return [n + 1 for n in numbers]

* *「Note that to annotate arguments, it is preferred to use an abstract collection type such as Sequence or Iterable rather than to use list or typing.List.」*

  * https://docs.python.org/ja/3/library/typing.html#typing.List

本日のロードマップ
------------------

* **自分に必要なリントルールを自分で書けるようになろう**！
* 「引数の型ヒントをlistにしてはいけません」を様々なリンタ向けに表現していく
* 1つのルールを複数の方法で実装して、各ツールの理解を深める

様々なリンタ
------------------

* Python で書かれたリンタ：flake8
* Rust 製のツール：ast-grep
* 発展：Rust で直接書く

.. include:: flake8.rst.txt

.. include:: rust-tools.rst.txt

まとめ
======

本日のふりかえり
----------------

* **自分に必要なリントルールは自分で書ける**
* 「引数の型ヒントをlistにしてはいけません」を様々な方法で実装した

実装した方法
------------

* flake8 プラグイン：Python の ``ast`` モジュール + Visitor パターン
* ast-grep：YAML でルール定義、Rust製で高速
* RustPython/Parser：Rust で直接パース

リンタを書くという選択肢を持とう
---------------------------------

* プロジェクト固有のコーディングスタイルを自動で適用できる
* コーディングエージェントにもリンタを持たせられる
* Happy Linting!
