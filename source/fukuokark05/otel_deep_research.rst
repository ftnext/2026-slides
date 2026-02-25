==================================================
deep research のブラックボックスを OTel で覗く
==================================================

:Event: 福岡Rubyist会議05
:Presented: 2026/02/28 nikkie

お前、誰よ（Python使いの自己紹介）
==================================================

* 普段はPythonコミュニティに所属
* 推し： `Python Meetup Fukuoka <https://www.youtube.com/@lycorptech_jp/search?query=Python%20Meetup>`__
* Rubyは今回の発表を機に久しぶりに書いた

.. 業務でもエージェント（deep research機能含む）開発

この一年、何をしていましたか？
==================================================

* テーマ："最近、何してる？"
* https://regional.rubykaigi.org/fukuoka05/

deep research
==================================================

2025/02/02 OpenAI `Introducing deep research <https://openai.com/index/introducing-deep-research/>`__

.. 日本語 https://openai.com/ja-JP/index/introducing-deep-research/

皆さん使ってますか？🙋
--------------------------------------------------

* GPT
* Gemini・Claude・Grok・Perplexityなどなど
* 公開実装を動かした
* 自作している

.. 網羅するより代表例を1つずつ紹介してみる

OpenAI deep research
--------------------------------------------------

* 〇〇を調べて：追加質問→人間が回答→Web検索→詳細レポート（10〜15分）
* 私は技術的な調査は **deep researchでOKじゃん** となった
* **専用モデル**による実装（Web検索だけではない）

.. in-depth: 徹底的な

.. https://openai.com/index/deep-research-system-card/
    専用モデル 2026/02にアップデートされてる

Open-source DeepResearch
==================================================

.. https://huggingface.co/blog/open-deep-research

* LLMを訓練するのではなく、**Web検索** させる（tool use）
* 専用モデルなしでもdeep research機能を実現
* 公開実装が次々と登場（本気で探せば100以上？）

tool use (=function call)
--------------------------------------------------

図解

私は工夫を知りたい
--------------------------------------------------

* 自作の参考にするために公開実装を動かす
* 作者ではないので、内部の動きがわからない（**ブラックボックス**）

.. 今ならコーディングエージェントに調べてもらう選択肢あり

LLMへの入力を全部分かりたい（束縛系）
--------------------------------------------------

* LLMアプリケーション開発における信念
* LLMのように考える
* 数学が分からなくても制御できる！

.. 「Think like your agents」https://www.anthropic.com/engineering/built-multi-agent-research-system

OpenTelemetry
==================================================

* コンテキスト伝播：リクエストに共通IDを付与してトレース
* LLMアプリケーション向けの機能追加が進む
* deep researchの内部動作を可視化できる
