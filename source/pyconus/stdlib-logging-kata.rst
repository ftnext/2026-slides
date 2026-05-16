:ogp_title: Understanding Python's logging: Combine components like Lego blocks!
:ogp_event_name: pyconus
:ogp_slide_name: stdlib-logging-kata
:ogp_description: PyCon US 2026 (DAY3). Sorry for absence

.. _logging.basicConfig(): https://docs.python.org/3/library/logging.html#logging.basicConfig
.. _When to use logging (Basic logging tutorial): https://docs.python.org/3/howto/logging.html#when-to-use-logging

======================================================================================
Understanding Python's logging: Combine components like Lego blocks!
======================================================================================

.. 頭の見栄えをよくできないか、LLMに相談
    レゴブロックを交換できるとか

Presentation material QR code
==============================

.. image:: ../_static//pyconus/pyconus-slide-qr.png

Thank you Myles Scolnick-san [#qr-generator-marimo-link]_ (`DAY1 talk <https://us.pycon.org/2026/schedule/presentation/78/>`__)

.. [#qr-generator-marimo-link] https://marimo.app/?mode=read&embedded=true&slug=tep83k

Understanding Python's logging: Combine components like Lego blocks!
======================================================================================

:Event: PyCon US 2026
:Presented: 2026/05/17 nikkie

Can you use Python's stdlib ``logging`` with **confidence**?
----------------------------------------------------------------------

Takeaway: Let's understand the ``logging`` module!
------------------------------------------------------------

.. Takeaways
    - Understand components like *Logger* and *Handler*
    - Understand how to **combine** components for logging

* components like *loggers* and *handlers*
* how to **combine** components for logging

Composable like Lego blocks (IMO)
--------------------------------------------------

.. "Simple" doesn't mean easy—it means combining simple things to build complex systems (like Lego blocks)

* Simplicity in Python Zen [#zen-of-python-simple-en]_
* "Simple" doesn't mean easy; many components
* Like Lego: **combine simple pieces** to build systems

.. レゴブロックの図を使うかも https://ftnext.github.io/2024-slides/ooc/software-lessons.html#/6

.. [#zen-of-python-simple-en] *Simple is better than complex.* (`The Zen of Python <https://peps.python.org/pep-0020/>`__)

Who this talk is for
--------------------------------------------------

.. ## Target Audience
    - Prerequisite: **Experience implementing logging in Python**
    - Experience with the logging module is not required
    - Perfect for those thinking "I don't quite understand the logging module..."

* Assumption: you have **implemented logging in Python** before
* Experience with the stdlib ``logging`` is not required
* If you feel "I still don't quite get the logging module...", this talk is exactly for you!

お前、誰よ？ [#lets-use-omae-dareyo]_ (Self-Introduction) 1/2
----------------------------------------------------------------------

.. As a machine learning engineer working with LLMs and NLP, I want to log all LLM inputs/outputs to understand everything thoroughly.  
    Through developing LLM applications, I've gained deep insights into Python logging patterns.

* nikkie / :fab:`github` `@ftnext <https://github.com/ftnext>`__ / 9 years with Python
* Machine learning engineer🇯🇵🗼, LLMs, Develop AI Agent
* In LLM application development, I want to **log all LLM inputs/outputs** to understand everything thoroughly

.. image:: ../_static/uzabase-white-logo.png
    :target: https://uzabaseglobal.com/

.. [#lets-use-omae-dareyo] means "Who are you?". A common phrase used in Japanese communities to introduce yourself.

お前、誰よ？ (Self-Introduction) 2/2
--------------------------------------------------

.. This talk is based on my blog post

* Everyday `blogging (in Japanese) <https://nikkie-ftnext.hatenablog.com/>`__ over 1000 days (articles referenced in slide)
* `SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ (9k star) maintainer
* Codex Ambassador (Tokyo)
* Volunteer staff of the monthly `Start Python Club <https://startpython.connpass.com/>`__ (online)

Five chapters
--------------------------------------------------

1. Components of the ``logging`` module
2. How is a logger's level determined?
3. Let's log to the root logger: *Propagation* (**combined logging**)
4. Dealing with problematic logging in real-world libraries
5. Gleanings

.. include:: en/logging-components.rst.txt

.. include:: en/logger-level.rst.txt

.. include:: en/propagate-to-root-logger.rst.txt

.. include:: en/resistance-against-real-world-logging.rst.txt

.. include:: en/gleanings.rst.txt

🌯Back to the first question: can you use Python's stdlib ``logging`` with confidence?
================================================================================================

* A logger's ``NOTSET`` level: use it with **the same effective level as an ancestor logger**
* Propagation to the root logger: **output through the root logger's handlers**

Summary🌯: Understanding Python's logging: Combine components like Lego blocks!
------------------------------------------------------------------------------------------------

* Introduced 1 **pattern** derived from ``NOTSET`` and ``propagate``: logging through the root logger
* The **library user** logs in the **format and destination** they want

🌯To **library authors**: "should only call loggers"
------------------------------------------------------------

* You only want to **record events**
* You do not care about log format or destination, assuming users configure those freely
* 👉"Do not touch the root logger in a library"

Even in **local scripts**, not only libraries like HTTPXYZ
------------------------------------------------------------

.. code-block:: python
    :caption: Configure the root logger in one place; inside functions, only call loggers

    def awesome():
        # logger call only (recording an event)
    def fabulous():
        # logger call only (recording an event)
    def main():
        logging.basicConfig(...)  # level, handlers, and formatters on the root logger
        awesome()
        fabulous()

Thank you!
--------------------------------------------------

Happy Python Logging♪

Appendix
======================================================================

Earlier talks and posts this talk builds on
--------------------------------------------------

* My blog post `Pythonで標準ライブラリloggingを使って自作ライブラリの中でロギングしたい未来の私へ <https://nikkie-ftnext.hatenablog.com/entry/python-logging-developing-library-take-advantage-nullhandler-and-propagate>`__
* PyCon mini Shizuoka 2024 continue in February: `ライブラリ開発者に贈る「ロギングで NullHandler 以外はいけません」 <https://ftnext.github.io/2025-slides/pyconshizu/logging-with-nullhandler.html#/1>`__

Thanks: attakei [#thanks-footnotes-en]_
------------------------------------------------------------

This deck is built with attakei's `sphinx-revealjs <https://pypi.org/project/sphinx-revealjs/>`__ plus these **extensions I made**

* My signature work: `sphinx-new-tab-link <https://pypi.org/project/sphinx-new-tab-link/>`__
* `sphinx-revealjs-copycode <https://pypi.org/project/sphinx-revealjs-copycode/>`__
* `sphinx-revealjs-ext-codeblock <https://pypi.org/project/sphinx-revealjs-ext-codeblock/>`__

.. [#thanks-footnotes-en] Thank you very much for adding footnote support!

EOF
===
