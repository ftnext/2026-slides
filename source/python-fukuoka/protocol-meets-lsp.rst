:ogp_title: Protocol meets ISP
:ogp_event_name: python-fukuoka
:ogp_slide_name: protocol-meets-lsp
:ogp_description: typing.Protocolをインターフェースとして捉え、ISPで小さく設計するLT

======================================================================
``typing.Protocol`` とインターフェース分離原則
======================================================================

:Event: [特集:型] Python Meetup Fukuoka #7
:Presented: 2026/06/05 nikkie

伝えたいこと
======================================================================

* ``typing.Protocol`` は **インターフェース** と捉えられる
* インターフェースは **使い方を示す** もの
* 色々知らなくても使えるよう「インターフェースは小さく」（インターフェース分離原則。SOLID原則のI）

``typing.Protocol``
======================================================================

.. code-block:: python
    :caption: `ドキュメント <https://docs.python.org/ja/3/library/typing.html#typing.Protocol>`__ の例

    from typing import Protocol


    class Proto(Protocol):
        def meth(self) -> int: ...

何のためのもの？ー静的ダックタイピング🐤
======================================================================

* ダックタイピング 「アヒルのように見えて、アヒルのように鳴けば、それはアヒルである。」

    * 型を見ない。振る舞い優先

* ``typing.Protocol`` で **型チェッカに伝わるダックタイピング**

ABC（抽象基底クラス）とは違う？
----------------------------------------------------------------------

:ABC: どのクラスを継承したか（名前）
:typing.Protocol: どのメソッドを持っているか

Structural Subtyping（**構造** で型を見る）

例：``SupportsClose`` protocol
======================================================================

.. code-block:: python
    :caption: ``close()`` できるもの [#protocol-example-ref]_

    from typing import Protocol


    class SupportsClose(Protocol):
        def close(self) -> None: ...

.. [#protocol-example-ref] 例はこちらから https://typing.python.org/en/latest/reference/protocols.html#simple-user-defined-protocols

``SupportsClose`` で型ヒント
----------------------------------------------------------------------

.. code-block:: python
    :caption: ``close_all()`` は ``close()`` できるものを受け取る

    from collections.abc import Iterable


    def close_all(items: Iterable[SupportsClose]) -> None:
        for item in items:
            item.close()

静的ダックタイピング！
----------------------------------------------------------------------

.. code-block:: python
    :caption: ``close(self) -> None`` を持つので **型チェッカは受け入れる**

    class Resource:  # SupportsCloseを継承していない
        def close(self) -> None:
            self.resource.release()


    close_all([Resource(), open("some/file")])  # 型チェッカはOK

💡 ``SupportsClose`` は **使い方** を表している
======================================================================

``close_all()`` から見える世界：

* ``close()`` が呼べる（使い方）
* それ以外は関心がない

ISP：インターフェース分離原則
======================================================================

* SOLID原則（5つの設計原則）の1つ
* 私の理解：**インターフェースは使い方を過不足無く示す**
* ``typing.Protocol`` による protocol はインターフェースと捉えられる！

大きすぎるProtocol
----------------------------------------------------------------------

.. code-block:: python
    :caption: ``close_all()`` が使わない ``other_method()``

    class BigProtocolExample(Protocol):
        def close(self) -> None: ...
        def other_method(self) -> None: ...


    def close_all(items: Iterable[BigProtocolExample]) -> None:
        for item in items:
            item.close()

提案：ISPに沿って、小さく分けましょう
----------------------------------------------------------------------

.. code-block:: python
    :caption: **最小の使い方** （protocol）で使う側へ示す

    class SupportsClose(Protocol):
        def close(self) -> None: ...


    class OtherProtocol(Protocol):
        def other_method(self) -> None: ...

まとめ🌯 ``typing.Protocol`` とインターフェース分離原則
======================================================================

* ``typing.Protocol`` はインターフェースとして気づき、ISPを適用した
* Protocol を小さくして、使い方を表してみては

ご清聴ありがとうございました！
----------------------------------------------------------------------

* nikkie（にっきー）・Python使い・:fab:`github` `@ftnext <https://github.com/ftnext>`__ `ブログ <https://nikkie-ftnext.hatenablog.com/>`__ 連続1250日突破
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png

参考
----------------------------------------------------------------------

* `typing.Protocol <https://docs.python.org/ja/3/library/typing.html#typing.Protocol>`__
* `Protocols and structural subtyping <https://typing.python.org/en/latest/reference/protocols.html>`__
* 『Fluent Python 第2版』
* 『ちょうぜつソフトウェア設計入門』
