==================================================
わたしの、最高の相棒、Codex
==================================================

わたしの、最高の **相棒**、Codex
==================================================

自動レビュー、モバイル、App Server

:Event: 開発フローの中で活かすCodex ``#codex_findy``
:Presented: 2026/06/04 nikkie（スペース連打 or 矢印キーでめくります）

お前、誰よ（Python使いの自己紹介）
==================================================

* nikkie（にっきー）・Python歴8年・ **Codex Ambassador** (Tokyo)
* 機械学習エンジニア（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A提供 <https://jp.ub-speeda.com/news/20260319/>`__）

.. image:: ../_static/uzabase-white-logo.png

.. （仕事はペアプロ環境）個人開発の事例中心

3月 [#codex-findy-march]_ にもお話ししました
------------------------------------------------------------

.. raw:: html

    <iframe width="800" height="480" src="https://ftnext.github.io/2026-slides/codex-findy/my-best-partner-codex-cli.html#/1"
        title="わたしの、最高の相棒、Codex CLI"></iframe>

.. [#codex-findy-march] アーカイブ https://findy-code.io/events/VL_rdU3iJcEoP

3月からの差分：**Codex App** [#why-app]_
==================================================

.. image:: ../_static/codex-findy/app-screenshot-light.webp
    :alt: https://developers.openai.com/images/codex/app/app-screenshot-light.webp
    :target: https://developers.openai.com/codex/app

.. [#why-app] 理解していなくても `git worktreeが簡単に使えた <https://developers.openai.com/codex/app/worktrees>`__ ので、CLIから乗り換えが進みました

Codexの提供形態 [#codex-quickstart-doc]_ (私の利用量)
------------------------------------------------------------

* **App** (多) 👈おすすめ
* CLI (少)
* Cloud (多)
* VS Codeなどの拡張 (少)

.. [#codex-quickstart-doc] https://developers.openai.com/codex/quickstart#setup

Appって何ができるの？ ー おすすめ動画
------------------------------------------------------------

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/LoX9_dnXthc?si=pzwvD_FUClL1bzcg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

イチオシ機能：**ペット** と一緒 🏃‍♂️
------------------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="en" dir="ltr">Pets. Now in Codex.<br><br>Use /pet to wake your pet. <a href="https://t.co/aAm4lLP4LW">pic.twitter.com/aAm4lLP4LW</a></p>&mdash; OpenAI Developers (@OpenAIDevs) <a href="https://x.com/OpenAIDevs/status/2050275713824211041?ref_src=twsrc%5Etfw">2026年5月1日</a></blockquote> <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script>

本題へ：開発フローの中で活かすCodex (IMO [#ambassador-disclaimer]_)
======================================================================

* レビュー
* 実装
* コードリーディング
* 開発ワークフロー

.. [#ambassador-disclaimer] Codex Ambassadorといっても私はめちゃめちゃ知っているわけではありません。紹介されなかったけどこれが便利というものがある方はぜひ発信を🙏（拡散します）

レビュー
==================================================

ひとつのことを極め抜け

1. Codex Cloud
2. ローカルでの開発

.. （なぜレビューさせるのか。人間が見るところを減らしたい。）

OpenAIはCodexでレビュー [#example-codex-github]_
------------------------------------------------------------

    Every pull request at OpenAI is now reviewed by Codex before human eyes see it,

https://x.com/lennysan/status/2022121036364529702

.. [#example-codex-github] 例：https://github.com/openai/codex/pulls chatgpt-codex-connector[bot]

.. _Codex code review in GitHub: https://developers.openai.com/codex/integrations/github

`Codex code review in GitHub`_
==================================================

* Codex Cloud は **簡単** にGitHubと連携設定できます
* PRにpushされるたびにCodexがレビュー
* レビューは本当に頼りにしています（例：GitHub Actionsのセキュリティ面）

設定例（画像は設定画面へのリンクです）
------------------------------------------------------------

.. image:: ../_static/aidd-auto-pilot2/codex-web-review-easy-setting.png
    :target: https://chatgpt.com/codex/cloud/settings/code-review
    :scale: 60%

Codex Cloudのレビューのここが推し！
------------------------------------------------------------

* 差分を読むだけにあらず
* **Cloudの環境を使ってコマンド実行**。仮説を持ったレビュー

ローカルのCodex {CLI,App}
==================================================

* ``/review``
* ``codex review``

.. TODO 仕組みの情報を追加したい

Codex以外でも（Cursor、VS Code）
------------------------------------------------------------

* CursorのComposer 2.5で実装
* レビュー目的で私は **新規セッションでGPTを呼び出す**
* plan(Opus 4.8)、実装(Composer 2.5)、レビュー(GPT-5.5)と切り替えるのを試してます

.. _Codex plugin for Claude Code: https://github.com/openai/codex-plugin-cc

ローカル開発で `Codex plugin for Claude Code`_
------------------------------------------------------------

* OpenAIによるClaude Codeプラグイン
* Claude CodeからCodexを呼び出せる（スキルやフックを提供）
* 例：Claude CodeがStopするとCodexがレビュー（レビューゲート）

.. （/goalでもいける説 PRの面倒のアイデア？）

PRの面倒 ✖️ 自動コードレビュー
------------------------------------------------------------

Codex Cloudの自動コードレビューと組合せる

* ``/autofix-pr`` (Claude Code on the web)
* Devin

Codexのレビューを極め抜け
==================================================

* Codex CloudでGitHubのプルリクレビュー設定はおすすめ
* ローカルでの開発でも、Codex(GPT)のレビューを求めに行く

🔖開発フローの中で活かすCodex
------------------------------------------------------------

* レビュー
* **実装**
* コードリーディング
* 開発ワークフロー

自動レビュー
==================================================

* Codexが **実装** するのを大きくサポート
* コマンド実行の *許可を求めてこなくなる*
* プルリクエストや差分の **コードレビューではない** です

Codex App「自動レビュー」（代理で承認）
------------------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="en" dir="ltr">Auto-review is a new mode that lets Codex work longer with fewer approvals and safer execution.<br><br>It helps Codex keep moving through tests, builds, and more, including during long tasks and automations, while a separate agent checks higher-risk steps in context before they run. <a href="https://t.co/TCcNC5yB0H">pic.twitter.com/TCcNC5yB0H</a></p>&mdash; OpenAI Developers (@OpenAIDevs) <a href="https://x.com/OpenAIDevs/status/2047436655863464011?ref_src=twsrc%5Etfw">2026年4月23日</a></blockquote>

.. https://developers.openai.com/codex/concepts/sandboxing/auto-review

Codex CLIは ``/permissions``
------------------------------------------------------------

TODO

自走例
------------------------------------------------------------

* Opus 4.7(high)と `superpowers <https://claude.com/plugins/superpowers>`__ で長大な計画（4000行）を作った
* GPT-5.5(高)とsuperpowersで実装（Codex Appの自動レビュー）
* 実装が終わるまでの **2時間**、人間にコマンド実行許可を求めて止まることがなかった

自動レビューは何をするのか
------------------------------------------------------------

* LLMがコマンドの **実行許可を人間の代わりに** 見てくれる
* サブエージェントによる実装（``guardian_subagent``）

.. メインブランチpushは弾かれる

.. TODO 仕組みをのぞいたネタが追加できそう

参考：同様の機能の流れ
------------------------------------------------------------

* Claude Code `auto mode <https://code.claude.com/docs/ja/auto-mode-config>`__
* Cursor (3.6) `Auto-review Run Mode <https://cursor.com/ja/docs/agent/tools/terminal#auto-review>`__

2026年最高の発明、自動レビュー
==================================================

* Codex {App,CLI}（や他のコーディングエージェント）でぜひ設定しましょう
* 仕組み：LLMにプロンプトで代理に承認させています

コーディングエージェント自走が圧倒的に簡単に
------------------------------------------------------------

.. raw:: html

    <iframe class="speakerdeck-iframe" style="border: 0px; background: rgba(0, 0, 0, 0.1) padding-box; margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" frameborder="0" src="https://speakerdeck.com/player/6f8da4e8af70435693f4fdd940e956e4?slide=3" title="夜を制する者が “AI Agent 大民主化時代” を制する" allowfullscreen="true" allow="web-share" data-ratio="1.7777777777777777"></iframe>

CM：導入するなら
==================================================

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="en" dir="ltr">Want to (officially) use Codex at work?<br><br>Send this post to your CTO to bring your team to Codex. Eligible enterprise customers who switch in the next 30 days get 2 free months of Codex usage for new users. <a href="https://t.co/38e8y7MAmg">pic.twitter.com/38e8y7MAmg</a></p>&mdash; OpenAI Developers (@OpenAIDevs) <a href="https://x.com/OpenAIDevs/status/2054586214112780518?ref_src=twsrc%5Etfw">2026年5月13日</a></blockquote>

🔖開発フローの中で活かすCodex
------------------------------------------------------------

* レビュー
* 実装
* **コードリーディング**
* 開発ワークフロー

コードリーディング
==================================================

* ChatGPTのモバイルアプリ使ってる方？🙋（私はiPhoneで）
* ChatGPTのモバイルアプリから、あなたのPCのCodex Appに接続できます
* （Codex Cloudとは別の話）

.. revealjs-break::
    :notitle:

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="en" dir="ltr">You&#39;ve been asking for this one...<br><br>Now in preview: Codex in the ChatGPT mobile app.<br><br>Start new work, review outputs, steer execution, and approve next steps, all from the ChatGPT mobile app. Codex will keep running on your laptop, Mac mini, or devbox. <a href="https://t.co/9i2Jckjt9z">pic.twitter.com/9i2Jckjt9z</a></p>&mdash; OpenAI (@OpenAI) <a href="https://x.com/OpenAI/status/2055016850849993072?ref_src=twsrc%5Etfw">2026年5月14日</a></blockquote>

モバイルでCodex
------------------------------------------------------------

* あなたのPCで動くCodex Appにモバイルから接続
* 私はPCでCodex Appで常時作業
* スマホさえ持っていれば、PCにcloneしたコードについて質問して **PCが手元になくても** 回答を得られる

元々Codexでソースコード読んでました
------------------------------------------------------------

.. raw:: html

    <iframe width="800" height="480" src="https://ftnext.github.io/2025-slides/lunchwithai-codex2/invincible-code-reading.html"
        title="Codex CLIで加速するコードリーディング"></iframe>

仕事中
------------------------------------------------------------

* 通勤中は投げておいた質問の回答を読みながら
* 仕事中常時ペアプロ。休憩時間に使ってるライブラリへの疑問をモバイルから自宅のCodexに投げる

モバイルで超快適コードリーディング
==================================================

* Codex AppにChatGPTモバイルアプリから接続する設定をぜひ！
* ここでもポイントは「自動レビュー」
* なおMacBookは画面ロックせず低電力モードで待機（*最適化の余地あり*）

🔖開発フローの中で活かすCodex
------------------------------------------------------------

* レビュー
* 実装
* コードリーディング
* **開発ワークフロー**

App Server
==================================================

Codexを使った *開発ワークフローをカスタマイズ* できる

**いろんな形態** で提供できる秘密
------------------------------------------------------------

* App
* CLI
* Cloud
* VS Code拡張

.. _Codex ハーネスの解放：App Server を構築した方法: https://openai.com/ja-JP/index/unlocking-the-codex-harness/

記事 `Codex ハーネスの解放：App Server を構築した方法`_
------------------------------------------------------------

* **JSON-RPC** プロトコル
* 異なるクライアント（CLI、App、IDE拡張、...）が同じCodexハーネスを使用できる
* CLIで ``codex app-server``

App Server **SDK** [#app-server-sdk-docs]_
------------------------------------------------------------

* TypeScript
* **Python** (NEW!!)

.. [#app-server-sdk-docs] https://developers.openai.com/codex/sdk

App Server SDK
------------------------------------------------------------

* npm `@openai/codex-sdk <https://www.npmjs.com/package/@openai/codex-sdk>`__ （例：`nrslib/takt <https://github.com/nrslib/takt/blob/v0.43.0/package.json#L67>`__）
* PyPI `openai-codex <https://pypi.org/project/openai-codex/>`__

TODO レビューもさせる例
------------------------------------------------------------

ぜひ構築してみてください！
==================================================

* `Awesome Codex App Server <https://posfie.com/@ftnext/p/SpkW6rS>`__ （更新中） 

まとめ🌯 わたしの、最高の相棒、Codex
==================================================

:自動レビュー: **自走** が簡単に
:モバイル: スマホ片手にどこからでも **コードリーディング**
:App Server: **開発ワークフロー** も組める！

ご清聴ありがとうございました！
--------------------------------------------------

Happy Development♪

Appendix：開発フローの中でさらに活かすCodex
==================================================

* 調査
* 自動化

助けてCodexえもん〜
==================================================

落ちた GitHub Actions の調査

TODO
------------------------------------------------------------

自動化
==================================================

* シェルスクリプトに秀でていると感じる

3月に話しました
------------------------------------------------------------

TODO

直近ではLLMを使おうとしたら綺麗にシェルスクリプトに収められた
----------------------------------------------------------------------

* TODO：Claude Code Actionからシェルスクリプトにした例

EOF
===
