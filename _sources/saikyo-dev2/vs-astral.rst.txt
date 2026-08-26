:ogp_title: 2026年、倒したい誰かがいる
:ogp_event_name: saikyo-dev2
:ogp_slide_name: vs-astral
:ogp_description: 埼京.dev #2【2026年の野望LT】
:ogp_image_name: saikyo-dev2

==================================================
2026年、倒したい誰かがいる
==================================================

:Event: 埼京.dev #2【2026年の野望LT】
:Presented: 2026/02/19 nikkie

願いは口にしないと叶わない [#kumiko]_
==================================================

野望も口にしないと叶わない

.. [#kumiko] `黄前久美子（ピクシブ百科事典） <https://dic.pixiv.net/a/%E9%BB%84%E5%89%8D%E4%B9%85%E7%BE%8E%E5%AD%90>`__

2026年、倒したい **誰か** がいる
--------------------------------------------------

`今、話したい誰かがいる <[https://youtu.be/t62NiZIvrZQ?si=gk2UEXY3VsH_86sU&t=53](https://youtu.be/t62NiZIvrZQ?si=gk2UEXY3VsH_86sU&t=53)>`__ から（心が叫びたがってるんだ。）

**Astral**
==================================================

* https://astral.sh/about
* PythonツールチェインOSSを開発する企業
* Rust製なので爆速 + 簡単（**大感謝**）

いつも大変お世話になっております
--------------------------------------------------

* Ruff（リンタ・フォーマッタ）
* uv（Pythonプロジェクト管理）
* ty（型チェッカ）

**Ruffだけ** あればいい
--------------------------------------------------

* 以前：Flake8・Blackなど複数のリンタ・フォーマッタを組合せる環境

.. code-block:: shell

    uvx ruff format
    uvx ruff check --fix --extend-select I
    # または uv format

uv、PythonにおけるCargo
--------------------------------------------------

* 「Python環境構築、大変じゃないですか？」
* ``uv run`` するだけでPythonも自動インストール、超簡単

.. code-block:: shell

    uv sync

しかし納得できていないところも
==================================================

一例：Ruffにプラグインがない

Ruffにはプラグインが望まれているが、まだない
--------------------------------------------------

* `Meta issue: plugin system #283 <https://github.com/astral-sh/ruff/issues/283>`__ (2023/09 2年半以上オープン。*放置*？)
* 本家へルールのプルリクという道だけっぽい（送れないルールは？）
* 速くなる。しかし、既存のリンタでできていたことができない（困ってます。 **なぜ両立しない**？） [#why_ruff_no_plugin_article]_

.. [#why_ruff_no_plugin_article] `RuffはFlake8の全ての要素を含んでいる、のでしょうか？ <https://nikkie-ftnext.hatenablog.com/entry/is-ruff-superset-of-flake8-my-answer-is-no-202501>`__

私は、納得したい
--------------------------------------------------

* **高速 & 既存リンタの機能を全カバー** なら、使わない理由がない
* なぜトレードオフを迫るのか（私がAstralにいたら、もっとうまくやれるのに）
* 怠慢？それとも本当に難しい？→手を動かして確認する

2026年の野望：Rust製Pythonツール
==================================================

* *俺はRustが書けねぇんだ コノヤロー!!!* → 生成AIでカバーする
* 「高速 & 既存リンタの機能全カバー」から始めてみる
* なお、uv（やty）にも思うところはある [#to_astral_article]_

.. [#to_astral_article] 「*コミュニティの要望が高い機能が放置されている*」ように映ってます。`python-build-standaloneのAstral社移管に思うこと <https://nikkie-ftnext.hatenablog.com/entry/thoughts-astral-take-stewardship-python-build-standalone#%E3%83%A2%E3%83%A4%E3%83%83%E3%81%A8%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E5%85%A8%E9%83%A8%E8%A6%81%E6%9C%9B%E3%81%AB%E5%BF%9C%E3%81%88%E7%B6%9A%E3%81%91%E3%82%89%E3%82%8C%E3%82%8B>`__

ご清聴ありがとうございました
--------------------------------------------------

.. Astralに喧嘩を売って散るかもしれません。良ければ気にしていただけると嬉しいです

* nikkie（にっきー）・Python使い・:fab:`github` `@ftnext <https://github.com/ftnext>`__・`ブログ <https://nikkie-ftnext.hatenablog.com/>`__ 連続1100日突破
* 機械学習エンジニア。 `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）

.. image:: ../_static/uzabase-white-logo.png
