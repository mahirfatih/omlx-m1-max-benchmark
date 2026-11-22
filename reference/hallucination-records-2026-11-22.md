# Hallucination — the questions and the answers

**Date:** 2026-11-22. 102 languages × 2 probes. Both tables are the raw record behind the summary in [`../evidence/hallucination-2026-11-22.md`](../evidence/hallucination-2026-11-22.md); nothing is aggregated away.

**What was asked, once per batch of probes:**

> Given a list of programming-language API names, say which are real and which are invented, with a confidence in [0,1] for each. Answer as JSON.

Each language contributes two names: one **genuine** documented API, and one **fabricated twin** (the same shape with a small, plausible change). The model never sees which is which.

## Who got what wrong

| Model | Answered | Hallucination (fake → "real") | False alarm (real → "fake") | Misses |
| :--- | ---: | ---: | ---: | ---: |
| `GLM-4.7-Flash-8bit` (`glm47`) | 165/204 | **2%** (2/85) | 2% (2/80) | 4 |
| `GLM-4.7-Flash-8bit` (`glm47-hot`) | 165/204 | **2%** (2/85) | 2% (2/80) | 4 |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear`) | 204/204 | **0%** (0/102) | 1% (1/102) | 1 |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear-hot`) | 204/204 | **0%** (0/102) | 1% (1/102) | 1 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling`) | 188/204 | **0%** (0/94) | 0% (0/94) | 0 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-hot`) | 188/204 | **0%** (0/94) | 0% (0/94) | 0 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp`) | 204/204 | **0%** (0/102) | 0% (0/102) | 0 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp-hot`) | 204/204 | **0%** (0/102) | 0% (0/102) | 0 |

**4 hallucinations in this run** — a fabricated name called real — against 6 false alarms, a real API called fake. The miss table below names every one.

## Every miss, with the name and the confidence

| Model | Direction | Language | Name the model judged | Stated confidence |
| :--- | :--- | :--- | :--- | ---: |
| `GLM-4.7-Flash (glm47)` | **fake → "real"** (hallucination) | `matlab` | `zerosx` | 1.00 |
| `GLM-4.7-Flash (glm47)` | **fake → "real"** (hallucination) | `objective-c` | `NSArrayx` | — |
| `GLM-4.7-Flash (glm47)` | real → "fake" (false alarm) | `purescript` | `map` | 0.90 |
| `GLM-4.7-Flash (glm47)` | real → "fake" (false alarm) | `mint` | `component` | 0.90 |
| `GLM-4.7-Flash (glm47-hot)` | **fake → "real"** (hallucination) | `matlab` | `zerosx` | 1.00 |
| `GLM-4.7-Flash (glm47-hot)` | **fake → "real"** (hallucination) | `objective-c` | `NSArrayx` | — |
| `GLM-4.7-Flash (glm47-hot)` | real → "fake" (false alarm) | `purescript` | `map` | 0.90 |
| `GLM-4.7-Flash (glm47-hot)` | real → "fake" (false alarm) | `mint` | `component` | 0.90 |
| `Kimi-Linear-48B-A3B-Instruct (kimi-linear)` | real → "fake" (false alarm) | `pascal` | `writeln` | 1.00 |
| `Kimi-Linear-48B-A3B-Instruct (kimi-linear-hot)` | real → "fake" (false alarm) | `pascal` | `writeln` | 1.00 |

## The full record, per model

`expected` is whether the name is real; `got_real` is whether the model said it is. They agree unless the row is a miss. `conf` is the confidence the model stated, or `—` when it did not state one.

### `GLM-4.7-Flash (glm47)`

165/204 answered, 4 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 1.00 | ✅ |
| `abap` | `WRITE` | yes | yes | 1.00 | ✅ |
| `actionscript` | `tracex` | no | no | 1.00 | ✅ |
| `actionscript` | `trace` | yes | yes | 1.00 | ✅ |
| `ada` | `Put_Linex` | no | no | 1.00 | ✅ |
| `ada` | `Put_Line` | yes | yes | 1.00 | ✅ |
| `apex` | `Database.queryx` | no | no | 1.00 | ✅ |
| `apex` | `Database.query` | yes | yes | 1.00 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `bash` | `readx` | no | no | 1.00 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 0.90 | ✅ |
| `blade` | `@foreach` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 0.10 | ✅ |
| `cairo` | `felt252` | yes | yes | 1.00 | ✅ |
| `clojure` | `mapx` | no | no | 0.50 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 1.00 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 1.00 | ✅ |
| `coffeescript` | `->x` | no | no | 1.00 | ✅ |
| `coffeescript` | `->` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.00 | ✅ |
| `crystal` | `Array#map` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.map` | yes | yes | 1.00 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 1.00 | ✅ |
| `elm` | `List.mapx` | no | no | 1.00 | ✅ |
| `elm` | `List.map` | yes | yes | 1.00 | ✅ |
| `erb` | `<% %>x` | no | no | 1.00 | ✅ |
| `erb` | `<% %>` | yes | yes | 1.00 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.50 | ✅ |
| `erlang` | `lists:map` | yes | yes | 1.00 | ✅ |
| `fortran` | `allocatex` | no | no | 1.00 | ✅ |
| `fortran` | `allocate` | yes | yes | 1.00 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.50 | ✅ |
| `fsharp` | `List.map` | yes | yes | 1.00 | ✅ |
| `gdscript` | `printx` | no | no | 1.00 | ✅ |
| `gdscript` | `print` | yes | yes | 1.00 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.00 | ✅ |
| `gleam` | `list.map` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.10 | ✅ |
| `graphviz` | `digraph` | yes | yes | 1.00 | ✅ |
| `groovy` | `eachx` | no | no | 1.00 | ✅ |
| `groovy` | `each` | yes | yes | 1.00 | ✅ |
| `haml` | `%divx` | no | no | 0.90 | ✅ |
| `haml` | `%div` | yes | yes | 1.00 | ✅ |
| `haskell` | `mapx` | no | no | 1.00 | ✅ |
| `html` | `<a hrefx>` | no | no | 1.00 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 1.00 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 1.00 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 1.00 | ✅ |
| `jinja` | `{% forx %}` | no | no | 1.00 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `json` | `nullx` | no | no | 1.00 | ✅ |
| `julia` | `pushx!` | no | no | 0.50 | ✅ |
| `julia` | `push!` | yes | yes | 1.00 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 1.00 | ✅ |
| `latex` | `\sectionx` | no | no | 1.00 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.90 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 1.00 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.50 | ✅ |
| `lisp` | `mapcar` | yes | yes | 1.00 | ✅ |
| `livescript` | `->x` | no | no | 1.00 | ✅ |
| `livescript` | `->` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | yes | 1.00 | ❌ |
| `mermaid` | `graph TDx` | no | no | 0.10 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | 0.90 | ✅ |
| `mint` | `component` | yes | no | 0.90 | ❌ |
| `mojo` | `fnx` | no | no | 0.00 | ✅ |
| `mojo` | `fn` | yes | yes | 1.00 | ✅ |
| `move` | `vectorx` | no | no | 0.10 | ✅ |
| `move` | `vector` | yes | yes | 1.00 | ✅ |
| `nim` | `seqx` | no | no | 0.00 | ✅ |
| `nim` | `seq` | yes | yes | 1.00 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 1.00 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `objective-c` | `NSArrayx` | no | yes | — | ❌ |
| `ocaml` | `List.mapx` | no | no | 0.50 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.00 | ✅ |
| `odin` | `fmt.println` | yes | yes | 1.00 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.10 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 1.00 | ✅ |
| `pascal` | `writelnx` | no | no | 1.00 | ✅ |
| `pascal` | `writeln` | yes | yes | 1.00 | ✅ |
| `perl` | `pushx` | no | no | 1.00 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.10 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 1.00 | ✅ |
| `prolog` | `findallx` | no | no | 0.50 | ✅ |
| `prolog` | `findall` | yes | yes | 1.00 | ✅ |
| `purescript` | `mapx` | no | no | 0.90 | ✅ |
| `purescript` | `map` | yes | no | 0.90 | ❌ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 1.00 | ✅ |
| `r` | `data.framex` | no | no | 0.10 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.90 | ✅ |
| `reasonml` | `List.map` | yes | yes | 1.00 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.90 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 1.00 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.map` | yes | yes | 1.00 | ✅ |
| `scheme` | `mapx` | no | no | 0.50 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 0.90 | ✅ |
| `slim` | `.class` | yes | yes | 1.00 | ✅ |
| `smalltalk` | `dox:` | no | no | 1.00 | ✅ |
| `smalltalk` | `do:` | yes | yes | 1.00 | ✅ |
| `solidity` | `mappingx` | no | no | 1.00 | ✅ |
| `solidity` | `mapping` | yes | yes | 1.00 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 0.10 | ✅ |
| `tex` | `\def` | yes | yes | 1.00 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `toml` | `[table]` | yes | yes | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | 1.00 | ✅ |
| `tsql` | `TOP` | yes | yes | 1.00 | ✅ |
| `twig` | `{% forx %}` | no | no | 1.00 | ✅ |
| `twig` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 0.10 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | 0.00 | ✅ |
| `v` | `println` | yes | yes | 1.00 | ✅ |
| `vba` | `MsgBoxx` | no | no | 1.00 | ✅ |
| `vba` | `MsgBox` | yes | yes | 1.00 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 1.00 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 1.00 | ✅ |
| `vhdl` | `processx` | no | no | 1.00 | ✅ |
| `vhdl` | `process` | yes | yes | 1.00 | ✅ |
| `vue` | `<template>` | yes | yes | 1.00 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |

### `GLM-4.7-Flash (glm47-hot)`

165/204 answered, 4 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 1.00 | ✅ |
| `abap` | `WRITE` | yes | yes | 1.00 | ✅ |
| `actionscript` | `tracex` | no | no | 1.00 | ✅ |
| `actionscript` | `trace` | yes | yes | 1.00 | ✅ |
| `ada` | `Put_Linex` | no | no | 1.00 | ✅ |
| `ada` | `Put_Line` | yes | yes | 1.00 | ✅ |
| `apex` | `Database.queryx` | no | no | 1.00 | ✅ |
| `apex` | `Database.query` | yes | yes | 1.00 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `bash` | `readx` | no | no | 1.00 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 0.90 | ✅ |
| `blade` | `@foreach` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 0.10 | ✅ |
| `cairo` | `felt252` | yes | yes | 1.00 | ✅ |
| `clojure` | `mapx` | no | no | 0.50 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 1.00 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 1.00 | ✅ |
| `coffeescript` | `->x` | no | no | 1.00 | ✅ |
| `coffeescript` | `->` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.00 | ✅ |
| `crystal` | `Array#map` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.map` | yes | yes | 1.00 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 1.00 | ✅ |
| `elm` | `List.mapx` | no | no | 1.00 | ✅ |
| `elm` | `List.map` | yes | yes | 1.00 | ✅ |
| `erb` | `<% %>x` | no | no | 1.00 | ✅ |
| `erb` | `<% %>` | yes | yes | 1.00 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.50 | ✅ |
| `erlang` | `lists:map` | yes | yes | 1.00 | ✅ |
| `fortran` | `allocatex` | no | no | 1.00 | ✅ |
| `fortran` | `allocate` | yes | yes | 1.00 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.50 | ✅ |
| `fsharp` | `List.map` | yes | yes | 1.00 | ✅ |
| `gdscript` | `printx` | no | no | 1.00 | ✅ |
| `gdscript` | `print` | yes | yes | 1.00 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.00 | ✅ |
| `gleam` | `list.map` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.10 | ✅ |
| `graphviz` | `digraph` | yes | yes | 1.00 | ✅ |
| `groovy` | `eachx` | no | no | 1.00 | ✅ |
| `groovy` | `each` | yes | yes | 1.00 | ✅ |
| `haml` | `%divx` | no | no | 0.90 | ✅ |
| `haml` | `%div` | yes | yes | 1.00 | ✅ |
| `haskell` | `mapx` | no | no | 1.00 | ✅ |
| `html` | `<a hrefx>` | no | no | 1.00 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 1.00 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 1.00 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 1.00 | ✅ |
| `jinja` | `{% forx %}` | no | no | 1.00 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `json` | `nullx` | no | no | 1.00 | ✅ |
| `julia` | `pushx!` | no | no | 0.50 | ✅ |
| `julia` | `push!` | yes | yes | 1.00 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 1.00 | ✅ |
| `latex` | `\sectionx` | no | no | 1.00 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.90 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 1.00 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.50 | ✅ |
| `lisp` | `mapcar` | yes | yes | 1.00 | ✅ |
| `livescript` | `->x` | no | no | 1.00 | ✅ |
| `livescript` | `->` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | yes | 1.00 | ❌ |
| `mermaid` | `graph TDx` | no | no | 0.10 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | 0.90 | ✅ |
| `mint` | `component` | yes | no | 0.90 | ❌ |
| `mojo` | `fnx` | no | no | 0.00 | ✅ |
| `mojo` | `fn` | yes | yes | 1.00 | ✅ |
| `move` | `vectorx` | no | no | 0.10 | ✅ |
| `move` | `vector` | yes | yes | 1.00 | ✅ |
| `nim` | `seqx` | no | no | 0.00 | ✅ |
| `nim` | `seq` | yes | yes | 1.00 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 1.00 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `objective-c` | `NSArrayx` | no | yes | — | ❌ |
| `ocaml` | `List.mapx` | no | no | 0.50 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.00 | ✅ |
| `odin` | `fmt.println` | yes | yes | 1.00 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.10 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 1.00 | ✅ |
| `pascal` | `writelnx` | no | no | 1.00 | ✅ |
| `pascal` | `writeln` | yes | yes | 1.00 | ✅ |
| `perl` | `pushx` | no | no | 1.00 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.10 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 1.00 | ✅ |
| `prolog` | `findallx` | no | no | 0.50 | ✅ |
| `prolog` | `findall` | yes | yes | 1.00 | ✅ |
| `purescript` | `mapx` | no | no | 0.90 | ✅ |
| `purescript` | `map` | yes | no | 0.90 | ❌ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 1.00 | ✅ |
| `r` | `data.framex` | no | no | 0.10 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.90 | ✅ |
| `reasonml` | `List.map` | yes | yes | 1.00 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.90 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 1.00 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.map` | yes | yes | 1.00 | ✅ |
| `scheme` | `mapx` | no | no | 0.50 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 0.90 | ✅ |
| `slim` | `.class` | yes | yes | 1.00 | ✅ |
| `smalltalk` | `dox:` | no | no | 1.00 | ✅ |
| `smalltalk` | `do:` | yes | yes | 1.00 | ✅ |
| `solidity` | `mappingx` | no | no | 1.00 | ✅ |
| `solidity` | `mapping` | yes | yes | 1.00 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 0.10 | ✅ |
| `tex` | `\def` | yes | yes | 1.00 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `toml` | `[table]` | yes | yes | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | 1.00 | ✅ |
| `tsql` | `TOP` | yes | yes | 1.00 | ✅ |
| `twig` | `{% forx %}` | no | no | 1.00 | ✅ |
| `twig` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 0.10 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | 0.00 | ✅ |
| `v` | `println` | yes | yes | 1.00 | ✅ |
| `vba` | `MsgBoxx` | no | no | 1.00 | ✅ |
| `vba` | `MsgBox` | yes | yes | 1.00 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 1.00 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 1.00 | ✅ |
| `vhdl` | `processx` | no | no | 1.00 | ✅ |
| `vhdl` | `process` | yes | yes | 1.00 | ✅ |
| `vue` | `<template>` | yes | yes | 1.00 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |

### `Kimi-Linear-48B-A3B-Instruct (kimi-linear)`

204/204 answered, 1 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.90 | ✅ |
| `abap` | `WRITE` | yes | yes | 1.00 | ✅ |
| `actionscript` | `tracex` | no | no | 1.00 | ✅ |
| `actionscript` | `trace` | yes | yes | 1.00 | ✅ |
| `ada` | `Put_Linex` | no | no | 1.00 | ✅ |
| `ada` | `Put_Line` | yes | yes | 1.00 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.90 | ✅ |
| `apex` | `Database.query` | yes | yes | 1.00 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `assembly` | `movx` | no | no | 1.00 | ✅ |
| `assembly` | `mov` | yes | yes | 1.00 | ✅ |
| `bash` | `readx` | no | no | 1.00 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 1.00 | ✅ |
| `blade` | `@foreach` | yes | yes | 1.00 | ✅ |
| `c` | `memcpyx` | no | no | 1.00 | ✅ |
| `c` | `memcpy` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 1.00 | ✅ |
| `cairo` | `felt252` | yes | yes | 1.00 | ✅ |
| `clojure` | `mapx` | no | no | 1.00 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 1.00 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 1.00 | ✅ |
| `coffeescript` | `->x` | no | no | 1.00 | ✅ |
| `coffeescript` | `->` | yes | yes | 1.00 | ✅ |
| `cpp` | `std::vectorx` | no | no | 1.00 | ✅ |
| `cpp` | `std::vector` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 1.00 | ✅ |
| `crystal` | `Array#map` | yes | yes | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.mapx` | no | no | 1.00 | ✅ |
| `dart` | `List.map` | yes | yes | 1.00 | ✅ |
| `ejs` | `<% %>x` | no | no | 1.00 | ✅ |
| `ejs` | `<% %>` | yes | yes | 1.00 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 1.00 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 1.00 | ✅ |
| `elm` | `List.mapx` | no | no | 0.90 | ✅ |
| `elm` | `List.map` | yes | yes | 1.00 | ✅ |
| `erb` | `<% %>x` | no | no | 1.00 | ✅ |
| `erb` | `<% %>` | yes | yes | 1.00 | ✅ |
| `erlang` | `lists:mapx` | no | no | 1.00 | ✅ |
| `erlang` | `lists:map` | yes | yes | 1.00 | ✅ |
| `fortran` | `allocatex` | no | no | 1.00 | ✅ |
| `fortran` | `allocate` | yes | yes | 1.00 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 1.00 | ✅ |
| `fsharp` | `List.map` | yes | yes | 1.00 | ✅ |
| `gdscript` | `printx` | no | no | 0.90 | ✅ |
| `gdscript` | `print` | yes | yes | 1.00 | ✅ |
| `gleam` | `list.mapx` | no | no | 1.00 | ✅ |
| `gleam` | `list.map` | yes | yes | 1.00 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 1.00 | ✅ |
| `go` | `fmt.Println` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 1.00 | ✅ |
| `graphviz` | `digraph` | yes | yes | 1.00 | ✅ |
| `groovy` | `eachx` | no | no | 1.00 | ✅ |
| `groovy` | `each` | yes | yes | 1.00 | ✅ |
| `haml` | `%divx` | no | no | 1.00 | ✅ |
| `haml` | `%div` | yes | yes | 1.00 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 1.00 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 1.00 | ✅ |
| `haskell` | `mapx` | no | no | 1.00 | ✅ |
| `haskell` | `map` | yes | yes | 1.00 | ✅ |
| `html` | `<a hrefx>` | no | no | 1.00 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 1.00 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 1.00 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 1.00 | ✅ |
| `jinja` | `{% forx %}` | no | no | 1.00 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `json` | `nullx` | no | no | 1.00 | ✅ |
| `json` | `null` | yes | yes | 1.00 | ✅ |
| `jsx` | `React.createElementx` | no | no | 1.00 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 1.00 | ✅ |
| `julia` | `pushx!` | no | no | 1.00 | ✅ |
| `julia` | `push!` | yes | yes | 1.00 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 1.00 | ✅ |
| `latex` | `\sectionx` | no | no | 1.00 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 1.00 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 1.00 | ✅ |
| `lisp` | `mapcarx` | no | no | 1.00 | ✅ |
| `lisp` | `mapcar` | yes | yes | 1.00 | ✅ |
| `livescript` | `->x` | no | no | 1.00 | ✅ |
| `livescript` | `->` | yes | yes | 1.00 | ✅ |
| `lua` | `table.insertx` | no | no | 1.00 | ✅ |
| `lua` | `table.insert` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 1.00 | ✅ |
| `matlab` | `zeros` | yes | yes | 1.00 | ✅ |
| `mermaid` | `graph TDx` | no | no | 1.00 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | 1.00 | ✅ |
| `mint` | `component` | yes | yes | 1.00 | ✅ |
| `mojo` | `fnx` | no | no | 1.00 | ✅ |
| `mojo` | `fn` | yes | yes | 1.00 | ✅ |
| `move` | `vectorx` | no | no | 1.00 | ✅ |
| `move` | `vector` | yes | yes | 1.00 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 1.00 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 1.00 | ✅ |
| `nim` | `seqx` | no | no | 1.00 | ✅ |
| `nim` | `seq` | yes | yes | 1.00 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 1.00 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 1.00 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 1.00 | ✅ |
| `ocaml` | `List.mapx` | no | no | 1.00 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 1.00 | ✅ |
| `odin` | `fmt.println` | yes | yes | 1.00 | ✅ |
| `orgmode` | `* Headingx` | no | no | 1.00 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 1.00 | ✅ |
| `pascal` | `writelnx` | no | no | 1.00 | ✅ |
| `pascal` | `writeln` | yes | no | 1.00 | ❌ |
| `perl` | `pushx` | no | no | 1.00 | ✅ |
| `perl` | `push` | yes | yes | 1.00 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 1.00 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.90 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 1.00 | ✅ |
| `prolog` | `findallx` | no | no | 1.00 | ✅ |
| `prolog` | `findall` | yes | yes | 1.00 | ✅ |
| `pug` | `extendsx` | no | no | 1.00 | ✅ |
| `pug` | `extends` | yes | yes | 1.00 | ✅ |
| `purescript` | `mapx` | no | no | 1.00 | ✅ |
| `purescript` | `map` | yes | yes | 1.00 | ✅ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 1.00 | ✅ |
| `qsharp` | `Qubit` | yes | yes | 1.00 | ✅ |
| `r` | `data.framex` | no | no | 1.00 | ✅ |
| `r` | `data.frame` | yes | yes | 1.00 | ✅ |
| `reasonml` | `List.mapx` | no | no | 1.00 | ✅ |
| `reasonml` | `List.map` | yes | yes | 1.00 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 1.00 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 1.00 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.mapx` | no | no | 1.00 | ✅ |
| `scala` | `List.map` | yes | yes | 1.00 | ✅ |
| `scheme` | `mapx` | no | no | 1.00 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 1.00 | ✅ |
| `slim` | `.class` | yes | yes | 1.00 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.90 | ✅ |
| `smalltalk` | `do:` | yes | yes | 1.00 | ✅ |
| `solidity` | `mappingx` | no | no | 1.00 | ✅ |
| `solidity` | `mapping` | yes | yes | 1.00 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `svelte` | `{#eachx}` | no | no | 1.00 | ✅ |
| `svelte` | `{#each}` | yes | yes | 1.00 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 1.00 | ✅ |
| `tex` | `\def` | yes | yes | 1.00 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `toml` | `[table]` | yes | yes | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | 0.90 | ✅ |
| `tsql` | `TOP` | yes | yes | 1.00 | ✅ |
| `tsx` | `useStatex` | no | no | 1.00 | ✅ |
| `tsx` | `useState` | yes | yes | 1.00 | ✅ |
| `twig` | `{% forx %}` | no | no | 1.00 | ✅ |
| `twig` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 1.00 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | 1.00 | ✅ |
| `v` | `println` | yes | yes | 1.00 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.90 | ✅ |
| `vba` | `MsgBox` | yes | yes | 1.00 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 1.00 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 1.00 | ✅ |
| `vhdl` | `processx` | no | no | 1.00 | ✅ |
| `vhdl` | `process` | yes | yes | 1.00 | ✅ |
| `vue` | `<templatex>` | no | no | 1.00 | ✅ |
| `vue` | `<template>` | yes | yes | 1.00 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 1.00 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 1.00 | ✅ |

### `Kimi-Linear-48B-A3B-Instruct (kimi-linear-hot)`

204/204 answered, 1 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.90 | ✅ |
| `abap` | `WRITE` | yes | yes | 1.00 | ✅ |
| `actionscript` | `tracex` | no | no | 1.00 | ✅ |
| `actionscript` | `trace` | yes | yes | 1.00 | ✅ |
| `ada` | `Put_Linex` | no | no | 1.00 | ✅ |
| `ada` | `Put_Line` | yes | yes | 1.00 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.90 | ✅ |
| `apex` | `Database.query` | yes | yes | 1.00 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `assembly` | `movx` | no | no | 1.00 | ✅ |
| `assembly` | `mov` | yes | yes | 1.00 | ✅ |
| `bash` | `readx` | no | no | 1.00 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 1.00 | ✅ |
| `blade` | `@foreach` | yes | yes | 1.00 | ✅ |
| `c` | `memcpyx` | no | no | 1.00 | ✅ |
| `c` | `memcpy` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 1.00 | ✅ |
| `cairo` | `felt252` | yes | yes | 1.00 | ✅ |
| `clojure` | `mapx` | no | no | 1.00 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 1.00 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 1.00 | ✅ |
| `coffeescript` | `->x` | no | no | 1.00 | ✅ |
| `coffeescript` | `->` | yes | yes | 1.00 | ✅ |
| `cpp` | `std::vectorx` | no | no | 1.00 | ✅ |
| `cpp` | `std::vector` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 1.00 | ✅ |
| `crystal` | `Array#map` | yes | yes | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.mapx` | no | no | 1.00 | ✅ |
| `dart` | `List.map` | yes | yes | 1.00 | ✅ |
| `ejs` | `<% %>x` | no | no | 1.00 | ✅ |
| `ejs` | `<% %>` | yes | yes | 1.00 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 1.00 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 1.00 | ✅ |
| `elm` | `List.mapx` | no | no | 0.90 | ✅ |
| `elm` | `List.map` | yes | yes | 1.00 | ✅ |
| `erb` | `<% %>x` | no | no | 1.00 | ✅ |
| `erb` | `<% %>` | yes | yes | 1.00 | ✅ |
| `erlang` | `lists:mapx` | no | no | 1.00 | ✅ |
| `erlang` | `lists:map` | yes | yes | 1.00 | ✅ |
| `fortran` | `allocatex` | no | no | 1.00 | ✅ |
| `fortran` | `allocate` | yes | yes | 1.00 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 1.00 | ✅ |
| `fsharp` | `List.map` | yes | yes | 1.00 | ✅ |
| `gdscript` | `printx` | no | no | 0.90 | ✅ |
| `gdscript` | `print` | yes | yes | 1.00 | ✅ |
| `gleam` | `list.mapx` | no | no | 1.00 | ✅ |
| `gleam` | `list.map` | yes | yes | 1.00 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 1.00 | ✅ |
| `go` | `fmt.Println` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 1.00 | ✅ |
| `graphviz` | `digraph` | yes | yes | 1.00 | ✅ |
| `groovy` | `eachx` | no | no | 1.00 | ✅ |
| `groovy` | `each` | yes | yes | 1.00 | ✅ |
| `haml` | `%divx` | no | no | 1.00 | ✅ |
| `haml` | `%div` | yes | yes | 1.00 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 1.00 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 1.00 | ✅ |
| `haskell` | `mapx` | no | no | 1.00 | ✅ |
| `haskell` | `map` | yes | yes | 1.00 | ✅ |
| `html` | `<a hrefx>` | no | no | 1.00 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 1.00 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 1.00 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 1.00 | ✅ |
| `jinja` | `{% forx %}` | no | no | 1.00 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `json` | `nullx` | no | no | 1.00 | ✅ |
| `json` | `null` | yes | yes | 1.00 | ✅ |
| `jsx` | `React.createElementx` | no | no | 1.00 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 1.00 | ✅ |
| `julia` | `pushx!` | no | no | 1.00 | ✅ |
| `julia` | `push!` | yes | yes | 1.00 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 1.00 | ✅ |
| `latex` | `\sectionx` | no | no | 1.00 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 1.00 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 1.00 | ✅ |
| `lisp` | `mapcarx` | no | no | 1.00 | ✅ |
| `lisp` | `mapcar` | yes | yes | 1.00 | ✅ |
| `livescript` | `->x` | no | no | 1.00 | ✅ |
| `livescript` | `->` | yes | yes | 1.00 | ✅ |
| `lua` | `table.insertx` | no | no | 1.00 | ✅ |
| `lua` | `table.insert` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 1.00 | ✅ |
| `matlab` | `zeros` | yes | yes | 1.00 | ✅ |
| `mermaid` | `graph TDx` | no | no | 1.00 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | 1.00 | ✅ |
| `mint` | `component` | yes | yes | 1.00 | ✅ |
| `mojo` | `fnx` | no | no | 1.00 | ✅ |
| `mojo` | `fn` | yes | yes | 1.00 | ✅ |
| `move` | `vectorx` | no | no | 1.00 | ✅ |
| `move` | `vector` | yes | yes | 1.00 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 1.00 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 1.00 | ✅ |
| `nim` | `seqx` | no | no | 1.00 | ✅ |
| `nim` | `seq` | yes | yes | 1.00 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 1.00 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 1.00 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 1.00 | ✅ |
| `ocaml` | `List.mapx` | no | no | 1.00 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 1.00 | ✅ |
| `odin` | `fmt.println` | yes | yes | 1.00 | ✅ |
| `orgmode` | `* Headingx` | no | no | 1.00 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 1.00 | ✅ |
| `pascal` | `writelnx` | no | no | 1.00 | ✅ |
| `pascal` | `writeln` | yes | no | 1.00 | ❌ |
| `perl` | `pushx` | no | no | 1.00 | ✅ |
| `perl` | `push` | yes | yes | 1.00 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 1.00 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.90 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 1.00 | ✅ |
| `prolog` | `findallx` | no | no | 1.00 | ✅ |
| `prolog` | `findall` | yes | yes | 1.00 | ✅ |
| `pug` | `extendsx` | no | no | 1.00 | ✅ |
| `pug` | `extends` | yes | yes | 1.00 | ✅ |
| `purescript` | `mapx` | no | no | 1.00 | ✅ |
| `purescript` | `map` | yes | yes | 1.00 | ✅ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 1.00 | ✅ |
| `qsharp` | `Qubit` | yes | yes | 1.00 | ✅ |
| `r` | `data.framex` | no | no | 1.00 | ✅ |
| `r` | `data.frame` | yes | yes | 1.00 | ✅ |
| `reasonml` | `List.mapx` | no | no | 1.00 | ✅ |
| `reasonml` | `List.map` | yes | yes | 1.00 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 1.00 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 1.00 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.mapx` | no | no | 1.00 | ✅ |
| `scala` | `List.map` | yes | yes | 1.00 | ✅ |
| `scheme` | `mapx` | no | no | 1.00 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 1.00 | ✅ |
| `slim` | `.class` | yes | yes | 1.00 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.90 | ✅ |
| `smalltalk` | `do:` | yes | yes | 1.00 | ✅ |
| `solidity` | `mappingx` | no | no | 1.00 | ✅ |
| `solidity` | `mapping` | yes | yes | 1.00 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `svelte` | `{#eachx}` | no | no | 1.00 | ✅ |
| `svelte` | `{#each}` | yes | yes | 1.00 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 1.00 | ✅ |
| `tex` | `\def` | yes | yes | 1.00 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `toml` | `[table]` | yes | yes | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | 0.90 | ✅ |
| `tsql` | `TOP` | yes | yes | 1.00 | ✅ |
| `tsx` | `useStatex` | no | no | 1.00 | ✅ |
| `tsx` | `useState` | yes | yes | 1.00 | ✅ |
| `twig` | `{% forx %}` | no | no | 1.00 | ✅ |
| `twig` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 1.00 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | 1.00 | ✅ |
| `v` | `println` | yes | yes | 1.00 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.90 | ✅ |
| `vba` | `MsgBox` | yes | yes | 1.00 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 1.00 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 1.00 | ✅ |
| `vhdl` | `processx` | no | no | 1.00 | ✅ |
| `vhdl` | `process` | yes | yes | 1.00 | ✅ |
| `vue` | `<templatex>` | no | no | 1.00 | ✅ |
| `vue` | `<template>` | yes | yes | 1.00 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 1.00 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 1.00 | ✅ |

### `Inkling-2-Mini-oQ4e-mtp (inkling)`

188/204 answered, 0 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.85 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.95 | ✅ |
| `ada` | `Put_Linex` | no | no | 0.99 | ✅ |
| `ada` | `Put_Line` | yes | yes | 0.98 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.95 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.90 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 0.80 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 0.95 | ✅ |
| `assembly` | `movx` | no | no | 0.70 | ✅ |
| `assembly` | `mov` | yes | yes | 0.99 | ✅ |
| `bash` | `readx` | no | no | 0.95 | ✅ |
| `bash` | `read` | yes | yes | 0.99 | ✅ |
| `blade` | `@foreachx` | no | no | 0.95 | ✅ |
| `blade` | `@foreach` | yes | yes | 0.98 | ✅ |
| `c` | `memcpyx` | no | no | 0.98 | ✅ |
| `c` | `memcpy` | yes | yes | 0.99 | ✅ |
| `cairo` | `felt252x` | no | no | 0.85 | ✅ |
| `cairo` | `felt252` | yes | yes | 0.90 | ✅ |
| `clojure` | `mapx` | no | no | 0.90 | ✅ |
| `clojure` | `map` | yes | yes | 0.99 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 0.99 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 0.99 | ✅ |
| `cpp` | `std::vectorx` | no | no | 0.99 | ✅ |
| `cpp` | `std::vector` | yes | yes | 0.99 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.90 | ✅ |
| `crystal` | `Array#map` | yes | yes | 0.95 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 0.98 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 0.99 | ✅ |
| `css` | `display: flexx` | no | no | 0.99 | ✅ |
| `css` | `display: flex` | yes | yes | 0.99 | ✅ |
| `dart` | `List.mapx` | no | no | 0.95 | ✅ |
| `dart` | `List.map` | yes | yes | 0.99 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.95 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.98 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.90 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.99 | ✅ |
| `elm` | `List.mapx` | no | no | 0.95 | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
| `erb` | `<% %>x` | no | no | 0.90 | ✅ |
| `erb` | `<% %>` | yes | yes | 0.98 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.95 | ✅ |
| `erlang` | `lists:map` | yes | yes | 0.99 | ✅ |
| `fortran` | `allocatex` | no | no | 0.99 | ✅ |
| `fortran` | `allocate` | yes | yes | 0.98 | ✅ |
| `freemarker` | `<#listx>` | no | no | 0.95 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.95 | ✅ |
| `fsharp` | `List.map` | yes | yes | 0.99 | ✅ |
| `gdscript` | `printx` | no | no | 0.97 | ✅ |
| `gdscript` | `print` | yes | yes | 0.98 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.90 | ✅ |
| `gleam` | `list.map` | yes | yes | 0.90 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 0.98 | ✅ |
| `go` | `fmt.Println` | yes | yes | 0.99 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.90 | ✅ |
| `graphviz` | `digraph` | yes | yes | 0.97 | ✅ |
| `groovy` | `eachx` | no | no | 0.99 | ✅ |
| `groovy` | `each` | yes | yes | 0.97 | ✅ |
| `haml` | `%divx` | no | no | 0.80 | ✅ |
| `haml` | `%div` | yes | yes | 0.98 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.95 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.98 | ✅ |
| `haskell` | `mapx` | no | no | 0.90 | ✅ |
| `haskell` | `map` | yes | yes | 0.99 | ✅ |
| `html` | `<a hrefx>` | no | no | 0.98 | ✅ |
| `html` | `<a href>` | yes | yes | 0.99 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 0.98 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 0.99 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 0.98 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 0.99 | ✅ |
| `jinja` | `{% forx %}` | no | no | 0.95 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `json` | `nullx` | no | no | 0.99 | ✅ |
| `json` | `null` | yes | yes | 0.99 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.95 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.98 | ✅ |
| `julia` | `pushx!` | no | no | 0.97 | ✅ |
| `julia` | `push!` | yes | yes | 0.98 | ✅ |
| `kotlin` | `listOfx` | no | no | 0.98 | ✅ |
| `kotlin` | `listOf` | yes | yes | 0.98 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 0.97 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 0.97 | ✅ |
| `latex` | `\sectionx` | no | no | 0.95 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.95 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 0.98 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.97 | ✅ |
| `lisp` | `mapcar` | yes | yes | 0.99 | ✅ |
| `lua` | `table.insertx` | no | no | 0.99 | ✅ |
| `lua` | `table.insert` | yes | yes | 0.99 | ✅ |
| `markdown` | `## headingx` | no | no | 0.80 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 0.98 | ✅ |
| `matlab` | `zeros` | yes | yes | 0.99 | ✅ |
| `mermaid` | `graph TDx` | no | no | 0.95 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 0.99 | ✅ |
| `mojo` | `fnx` | no | no | 0.90 | ✅ |
| `mojo` | `fn` | yes | yes | 0.95 | ✅ |
| `move` | `vectorx` | no | no | 0.90 | ✅ |
| `move` | `vector` | yes | yes | 0.90 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.95 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.98 | ✅ |
| `nim` | `seqx` | no | no | 0.90 | ✅ |
| `nim` | `seq` | yes | yes | 0.95 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 0.95 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.95 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.99 | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.95 | ✅ |
| `ocaml` | `List.map` | yes | yes | 0.99 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.90 | ✅ |
| `odin` | `fmt.println` | yes | yes | 0.90 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.75 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 0.90 | ✅ |
| `pascal` | `writelnx` | no | no | 0.99 | ✅ |
| `pascal` | `writeln` | yes | yes | 0.95 | ✅ |
| `perl` | `pushx` | no | no | 0.95 | ✅ |
| `perl` | `push` | yes | yes | 0.99 | ✅ |
| `php` | `array_mapx` | no | no | 0.99 | ✅ |
| `php` | `array_map` | yes | yes | 0.99 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.95 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 0.99 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.90 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.98 | ✅ |
| `prolog` | `findallx` | no | no | 0.95 | ✅ |
| `prolog` | `findall` | yes | yes | 0.90 | ✅ |
| `pug` | `extendsx` | no | no | 0.95 | ✅ |
| `pug` | `extends` | yes | yes | 0.95 | ✅ |
| `python` | `functools.reducex` | no | no | 0.99 | ✅ |
| `python` | `functools.reduce` | yes | yes | 0.99 | ✅ |
| `r` | `data.framex` | no | no | 0.98 | ✅ |
| `r` | `data.frame` | yes | yes | 0.99 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 0.85 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 0.95 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 0.97 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 0.98 | ✅ |
| `rust` | `Vec::pushx` | no | no | 0.98 | ✅ |
| `rust` | `Vec::push` | yes | yes | 0.98 | ✅ |
| `scala` | `List.mapx` | no | no | 0.95 | ✅ |
| `scala` | `List.map` | yes | yes | 0.99 | ✅ |
| `scheme` | `mapx` | no | no | 0.90 | ✅ |
| `scheme` | `map` | yes | yes | 0.99 | ✅ |
| `slim` | `.classx` | no | no | 0.78 | ✅ |
| `slim` | `.class` | yes | yes | 0.98 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.90 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 0.99 | ✅ |
| `solidity` | `mapping` | yes | yes | 0.99 | ✅ |
| `sql` | `GROUP BYx` | no | no | 0.99 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 0.99 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.95 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.98 | ✅ |
| `swift` | `Array.mapx` | no | no | 0.98 | ✅ |
| `swift` | `Array.map` | yes | yes | 0.98 | ✅ |
| `tex` | `\defx` | no | no | 0.95 | ✅ |
| `tex` | `\def` | yes | yes | 0.99 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 0.95 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 0.90 | ✅ |
| `toml` | `[table]` | yes | yes | 0.98 | ✅ |
| `tsql` | `TOPx` | no | no | 0.95 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.98 | ✅ |
| `tsx` | `useStatex` | no | no | 0.95 | ✅ |
| `tsx` | `useState` | yes | yes | 0.98 | ✅ |
| `twig` | `{% forx %}` | no | no | 0.95 | ✅ |
| `twig` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 0.98 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 0.95 | ✅ |
| `typst` | `#letx` | no | no | 0.95 | ✅ |
| `typst` | `#let` | yes | yes | 0.98 | ✅ |
| `v` | `printlnx` | no | no | 0.90 | ✅ |
| `v` | `println` | yes | yes | 0.95 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.95 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.99 | ✅ |
| `velocity` | `#foreachx` | no | no | 0.95 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 0.98 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 0.98 | ✅ |
| `vhdl` | `processx` | no | no | 0.99 | ✅ |
| `vhdl` | `process` | yes | yes | 0.99 | ✅ |
| `vue` | `<templatex>` | no | no | 0.95 | ✅ |
| `vue` | `<template>` | yes | yes | 0.98 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 0.95 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 0.95 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.90 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.90 | ✅ |

### `Inkling-2-Mini-oQ4e-mtp (inkling-hot)`

188/204 answered, 0 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.85 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.95 | ✅ |
| `ada` | `Put_Linex` | no | no | 0.99 | ✅ |
| `ada` | `Put_Line` | yes | yes | 0.98 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.95 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.90 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 0.80 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 0.95 | ✅ |
| `assembly` | `movx` | no | no | 0.70 | ✅ |
| `assembly` | `mov` | yes | yes | 0.99 | ✅ |
| `bash` | `readx` | no | no | 0.95 | ✅ |
| `bash` | `read` | yes | yes | 0.99 | ✅ |
| `blade` | `@foreachx` | no | no | 0.95 | ✅ |
| `blade` | `@foreach` | yes | yes | 0.98 | ✅ |
| `c` | `memcpyx` | no | no | 0.98 | ✅ |
| `c` | `memcpy` | yes | yes | 0.99 | ✅ |
| `cairo` | `felt252x` | no | no | 0.85 | ✅ |
| `cairo` | `felt252` | yes | yes | 0.90 | ✅ |
| `clojure` | `mapx` | no | no | 0.90 | ✅ |
| `clojure` | `map` | yes | yes | 0.99 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 0.99 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 0.99 | ✅ |
| `cpp` | `std::vectorx` | no | no | 0.99 | ✅ |
| `cpp` | `std::vector` | yes | yes | 0.99 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.90 | ✅ |
| `crystal` | `Array#map` | yes | yes | 0.95 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 0.98 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 0.99 | ✅ |
| `css` | `display: flexx` | no | no | 0.99 | ✅ |
| `css` | `display: flex` | yes | yes | 0.99 | ✅ |
| `dart` | `List.mapx` | no | no | 0.95 | ✅ |
| `dart` | `List.map` | yes | yes | 0.99 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.95 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.98 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.90 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.99 | ✅ |
| `elm` | `List.mapx` | no | no | 0.95 | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
| `erb` | `<% %>x` | no | no | 0.90 | ✅ |
| `erb` | `<% %>` | yes | yes | 0.98 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.95 | ✅ |
| `erlang` | `lists:map` | yes | yes | 0.99 | ✅ |
| `fortran` | `allocatex` | no | no | 0.99 | ✅ |
| `fortran` | `allocate` | yes | yes | 0.98 | ✅ |
| `freemarker` | `<#listx>` | no | no | 0.95 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.95 | ✅ |
| `fsharp` | `List.map` | yes | yes | 0.99 | ✅ |
| `gdscript` | `printx` | no | no | 0.97 | ✅ |
| `gdscript` | `print` | yes | yes | 0.98 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.90 | ✅ |
| `gleam` | `list.map` | yes | yes | 0.90 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 0.98 | ✅ |
| `go` | `fmt.Println` | yes | yes | 0.99 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.90 | ✅ |
| `graphviz` | `digraph` | yes | yes | 0.97 | ✅ |
| `groovy` | `eachx` | no | no | 0.99 | ✅ |
| `groovy` | `each` | yes | yes | 0.97 | ✅ |
| `haml` | `%divx` | no | no | 0.80 | ✅ |
| `haml` | `%div` | yes | yes | 0.98 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.95 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.98 | ✅ |
| `haskell` | `mapx` | no | no | 0.90 | ✅ |
| `haskell` | `map` | yes | yes | 0.99 | ✅ |
| `html` | `<a hrefx>` | no | no | 0.98 | ✅ |
| `html` | `<a href>` | yes | yes | 0.99 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 0.98 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 0.99 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 0.98 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 0.99 | ✅ |
| `jinja` | `{% forx %}` | no | no | 0.95 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `json` | `nullx` | no | no | 0.99 | ✅ |
| `json` | `null` | yes | yes | 0.99 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.95 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.98 | ✅ |
| `julia` | `pushx!` | no | no | 0.97 | ✅ |
| `julia` | `push!` | yes | yes | 0.98 | ✅ |
| `kotlin` | `listOfx` | no | no | 0.98 | ✅ |
| `kotlin` | `listOf` | yes | yes | 0.98 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 0.97 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 0.97 | ✅ |
| `latex` | `\sectionx` | no | no | 0.95 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.95 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 0.98 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.97 | ✅ |
| `lisp` | `mapcar` | yes | yes | 0.99 | ✅ |
| `lua` | `table.insertx` | no | no | 0.99 | ✅ |
| `lua` | `table.insert` | yes | yes | 0.99 | ✅ |
| `markdown` | `## headingx` | no | no | 0.80 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 0.98 | ✅ |
| `matlab` | `zeros` | yes | yes | 0.99 | ✅ |
| `mermaid` | `graph TDx` | no | no | 0.95 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 0.99 | ✅ |
| `mojo` | `fnx` | no | no | 0.90 | ✅ |
| `mojo` | `fn` | yes | yes | 0.95 | ✅ |
| `move` | `vectorx` | no | no | 0.90 | ✅ |
| `move` | `vector` | yes | yes | 0.90 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.95 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.98 | ✅ |
| `nim` | `seqx` | no | no | 0.90 | ✅ |
| `nim` | `seq` | yes | yes | 0.95 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 0.95 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.95 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.99 | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.95 | ✅ |
| `ocaml` | `List.map` | yes | yes | 0.99 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.90 | ✅ |
| `odin` | `fmt.println` | yes | yes | 0.90 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.75 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 0.90 | ✅ |
| `pascal` | `writelnx` | no | no | 0.99 | ✅ |
| `pascal` | `writeln` | yes | yes | 0.95 | ✅ |
| `perl` | `pushx` | no | no | 0.95 | ✅ |
| `perl` | `push` | yes | yes | 0.99 | ✅ |
| `php` | `array_mapx` | no | no | 0.99 | ✅ |
| `php` | `array_map` | yes | yes | 0.99 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.95 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 0.99 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.90 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.98 | ✅ |
| `prolog` | `findallx` | no | no | 0.95 | ✅ |
| `prolog` | `findall` | yes | yes | 0.90 | ✅ |
| `pug` | `extendsx` | no | no | 0.95 | ✅ |
| `pug` | `extends` | yes | yes | 0.95 | ✅ |
| `python` | `functools.reducex` | no | no | 0.99 | ✅ |
| `python` | `functools.reduce` | yes | yes | 0.99 | ✅ |
| `r` | `data.framex` | no | no | 0.98 | ✅ |
| `r` | `data.frame` | yes | yes | 0.99 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 0.85 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 0.95 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 0.97 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 0.98 | ✅ |
| `rust` | `Vec::pushx` | no | no | 0.98 | ✅ |
| `rust` | `Vec::push` | yes | yes | 0.98 | ✅ |
| `scala` | `List.mapx` | no | no | 0.95 | ✅ |
| `scala` | `List.map` | yes | yes | 0.99 | ✅ |
| `scheme` | `mapx` | no | no | 0.90 | ✅ |
| `scheme` | `map` | yes | yes | 0.99 | ✅ |
| `slim` | `.classx` | no | no | 0.78 | ✅ |
| `slim` | `.class` | yes | yes | 0.98 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.90 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 0.99 | ✅ |
| `solidity` | `mapping` | yes | yes | 0.99 | ✅ |
| `sql` | `GROUP BYx` | no | no | 0.99 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 0.99 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.95 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.98 | ✅ |
| `swift` | `Array.mapx` | no | no | 0.98 | ✅ |
| `swift` | `Array.map` | yes | yes | 0.98 | ✅ |
| `tex` | `\defx` | no | no | 0.95 | ✅ |
| `tex` | `\def` | yes | yes | 0.99 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 0.95 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 0.90 | ✅ |
| `toml` | `[table]` | yes | yes | 0.98 | ✅ |
| `tsql` | `TOPx` | no | no | 0.95 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.98 | ✅ |
| `tsx` | `useStatex` | no | no | 0.95 | ✅ |
| `tsx` | `useState` | yes | yes | 0.98 | ✅ |
| `twig` | `{% forx %}` | no | no | 0.95 | ✅ |
| `twig` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 0.98 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 0.95 | ✅ |
| `typst` | `#letx` | no | no | 0.95 | ✅ |
| `typst` | `#let` | yes | yes | 0.98 | ✅ |
| `v` | `printlnx` | no | no | 0.90 | ✅ |
| `v` | `println` | yes | yes | 0.95 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.95 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.99 | ✅ |
| `velocity` | `#foreachx` | no | no | 0.95 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 0.98 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 0.98 | ✅ |
| `vhdl` | `processx` | no | no | 0.99 | ✅ |
| `vhdl` | `process` | yes | yes | 0.99 | ✅ |
| `vue` | `<templatex>` | no | no | 0.95 | ✅ |
| `vue` | `<template>` | yes | yes | 0.98 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 0.95 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 0.95 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.90 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.90 | ✅ |

### `Inkling-2-Mini-oQ4e-mtp (inkling-mtp)`

204/204 answered, 0 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.95 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.95 | ✅ |
| `actionscript` | `tracex` | no | no | 0.95 | ✅ |
| `actionscript` | `trace` | yes | yes | 0.99 | ✅ |
| `ada` | `Put_Linex` | no | no | 0.95 | ✅ |
| `ada` | `Put_Line` | yes | yes | 0.98 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.95 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.90 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 0.75 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 0.95 | ✅ |
| `assembly` | `movx` | no | no | 0.75 | ✅ |
| `assembly` | `mov` | yes | yes | 0.99 | ✅ |
| `bash` | `readx` | no | no | 0.95 | ✅ |
| `bash` | `read` | yes | yes | 0.99 | ✅ |
| `blade` | `@foreachx` | no | no | 0.97 | ✅ |
| `blade` | `@foreach` | yes | yes | 0.99 | ✅ |
| `c` | `memcpyx` | no | no | 0.98 | ✅ |
| `c` | `memcpy` | yes | yes | 0.99 | ✅ |
| `cairo` | `felt252x` | no | no | 0.95 | ✅ |
| `cairo` | `felt252` | yes | yes | 0.98 | ✅ |
| `clojure` | `mapx` | no | no | 0.90 | ✅ |
| `clojure` | `map` | yes | yes | 0.98 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 0.95 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 0.98 | ✅ |
| `coffeescript` | `->x` | no | no | 0.80 | ✅ |
| `coffeescript` | `->` | yes | yes | 0.98 | ✅ |
| `cpp` | `std::vectorx` | no | no | 0.98 | ✅ |
| `cpp` | `std::vector` | yes | yes | 0.99 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.95 | ✅ |
| `crystal` | `Array#map` | yes | yes | 0.98 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 0.98 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 0.98 | ✅ |
| `css` | `display: flexx` | no | no | 0.97 | ✅ |
| `css` | `display: flex` | yes | yes | 0.99 | ✅ |
| `dart` | `List.mapx` | no | no | 0.95 | ✅ |
| `dart` | `List.map` | yes | yes | 0.99 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.95 | ✅ |
| `ejs` | `<% %>` | yes | yes | 1.00 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.90 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.99 | ✅ |
| `elm` | `List.mapx` | no | no | 0.95 | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
| `erb` | `<% %>x` | no | no | 0.90 | ✅ |
| `erb` | `<% %>` | yes | yes | 0.98 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.95 | ✅ |
| `erlang` | `lists:map` | yes | yes | 0.98 | ✅ |
| `fortran` | `allocatex` | no | no | 0.95 | ✅ |
| `fortran` | `allocate` | yes | yes | 0.98 | ✅ |
| `freemarker` | `<#listx>` | no | no | 0.97 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 0.98 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.90 | ✅ |
| `fsharp` | `List.map` | yes | yes | 0.98 | ✅ |
| `gdscript` | `printx` | no | no | 0.95 | ✅ |
| `gdscript` | `print` | yes | yes | 0.95 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.95 | ✅ |
| `gleam` | `list.map` | yes | yes | 0.90 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 0.98 | ✅ |
| `go` | `fmt.Println` | yes | yes | 0.99 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.95 | ✅ |
| `graphviz` | `digraph` | yes | yes | 0.99 | ✅ |
| `groovy` | `eachx` | no | no | 0.95 | ✅ |
| `groovy` | `each` | yes | yes | 0.95 | ✅ |
| `haml` | `%divx` | no | no | 0.85 | ✅ |
| `haml` | `%div` | yes | yes | 0.99 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.98 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 1.00 | ✅ |
| `haskell` | `mapx` | no | no | 0.95 | ✅ |
| `haskell` | `map` | yes | yes | 0.99 | ✅ |
| `html` | `<a hrefx>` | no | no | 0.97 | ✅ |
| `html` | `<a href>` | yes | yes | 0.99 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 0.98 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 0.98 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 0.98 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 0.99 | ✅ |
| `jinja` | `{% forx %}` | no | no | 0.95 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 0.99 | ✅ |
| `json` | `nullx` | no | no | 0.97 | ✅ |
| `json` | `null` | yes | yes | 0.99 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.98 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.95 | ✅ |
| `julia` | `pushx!` | no | no | 0.95 | ✅ |
| `julia` | `push!` | yes | yes | 0.98 | ✅ |
| `kotlin` | `listOfx` | no | no | 0.98 | ✅ |
| `kotlin` | `listOf` | yes | yes | 0.98 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 0.97 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 0.97 | ✅ |
| `latex` | `\sectionx` | no | no | 0.97 | ✅ |
| `latex` | `\section` | yes | yes | 0.99 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.95 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 0.99 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.95 | ✅ |
| `lisp` | `mapcar` | yes | yes | 0.98 | ✅ |
| `livescript` | `->x` | no | no | 0.80 | ✅ |
| `livescript` | `->` | yes | yes | 0.98 | ✅ |
| `lua` | `table.insertx` | no | no | 0.97 | ✅ |
| `lua` | `table.insert` | yes | yes | 0.98 | ✅ |
| `markdown` | `## headingx` | no | no | 0.75 | ✅ |
| `markdown` | `## heading` | yes | yes | 0.98 | ✅ |
| `matlab` | `zerosx` | no | no | 0.97 | ✅ |
| `matlab` | `zeros` | yes | yes | 0.99 | ✅ |
| `mermaid` | `graph TDx` | no | no | 0.98 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 0.99 | ✅ |
| `mint` | `componentx` | no | no | 0.75 | ✅ |
| `mint` | `component` | yes | yes | 0.55 | ✅ |
| `mojo` | `fnx` | no | no | 0.95 | ✅ |
| `mojo` | `fn` | yes | yes | 0.98 | ✅ |
| `move` | `vectorx` | no | no | 0.95 | ✅ |
| `move` | `vector` | yes | yes | 0.95 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.75 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.85 | ✅ |
| `nim` | `seqx` | no | no | 0.95 | ✅ |
| `nim` | `seq` | yes | yes | 0.98 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 0.95 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 0.99 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.98 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.99 | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.90 | ✅ |
| `ocaml` | `List.map` | yes | yes | 0.98 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.95 | ✅ |
| `odin` | `fmt.println` | yes | yes | 0.90 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.85 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 0.99 | ✅ |
| `pascal` | `writelnx` | no | no | 0.95 | ✅ |
| `pascal` | `writeln` | yes | yes | 0.98 | ✅ |
| `perl` | `pushx` | no | no | 0.97 | ✅ |
| `perl` | `push` | yes | yes | 0.99 | ✅ |
| `php` | `array_mapx` | no | no | 0.99 | ✅ |
| `php` | `array_map` | yes | yes | 0.99 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.90 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 0.99 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.95 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.95 | ✅ |
| `prolog` | `findallx` | no | no | 0.95 | ✅ |
| `prolog` | `findall` | yes | yes | 0.90 | ✅ |
| `pug` | `extendsx` | no | no | 0.98 | ✅ |
| `pug` | `extends` | yes | yes | 1.00 | ✅ |
| `purescript` | `mapx` | no | no | 0.98 | ✅ |
| `purescript` | `map` | yes | yes | 0.99 | ✅ |
| `python` | `functools.reducex` | no | no | 0.98 | ✅ |
| `python` | `functools.reduce` | yes | yes | 0.99 | ✅ |
| `qsharp` | `Qubitx` | no | no | 0.98 | ✅ |
| `qsharp` | `Qubit` | yes | yes | 0.95 | ✅ |
| `r` | `data.framex` | no | no | 0.95 | ✅ |
| `r` | `data.frame` | yes | yes | 0.99 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.98 | ✅ |
| `reasonml` | `List.map` | yes | yes | 0.98 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.98 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 0.95 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 0.85 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 0.98 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 0.95 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 0.97 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 0.97 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 0.98 | ✅ |
| `rust` | `Vec::pushx` | no | no | 0.98 | ✅ |
| `rust` | `Vec::push` | yes | yes | 0.98 | ✅ |
| `scala` | `List.mapx` | no | no | 0.95 | ✅ |
| `scala` | `List.map` | yes | yes | 0.99 | ✅ |
| `scheme` | `mapx` | no | no | 0.90 | ✅ |
| `scheme` | `map` | yes | yes | 0.98 | ✅ |
| `slim` | `.classx` | no | no | 0.85 | ✅ |
| `slim` | `.class` | yes | yes | 0.99 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.90 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 0.95 | ✅ |
| `solidity` | `mapping` | yes | yes | 0.98 | ✅ |
| `sql` | `GROUP BYx` | no | no | 0.99 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 0.99 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.98 | ✅ |
| `svelte` | `{#each}` | yes | yes | 1.00 | ✅ |
| `swift` | `Array.mapx` | no | no | 0.98 | ✅ |
| `swift` | `Array.map` | yes | yes | 0.98 | ✅ |
| `tex` | `\defx` | no | no | 0.97 | ✅ |
| `tex` | `\def` | yes | yes | 0.99 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 0.97 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 0.98 | ✅ |
| `toml` | `[tablex]` | no | no | 0.90 | ✅ |
| `toml` | `[table]` | yes | yes | 0.97 | ✅ |
| `tsql` | `TOPx` | no | no | 0.95 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.95 | ✅ |
| `tsx` | `useStatex` | no | no | 0.97 | ✅ |
| `tsx` | `useState` | yes | yes | 1.00 | ✅ |
| `twig` | `{% forx %}` | no | no | 0.95 | ✅ |
| `twig` | `{% for %}` | yes | yes | 0.99 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 0.98 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 0.95 | ✅ |
| `typst` | `#letx` | no | no | 0.97 | ✅ |
| `typst` | `#let` | yes | yes | 0.99 | ✅ |
| `v` | `printlnx` | no | no | 0.95 | ✅ |
| `v` | `println` | yes | yes | 0.98 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.95 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.95 | ✅ |
| `velocity` | `#foreachx` | no | no | 0.95 | ✅ |
| `velocity` | `#foreach` | yes | yes | 0.98 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 0.95 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 0.98 | ✅ |
| `vhdl` | `processx` | no | no | 0.95 | ✅ |
| `vhdl` | `process` | yes | yes | 0.98 | ✅ |
| `vue` | `<templatex>` | no | no | 0.98 | ✅ |
| `vue` | `<template>` | yes | yes | 1.00 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 0.95 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 0.97 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.95 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.90 | ✅ |

### `Inkling-2-Mini-oQ4e-mtp (inkling-mtp-hot)`

204/204 answered, 0 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.95 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.95 | ✅ |
| `actionscript` | `tracex` | no | no | 0.95 | ✅ |
| `actionscript` | `trace` | yes | yes | 0.98 | ✅ |
| `ada` | `Put_Linex` | no | no | 0.95 | ✅ |
| `ada` | `Put_Line` | yes | yes | 0.95 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.90 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.90 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 0.75 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 0.90 | ✅ |
| `assembly` | `movx` | no | no | 0.85 | ✅ |
| `assembly` | `mov` | yes | yes | 0.99 | ✅ |
| `bash` | `readx` | no | no | 0.97 | ✅ |
| `bash` | `read` | yes | yes | 0.99 | ✅ |
| `blade` | `@foreachx` | no | no | 0.95 | ✅ |
| `blade` | `@foreach` | yes | yes | 0.98 | ✅ |
| `c` | `memcpyx` | no | no | 0.98 | ✅ |
| `c` | `memcpy` | yes | yes | 0.99 | ✅ |
| `cairo` | `felt252x` | no | no | 0.90 | ✅ |
| `cairo` | `felt252` | yes | yes | 0.95 | ✅ |
| `clojure` | `mapx` | no | no | 0.90 | ✅ |
| `clojure` | `map` | yes | yes | 0.95 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 0.95 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 0.98 | ✅ |
| `coffeescript` | `->x` | no | no | 0.80 | ✅ |
| `coffeescript` | `->` | yes | yes | 0.98 | ✅ |
| `cpp` | `std::vectorx` | no | no | 0.98 | ✅ |
| `cpp` | `std::vector` | yes | yes | 0.99 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.95 | ✅ |
| `crystal` | `Array#map` | yes | yes | 0.98 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 0.98 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 0.99 | ✅ |
| `css` | `display: flexx` | no | no | 0.98 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.mapx` | no | no | 0.95 | ✅ |
| `dart` | `List.map` | yes | yes | 0.99 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.90 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.97 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.90 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.99 | ✅ |
| `elm` | `List.mapx` | no | no | 0.95 | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
| `erb` | `<% %>x` | no | no | 0.90 | ✅ |
| `erb` | `<% %>` | yes | yes | 0.98 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.95 | ✅ |
| `erlang` | `lists:map` | yes | yes | 0.99 | ✅ |
| `fortran` | `allocatex` | no | no | 0.95 | ✅ |
| `fortran` | `allocate` | yes | yes | 0.95 | ✅ |
| `freemarker` | `<#listx>` | no | no | 0.95 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 0.98 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.90 | ✅ |
| `fsharp` | `List.map` | yes | yes | 0.98 | ✅ |
| `gdscript` | `printx` | no | no | 0.95 | ✅ |
| `gdscript` | `print` | yes | yes | 0.95 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.90 | ✅ |
| `gleam` | `list.map` | yes | yes | 0.90 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 0.98 | ✅ |
| `go` | `fmt.Println` | yes | yes | 0.99 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.90 | ✅ |
| `graphviz` | `digraph` | yes | yes | 0.99 | ✅ |
| `groovy` | `eachx` | no | no | 0.95 | ✅ |
| `groovy` | `each` | yes | yes | 0.95 | ✅ |
| `haml` | `%divx` | no | no | 0.80 | ✅ |
| `haml` | `%div` | yes | yes | 0.98 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.95 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.97 | ✅ |
| `haskell` | `mapx` | no | no | 0.90 | ✅ |
| `haskell` | `map` | yes | yes | 0.99 | ✅ |
| `html` | `<a hrefx>` | no | no | 0.95 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 0.98 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 0.98 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 0.98 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 0.99 | ✅ |
| `jinja` | `{% forx %}` | no | no | 0.95 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `json` | `nullx` | no | no | 0.98 | ✅ |
| `json` | `null` | yes | yes | 1.00 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.97 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.99 | ✅ |
| `julia` | `pushx!` | no | no | 0.90 | ✅ |
| `julia` | `push!` | yes | yes | 0.95 | ✅ |
| `kotlin` | `listOfx` | no | no | 0.98 | ✅ |
| `kotlin` | `listOf` | yes | yes | 0.98 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 0.97 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 0.97 | ✅ |
| `latex` | `\sectionx` | no | no | 0.97 | ✅ |
| `latex` | `\section` | yes | yes | 0.99 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.95 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 0.98 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.95 | ✅ |
| `lisp` | `mapcar` | yes | yes | 0.99 | ✅ |
| `livescript` | `->x` | no | no | 0.80 | ✅ |
| `livescript` | `->` | yes | yes | 0.98 | ✅ |
| `lua` | `table.insertx` | no | no | 0.98 | ✅ |
| `lua` | `table.insert` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 0.75 | ✅ |
| `markdown` | `## heading` | yes | yes | 0.98 | ✅ |
| `matlab` | `zerosx` | no | no | 0.98 | ✅ |
| `matlab` | `zeros` | yes | yes | 1.00 | ✅ |
| `mermaid` | `graph TDx` | no | no | 0.95 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 0.99 | ✅ |
| `mint` | `componentx` | no | no | 0.60 | ✅ |
| `mint` | `component` | yes | yes | 0.40 | ✅ |
| `mojo` | `fnx` | no | no | 0.90 | ✅ |
| `mojo` | `fn` | yes | yes | 0.90 | ✅ |
| `move` | `vectorx` | no | no | 0.90 | ✅ |
| `move` | `vector` | yes | yes | 0.90 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.95 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.95 | ✅ |
| `nim` | `seqx` | no | no | 0.90 | ✅ |
| `nim` | `seq` | yes | yes | 0.95 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 0.95 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.95 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.99 | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.90 | ✅ |
| `ocaml` | `List.map` | yes | yes | 0.98 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.95 | ✅ |
| `odin` | `fmt.println` | yes | yes | 0.95 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.85 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 0.95 | ✅ |
| `pascal` | `writelnx` | no | no | 0.95 | ✅ |
| `pascal` | `writeln` | yes | yes | 0.95 | ✅ |
| `perl` | `pushx` | no | no | 0.95 | ✅ |
| `perl` | `push` | yes | yes | 0.99 | ✅ |
| `php` | `array_mapx` | no | no | 0.99 | ✅ |
| `php` | `array_map` | yes | yes | 0.99 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.95 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 0.99 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.95 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.97 | ✅ |
| `prolog` | `findallx` | no | no | 0.90 | ✅ |
| `prolog` | `findall` | yes | yes | 0.75 | ✅ |
| `pug` | `extendsx` | no | no | 0.95 | ✅ |
| `pug` | `extends` | yes | yes | 0.97 | ✅ |
| `purescript` | `mapx` | no | no | 0.95 | ✅ |
| `purescript` | `map` | yes | yes | 0.97 | ✅ |
| `python` | `functools.reducex` | no | no | 0.98 | ✅ |
| `python` | `functools.reduce` | yes | yes | 0.99 | ✅ |
| `qsharp` | `Qubitx` | no | no | 0.98 | ✅ |
| `qsharp` | `Qubit` | yes | yes | 0.95 | ✅ |
| `r` | `data.framex` | no | no | 0.95 | ✅ |
| `r` | `data.frame` | yes | yes | 1.00 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.90 | ✅ |
| `reasonml` | `List.map` | yes | yes | 0.85 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.90 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 0.85 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 0.85 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 0.99 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 0.95 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 0.98 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 0.98 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 0.98 | ✅ |
| `rust` | `Vec::pushx` | no | no | 0.98 | ✅ |
| `rust` | `Vec::push` | yes | yes | 0.98 | ✅ |
| `scala` | `List.mapx` | no | no | 0.95 | ✅ |
| `scala` | `List.map` | yes | yes | 0.99 | ✅ |
| `scheme` | `mapx` | no | no | 0.90 | ✅ |
| `scheme` | `map` | yes | yes | 0.95 | ✅ |
| `slim` | `.classx` | no | no | 0.80 | ✅ |
| `slim` | `.class` | yes | yes | 0.98 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.95 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 0.95 | ✅ |
| `solidity` | `mapping` | yes | yes | 0.98 | ✅ |
| `sql` | `GROUP BYx` | no | no | 0.99 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 0.99 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.95 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.98 | ✅ |
| `swift` | `Array.mapx` | no | no | 0.98 | ✅ |
| `swift` | `Array.map` | yes | yes | 0.98 | ✅ |
| `tex` | `\defx` | no | no | 0.95 | ✅ |
| `tex` | `\def` | yes | yes | 0.99 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 0.95 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 0.98 | ✅ |
| `toml` | `[tablex]` | no | no | 0.90 | ✅ |
| `toml` | `[table]` | yes | yes | 0.98 | ✅ |
| `tsql` | `TOPx` | no | no | 0.95 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.97 | ✅ |
| `tsx` | `useStatex` | no | no | 0.95 | ✅ |
| `tsx` | `useState` | yes | yes | 0.99 | ✅ |
| `twig` | `{% forx %}` | no | no | 0.95 | ✅ |
| `twig` | `{% for %}` | yes | yes | 0.98 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 0.98 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 0.90 | ✅ |
| `typst` | `#letx` | no | no | 0.95 | ✅ |
| `typst` | `#let` | yes | yes | 0.99 | ✅ |
| `v` | `printlnx` | no | no | 0.95 | ✅ |
| `v` | `println` | yes | yes | 0.95 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.95 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.97 | ✅ |
| `velocity` | `#foreachx` | no | no | 0.97 | ✅ |
| `velocity` | `#foreach` | yes | yes | 0.98 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 0.95 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 0.98 | ✅ |
| `vhdl` | `processx` | no | no | 0.95 | ✅ |
| `vhdl` | `process` | yes | yes | 0.98 | ✅ |
| `vue` | `<templatex>` | no | no | 0.95 | ✅ |
| `vue` | `<template>` | yes | yes | 0.98 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 0.95 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 0.98 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.95 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.90 | ✅ |
