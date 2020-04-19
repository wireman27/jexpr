# What problem are we trying to solve?

When reading a Japanese text, it is quite hard to be able to distinguish expressions from just words put together. A lot of times a bunch of words just don't make sense when put together but are actually an expression when consulted with jisho.org (which itself gets its expression data from JMDict).

An example of this is "ピンと来る" from [this](https://qiita.com/maskedw/items/e73df32007934e75d9e3) blog post. You can't really tell it's an expression unless you look up the entire phrase. Other examples are "ゼロから" and "いつまで経っても" from [another](https://jaguchi.com/blog/2019/12/japanese-is-hard/) blog post.

Some expressions are more intuitive to understand than others. For example, "いつまで経っても" definitely is easier to understand than "ピンと来る" but the idea is to inculcate a habit of seeing these expressions for what they are and use them as so. More generally, the idea is to appreciate these idioms/expressions and use them more often in writing or daily conversation.

# What are we building?

A command line tool in Python that spits out a list of expressions found in a piece of text. Salient features:

- Highlights the snippet where the expression is found
- Allows you to input either a URL, a file or a string of text

# Shell Prerequisites

- Must have shebang and must be added to $PATH
- 

# Steps to get there

## Basic

1. Write a script to parse out the JMDict file to only capture expressions. (Completed)
2. Do some preliminary indexing of this data into Solr (The output of 1 is probably going to be a large XML file so some custom logic will have to be written in Solr to be able to parse out each node of the tree as a document in Solr) (Completed)
3. Sample text will likely be large paragraphs. Write a script to make the search query more manageable (possibly split on full-stops and then search each sentence individually) 

## Intermediate


## Advanced


# Toolbox

- Apache Solr
- JMDict
- Falcon

# Notes

- In Solr, ensure that the field type is `text_ja` for all fields that contain Japanese text. This field type only applies Japanese specific filters at index time and this is okay. 
- What we might need to do is check if each of the 11,500 expressions 'fit in' into the text somehow and return only those expressions. It's almost like our expressions collection has 'more knowledge' that our humble MeCab morphological analyzer doesn't.
- Single letter expressions don't count. Too much noise.