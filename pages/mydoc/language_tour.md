---
title: Botlang basics
sidebar: mydoc_sidebar
permalink: language_tour.html
summary: This chapter will walk you through the language syntax and semantics in a step-by-step fashion, with plenty of examples.
folder: mydoc
---

## Interacting with Botlang

Botcenter provides a web environment to interact with Botlang, create bots, and test them. It comes with an editor and an interactive console to communicate with your bots.

You can access the IDE by clicking on the link in the top menu. To execute code, click the "run" button or press Ctrl+Enter on your keyboard.

## Values

Botlang's basic values are numbers, booleans, strings, lists, dictionaries and functions. There's also a special value for bot results, but we will cover that in the next chapter.

### Simple values

Numbers are written in the usual way:

<pre>
<code class="language-scheme">2
3.1415</code>
</pre>

Botlang provides many mathematical operations for number manipulation. As every other operation in the language, they are applied using a fully parenthesized [prefix notation](https://en.wikipedia.org/wiki/Polish_notation#Computer_programming):

<pre>
<code class="language-scheme">(+ 2 3)
(* 3 101.33)
(sqrt 2)</code>
</pre>

Booleans are writen as **#t** for true and **#f** for false:

<pre>
<code class="language-scheme">(or #t #f)</code>
</pre>

Strings are written between double quotation marks. Any Unicode character can be used within a string, except for an unescaped double quote. To include a double quotation mark in a string it must be preceded by a backslash.

<pre>
<code class="language-scheme">"Holi"
"Diego \"Doge\" Orellana"
"λx:(μα.α→α).xx"</code>
</pre>

As in many other languages, **\n** produces a newline when used within a string. Botlang comes with handy functions for string manipulation, such as **append** which provides concatenation. To concatenate a number with a string it is necessary to convert it to a string first, which can be done with the **str** function.

<pre>
<code class="language-scheme">(append
    "I'm a kawaii string, and I can include calculations. Look:\n"
    "2 + 2 = "
    (str (+ 2 2))
    "\nTold you, I'm great :)"
)</code>
</pre>

### Lists

A list is a sequence of values. Any value can be stored in a list (including functions), and a list can hold values of different types.

There are at least three ways to build a list.

* With the **list** function:
    <pre><code class="language-scheme">(list 1 2 3 4)</code></pre>
    The function accepts any number of arguments, each of which corresponds to a value that will be stored in the list, in that same order.
    
* Through the **cons** operator:
    <pre><code class="language-scheme">(cons 1 (list 2 3))</code></pre>
    This function accepts two arguments. If the second one is a list, the first one will be added to the beginning of it. If it's not, then a list of two elements (the arguments) will be returned.
    
* From the **quote** syntax:
    <pre><code class="language-scheme">'(1 2 3 4)</code></pre>
    This creates an explicit list, in which each element corresponds to what is explicitly written. This means that no evaluation will be performed on the list's elements, so identifiers will be only symbols.
    
    For example, the following snippet produces a list of three symbols: **+**, **2** and **3**.
    <pre><code class="language-scheme">'(+ 2 3)</code></pre>

### Dictionaries

### Functions

## Definitions and Expressions

### Identifiers

### Function Calls

### Conditionals

## Lists, Iteration and Recursion

### Predefined List Loops

### List Iteration from Scratch

### Tail Recursion
