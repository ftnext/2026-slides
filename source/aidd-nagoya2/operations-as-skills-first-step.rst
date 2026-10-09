:ogp_title: 小事例紹介：運用 as Agent Skills
:ogp_event_name: aidd-nagoya2
:ogp_slide_name: operations-as-skills-first-step
:ogp_description: AI駆動開発勉強会 名古屋支部#2

============================================================
小事例紹介：**運用** as Agent Skills
============================================================

:Event: AI駆動開発勉強会 名古屋支部#2
:Presented: 2026/10/09 nikkie

お前、誰よ
============================================================

* nikkie（にっきー） [#nikkie-uuid]_ ・`Codex Ambassador (Tokyo) <https://nikkie-ftnext.hatenablog.com/entry/announcement-one-of-codex-ambassadors-tokyo>`__・Devin Ambassador
* 機械学習エンジニア・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__・`Slackbot <https://jp.ub-speeda.com/news/20260910/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#nikkie-uuid] UUID `28fb3f96-a221-462c-93bd-567b431715b9 <https://x.com/ftnext/status/2041119610368602138>`__

個人「全部使えばええんや！」（マインド）
---------------------------------------------------

* `OpenAI DevDay 2026 <https://nikkie-ftnext.hatenablog.com/entry/openai-docs-whats-new-devday-2026-reading-notes>`__ で個人的イチオシは **Sign in with ChatGPT**
* `Devin <https://devin.ai/blog/sign-in-with-chatgpt>`__ で、ChatGPTのサブスクからGPTモデルが使えます（`他にNotionなど <https://learn.chatgpt.com/docs/sign-in-with-chatgpt#partners>`__）
* Try `llm-chatgpt-plan <https://x.com/ftnext/status/2107987551567102426>`__

`connpass <https://aid.connpass.com/event/404553/>`__ 「チームでAIを扱う」
------------------------------------------------------------------------------------------------------

* 私はAIで増幅されているが、チームの増幅率はもっと小さい感覚。わからん殺しされている
* 暗中模索🤯の中、**運用の知識を共有できた** 小さな事例を話します [#theme-respect]_

.. [#theme-respect] DevDayの話かで迷いましたが、封印して私目線で「チームでAIを扱う」話をします！

運用 as Agent Skills
============================================================

* 開発チーム（4人）で抱えていた小さな **運用の手順をAgent Skillに** した
* **皆** お気にのコーディングエージェントと **運用できる** ように

小さな運用
---------------------------------------------------

* 毎日未明にKubernetesのジョブが動き、失敗すると勤務開始前にSlack通知が届いている
* PDFを元にLLMでデータ生成を何件もする。**1件でも生成失敗** したら、ジョブは **エラー終了** する
* 有志が生成失敗を特定し、ローカル環境でリトライして復旧（機会は均等）

私は初回、Codexとタッグで
============================================================

* ソースコードとエラーメッセージをCodex（デスクトップアプリ）に渡して「復旧したいからサポートして」と質問しまくる
* 起きた事象を把握し、生成失敗の特定・復旧を実施

思い出した：LayerXさんの事例
---------------------------------------------------

* 入社した `ちゃんさん <https://x.com/chan_san_jp>`__、「*教わったオペレーションを片っ端からSkillにしていく*」
* ref: Podcast #あらたまいくお `いくお、会社やめるってよ <https://open.spotify.com/episode/0cRDd2qbUTGr5yySC5Hp4p?si=bvNXEr9ISmqRatGIuiPUcQ>`__ 21:00過ぎ

.. https://x.com/chan_san_jp/status/2023714833544474642

初回運用のセッションをスキルに
---------------------------------------------------

* Codexなら `$skill-creator <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md>`__
* セッションから、確定した **手順を取り出し** た
* 未来の私は全て忘れているので、コーディングエージェントと一緒なら思い出せるように

.. 参考 echoするだけシェルスクリプト

今回の運用手順のスキル（概略）
---------------------------------------------------

1. エラーメッセージに記載された失敗の行を確認
2. 生成失敗した入力を特定（エージェント用に :file:`scripts/`）
3. ローカルから生成リトライ（LLMでの生成に時間がかかる時もエージェントが見ててくれる）

ひろがる使用者
============================================================

* 「試しにAgent Skillにしてみた」と共有
* チームメイトが対応時に使ってくれた
* `Agent Skillsの規格 <https://agentskills.io/specification>`__ で、ツールの違いは吸収（Codexデスクトップ・Cursor）

使うことで、手順も育つ
---------------------------------------------------

* 使い手が増える中で「今回の運用ではこれも追加で調べた」
* 今回は私が **スキルを更新**
* チーム共通スキルを、皆で育てる可能性

まとめ🌯小事例紹介：運用 as Agent Skills
============================================================

* 人とAIで行った **運用セッションをAgent Skillとして残した**
* 皆 **詳しいAgentと作業** でき、運用知識共有に繋がった
* Skillを装備したエージェントが *自動で復旧* する可能性も拓いている

ご清聴ありがとうございました
---------------------------------------------------

Happy Development ❤️🤖（ステッカードゾー）
