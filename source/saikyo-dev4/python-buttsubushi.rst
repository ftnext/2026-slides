============================================================
Pythonを破壊する たった1行
============================================================

:Event: 埼京.dev #4【最恐の失敗談】
:Presented: 2026/07/23 nikkie

⚠️⚠️⚠️ 危険ですので、ここで聞いた話は試そうとせず忘れてください 👻👻👻
======================================================================

5月PyCon US登壇へ
============================================================

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">飛行機乗れました<br><br>PyCon US行ってきます✈️</p>&mdash; nikkie(にっきー) / にっP (@ftnext) <a href="https://x.com/ftnext/status/2054830437537882560?ref_src=twsrc%5Etfw">2026年5月14日</a></blockquote> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>

.. revealjs-break::
    :notitle:

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">アメリカのホテルまで着きましたが、<br>eSIMつながらないし、<br>何も参照できない中で空港からの移動を強いられるし（ぼったくられるで済んだ）、<br>正直もう帰りたい... <a href="https://t.co/lM85H4FCbj">https://t.co/lM85H4FCbj</a></p>&mdash; nikkie(にっきー) / にっP (@ftnext) <a href="https://x.com/ftnext/status/2055024566251163806?ref_src=twsrc%5Etfw">2026年5月14日</a></blockquote>

二度と海外なんかいかん
--------------------------------------------------

* `トラブル続きの PyCon US 2026、2日でギブアップ <https://nikkie-ftnext.hatenablog.com/entry/pyconus-2026-trip-series-of-trouble-gave-up>`__
* こちらの最恐の失敗談の続きは懇親会にて

**技術の話** をするぞ！！
--------------------------------------------------

.. image:: ../_static/nikkie-findy-python.png
    :target: https://findy-code.io/media/articles/chotto-wakaru-python

* Googleが直近やってた失敗について（google/adk-python [#adk-python-unboundlocalerror-issue]_）

.. [#adk-python-unboundlocalerror-issue] `adk api_server --a2a fails to register A2A routes in google-adk==2.2.0 #5994 <https://github.com/google/adk-python/issues/5994>`__

Pythonで関数
============================================================

.. code-block:: python

    import json

    def f():
        data = json.loads("{}")
        return data

    if __name__ == "__main__":
        print(f())

あーっと、手が滑ったー！
--------------------------------------------------

.. code-block:: diff

    import json

    def f():
        data = json.loads("{}")
    +    import json
        return data

    if __name__ == "__main__":
        print(f())

これだけで動きません [#adk-python-fix]_
--------------------------------------------------

.. code-block:: console

    Traceback (most recent call last):
      File "/.../example.py", line 11, in <module>
        print(f())
              ~^^
      File "/.../example.py", line 5, in f
        data = json.loads("{}")
               ^^^^
    UnboundLocalError: cannot access local variable 'json' where it is not associated with a value

.. [#adk-python-fix] 混入した1行だけの修正に *2ヶ月* 要したという最恐要素もあります（2.2.0 -> `2.5.0 <https://github.com/google/adk-python/releases/tag/v2.5.0>`__）隔週リリース

.. _UnboundLocalError: https://docs.python.org/ja/3/library/exceptions.html#UnboundLocalError

`UnboundLocalError`_
============================================================

    関数やメソッド内のローカルな変数に対して参照を行ったが、その変数には値が代入されていなかった場合に送出されます。

Before（正常）
--------------------------------------------------

.. code-block:: python

    import json

    def f():
        data = json.loads("{}")  # global scopeでimportしたjson
        return data

関数内に ``import`` を入れただけで
--------------------------------------------------

.. code-block:: python
    :caption: ローカル変数 ``json`` に値が代入されていない

    import json  # global scopeのjsonはf()の中では見ない

    def f():
        data = json.loads("{}")  # 2. ここのjsonはローカル変数
        import json  # 1. jsonという名前に束縛
        return data

シンボルテーブル！
============================================================

* 最初はAST（抽象構文木）が違うのかなと考えた
* 調べたところ、ASTの先、 **コンパイル時** のシンボルテーブルの存在を知る
* 標準ライブラリ `symtable <https://docs.python.org/ja/3/library/symtable.html>`__

Before（正常）
--------------------------------------------------

.. code-block:: python

    import json

    def f():
        data = json.loads("{}")
        return data

.. code-block:: txt
    :emphasize-lines: 2

    data local=True global=False imported=False
    json local=False global=True imported=False

関数内に ``import`` を入れると
--------------------------------------------------

.. code-block:: python

    import json

    def f():
        data = json.loads("{}")
        import json
        return data

.. code-block:: txt
    :emphasize-lines: 2

    data local=True global=False imported=False
    json local=True global=False imported=True

シンボルテーブル上での ``json`` の変化
--------------------------------------------------

.. code-block:: diff

    def f():
        data = json.loads("{}")
    +    import json
        return data

.. code-block:: diff

    -json local=False global=True imported=False
    +json local=True global=False imported=True

まとめ🌯：Pythonを破壊するたった1行
============================================================

* ファイル冒頭の ``import`` を関数内後方に追加するだけ
* **値が参照される前のローカル変数の参照** となって例外送出
* 危険な力ですので、試そうとせず **忘れて** ください

ご清聴ありがとうございました
--------------------------------------------------

* nikkie（にっきー） [#nikkie-uuid]_ ・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__・Devin Ambassador
* 機械学習エンジニア・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-uuid] UUID `28fb3f96-a221-462c-93bd-567b431715b9 <https://x.com/ftnext/status/2041119610368602138>`__

References
============================================================

* 公式ドキュメントのFAQ `なぜ変数に値があるのに UnboundLocalError が出るのですか？ <https://docs.python.org/ja/3/faq/programming.html#faq-unboundlocalerror>`__
* 拙ブログ `くくく... 我はPythonの関数の本体にimportを1つ加えるだけで壊せるのだが？ <https://nikkie-ftnext.hatenablog.com/entry/python-unboundlocalerror-add-import-to-function>`__

EOF
===
