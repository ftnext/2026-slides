==================================================
deep researchの ブラックボックスを OTelで覗く
==================================================

:Event: 福岡Rubyist会議05
:Presented: 2026/02/28 nikkie（`サンプルコード <https://github.com/ftnext/2026-slides/tree/main/samplecode/deep-research-otel>`__）

お前、誰よ（Python使いの自己紹介）
==================================================

* 東京在住。機械学習エンジニア
* `Speeda AI Agent <https://jp.ub-speeda.com/news/speeda-promotion-gallery/>`__ 開発（deep research 機能含む） [#hiring]_

.. image:: ../_static/uzabase-white-logo.png

.. [#hiring] `We're hiring! <https://hrmos.co/pages/uzabase/jobs/1829077236709650481>`__

もう少し自己紹介
--------------------------------------------------

* コマンドラインから `llm-deep-research <https://github.com/ftnext/llm-deep-research>`__ [#simonw-llm-plugin]_
* `Python Meetup Fukuoka <https://www.youtube.com/@lycorptech_jp/search?query=Python%20Meetup>`__ が熱くて🔥たびたび参加（`次回3/4 <https://lycorptech-fukuoka.connpass.com/event/380867/>`__）
* 今回の発表を機に、Rubyは5年以上ぶり（PythonをLLMで変換）

.. [#simonw-llm-plugin] Simon Willisonさんの `llm <https://pypi.org/project/llm/>`__ のプラグイン

この一年、何をしていましたか？
==================================================

* テーマ："最近、何してる？"
* https://regional.rubykaigi.org/fukuoka05/

deep research💫 [#in-depth-tips]_
==================================================

2025/02/02 OpenAI `Introducing deep research <https://openai.com/index/introducing-deep-research/>`__

.. 日本語 https://openai.com/ja-JP/index/introducing-deep-research/

.. [#in-depth-tips] in-depth: 徹底的な

皆さん使ってますか？🙋
--------------------------------------------------

* GPT (OpenAI)
* `Gemini <https://gemini.google/overview/deep-research/>`__ ・ `Claude <https://claude.com/blog/research>`__ などなど [#deep-research-services]_
* 公開実装を動かした
* 自作している

.. [#deep-research-services] X (`Grok <https://x.ai/news/grok-3>`__)・ `Perplexity <https://www.perplexity.ai/ja/hub/blog/introducing-perplexity-deep-research>`__ などなど

.. 網羅するより代表例を1つずつ紹介してみる

OpenAI deep research
--------------------------------------------------

.. image:: ../_static/fukuokark05/openai-deep-research-example.png

.. revealjs-break::
  :notitle:

1. 人間が調査を依頼
2. LLMから追加で質問 [#202602-deep-research-update]_
3. 人間から回答
4. **LLMがWebを調査** （10分程度）
5. 詳細なレポート

.. [#202602-deep-research-update] 2026/02にアップデートが入りました（`Deep research in ChatGPT <https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt>`__）

私の **代わりにWebを調査** してきてくれる！
--------------------------------------------------

* 調査計画
* Web検索 [#deep-research-supplement]_
* Webブラウジング

.. [#deep-research-supplement] 手元のファイル指定も可

LLMに **道具を渡して** 再現させよう！
--------------------------------------------------

* OpenAIは *専用モデル* で実現 [#deep-research-model]_
* GPTのような規模のモデルは開発できずとも
* LLMは道具が使える（tool use = function calling）

.. [#deep-research-model] 「*The deep research model is powered by an early version of OpenAI o3 that is optimized for web browsing.*」 `Deep Research System Card <https://openai.com/index/deep-research-system-card/>`__

.. tool useはコーディングエージェントを実現する要素でもある

.. Googleの論文あった

.. 専用モデルを開発する論文もある（OpenAIのモデルよりは小さなモデル）

.. revealjs-break::
    :notitle:

.. raw:: html

    <iframe class="speakerdeck-iframe" style="border: 0px; background: rgba(0, 0, 0, 0.1) padding-box; margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" frameborder="0" src="https://speakerdeck.com/player/f912a0d061334d5aaf2fbf09ace3888c?slide=11" title="AIエージェントとは（UB Tech vol.21）" allowfullscreen="true" data-ratio="1.7777777777777777"></iframe>

.. revealjs-break::
    :notitle:

1. LLMにプロンプトとtool一覧を送る
2. LLM「このtoolをこれこれの引数で呼び出したい」（JSON） [#mcp-tools]_
3. **アプリケーションでtoolを呼び出し、結果をLLMに返す**
4. LLMがtoolの結果を元に（必要であればさらにtool呼び出し）回答

.. [#mcp-tools] MCP（Model Control Protocol）はtool呼び出しを統一するものでした

.. _Open-source DeepResearch: https://huggingface.co/blog/open-deep-research

`Open-source DeepResearch`_
==================================================

* OpenAIの発表を受けて、Hugging Faceが24時間再現チャレンジ
* https://github.com/huggingface/smolagents/tree/main/examples/open_deep_research

    This agent achieves **55% pass@1** on the GAIA [#gaia-paper]_ validation set, compared to **67%** for the original Deep Research.

.. [#gaia-paper] `[2311.12983] GAIA: a benchmark for General AI Assistants <https://arxiv.org/abs/2311.12983>`__

Hugging Face製deep researchの工夫
--------------------------------------------------

* テキストブラウザ（*an extremely simple text-based web browser*）
* *CodeAct* [#codeact-paper]_ ：計画をコード（Python）で表現

.. [#codeact-paper] `[2402.01030] Executable Code Actions Elicit Better LLM Agents <https://arxiv.org/abs/2402.01030>`__

例えば、フレームワークにはだいたい公開実装あり
--------------------------------------------------

* `Pydantic AI <https://github.com/pydantic/pydantic-ai/blob/main/examples/pydantic_ai_examples/flight_booking.py>`__
* `Agent Development Kit <https://github.com/google/adk-samples/tree/main/python/agents/deep-search>`__ (Google)
* `Strands Agents <https://github.com/strands-agents/samples/tree/main/02-samples/14-research-agent>`__ (AWS)
* `Agent Framework <https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents>`__ (Microsoft)

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

コンテキスト伝播🏃‍♂️ [#otel-context-propagation]_
------------------------------------------------------------

.. image:: ../_static/fukuokark05/otel-docs-context-propagation-example.svg

.. [#otel-context-propagation] 図は https://opentelemetry.io/ja/docs/concepts/context-propagation/#traces より（マイクロサービスアーキテクチャで分散トレーシング）

トレース例🏃‍♂️
--------------------------------------------------

.. code-block:: json

  {
      "name": "GET /",
      "context": {
          "trace_id": "0x9591b67e3eb9f91ecadc84aec50e79f0",
          "span_id": "0x9bf997b809109fa3",
          "trace_state": "[]"
      },
      "kind": "SpanKind.SERVER",
      "parent_id": "0x119f828276ebd665",
      "start_time": "2026-02-27T10:57:22.142571Z",
      "end_time": "2026-02-27T10:57:22.143700Z",
      "status": {
          "status_code": "UNSET"
      },
      "attributes": {
          "http.scheme": "http",
          "http.host": "127.0.0.1:8000",
          "net.host.port": 8000,
          "http.flavor": "1.1",
          "http.target": "/",
          "http.url": "http://127.0.0.1:8000/",
          "http.method": "GET",
          "http.server_name": "localhost:8000",
          "http.user_agent": "Faraday v2.14.1",
          "net.peer.ip": "127.0.0.1",
          "net.peer.port": 62375,
          "http.route": "/",
          "http.status_code": 200
      },
      "events": [],
      "links": [],
      "resource": {
          "attributes": {
              "telemetry.sdk.language": "python",
              "telemetry.sdk.name": "opentelemetry",
              "telemetry.sdk.version": "1.35.0",
              "service.name": "unknown_service"
          },
          "schema_url": ""
      }
  }

フィールド名：Semantic conventions🏃‍♂️
--------------------------------------------------

* https://opentelemetry.io/docs/specs/semconv/
* LLMアプリケーション向けのセマンティック規約策定が **現在進行系** 🔥

    * https://opentelemetry.io/docs/specs/semconv/gen-ai/

例えば Gemini
--------------------------------------------------

* Pythonでは `google-genai <https://pypi.org/project/google-genai/>`__ SDK
* `opentelemetry-instrumentation-google-genai <https://pypi.org/project/opentelemetry-instrumentation-google-genai/>`__ で *計装* を提供
* 無料。ただし、入力データはGoogleのモデルの訓練に使われる [#google-gemini-api]_

.. [#google-gemini-api] DeepMindによるGemini APIが無料。本番利用向けにGoogle CloudのVertex AIもあります

悩まされていたブラックボックス📦
--------------------------------------------------

.. code-block:: python

    from deep_research_lib import ResearchAgent  # Geminiを使ったdeep research

    result = ResearchAgent().run(query)

google-genaiを計装（簡略版）🈳 [#research-python-impl]_
------------------------------------------------------------

.. code-block:: python
    :emphasize-lines: 2,4

    from deep_research_lib import ResearchAgent
    from opentelemetry.instrumentation.google_genai import GoogleGenAiSdkInstrumentor

    GoogleGenAiSdkInstrumentor().instrument()
    result = ResearchAgent().run(query)

.. [#research-python-impl] https://github.com/ftnext/2026-slides/tree/main/samplecode/deep-research-otel/python （``uvx --with llm-deep-research llm -m genai-processors-research QUERY`` も提供してます）

.. Geminiへの入力が見られた

回答：この一年、何をしていましたか？
==================================================

* deep researchの実装を見つける
* **OpenTelemetryを有効にして動かす** （鑑賞）
* 気になる箇所のソースを読み理解深める（自分の実装に活かす）

これを **Ruby** でやることを考えます
==================================================

https://github.com/ftnext/2026-slides/tree/main/samplecode/deep-research-otel

今回のdeep research [#genai-processors-research]_
------------------------------------------------------------

1. topic_generator
2. topic_researcher
3. research_synthesizer

.. [#genai-processors-research] Googleの `genai-processors <https://pypi.org/project/genai-processors/>`__ の `Research Agent Example <https://github.com/google-gemini/genai-processors/tree/main/examples/research>`__ （Web検索のみでブラウジングがないところが伸びしろ）

.. revealjs-break::
    :notitle:

.. image:: ../_static/fukuokark05/genai-processor-research.drawio.png
  :scale: 200%

Gemini APIのリクエストにFaraday
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
    :caption: リクエストボディは記録されない

    ENV["OTEL_TRACES_EXPORTER"] = "console"
    OpenTelemetry::SDK.configure do |c|
      c.use 'OpenTelemetry::Instrumentation::Faraday'
    end

    agent = ResearchAgent.new(api_key: api_key, config: config)
    result = agent.run(USER_QUERY)

Workaround: faradayのMiddleware（イメージ）
--------------------------------------------------

.. code-block:: ruby

  class OtelBodyCaptureMiddleware < Faraday::Middleware
    def call(env)
      # 詳しくは次スライド
      # span.set_attribute("http.request.body", body_str)
    end
  end

  agent = ResearchAgent.new(api_key: api_key, config: config) do |conn|
    conn.builder.insert_after(
      OpenTelemetry::Instrumentation::Faraday::Middlewares::Old::TracerMiddleware,
      OtelBodyCaptureMiddleware
    )
  end

.. revealjs-break::
    :notitle:

.. code-block:: ruby

    class OtelBodyCaptureMiddleware < Faraday::Middleware
      def call(env)
        span = OpenTelemetry::Trace.current_span
        if span&.recording?
          body = env.body
          body_str = body.is_a?(String) ? body : JSON.generate(body)
          span.set_attribute("http.request.body", body_str)
        end

        response = @app.call(env)

        if span&.recording?
          span.set_attribute("http.response.body", response.body.to_s)
        end
        response
      end
    end

google-genaiを計装するのと同じ体験をしたい！
==================================================

.. code-block:: python
    :emphasize-lines: 2,4

    from deep_research_lib import ResearchAgent
    from opentelemetry.instrumentation.google_genai import GoogleGenAiSdkInstrumentor

    GoogleGenAiSdkInstrumentor().instrument()
    result = ResearchAgent().run(query)

スコープを絞って自作
--------------------------------------------------

.. code-block:: ruby

    require_relative './deep_research_lib'
    require_relative './instrumentor'

    MyGoogleGenai::Instrumentation::Instrumentor.new.instrument
    result = ResearchAgent.new(api_key: api_key, config: config).run(USER_QUERY)

https://github.com/ftnext/2026-slides/tree/main/samplecode/deep-research-otel/ruby-v2

LLMへの入力、全部分かる！🙌
--------------------------------------------------

.. code-block:: txt

   events=
    [#<struct OpenTelemetry::SDK::Trace::Event
      name="gen_ai.user.message",
      attributes=
       {"content" =>
         "You are an expert at generating topics for research, based on the user's content.\n" +
         "\n" +
         "Your first task is to devise a number of concrete research areas needed to address the user's content.\n" +
         "\n" +

最後に：deep researchを作ってみたくなった方へ
==================================================

* 自作以外に：Googleは `interactions API <https://ai.google.dev/gemini-api/docs/interactions?hl=ja>`__ としてdeep researchを提供しています
* 自作する場合：コーディングエージェントのハーネスを使う（`Claude Agent SDK <https://pypi.org/project/claude-agent-sdk/>`__ など） [#claude-code-oneliner-research]_

.. [#claude-code-oneliner-research] `The one-liner research agent <https://platform.claude.com/cookbook/claude-agent-sdk-00-the-one-liner-research-agent>`__

ご清聴ありがとうございました
--------------------------------------------------

deep research のブラックボックスを OTel で覗く

Appendix
==================================================

なぜGemini？
--------------------------------------------------

* `anthropic-sdk-ruby <https://github.com/anthropics/anthropic-sdk-ruby>`__ と `opentelemetry-instrumentation-anthropic <https://github.com/open-telemetry/opentelemetry-ruby-contrib/tree/main/instrumentation/anthropic>`__ を知った
* Pythonのgoogle-genaiとその計装ライブラリとの関係とはどうやら違うよう [#anthropic-sdk-ruby-practice]_
* 無料で使えるGemini（入力は学習利用される点には注意）

.. [#anthropic-sdk-ruby-practice] https://github.com/ftnext/2026-slides/tree/main/samplecode/deep-research-otel/claude

検索ツールの呼び出し
--------------------------------------------------

* GeminiにGoogle検索させる箇所
* クライアントサイドでなく **サーバサイド**
* Geminiがサーバサイドで検索して、その結果を元に返答しています

EOF
===
