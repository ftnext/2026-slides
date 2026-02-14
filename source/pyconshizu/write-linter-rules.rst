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

flake8 プラグインとしてルールを追加する
=======================================

前提知識：AST（抽象構文木）
---------------------------

* ソースコードを木構造のデータとして表現したもの
* Python標準ライブラリの ``ast`` モジュールで扱える

``ast`` モジュールの使い方
--------------------------

* ``ast.parse()`` でソースコードをASTに変換
* ``ast.dump()`` でASTの中身を確認できる
* ``python -m ast`` コマンドでも確認可能

ASTを体験する： ``print("Hello")``
------------------------------------

.. code-block:: pycon

    >>> import ast
    >>> tree = ast.parse('print("Hello")')
    >>> print(ast.dump(tree, indent=2))
    Module(
      body=[
        Expr(
          value=Call(
            func=Name(id='print', ctx=Load()),
            args=[
              Constant(value='Hello')]))])

``print("Hello")`` のASTを読む
-------------------------------

* ``print("Hello")`` は関数呼び出し（ ``ast.Call`` ）
* ソースコードの構造がデータとしてプログラムから扱える！

前提知識：Visitor パターン
--------------------------

* デザインパターンのひとつ
* データ構造の各要素は訪問者（Visitor）を **受け入れる** （accept）
* 操作の詳細はVisitor側に書く → データ構造を変えずに新しい操作を追加できる

``ast.NodeVisitor``
-------------------

* ASTの各ノードを巡回するための基底クラス
* ``visit_XXX`` メソッドでノードの種類ごとに処理を分岐

  * 例: ``visit_Name`` は ``ast.Name`` ノードが見つかるたびに呼ばれる

* ``generic_visit`` で子ノードを再帰的に辿る

Visitorを体験する
------------------

.. code-block:: python

    import ast

    class PrintFinder(ast.NodeVisitor):
        def visit_Name(self, node):
            if node.id == "print":
                print(f"Found print at line {node.lineno}, col {node.col_offset}")
            self.generic_visit(node)

    source = 'print("Hello")'
    tree = ast.parse(source)
    PrintFinder().visit(tree)

* 実行すると ``Found print at line 1, col 0`` と出力される
* ASTのノードを巡回し、特定の条件にマッチするものを見つける — これがリントルールの基本

``ast.arg.annotation`` の4パターン
------------------------------------

* ``None``: 型ヒントなし（ ``def func(a)`` ）
* ``ast.Name``: 単純な型（ ``def func(b: int)`` ）

``ast.arg.annotation`` の4パターン（続）
-----------------------------------------

* ``ast.Subscript``: ジェネリック型（ ``def func(d: list[str])`` ） ← ターゲット
* ``ast.Attribute``: 修飾名（ ``def func(tree: ast.AST)`` ）
* すべてのパターンを考慮する必要がある

型ヒントのルールチェッカー
--------------------------

.. code-block:: python

    class ArgumentConcreteTypeHintChecker(ast.NodeVisitor):
        def visit_arg(self, node):
            annotation = node.annotation
            if annotation.value.id == "list":
                print(f"Fix at {node.lineno}:{node.col_offset}")
                print(ast.dump(node))
            self.generic_visit(node)

* ``ast.Subscript`` のケース（ ``list[int]`` ）を扱う
* 4パターンすべてを考慮した完成版に発展させる

flake8 プラグインのインターフェース
------------------------------------

* AST型プラグイン：flake8がパース済みの ``ast.AST`` を渡してくれる
* ``__init__(self, tree: ast.AST)``: ASTを受け取る
* ``run()`` メソッド: 4-tuple ``(行番号, 列番号, メッセージ, 型)`` を ``yield``

プラグインクラスの実装
----------------------

.. code-block:: python

    class Flake8KotohaPlugin:
        def run(self) -> Generator[
            tuple[int, int, str, Type[Any]], None, None
        ]:
            checker = ArgumentConcreteTypeHintChecker()
            checker.visit(self._tree)

            for lineno, col_offset, message in checker.errors:
                yield (lineno, col_offset, message, type(self))

* ``print()`` → ``self.errors`` リストへの蓄積に変更
* プラグインクラスが ``self.errors`` を ``yield``

パッケージングと配布
--------------------

.. code-block:: toml

    [project]
    dependencies = ["flake8"]

    [project.entry-points."flake8.extension"]
    KTH = "kotoha.plugins:Flake8KotohaPlugin"

* ``flake8.extension`` にプラグインを登録する
* エラーコードのプレフィックス規約（例: ``KTH``）

実行
----

.. code-block:: console

    $ flake8 --select KTH examples/use_iterable.py

* 公開パッケージ: `flake8-kotoha <https://pypi.org/project/flake8-kotoha/>`_

pylint でもプラグインとして書ける
---------------------------------

* pylint にもプラグイン機構がある
* flake8 と同様に、pylint プラグインとしてルールを追加できる

Ruff ではどうするか
===================

Ruff の強みと普及
-----------------

* Rust製で高速
* flake8, isort, autoflakeなどを1つのツールに統合
* ``ruff check`` で多くの既存ルールをカバー

Ruff にはプラグイン機構がない
-----------------------------

* 2025年12月時点で、Ruffにユーザがプラグインを追加する仕組みがない
* 前章で作った flake8 プラグインは Ruff では使えない

flake8 との併用は速度を損なう
-----------------------------

* カスタムルールのために flake8 を併用する選択肢

  * Ruff の「高速さ」というメリットが薄れる
  * CIの実行時間増加

* **高速さを損なわずにカスタムルールを書く方法が求められる**

代替手段
--------

* ast-grep: tree-sitter ベースで高速、YAML でルール定義
* Rust で直接書く: RustPython/Parser を使う

Rust製ツール ast-grep
=====================

ast-grep とは
-------------

* tree-sitter ベースの構造検索・リントツール（Rust製で高速）
* YAML でルールを定義できる
* インストール: ``uvx --from ast-grep-cli ast-grep``

tree-sitter の AST は Python の AST と異なる
--------------------------------------------

* Python ``ast`` モジュール: ``ast.arg`` → ``annotation`` → ``ast.Subscript``
* tree-sitter: ``typed_parameter`` → ``type`` → ``generic_type``
* ノードの種類名・階層構造が異なる

YAML ルールの構造
-----------------

.. code-block:: yaml

    id: do-not-use-list-as-typed-parameter
    language: Python
    rule:
      pattern:
        context: 'a: list[$TYPE]'
        selector: type
      inside:
        kind: typed_parameter
    fix: Iterable[$TYPE]

YAML ルールを読み解く（1）
--------------------------

* ``pattern`` + ``context``: コード片によるパターンマッチ

  * ``$TYPE`` はメタ変数（ ``int`` などにマッチ）

* ``selector``: マッチさせたいノード種類（ ``type`` ）

YAML ルールを読み解く（2）
--------------------------

* ``inside``: 親ノードの条件（ ``typed_parameter`` ）

  * **注意**: ``inside`` は直接の親のみを見る（祖先全体ではない）

* ``fix``: 自動修正 → flake8 プラグインにはなかった強み

実行
----

.. code-block:: console

    $ ast-grep scan --rule rule.yaml examples/use_iterable.py

デバッグのコツ
--------------

* ast-grep Playground の活用

  * https://ast-grep.github.io/playground.html

* AI モデルはいずれも正しい ast-grep ルールを生成できなかった

  * ツールを人間が理解する価値がここにある

補足：tree-sitter
-----------------

* ast-grep の裏側にあるパーサーライブラリ
* 多言語対応、インクリメンタルパース
* ast-grep の YAML ルールは、裏で tree-sitter クエリとして動いている

tree-sitter クエリの例
----------------------

.. code-block:: scheme

    (typed_parameter
      (identifier) @param_name
      type: (type
        (generic_type
          (identifier) @type_name
          (type_parameter
            (type
              (identifier) @inner_type))))
      (#eq? @type_name "list"))

* ast-grep を使うだけなら直接書く必要はない
* ルールのデバッグやノード構造の理解に役立つ

発展：Rust で書く
=================

この部分だけ Rust の知識を前提にします
---------------------------------------

* 雰囲気だけ掴んでいただければ！

RustPython/Parser とは
----------------------

* RustPython や Ruff が内部で使う Python パーサー（Rust製）
* Ruff のルールも、このパーサーが生成する AST を扱っている

Rust 環境の最小限セットアップ
-----------------------------

* ``cargo`` は Python でいう ``pip`` + ``venv`` に相当
* ``cargo init`` でプロジェクト作成
* ``cargo add rustpython-parser`` で依存追加

Python コードを Rust でパースする
---------------------------------

* Python 側: ``ast.dump(ast.parse(source))``
* Rust 側: ``parse(source, Mode::Module)`` + ``println!("{:#?}", ast)``

AST 表現の比較
--------------

* Python の AST と Rust の AST は同じ概念を異なる表現で持つ

  * Python: ``FunctionDef``, ``arg``, ``Subscript``
  * Rust: ``StmtFunctionDef``, ``Parameter``, ``Expr::Subscript``

* この AST を辿って、Python版と同様の判定ロジックを Rust で書ける

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
