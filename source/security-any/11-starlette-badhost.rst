======================================================================
"週に3億ダウンロード"のStarletteに見つかった脆弱性、BadHost
======================================================================

"週に3億ダウンロード"のStarletteに見つかった脆弱性、BadHost
======================================================================

:Event: Security.any #11 灼熱の攻防セキュリティLT
:Presented: 2026/07/16 nikkie

BadHost、聞いたなって方？🙋
======================================================================

* 2026年 **5月下旬** の事象です
* 「*みんなに伝えたい想い*」、モヤモヤを共有

GIGAZINE「週に3億回超ダウンロード〜〜」
---------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">週に3億回超ダウンロードされているオープンソースパッケージ「Starlette」の脆弱性により数百万のAIエージェントが危険にさらされる<a href="https://t.co/UPV3mzefg5">https://t.co/UPV3mzefg5</a></p>&mdash; GIGAZINE(ギガジン) (@gigazine) <a href="https://x.com/gigazine/status/2059455882606285040?ref_src=twsrc%5Etfw">2026年5月27日</a></blockquote> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>

.. revealjs-break::
    :notitle:

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">こちらのBadHostなんですが、一次情報を確認してほしいと思ってます<a href="https://t.co/jVf0UKEEd4">https://t.co/jVf0UKEEd4</a><br>Starlette 1.0.0以下(※1.0.1で修正済)、かつrequest.url.pathを使って認証を実装という条件下で、Hostヘッダで認証をbypass<br>「1文字挿入するだけ」はそれでbypassできるリンク先のPoC実装限定と思います <a href="https://t.co/IpvXc96NcG">https://t.co/IpvXc96NcG</a></p>&mdash; nikkie(にっきー) / にっP (@ftnext) <a href="https://x.com/ftnext/status/2061066544080421087?ref_src=twsrc%5Etfw">2026年5月31日</a></blockquote>

週に3億回超ダウンロードされているオープンソースパッケージ「**Starlette**」の脆弱性により数百万のAIエージェントが危険にさらされる
============================================================================================================================================

.. _Kludex/starlette: https://github.com/Kludex/starlette

`Kludex/starlette`_
---------------------------------------------------

    ✨ The little ASGI framework that shines. ✨

* 非同期対応のPython Webフレームワークの1つ
* `2026年3月 1.0 <https://marcelotryle.com/blog/starlette-1-0/>`__ 🎉

.. _FastAPI: https://github.com/fastapi/fastapi

`FastAPI`_ が依存する
---------------------------------------------------

* FastAPIは **10万スター超え** のPython Webフレームワーク（非同期対応）
* FastAPI = Starlette + Pydantic
* 👉（Starletteは）「週に3億回超ダウンロード」

FastAPIのWebサーバ部分は **ほとんどStarlette**
---------------------------------------------------

.. code-block:: python

    # https://github.com/fastapi/fastapi/blob/0.139.0/fastapi/applications.py#L42
    from starlette.applications import Starlette
    class FastAPI(Starlette):

    # https://github.com/fastapi/fastapi/blob/0.139.0/fastapi/requests.py#L2
    from starlette.requests import Request as Request

Starletteの脆弱性がそのままFastAPI（や依存するライブラリ [#many-libs-depend-on-fastapi]_ ）に波及した

.. [#many-libs-depend-on-fastapi] LiteLLM、vLLM、FastMCPなどなど多数がFastAPI（ひいてはStarlette）に依存

週に3億回超ダウンロードされているオープンソースパッケージ「Starlette」の **脆弱性** により数百万のAIエージェントが危険にさらされる
============================================================================================================================================

BadHost
---------------------------------------------------

* `CVE-2026-48710 <https://www.cve.org/CVERecord?id=CVE-2026-48710>`__・https://badhost.org/
* Starlette 1.0.0以下の ``request.url.path`` の脆弱性（1.0.1で修正。発表時最新は1.3.1）

.. _X41 D-Sec「1文字で認証バイパス」: https://x41-dsec.de/lab/advisories/x41-2026-002-starlette/

`X41 D-Sec「1文字で認証バイパス」`_
---------------------------------------------------

.. code-block:: python
    :caption: Hostヘッダに1文字「?」を加えて認証突破

    client.get("/admin", headers={"Host": "foo"})  # 403
    client.get("/admin", headers={"Host": "foo?"})  # 200

1文字でバイパスされる実装をしてるだけでは？🪓
---------------------------------------------------

.. code-block:: python
    :emphasize-lines: 3-4

    class AuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            # 1文字でバイパスされる実装（空文字列の条件って普通書きますか？）
            if request.url.path == "" or request.url.path == "/":
                return await call_next(request)
            return PlainTextResponse("Forbidden\n", status_code=403)

**誇張なく** この脆弱性に向き合いたい
======================================================================

* 「週に3億回超ダウンロード」や「1文字で認証バイパス」にげんなり（後者はセキュリティ機関なのにバズ欲しいんですか？）
* BadHostより前に `GHSA-86qp-5c8j-p5mr <https://github.com/Kludex/starlette/security/advisories/GHSA-86qp-5c8j-p5mr>`__ で指摘・修正済み

Missing Host header validation poisons request.url.path, bypassing path-based security checks
------------------------------------------------------------------------------------------------------

.. code-block:: python

    from starlette.datastructures import URL

    u = URL(
        scope={
            "scheme": "http",
            "server": ("example.com", 80),
            "path": "/foo",  # http://example.com/foo にもかかわらず
            "query_string": b"",
            "headers": [(b"host", b"example.com/abc?bar=")]
        }
    )
    # URLは http://example.com/abc?bar=/foo になってしまう（パスが/fooでなく**/abc**）
    # 脆弱性修正後は http://example.com/foo

原因箇所と修正
---------------------------------------------------

.. code-block:: diff
    :caption: *This* `PR <https://github.com/Kludex/starlette/pull/3279>`__ *validates the Host header against an allowlist regex (matching Werkzeug's and Django's approach) before using it*

    -if host_header is not None:
    +if host_header is not None and _HOST_RE.fullmatch(host_header):
        url = f"{scheme}://{host_header}{path}"


``client.get("/admin", headers={"Host": "foo?"})`` （先のコード）
------------------------------------------------------------------------------------------------------

* ``request.url`` は ``http://foo?/admin`` になってしまう
* ``?/admin`` はクエリ文字列なので **パスは空文字列**

.. code-block:: python

    if request.url.path == "" or request.url.path == "/":  # True or -> 短絡評価
        return await call_next(request)

``request.url.path`` を使ってはいけない状況だった
---------------------------------------------------

.. code-block:: python
    :caption: 現実的な実装に修正しても突破される

    class AuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            if request.url.path == "/":
                return await call_next(request)
            return PlainTextResponse("Forbidden\n", status_code=403)

    client.get("/admin", headers={"Host": "foo/?"})
    # http://foo/?/admin -> パスは/

.. そもそも認証は自前で実装しないという話もある

GHSA-86qp-5c8j-p5mr・BadHostを追って
======================================================================

3トピック

RFCで取り決めがあっても、何でも送ってくるんだな
---------------------------------------------------

* Hostヘッダには `RFC <https://datatracker.ietf.org/doc/html/rfc9110#name-host-and-authority>`__ 上 ``/``, ``?``, ``#`` などは使えない
* けれども **攻撃者は送ってくる**！
* ユーザ入力を信用してはいけません（Webサーバ実装するときはRFC外も考慮する）

``f"{scheme}://{host_header}{path}"`` 🐛
---------------------------------------------------

* URLを文字列結合で作っている箇所原因で `GHSA-jp82-jpqv-5vv3「Unvalidated request path concatenated into authority poisons request.url.hostname」 <https://github.com/Kludex/starlette/security/advisories/GHSA-jp82-jpqv-5vv3>`__ （1.3.1で修正済み）
* 攻撃例 ``curl --request-target '@google.com'``
* `弊社ブログ <https://tech.uzabase.com/entry/2023/11/29/185315>`__ より「構造化テキストを文字列結合で作らない」

各ライブラリ、依存するStarletteのバージョンを上げるか
------------------------------------------------------------

* FastAPI「`上げない <https://github.com/fastapi/fastapi/discussions/15593#discussioncomment-17065958>`__」（ロックしていないため）
* ロックしていたライブラリたちは上げる動き（`google/adk-python <https://github.com/google/adk-python/issues/6038>`__）
* LiteLLMは ``request.url.path`` を使っていたために `GHSA-4xpc-pv4p-pm3w <https://github.com/BerriAI/litellm/security/advisories/GHSA-4xpc-pv4p-pm3w>`__ が出た（1.84.0で修正済み）

まとめ🌯："週に3億ダウンロード"のStarletteに見つかった脆弱性、BadHost
======================================================================

* 「1文字で認証バイパス」のような、セキュリティの話に **バズ目的の表現が出てきて辟易**
* ``request.url`` に脆弱性があったと、**一次情報をもとに** 怖がり対処したい
* HTTPってRFC関係なく攻撃者は何でも送ってくるんですね（何も信用できない🥶）

ご清聴ありがとうございました！
---------------------------------------------------

* nikkie（にっきー） [#nikkie-uuid]_ ・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__
* 機械学習エンジニア・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-uuid] UUID `28fb3f96-a221-462c-93bd-567b431715b9 <https://x.com/ftnext/status/2041119610368602138>`__

Appendix：拙ブログより
======================================================================

* `Starlette に Security Advisory「Missing Host header validation poisons request.url.path, bypassing path-based security checks」（1.0.1 で修正済み） <https://nikkie-ftnext.hatenablog.com/entry/starlette-GHSA-86qp-5c8j-p5mr-fixed-at-1-0-1>`__
* `Starlette の GHSA-86qp-5c8j-p5mr は CVE-2026-48710 BadHost として登録されました（1.0.1で修正済み） <https://nikkie-ftnext.hatenablog.com/entry/2026/05/30/224650>`__

.. revealjs-break::

* `Starlette 1.0.0 以下の脆弱性について、NEMESIS の「CVE-2026-48710 - Bad Hosts in the Wild」を読んだメモ <https://nikkie-ftnext.hatenablog.com/entry/reading-nemesis-cve-2026-48710-bad-hosts-in-the-wild>`__
* `StarletteにSecurity Advisory「Unvalidated request path concatenated into authority poisons request.url.hostname」（1.3.0で修正済み） <https://nikkie-ftnext.hatenablog.com/entry/starlette-GHSA-jp82-jpqv-5vv3-fixed-at-1-3-0>`__

EOF
===
