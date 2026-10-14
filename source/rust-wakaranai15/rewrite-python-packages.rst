:ogp_title: Rustの練習を兼ねて、自作の小さなPythonパッケージをRustで書き直している話
:ogp_event_name: Rust、何もわからない… #15
:ogp_slide_name: rewrite-python-packages
:ogp_description: Rust、何もわからない… #15 LT

================================================================================
Rustの練習を兼ねて、自作の小さなPythonパッケージをRustで書き直している話
================================================================================

Rustの練習を兼ねて、自作の小さなPythonパッケージをRustで書き直している話
================================================================================

:Event: Rust、何もわからない… #15
:Presented: 2026/10/14 nikkie

.. 【15秒／累計0:15】
   普段はPythonを書いているnikkieです。今日は、自作の小さなPythonパッケージを
   Rustで書き直すことで、Rustの練習の機会を作っている話をします。

お前、誰よ
============================================================

* nikkie（にっきー）、 **Python** を書きます（小さなOSS公開、PyCon JP登壇）
* 機械学習エンジニア [#uzabase-message]_ ・`Speeda AI Agent <https://www.uzabase.com/jp/info/20250901/>`__ 開発（`A2A <https://jp.ub-speeda.com/news/20260319/>`__・`MCP <https://jp.ub-speeda.com/news/20260701/>`__・`Slackbot <https://jp.ub-speeda.com/news/20260910/>`__ 提供）

.. image:: ../_static/uzabase-white-logo.png

.. [#uzabase-message] お詫び申し上げます。`【第二報】NewsPicksのお客様の個人情報漏洩の可能性に関するお詫びとお知らせ <https://corp.newspicks.com/info/20261009>`__

モチベーション：Rust製ツールチェインの盛り上がり
---------------------------------------------------

* Astralによる `uv <https://github.com/astral-sh/uv>`__・`Ruff <https://github.com/astral-sh/ruff>`__・`ty <https://github.com/astral-sh/ty>`__ に *物申したい*
* pnpm（v12からRust実装）が面白い [#pnpm-v12-features]_

.. [#pnpm-v12-features] RustやPythonのパッケージ管理、Agent Skillsインストール

.. _sampleproject-rs: https://pypi.org/project/sampleproject-rs/

自作Pythonパッケージ `sampleproject-rs`_
======================================================================

* Pythonパッケージのサンプル `sampleproject <https://pypi.org/project/sampleproject/>`__ （チュートリアル例）
* Rust版sampleproject-rsを自作（**maturin**、**PyO3**）

.. code-block:: bash
   :caption: ``println!`` だけです

   $ uvx --from sampleproject-rs@0.2.3 sample
   Call your main application code here

.. revealjs-break::
   :notitle:

.. raw:: html

    <iframe width="800" height="480" src="https://ftnext.github.io/2025-slides/findy-techbaton/sampleproject-rs.html#/7/2"
        title="Rustで作るPythonパッケージの例 sampleproject-rs の紹介"></iframe>

8月のPyCon JP 2026より
======================================================================

.. raw:: html

    <iframe class="speakerdeck-iframe" style="border: 0px; background: padding-box rgba(0, 0, 0, 0.1); margin: 0px; padding: 0px; border-radius: 6px; box-shadow: rgba(0, 0, 0, 0.2) 0px 5px 40px; width: 100%; height: auto; aspect-ratio: 560 / 315;" frameborder="0" src="https://speakerdeck.com/player/3290bcc244f1413b95de881166ee86f6" title="PyO3 で既存 Python 評価器を Rust core 化する ー wasm-bindgen でブラウザにも配るための設計" allowfullscreen="true" allow="web-share" data-ratio="1.7777777777777777"></iframe>

Rust core化したsampleproject-rs v0.3
---------------------------------------------------

.. code-block:: text

   .
   ├── Cargo.toml  # workspace設定
   ├── pyproject.toml  # bindings-pyを見てPythonパッケージにする（maturin）
   ├── sample-core/  # Rust core
   │   ├── Cargo.toml
   │   └── src
   │       └── lib.rs
   ├── bindings-py/  # sample-coreに依存 + PyO3
   └── bindings-wasm/  # sample-core + wasm-bindgen

自作の小さなPythonパッケージをRust core化！
---------------------------------------------------

* 賢いAI（6 Solや6.1 Sol）に書き換えてもらい、私専用教材として参照
* 補完を切り、質問しまくって **写経** している
* GitHub ActionsはAIに任せた

学び1： ``String`` と ``&str`` の使い分け
======================================================================

.. code-block:: rust
    :caption: 返り値の ``String`` と ``&str`` は何が違う？

    pub fn extract_json(markdown: &str) -> Option<String> { }

    pub fn extract_json(markdown: &str) -> Option<&str> { }

引数の型は ``&str``
---------------------------------------------------

.. code-block:: rust
   :caption: `引数としての文字列スライス <https://doc.rust-jp.rs/book-ja/ch04-03-slices.html#%E5%BC%95%E6%95%B0%E3%81%A8%E3%81%97%E3%81%A6%E3%81%AE%E6%96%87%E5%AD%97%E5%88%97%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9>`__

   fn first_word(s: &str) -> &str {

.. code-block:: rust
   :caption: 「APIをより一般的で有益なものにできる」

   let word1 = first_word(&String::from("hello world"));  // Stringへの参照を渡す

   let word2 = first_word("hello world");   // 文字列リテラル（&str）を渡す

返り値： ``String`` も ``&str`` もある
-------------------------------------------------------------

* ``String``：新しい文字列を **作って返す**
* ``&str``：入力の **部分文字列** （参照して返す）

.. code-block:: rust

    pub fn to_snake_case(camel_case_str: &str) -> String { }

    pub fn extract_json(markdown: &str) -> Option<&str> { }

学び2： ``Result`` の扱い
======================================================================

.. code-block:: rust

    let input = args
        .input  // clap_stdin::FileOrStdin
        .contents()  // Result<T, StdinError>
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

.. https://docs.rs/clap-stdin/latest/clap_stdin/struct.FileOrStdin.html#method.contents

``Result`` は **消費** される
---------------------------------------------------

* ``Result`` の概念は発表を見聞きして理解していた（つもり）
* Rustで書いてみて消費に気づいた

    (略)動作対象である ``result`` を **消費** してしまう（『プログラミングRust 第2版』7.2）

.. _map_err(): https://doc.rust-lang.org/std/result/enum.Result.html#method.map_err

`map_err()`_ という選択
---------------------------------------------------

    leaving an ``Ok`` value untouched.

.. code-block:: rust

    let input = args.input.contents()
        .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

まとめ🌯Rustの練習を兼ねて、自作の小さなPythonパッケージをRustで書き直している話
================================================================================

* ``String`` は **新しい文字列** を作る、 ``&str`` は **部分文字列**
* ``Result`` はメソッド選択によっては **消費** されることに注意

ご清聴ありがとうございました！
---------------------------------------------------

参考：配布の経験とRust core化
======================================================================

* `2025年のLT：Rust製パッケージのCLIが動く理由 <https://ftnext.github.io/2025-slides/python-fukuoka/why-we-can-run-rust-package-cli#/1>`__
* `maturin generate-ciを参考にmacOS対応 <https://nikkie-ftnext.hatenablog.com/entry/maturin-generateci-github-support-macos-and-other-platform-build>`__
* `PyCon JP 2026のRust core化をsampleproject-rsへ <https://nikkie-ftnext.hatenablog.com/entry/pyconjp-2026-talk-rust-core-distribute-python-packge-and-wasm-apply-sampleproject-rs>`__

.. 本編外。maturinのbin bindingによるCLI配布と、PyO3によるPython拡張を区別する。

参考：文字列とResult
---------------------------------------------------

* `文字列処理のシグネチャ：&strかStringか <https://nikkie-ftnext.hatenablog.com/entry/which-choose-string-slice-or-string-in-rust-function-signature>`__
* `argparse FileTypeからclap-stdin FileOrStdinへ <https://nikkie-ftnext.hatenablog.com/entry/python-argparse-filetype-rust-clap-stdin-fileorstdin>`__
* `Rust公式：Resultのmap_err <https://doc.rust-lang.org/std/result/enum.Result.html#method.map_err>`__

.. 本編外。map_errとunwrapはselfを値で受け取る。
   Result自体は、中身のTとEがどちらもCopyの場合にはCopyになり得る。
