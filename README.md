# What is jexpr?

A very rough and ready command line tool written in Python that spits out a list of expressions found in a piece of Japanese text. All output is displayed in the terminal. The tool:

- Allows you to input either a URL or a file
- Highlights the snippet where the expression is found

# Usage Examples

_(Ensure you have `requests` and `lxml` installed)_

```bash
python3 jexpr.py -u https://jaguchi.com/blog/2019/12/japanese-is-hard/
```

or alternatively, with the `-f` switch

```bash
python3 jexpr.py -f data_raw/input_text/jaguchi.txt
```

If you make `jexpr.py` an executable, you can run it directly. Although, just make sure you're providing a full path to the input file if you're using the `-f` switch.

```bash
chmod +x jexpr.py
./jexpr.py -u https://jaguchi.com/blog/2019/12/japanese-is-hard/
```

# Attributions

1. All expression data is from [JMdict](http://www.edrdg.org/jmdict/edict_doc.html).
2. The example in `data_raw/input_text/jaguchi.txt` is from a [blog post](https://jaguchi.com/blog/2019/12/japanese-is-hard/) by Lena Morita that inspired this tool in the first place.


# What problem is this trying to solve?

When reading Japanese, it is sometimes quite hard to distinguish expressions from just words put together. A lot of times a bunch of words just don't make sense when put together but the entity as a whole is an expression that is commonly used.

An example of this is "ピンと来る" from [this](https://qiita.com/maskedw/items/e73df32007934e75d9e3) blog post. You can't really tell it's an expression unless you look up the entire phrase. Other examples are "ゼロから" and "いつまで経っても" from [another](https://jaguchi.com/blog/2019/12/japanese-is-hard/) blog post.

Some expressions are more intuitive than others. For example, "いつまで経っても" definitely is easier to understand than "ピンと来る" but the idea is to try to identify these at the outset without having to 'work out' what they actually mean. _(Yes, of course they're fun to work out, but a lot of times you don't even know what you need to be working out.)_

Moreover, it would be nice to inculcate a habit of seeing these expressions for what they are and use them as so. More generally, the idea is to appreciate these idioms/expressions and use them more often in writing or daily conversation.


# Caveats

Currently, searches are performed by simply looping through all the expressions and trying to find any occurrences of these expressions in the text. While this does not have drastic repercussions at the moment (since there are only about 11,600 total expressions and around 28,000 readings), things can slow down very quickly.

Another important limitation is the lack of any stemming. For example, "なって" is not stemmed to "なる". This has the unintended consequence of missing out on about 10 - 20 percent of all expressions. In addition, the relevant kanji is not added to expressions written purely in hiragana (however, a fairly exhaustive list of readings for each expression is usually sufficient to snuff out most of these cases).