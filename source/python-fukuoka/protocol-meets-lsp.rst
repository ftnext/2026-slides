:ogp_title: Protocol meets ISP
:ogp_event_name: python-fukuoka
:ogp_slide_name: protocol-meets-lsp
:ogp_description: typing.Protocolをインターフェースとして捉え、ISPで小さく設計するLT

======================================================================
Protocol meets ISP
======================================================================

``typing.Protocol`` を
インターフェースとして捉えてみる

:Event: Python Fukuoka
:Presented: 2026/06/05 nikkie

今日の前提
======================================================================

* Pythonの型ヒントは少し知っている
* ``Protocol`` は名前を聞いたことがある
* 5分なので、型システムの細部には踏み込みません

話したいこと
======================================================================

``Protocol`` は
**使い方を示すインターフェース**
として見られるのでは？

そしてインターフェースなら
**小さく** したい

``typing.Protocol``
======================================================================

.. code-block:: python

    from typing import Protocol


    class Proto(Protocol):
        def meth(self) -> int: ...

クラスを継承して定義します

でも、使う側のクラスは
``Proto`` を継承しなくてよい

静的ダックタイピング
======================================================================

``Protocol`` は、
型チェッカに伝わるダックタイピング

* どのクラスを継承したか、ではなく
* どのメソッドを持っているか、を見る

構造で型を見ている

例：``SupportsClose``
======================================================================

.. code-block:: python

    from typing import Protocol


    class SupportsClose(Protocol):
        def close(self) -> None: ...

``close()`` できるもの、
というインターフェース

``close_all()``
======================================================================

.. code-block:: python

    from collections.abc import Iterable


    def close_all(items: Iterable[SupportsClose]) -> None:
        for item in items:
            item.close()

``close_all()`` が知りたいのは
**closeできるか** だけ

継承していなくてもOK
======================================================================

.. code-block:: python

    class Resource:
        def close(self) -> None:
            self.resource.release()


    close_all([Resource(), open("some/file")])

``close() -> None`` を持つので
型チェッカは受け入れる

ここで気づいた
======================================================================

``SupportsClose`` は
「実装」ではなく **使い方** を表している

``close_all()`` から見える世界：

* ``close()`` が呼べる
* それ以外は関心がない

Protocol meets ISP
======================================================================

ISP：インターフェース分離原則

インターフェースは
利用時の概念の最小単位にする

``Protocol`` がインターフェースなら、
``Protocol`` も小さくしたい

大きすぎるProtocol
======================================================================

.. code-block:: python

    class BigProtocolExample(Protocol):
        def close(self) -> None: ...
        def other_method(self) -> None: ...


    def close_all(items: Iterable[BigProtocolExample]) -> None:
        for item in items:
            item.close()

``other_method()`` は使っていない

小さく分ける
======================================================================

.. code-block:: python

    class SupportsClose(Protocol):
        def close(self) -> None: ...


    class SupportsOtherMethod(Protocol):
        def other_method(self) -> None: ...

使う側が必要とする
最小のProtocolを受け取る

今日の主張
======================================================================

``Protocol`` は
**使い方を示す小さなインターフェース**
として書ける

* 継承関係ではなく、できることを見る
* 関数が使うメソッドだけをProtocolにする
* 大きくなったら、使い方ごとに分ける

まとめ
======================================================================

``typing.Protocol`` を
インターフェースとして捉えると、
ISPが自然に使える

``close_all()`` には
``SupportsClose`` だけで十分

小さなProtocolで、
使う側の関心を表そう

参考
======================================================================

* `typing.Protocol <https://docs.python.org/ja/3/library/typing.html#typing.Protocol>`__
* `Protocols and structural subtyping <https://typing.python.org/en/latest/reference/protocols.html>`__
* 『Fluent Python 第2版』
* 『ちょうぜつソフトウェア設計入門』
