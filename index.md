---
title: "Botlang: a bot-scripting language"
keywords: purpose language execution model runtime introduction
sidebar: mydoc_sidebar
permalink: index.html
summary: Botlang is an embedded functional domain-specific language (DSL) designed for scripting flexible and powerful interactive chat bots.
---

## Purpose

The purpose of Botlang is to provide a way to easily program interactive bots which respond to user messages, and to be able to deploy them in a live production environment. Specifically, Botlang aims to satisfy the following goals:

1. Allow the creation of bots with highly complex logic.
2. Allow interaction between a bot and external web services.
3. Be embeddable in a host Python application (especially, but not limited to, BotCenter).
4. Allow running arbitrary Botlang programs without touching the underlying host application.
4. Be able to resume an execution a long time after it was paused (waiting for a message to arrive).

## The language

As a way to accomplish the aforementioned goals, Botlang was born as an expressive functional and dynamically typed domain-specific language, with syntax and semantics inspired by [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)).

Botlang is:

* **Concise:** it provides a very simple and expressive syntax.
* **Flexible:** bots are functions, and functions are [first-class citizens](https://en.wikipedia.org/wiki/First-class_citizen).
* **Web-friendly:** it provides a simple API for dealing with HTTP requests and responses. JSON and XML are supported out-of-the-box.

These language features satisfy the first two goals we proposed. The third, fourth, and fifth ones are covered by the execution model.

## The execution model

Botlang code is executed by an interpreter which runs on top of Python, and can be imported as a library. This allows the inclusion of the language in any Python application, which can then execute Botlang code by passing a string to an instance of the runtime system, and then receive the computed result from it.

The Botlang library also allows the host application to expose its own functions to the language runtime instance, thus extending the latter's functionality. Each bot runs on its own runtime instance.

The fifth goal is achieved by means of an execution reconstruction mechanism:

1. Each bot node returns a special kind of value which contains a message to send to the user, a data dictionary with information gathered by the bot, and a lightweight execution state object.
2. The execution state object consists of only an integer and an array which holds only strings and numbers, hence it can be easily stored by the host application.
3. To resume an execution, the host application must provide an execution state object and a bot code string to a runtime instance. The bot will continue from the point it was left off.

## What Botlang IS NOT made for

As a domain-specific-language, Botlang was designed around the goals it aims to accomplish. Although it is general enough to be used in other domains, taking it too far would be a bad idea.

Botlang is bad at:

* **Intense calculations:** as an interpreted language running on top of Python's interpreter, there is a significant overhead in each calculation. If you need to perform expensive computations as part of your bot's logic, you should do that in an external function that you expose into your Botlang runtime instance.
* **Concurrency:** don't even try. If you need concurrency as part of your bot's logic, you are doing something wrong.