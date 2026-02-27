==================================================
deep research のブラックボックスを OTel で覗く
==================================================

:Event: 福岡Rubyist会議05
:Presented: 2026/02/28 nikkie

お前、誰よ（Python使いの自己紹介）
==================================================

* 東京在住。機械学習エンジニア
* `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（deep research 機能含む） [#hiring]_

.. image:: ../_static/uzabase-white-logo.png

.. [#hiring] `We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__

もう少し自己紹介
--------------------------------------------------

* コマンドラインからllm-deep-research（プラグイン）
* `Python Meetup Fukuoka <https://www.youtube.com/@lycorptech_jp/search?query=Python%20Meetup>`__ が熱くて🔥たびたび参加
* 今回の発表を機に、Rubyは5年以上ぶり

この一年、何をしていましたか？
==================================================

* テーマ："最近、何してる？"
* https://regional.rubykaigi.org/fukuoka05/

deep research💫
==================================================

2025/02/02 OpenAI `Introducing deep research <https://openai.com/index/introducing-deep-research/>`__

.. 日本語 https://openai.com/ja-JP/index/introducing-deep-research/

.. in-depth: 徹底的な

皆さん使ってますか？🙋
--------------------------------------------------

* GPT (OpenAI)
* Gemini・Claudeなどなど [#deep-research-services]_
* 公開実装を動かした
* 自作している

.. [#deep-research-services] Grok・Perplexity

.. 網羅するより代表例を1つずつ紹介してみる

OpenAI deep research
--------------------------------------------------

.. image:: ../_static/fukuokark05/openai-deep-research-example.png

.. 〇〇を調べて：追加質問→人間が回答→Web検索→詳細レポート（10〜15分）
    2026/02にアップデートが入った

.. revealjs-break::

* LLMが調査を **計画** してWeb（や指定したファイル）を **調査** （`Deep research in ChatGPT <https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt>`__）
* 私は技術的な調査は「deep researchでOKじゃん」となった
* OpenAIは **専用モデル** で実現 [#deep-research-model]_

.. https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt

.. [#deep-research-model] 「*The deep research model is powered by an early version of OpenAI o3 that is optimized for web browsing.*」 `Deep Research System Card <https://openai.com/index/deep-research-system-card/>`__

LLMにWeb検索させて再現させよう！
--------------------------------------------------

* OpenAIのように専用モデルは開発できずとも
* LLMは *道具が使える* （tool use = function calling）

.. tool useはコーディングエージェントを実現する要素でもある

.. 専用モデルを開発する論文もある（OpenAIのモデルよりは小さなモデル）

.. revealjs-break::
    :notitle:

.. raw:: html

    <iframe class="speakerdeck-iframe" style="border: 0px; background: rgba(0, 0, 0, 0.1) padding-box; margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" frameborder="0" src="https://speakerdeck.com/player/f912a0d061334d5aaf2fbf09ace3888c?slide=11" title="AIエージェントとは（UB Tech vol.21）" allowfullscreen="true" data-ratio="1.7777777777777777"></iframe>

.. _Open-source DeepResearch: https://huggingface.co/blog/open-deep-research

`Open-source DeepResearch`_
==================================================

* OpenAIの発表を受けて、Hugging Faceが24時間再現チャレンジ
* https://github.com/huggingface/smolagents/tree/main/examples/open_deep_research

    This agent achieves **55% pass@1** on the GAIA validation set, compared to **67%** for the original Deep Research.

.. LLMにテキストブラウザを渡した

公開実装が次々に登場
--------------------------------------------------

.. TODO

* 企業：LangChainなど
* コミュニティ

本気で探せば100以上？

私は工夫を知りたい
--------------------------------------------------

* 自作の参考にするために公開実装を動かす
* 作者ではないので、内部の動きが手に取るようにはわからない（**ブラックボックス**）

.. 今ならコーディングエージェントに調べてもらう選択肢あり

LLMへの入力を全部分かりたい（束縛系）
--------------------------------------------------

* LLMアプリケーション開発における私の信念
* deep researchを依頼された **LLMのように考える** [#think-like-agents]_
* 改善案を出しやすい（LLMより前は数学の理解が必要だった）

.. [#think-like-agents] 「*Think like your agents*」 Anthropic `How we built our multi-agent research system <https://www.anthropic.com/engineering/built-multi-agent-research-system>`__

**OpenTelemetry** (OTel) に目をつけた！
==================================================

* テレメトリ（トレース・メトリクス・ログ）から **可観測性** を得る手段

    * システムの出力から内部状態を理解する

* ベンダーやツールのロックインなし

.. https://opentelemetry.io/ja/docs/what-is-opentelemetry/

.. 今月のSoftwareDesign「再考・ログ設計」、よいです... https://x.com/gihyosd/status/2027337725746315549

コンテキスト伝播
--------------------------------------------------

リクエストにIDを付与して分散トレース

https://opentelemetry.io/ja/docs/concepts/context-propagation/#traces

.. 分散トレーシング
    コンテキスト伝播

Semantic conventions
--------------------------------------------------

* https://opentelemetry.io/docs/specs/semconv/
* LLMアプリケーション向けのセマンティック規約策定が現在進行系

    * https://opentelemetry.io/docs/specs/semconv/gen-ai/

例えば Gemini
--------------------------------------------------

* Pythonでは `google-genai <https://pypi.org/project/google-genai/>`__ SDK
* OTelライブラリが `opentelemetry-instrumentation-google-genai <https://pypi.org/project/opentelemetry-instrumentation-google-genai/>`__

.. TODO 計装という言葉の導入

Geminiを使ったdeep researchの計装イメージ
--------------------------------------------------

.. code-block:: python

    import deep_research_lib
    from opentelemetry.instrumentation.google_genai import GoogleGenAiSdkInstrumentor

    GoogleGenAiSdkInstrumentor().instrument()
    result = deep_research_lib.Agent().run(query)

.. TODO Python実装へのリンク

回答：この一年、何をしていましたか？
==================================================

* deep researchの実装を見つける
* OpenTelemetryを有効にして動かす（鑑賞）
* 気になる箇所のソースを読み理解深める（自分の実装に活かす）

これをRubyでやることを考えます
==================================================

.. TODO Ruby実装へのリンク

今回のdeep research
--------------------------------------------------

1. topic_generator
2. topic_researcher
3. research_synthesizer

Gemini APIのリクエストにfaraday
--------------------------------------------------

.. code-block:: ruby

    conn = Faraday.new(
      url: "https://generativelanguage.googleapis.com"
    )
    response = conn.post(
      "/v1beta/models/gemini-3-flash-preview:generateContent"
    ) do |req|
      req.headers["Content-type"] = "application/json"
      req.headers["x-goog-api-key"] = api_key
      req.body = {
        contents: [
          {
            parts: [
              { text: "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?" }
            ]
          }
        ]
      }.to_json
    end

opentelemetry-instrumentation-faraday
--------------------------------------------------

.. code-block:: ruby

    ENV["OTEL_TRACES_EXPORTER"] = "console"
    OpenTelemetry::SDK.configure do |c|
      c.use 'OpenTelemetry::Instrumentation::Faraday'
    end

限界：Gemini APIへのリクエストが不明
--------------------------------------------------

.. code-block:: ruby

    ENV["OTEL_TRACES_EXPORTER"] = "console"
    OpenTelemetry::SDK.configure do |c|
      c.use 'OpenTelemetry::Instrumentation::Faraday'
    end

    agent = ResearchAgent.new(api_key: api_key, config: config)
    result = agent.run(USER_QUERY)

Workaround: faradayのMiddleware
--------------------------------------------------

.. code-block:: ruby

  class OtelBodyCaptureMiddleware < Faraday::Middleware
    def call(env)

    end
  end

  agent = ResearchAgent.new(api_key: api_key, config: config) do |conn|
    attach_faraday_otel_middlewares(conn)
  end

最後に
==================================================

* Googleはinteractions APIとしてdeep researchを提供しています
* Claude Code SDK（コーディングエージェントのハーネス）を使う

ご清聴ありがとうございました
--------------------------------------------------

.. サーバサイドtool use
