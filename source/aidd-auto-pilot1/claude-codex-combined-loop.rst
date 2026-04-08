============================================================
Claude Codeで実装、 Codexでレビュー、合わせて自走の企て
============================================================

Claude Codeで実装、 Codexでレビュー、合わせて自走の企て
============================================================

:Event: 【AI駆動開発】AI自走環境構築・運用スペシャル #1
:Presented: 2026/04/09 nikkie

お前、誰よ？（**Python使い** の自己紹介）
============================================================

* nikkie（にっきー）
* 機械学習エンジニア・LLM・自然言語処理（`We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__）
* `Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A提供 <https://jp.ub-speeda.com/news/20260319/>`__）

.. image:: ../_static/uzabase-white-logo.png

**自走** に強い興味 [#2026-auto-pilot-article]_
------------------------------------------------------------

.. raw:: html

    <iframe class="speakerdeck-iframe" style="border: 0px; background: rgba(0, 0, 0, 0.1) padding-box; margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" frameborder="0" src="https://speakerdeck.com/player/6f8da4e8af70435693f4fdd940e956e4?slide=3" title="夜を制する者が “AI Agent 大民主化時代” を制する" allowfullscreen="true" allow="web-share" data-ratio="1.7777777777777777"></iframe>

.. [#2026-auto-pilot-article] `散文：夜に駆ける <https://nikkie-ftnext.hatenablog.com/entry/memorandum-auto-pilot-coding-agent-at-night-202602>`__ や `Devin からの pull request に GitHub Copilot で自動的にレビューし、Devin に自動的に修正してもらう <https://nikkie-ftnext.hatenablog.com/entry/devin-pull-request-github-copilot-review-devin-fix-auto-loop-first-step>`__

直近の個人開発フロー
============================================================

私は **合わせて** 使っています

* Claude Code
* Codex CLI

Claude Codeで実装（``/feature-dev``）
------------------------------------------------------------

.. code-block:: txt

    /feature-dev Add user authentication with OAuth 

* `claude-plugins-official <https://github.com/anthropics/claude-plugins-official>`__ marketplaceの `feature-dev <https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev>`__ プラグイン

.. code-block:: shell

    % claude plugins marketplace add https://github.com/anthropics/claude-plugins-official          
    % claude plugins install feature-dev@claude-plugins-official

.. _Feature Dev: https://claude.com/plugins/feature-dev

`Feature Dev`_
------------------------------------------------------------

    A structured 7-phase workflow

* code-explorer (Phase 2)
* code-architect (Phase 4)
* code-reviewer (Phase 6)

鹿野さんもおすすめ
------------------------------------------------------------

    | 手戻りを減らしたい
    | Claude Codeのfeature-devプラグインを使う

3/11 `Claude Codeを加速させる私の推しスキル・ツール・設定（Findyイベント登壇資料） <https://zenn.dev/ubie_dev/articles/claude-code-tips-findy-2026#%E6%89%8B%E6%88%BB%E3%82%8A%E3%82%92%E6%B8%9B%E3%82%89%E3%81%97%E3%81%9F%E3%81%84>`__

.. かのさん https://x.com/ftnext/status/2031577043176157449

実装し切ったらCodexでレビュー
------------------------------------------------------------

* :command:`codex review --base main`
* インタラクティブでないレビュー。時間がかかるが非常に鋭い
* （Slash command ``/review`` もある）

.. codex exec review

OpenAIはCodexで一通りレビュー
------------------------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">今やっている Agents SDK の開発では gpt-5-codex による考慮漏れのレビューで何度も救ってもらっているし、チームの中では codex のレビューは全部自動で走っていて、それを一通りやった上で人の目が入るようになってきています。</p>&mdash; Kazuhiro Sera (瀬良) (@seratch_ja) <a href="https://twitter.com/seratch_ja/status/1971925353741561877?ref_src=twsrc%5Etfw">2025年9月27日</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

直近の開発フロー まとめ
------------------------------------------------------------

.. TODO 画像にする

Claude Code ←→ 私 ←→ Codex CLI

.. 著名エンジニアも https://x.com/kenn/status/2041438528090058950

.. _openai/codex-plugin-cc: https://github.com/openai/codex-plugin-cc

openai/codex-plugin-cc は有効性の証左？
------------------------------------------------------------

    Claude Code のワークフローを維持したまま、Codex が強い場面だけ Codex を使えるようにする（`Claude Code 向け Codex Plugin の紹介 <https://x.com/reach_vb/status/2039251986357338257>`__）

.. code-block:: txt

    /codex:review

適用事例：20行の参照実装
------------------------------------------------------------

.. code-block:: python
    :caption: crude example of modifying (`PEP 723 <https://peps.python.org/pep-0723/#reference-implementation>`__)
    :linenos:

    import re

    import tomlkit

    REGEX = r'(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$'

    def add(script: str, dependency: str) -> str:
        match = re.search(REGEX, script)
        content = ''.join(
            line[2:] if line.startswith('# ') else line[1:]
            for line in match.group('content').splitlines(keepends=True)
        )

        config = tomlkit.parse(content)
        config['dependencies'].append(dependency)
        new_content = ''.join(
            f'# {line}' if line.strip() else f'#{line}'
            for line in tomlkit.dumps(config).splitlines(keepends=True)
        )

        start, end = match.span('content')
        return script[:start] + new_content + script[end:]

**500行**
------------------------------------------------------------

* 重厚な実装に！ https://github.com/ftnext/pep723/pull/6
* Codex (GPT-5.4)がPythonの仕様を熟知していて **考慮漏れを指摘しまくる** （10回近く）
* 20行の参照実装をもとにClaude Code (Sonnet 4.6)で実装していたが、Opus 4.6出動

.. このPEP自体の考慮漏れもある　

効果ありそう！ここで担当を整理
------------------------------------------------------------

:Claude Code: 実装
:Codex CLI: レビュー
:nikkie: 受け渡し役

受け渡すだけの私って、 **必要なくね** ？
============================================================

Claude Code ←→ 私 ←→ Codex CLI

**自動ループ** の構築を試みる
------------------------------------------------------------

.. TODO 画像にする

* Claude（実装） → Codex（レビュー） → Claude（実装） → Codex（レビュー） → ...
* レビューで指摘がなくなったり、前回と矛盾したりしたら止まる

私は takt に目をつけた 🎼
------------------------------------------------------------

* TAKT Agent Koordination Topology
* https://github.com/nrslib/takt
* 対応：Claude Code、Codex、OpenCode、Cursor、GitHub Copilot CLI (`v0.35.0 <https://github.com/nrslib/takt/blob/v0.35.0/docs/README.ja.md>`__)

.. code-block:: shell

    $ npm install -g takt@">=0.34.0"

作者nrsさんによる発信多数
------------------------------------------------------------

* `AIの見張り番をやめよう - AIチームを指揮するOSS「TAKT」を公開しました <https://zenn.dev/nrs/articles/c6842288a526d7>`__
* 3/12 `Claude Code Meetup Japan #3 LT <https://www.youtube.com/live/csJhIQFuYJw?si=8pj0UHkrAWNqfy4b&t=7688>`__
* 4/10 `Claude Code Meetup Japan #4 <https://aid.connpass.com/event/386203/>`__ LT & 4/15 `配信 <https://nrs-seminar.connpass.com/event/389688/>`__

私が理解したtakt
============================================================

* コーディングエージェントに任せたいタスクの **仕様書**
* コーディングエージェントを **ワークフロー** に従わせて、仕様書を実装してもらえる

（完全に理解への道半ば）

taktのワークフロー [#takt-0.34.0-rename-workflow]_
------------------------------------------------------------

* **YAMLファイル** を書く
* ``takt --workflow <workflow.yaml>``
* コーディングエージェントの動き方を **プログラミング**

.. _Workflow with Review: https://github.com/nrslib/takt/blob/main/docs/pieces.md#workflow-with-review

.. [#takt-0.34.0-rename-workflow] 音楽の比喩(piece)を使っていたのですが、 `v0.34.0 <https://x.com/nrslib/status/2039895144196129147>`__ でworkflowにrenameしました

例： `Workflow with Review`_ より
------------------------------------------------------------

.. literalinclude:: takt-example-workflow-with-review.yaml
    :language: yaml

実装とレビューのループ（抜粋）
------------------------------------------------------------

.. literalinclude:: takt-example-workflow-with-review.yaml
    :language: yaml
    :lines: 3,6-7,13-17,20-21,26-30

実装が完了したらレビューへ
------------------------------------------------------------

.. literalinclude:: takt-example-workflow-with-review.yaml
    :language: yaml
    :lines: 3,6-7,13-17
    :emphasize-lines: 5-6

修正が必要ならレビューから実装に戻る
------------------------------------------------------------

.. literalinclude:: takt-example-workflow-with-review.yaml
    :language: yaml
    :lines: 6,21,26-30
    :emphasize-lines: 6-7

レビューで ``codex review`` を呼ぶように指示
------------------------------------------------------------

.. literalinclude:: takt-claude-codex-combined-loop.yaml
    :language: yaml
    :lines: 34-47

taktの仕様書
------------------------------------------------------------

* 仕様書は渡してもいいし、 **一緒に作ってもいい**
* ``takt`` と起動すると `インタラクティブモード <https://github.com/nrslib/takt/blob/main/docs/cli-reference.ja.md#%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%A9%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96%E3%83%A2%E3%83%BC%E3%83%89>`__ に入って仕様書を作れる

インタラクティブモード（抜粋）
------------------------------------------------------------

.. code-block:: txt

    対話モードを選択してください:

    ❯ アシスタント (default)
        確認質問をしてから指示書を作成
      
      パススルー  # <- 仕様書が手元にある時
        入力をそのままタスクとして渡す

.. revealjs-break::
    :notitle:

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="ja" data-align="center" data-dnt="true"><p lang="ja" dir="ltr">TAKT でやり取りせず AI との会話の末に Issue を作らせて、それを takt add #99 で引き渡すという裏テクもあります<br><br>調査とかしながらシームレスに移行する場合にどうぞ！ <a href="https://t.co/xEXkx5OtLn">https://t.co/xEXkx5OtLn</a></p>&mdash; nrs (@nrslib) <a href="https://twitter.com/nrslib/status/2041098219267182956?ref_src=twsrc%5Etfw">2026年4月6日</a></blockquote>

まとめ🌯：Claude Codeで実装、 Codexでレビュー、合わせて自走の企て
======================================================================

* 直近の開発フローの紹介
* taktを使って **自動ループ** の構築を試みた（さらに育てていくぞ💪）

直近の開発フロー
------------------------------------------------------------

:Claude Code: 実装（``/feature-dev``）
:Codex CLI: レビュー（``codex review --base main``）
:nikkie: 受け渡し役

taktを使った自動ループ（一歩目）
------------------------------------------------------------

:implement: 実装（Opus 4.6）
:review: ``codex review`` を呼び出してレビュー（Opus 4.6）

止まるまで繰り返し実行される

ご清聴ありがとうございました
------------------------------------------------------------

Happy Development ❤️🤖
