# Hallucination — the questions and the answers

**Date:** 2026-11-12. 102 languages × 2 probes. Both tables are the raw record behind the summary in [`../evidence/hallucination-2026-11-12.md`](../evidence/hallucination-2026-11-12.md); nothing is aggregated away.

**What was asked, once per batch of probes:**

> Given a list of programming-language API names, say which are real and which are invented, with a confidence in [0,1] for each. Answer as JSON.

Each language contributes two names: one **genuine** documented API, and one **fabricated twin** (the same shape with a small, plausible change). The model never sees which is which.

## Who got what wrong

| Model | Answered | Hallucination (fake → "real") | False alarm (real → "fake") | Misses |
| :--- | ---: | ---: | ---: | ---: |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | 182/204 | **0%** (0/91) | 2% (2/91) | 2 |
| `Ornith-1.5-35B-A3B-MLX-4bit` | 204/204 | **0%** (0/102) | 2% (2/102) | 2 |
| `Qwen3.6-35B-A3B-4bit` | 204/204 | **0%** (0/102) | 0% (0/102) | 0 |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | 204/204 | **0%** (0/102) | 0% (0/102) | 0 |
| `gemma-4-26B-A4B-it-heretic-4bit` | 204/204 | **0%** (0/102) | 0% (0/102) | 0 |

**Every miss in this run is a false alarm, not a hallucination.** No model, on any of the 102 languages, called a fabricated name real. The two models that are not at 0% called two *real* APIs fake instead.

## Every miss, with the name and the confidence

| Model | Direction | Language | Name the model judged | Stated confidence |
| :--- | :--- | :--- | :--- | ---: |
| `Qwen3-Coder-30B-A3B-Instruct` | real → "fake" (false alarm) | `qsharp` | `Qubit` | — |
| `Qwen3-Coder-30B-A3B-Instruct` | real → "fake" (false alarm) | `mint` | `component` | — |
| `Ornith-1.5-35B-A3B` | real → "fake" (false alarm) | `qsharp` | `Qubit` | 0.85 |
| `Ornith-1.5-35B-A3B` | real → "fake" (false alarm) | `mint` | `component` | 0.50 |

## The full record, per model

`expected` is whether the name is real; `got_real` is whether the model said it is. They agree unless the row is a miss. `conf` is the confidence the model stated, or `—` when it did not state one.

### `Qwen3-Coder-30B-A3B-Instruct`

182/204 answered, 2 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | — | ✅ |
| `abap` | `WRITE` | yes | yes | — | ✅ |
| `actionscript` | `tracex` | no | no | — | ✅ |
| `actionscript` | `trace` | yes | yes | — | ✅ |
| `ada` | `Put_Linex` | no | no | 1.00 | ✅ |
| `ada` | `Put_Line` | yes | yes | 1.00 | ✅ |
| `apex` | `Database.queryx` | no | no | — | ✅ |
| `apex` | `Database.query` | yes | yes | — | ✅ |
| `asciidoc` | `= Titlex` | no | no | 0.95 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 0.95 | ✅ |
| `bash` | `readx` | no | no | 0.80 | ✅ |
| `bash` | `read` | yes | yes | 0.95 | ✅ |
| `blade` | `@foreachx` | no | no | 0.90 | ✅ |
| `blade` | `@foreach` | yes | yes | 1.00 | ✅ |
| `c` | `memcpyx` | no | no | 1.00 | ✅ |
| `c` | `memcpy` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | — | ✅ |
| `cairo` | `felt252` | yes | yes | — | ✅ |
| `clojure` | `mapx` | no | no | 0.90 | ✅ |
| `clojure` | `map` | yes | yes | 0.90 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 1.00 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 1.00 | ✅ |
| `coffeescript` | `->x` | no | no | — | ✅ |
| `coffeescript` | `->` | yes | yes | — | ✅ |
| `cpp` | `std::vectorx` | no | no | 1.00 | ✅ |
| `cpp` | `std::vector` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | — | ✅ |
| `crystal` | `Array#map` | yes | yes | — | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `dart` | `List.mapx` | no | no | 0.90 | ✅ |
| `dart` | `List.map` | yes | yes | 0.95 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.90 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.90 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.90 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.95 | ✅ |
| `elm` | `List.mapx` | no | no | — | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
| `erb` | `<% %>x` | no | no | 0.90 | ✅ |
| `erb` | `<% %>` | yes | yes | 1.00 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.80 | ✅ |
| `erlang` | `lists:map` | yes | yes | 0.90 | ✅ |
| `fortran` | `allocatex` | no | no | 0.90 | ✅ |
| `fortran` | `allocate` | yes | yes | 1.00 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.80 | ✅ |
| `fsharp` | `List.map` | yes | yes | 0.90 | ✅ |
| `gdscript` | `printx` | no | no | — | ✅ |
| `gdscript` | `print` | yes | yes | — | ✅ |
| `gleam` | `list.mapx` | no | no | — | ✅ |
| `gleam` | `list.map` | yes | yes | — | ✅ |
| `go` | `fmt.Printlnx` | no | no | — | ✅ |
| `go` | `fmt.Println` | yes | yes | — | ✅ |
| `graphviz` | `digraphx` | no | no | 1.00 | ✅ |
| `graphviz` | `digraph` | yes | yes | 0.90 | ✅ |
| `groovy` | `eachx` | no | no | 1.00 | ✅ |
| `groovy` | `each` | yes | yes | 1.00 | ✅ |
| `haml` | `%divx` | no | no | 0.90 | ✅ |
| `haml` | `%div` | yes | yes | 1.00 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.90 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.90 | ✅ |
| `haskell` | `mapx` | no | no | 0.85 | ✅ |
| `haskell` | `map` | yes | yes | 0.90 | ✅ |
| `html` | `<a hrefx>` | no | no | 0.90 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | — | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | — | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | — | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | — | ✅ |
| `json` | `nullx` | no | no | 1.00 | ✅ |
| `json` | `null` | yes | yes | 1.00 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.90 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.90 | ✅ |
| `julia` | `push!` | yes | yes | 0.90 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 0.90 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 0.95 | ✅ |
| `latex` | `\sectionx` | no | no | 0.95 | ✅ |
| `latex` | `\section` | yes | yes | 0.95 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.90 | ✅ |
| `lisp` | `mapcar` | yes | yes | 0.90 | ✅ |
| `livescript` | `->x` | no | no | — | ✅ |
| `livescript` | `->` | yes | yes | — | ✅ |
| `lua` | `table.insertx` | no | no | 1.00 | ✅ |
| `lua` | `table.insert` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 1.00 | ✅ |
| `matlab` | `zeros` | yes | yes | 1.00 | ✅ |
| `mermaid` | `graph TDx` | no | no | 1.00 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | — | ✅ |
| `mint` | `component` | yes | no | — | ❌ |
| `mojo` | `fnx` | no | no | — | ✅ |
| `mojo` | `fn` | yes | yes | — | ✅ |
| `move` | `vectorx` | no | no | — | ✅ |
| `move` | `vector` | yes | yes | — | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.90 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.90 | ✅ |
| `nim` | `seqx` | no | no | — | ✅ |
| `nim` | `seq` | yes | yes | — | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.80 | ✅ |
| `ocaml` | `List.map` | yes | yes | 0.90 | ✅ |
| `odin` | `fmt.printlnx` | no | no | — | ✅ |
| `odin` | `fmt.println` | yes | yes | — | ✅ |
| `pascal` | `writelnx` | no | no | 0.90 | ✅ |
| `pascal` | `writeln` | yes | yes | 1.00 | ✅ |
| `perl` | `pushx` | no | no | 0.80 | ✅ |
| `perl` | `push` | yes | yes | 0.95 | ✅ |
| `php` | `array_mapx` | no | no | 0.90 | ✅ |
| `php` | `array_map` | yes | yes | 0.95 | ✅ |
| `plantuml` | `@startumlx` | no | no | 1.00 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | — | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | — | ✅ |
| `prolog` | `findallx` | no | no | 0.80 | ✅ |
| `prolog` | `findall` | yes | yes | 0.90 | ✅ |
| `pug` | `extendsx` | no | no | 0.90 | ✅ |
| `pug` | `extends` | yes | yes | 0.90 | ✅ |
| `purescript` | `mapx` | no | no | — | ✅ |
| `purescript` | `map` | yes | yes | — | ✅ |
| `python` | `functools.reducex` | no | no | 0.90 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | — | ✅ |
| `qsharp` | `Qubit` | yes | no | — | ❌ |
| `r` | `data.framex` | no | no | 1.00 | ✅ |
| `r` | `data.frame` | yes | yes | 1.00 | ✅ |
| `reasonml` | `List.mapx` | no | no | — | ✅ |
| `reasonml` | `List.map` | yes | yes | — | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | — | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | — | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 0.90 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 0.95 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.mapx` | no | no | 0.90 | ✅ |
| `scala` | `List.map` | yes | yes | 0.95 | ✅ |
| `scheme` | `mapx` | no | no | 0.90 | ✅ |
| `scheme` | `map` | yes | yes | 0.90 | ✅ |
| `slim` | `.classx` | no | no | 0.90 | ✅ |
| `slim` | `.class` | yes | yes | 1.00 | ✅ |
| `solidity` | `mappingx` | no | no | 1.00 | ✅ |
| `solidity` | `mapping` | yes | yes | 1.00 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.90 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.90 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | — | ✅ |
| `tex` | `\defx` | no | no | 1.00 | ✅ |
| `tex` | `\def` | yes | yes | 0.90 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | — | ✅ |
| `tsql` | `TOP` | yes | yes | — | ✅ |
| `tsx` | `useStatex` | no | no | 0.90 | ✅ |
| `tsx` | `useState` | yes | yes | 0.90 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 1.00 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | — | ✅ |
| `v` | `println` | yes | yes | — | ✅ |
| `vba` | `MsgBoxx` | no | no | — | ✅ |
| `vba` | `MsgBox` | yes | yes | — | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 1.00 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 1.00 | ✅ |
| `vhdl` | `processx` | no | no | 1.00 | ✅ |
| `vhdl` | `process` | yes | yes | 1.00 | ✅ |
| `vue` | `<template>` | yes | yes | 0.90 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |

### `Ornith-1.5-35B-A3B`

204/204 answered, 2 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.85 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.90 | ✅ |
| `actionscript` | `tracex` | no | no | 0.90 | ✅ |
| `actionscript` | `trace` | yes | yes | 0.92 | ✅ |
| `ada` | `Put_Linex` | no | no | 0.98 | ✅ |
| `ada` | `Put_Line` | yes | yes | 0.98 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.95 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.98 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `assembly` | `movx` | no | no | 0.90 | ✅ |
| `assembly` | `mov` | yes | yes | 0.98 | ✅ |
| `bash` | `readx` | no | no | 0.95 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 0.95 | ✅ |
| `blade` | `@foreach` | yes | yes | 0.90 | ✅ |
| `c` | `memcpyx` | no | no | 1.00 | ✅ |
| `c` | `memcpy` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 0.90 | ✅ |
| `cairo` | `felt252` | yes | yes | 0.90 | ✅ |
| `clojure` | `mapx` | no | no | 0.95 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 0.98 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 0.98 | ✅ |
| `coffeescript` | `->x` | no | no | 0.85 | ✅ |
| `coffeescript` | `->` | yes | yes | 0.92 | ✅ |
| `cpp` | `std::vectorx` | no | no | 1.00 | ✅ |
| `cpp` | `std::vector` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.90 | ✅ |
| `crystal` | `Array#map` | yes | yes | 0.90 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 0.98 | ✅ |
| `css` | `display: flex` | yes | yes | 0.99 | ✅ |
| `dart` | `List.mapx` | no | no | 0.97 | ✅ |
| `dart` | `List.map` | yes | yes | 0.98 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.98 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.98 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.97 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.98 | ✅ |
| `elm` | `List.mapx` | no | no | 0.90 | ✅ |
| `elm` | `List.map` | yes | yes | 0.98 | ✅ |
| `erb` | `<% %>x` | no | no | 0.95 | ✅ |
| `erb` | `<% %>` | yes | yes | 0.95 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.95 | ✅ |
| `erlang` | `lists:map` | yes | yes | 1.00 | ✅ |
| `fortran` | `allocatex` | no | no | 0.98 | ✅ |
| `fortran` | `allocate` | yes | yes | 0.98 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.95 | ✅ |
| `fsharp` | `List.map` | yes | yes | 1.00 | ✅ |
| `gdscript` | `printx` | no | no | 0.95 | ✅ |
| `gdscript` | `print` | yes | yes | 0.98 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.90 | ✅ |
| `gleam` | `list.map` | yes | yes | 0.90 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 1.00 | ✅ |
| `go` | `fmt.Println` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.98 | ✅ |
| `graphviz` | `digraph` | yes | yes | 0.98 | ✅ |
| `groovy` | `eachx` | no | no | 0.98 | ✅ |
| `groovy` | `each` | yes | yes | 0.98 | ✅ |
| `haml` | `%divx` | no | no | 0.90 | ✅ |
| `haml` | `%div` | yes | yes | 0.85 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.98 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.98 | ✅ |
| `haskell` | `mapx` | no | no | 0.92 | ✅ |
| `haskell` | `map` | yes | yes | 0.98 | ✅ |
| `html` | `<a hrefx>` | no | no | 0.98 | ✅ |
| `html` | `<a href>` | yes | yes | 0.99 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 1.00 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 1.00 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 1.00 | ✅ |
| `jinja` | `{% forx %}` | no | no | 0.95 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 0.95 | ✅ |
| `json` | `nullx` | no | no | 0.98 | ✅ |
| `json` | `null` | yes | yes | 0.99 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.98 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.98 | ✅ |
| `julia` | `pushx!` | no | no | 0.95 | ✅ |
| `julia` | `push!` | yes | yes | 1.00 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 1.00 | ✅ |
| `latex` | `\sectionx` | no | no | 1.00 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.95 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 0.95 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.90 | ✅ |
| `lisp` | `mapcar` | yes | yes | 0.95 | ✅ |
| `livescript` | `->x` | no | no | 0.85 | ✅ |
| `livescript` | `->` | yes | yes | 0.92 | ✅ |
| `lua` | `table.insertx` | no | no | 0.97 | ✅ |
| `lua` | `table.insert` | yes | yes | 0.98 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 0.97 | ✅ |
| `matlab` | `zeros` | yes | yes | 0.98 | ✅ |
| `mermaid` | `graph TDx` | no | no | 0.95 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 0.95 | ✅ |
| `mint` | `componentx` | no | no | 0.60 | ✅ |
| `mint` | `component` | yes | no | 0.50 | ❌ |
| `mojo` | `fnx` | no | no | 0.75 | ✅ |
| `mojo` | `fn` | yes | yes | 0.90 | ✅ |
| `move` | `vectorx` | no | no | 0.85 | ✅ |
| `move` | `vector` | yes | yes | 0.85 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.98 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.98 | ✅ |
| `nim` | `seqx` | no | no | 0.90 | ✅ |
| `nim` | `seq` | yes | yes | 0.95 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 0.95 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 0.95 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.95 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.98 | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.95 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.85 | ✅ |
| `odin` | `fmt.println` | yes | yes | 0.85 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.95 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 0.98 | ✅ |
| `pascal` | `writelnx` | no | no | 0.98 | ✅ |
| `pascal` | `writeln` | yes | yes | 0.98 | ✅ |
| `perl` | `pushx` | no | no | 0.95 | ✅ |
| `perl` | `push` | yes | yes | 0.97 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.98 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 0.98 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.95 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.98 | ✅ |
| `prolog` | `findallx` | no | no | 0.90 | ✅ |
| `prolog` | `findall` | yes | yes | 0.95 | ✅ |
| `pug` | `extendsx` | no | no | 0.98 | ✅ |
| `pug` | `extends` | yes | yes | 0.95 | ✅ |
| `purescript` | `mapx` | no | no | 0.95 | ✅ |
| `purescript` | `map` | yes | yes | 0.95 | ✅ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 0.85 | ✅ |
| `qsharp` | `Qubit` | yes | no | 0.85 | ❌ |
| `r` | `data.framex` | no | no | 0.97 | ✅ |
| `r` | `data.frame` | yes | yes | 0.98 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.90 | ✅ |
| `reasonml` | `List.map` | yes | yes | 0.92 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.80 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 0.80 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 0.97 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 0.98 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.mapx` | no | no | 0.97 | ✅ |
| `scala` | `List.map` | yes | yes | 0.98 | ✅ |
| `scheme` | `mapx` | no | no | 0.95 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 0.90 | ✅ |
| `slim` | `.class` | yes | yes | 0.85 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.90 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 0.98 | ✅ |
| `solidity` | `mapping` | yes | yes | 0.98 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.98 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.98 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 0.95 | ✅ |
| `tex` | `\def` | yes | yes | 0.98 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 0.95 | ✅ |
| `toml` | `[table]` | yes | yes | 0.98 | ✅ |
| `tsql` | `TOPx` | no | no | 0.90 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.95 | ✅ |
| `tsx` | `useStatex` | no | no | 0.98 | ✅ |
| `tsx` | `useState` | yes | yes | 0.98 | ✅ |
| `twig` | `{% forx %}` | no | no | 0.95 | ✅ |
| `twig` | `{% for %}` | yes | yes | 0.95 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 0.95 | ✅ |
| `typst` | `#let` | yes | yes | 0.98 | ✅ |
| `v` | `printlnx` | no | no | 0.85 | ✅ |
| `v` | `println` | yes | yes | 0.85 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.90 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.95 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 0.98 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 0.98 | ✅ |
| `vhdl` | `processx` | no | no | 0.98 | ✅ |
| `vhdl` | `process` | yes | yes | 0.98 | ✅ |
| `vue` | `<templatex>` | no | no | 0.95 | ✅ |
| `vue` | `<template>` | yes | yes | 0.95 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 0.95 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 0.95 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.90 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.92 | ✅ |

### `Qwen3.6-35B-A3B`

204/204 answered, 0 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.95 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.95 | ✅ |
| `actionscript` | `tracex` | no | no | 0.95 | ✅ |
| `actionscript` | `trace` | yes | yes | 0.95 | ✅ |
| `ada` | `Put_Linex` | no | no | 1.00 | ✅ |
| `ada` | `Put_Line` | yes | yes | 1.00 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.95 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.95 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `assembly` | `movx` | no | no | 0.95 | ✅ |
| `assembly` | `mov` | yes | yes | 0.99 | ✅ |
| `bash` | `readx` | no | no | 1.00 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 1.00 | ✅ |
| `blade` | `@foreach` | yes | yes | 1.00 | ✅ |
| `c` | `memcpyx` | no | no | 1.00 | ✅ |
| `c` | `memcpy` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 0.95 | ✅ |
| `cairo` | `felt252` | yes | yes | 1.00 | ✅ |
| `clojure` | `mapx` | no | no | 1.00 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 1.00 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 1.00 | ✅ |
| `coffeescript` | `->x` | no | no | 0.95 | ✅ |
| `coffeescript` | `->` | yes | yes | 0.95 | ✅ |
| `cpp` | `std::vectorx` | no | no | 1.00 | ✅ |
| `cpp` | `std::vector` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.95 | ✅ |
| `crystal` | `Array#map` | yes | yes | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.mapx` | no | no | 0.95 | ✅ |
| `dart` | `List.map` | yes | yes | 0.99 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.95 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.95 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.95 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.99 | ✅ |
| `elm` | `List.mapx` | no | no | 0.95 | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
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
| `gdscript` | `printx` | no | no | 0.95 | ✅ |
| `gdscript` | `print` | yes | yes | 0.95 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.95 | ✅ |
| `gleam` | `list.map` | yes | yes | 1.00 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 1.00 | ✅ |
| `go` | `fmt.Println` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 1.00 | ✅ |
| `graphviz` | `digraph` | yes | yes | 1.00 | ✅ |
| `groovy` | `eachx` | no | no | 1.00 | ✅ |
| `groovy` | `each` | yes | yes | 1.00 | ✅ |
| `haml` | `%divx` | no | no | 1.00 | ✅ |
| `haml` | `%div` | yes | yes | 1.00 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.95 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.95 | ✅ |
| `haskell` | `mapx` | no | no | 0.95 | ✅ |
| `haskell` | `map` | yes | yes | 0.99 | ✅ |
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
| `jsx` | `React.createElementx` | no | no | 0.95 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.95 | ✅ |
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
| `livescript` | `->x` | no | no | 0.95 | ✅ |
| `livescript` | `->` | yes | yes | 0.95 | ✅ |
| `lua` | `table.insertx` | no | no | 1.00 | ✅ |
| `lua` | `table.insert` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 1.00 | ✅ |
| `matlab` | `zeros` | yes | yes | 1.00 | ✅ |
| `mermaid` | `graph TDx` | no | no | 1.00 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | 0.95 | ✅ |
| `mint` | `component` | yes | yes | 0.95 | ✅ |
| `mojo` | `fnx` | no | no | 0.95 | ✅ |
| `mojo` | `fn` | yes | yes | 1.00 | ✅ |
| `move` | `vectorx` | no | no | 0.95 | ✅ |
| `move` | `vector` | yes | yes | 1.00 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.95 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.95 | ✅ |
| `nim` | `seqx` | no | no | 0.95 | ✅ |
| `nim` | `seq` | yes | yes | 1.00 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 1.00 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.95 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.99 | ✅ |
| `ocaml` | `List.mapx` | no | no | 1.00 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.95 | ✅ |
| `odin` | `fmt.println` | yes | yes | 1.00 | ✅ |
| `orgmode` | `* Headingx` | no | no | 1.00 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 1.00 | ✅ |
| `pascal` | `writelnx` | no | no | 1.00 | ✅ |
| `pascal` | `writeln` | yes | yes | 1.00 | ✅ |
| `perl` | `pushx` | no | no | 0.95 | ✅ |
| `perl` | `push` | yes | yes | 0.99 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 1.00 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.95 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.95 | ✅ |
| `prolog` | `findallx` | no | no | 1.00 | ✅ |
| `prolog` | `findall` | yes | yes | 1.00 | ✅ |
| `pug` | `extendsx` | no | no | 0.95 | ✅ |
| `pug` | `extends` | yes | yes | 0.95 | ✅ |
| `purescript` | `mapx` | no | no | 0.95 | ✅ |
| `purescript` | `map` | yes | yes | 0.95 | ✅ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 0.95 | ✅ |
| `qsharp` | `Qubit` | yes | yes | 0.95 | ✅ |
| `r` | `data.framex` | no | no | 1.00 | ✅ |
| `r` | `data.frame` | yes | yes | 1.00 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.95 | ✅ |
| `reasonml` | `List.map` | yes | yes | 0.95 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.95 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 0.95 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.mapx` | no | no | 0.95 | ✅ |
| `scala` | `List.map` | yes | yes | 0.99 | ✅ |
| `scheme` | `mapx` | no | no | 1.00 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 1.00 | ✅ |
| `slim` | `.class` | yes | yes | 1.00 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.95 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 1.00 | ✅ |
| `solidity` | `mapping` | yes | yes | 1.00 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.95 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.95 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 1.00 | ✅ |
| `tex` | `\def` | yes | yes | 1.00 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `toml` | `[table]` | yes | yes | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | 0.95 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.95 | ✅ |
| `tsx` | `useStatex` | no | no | 0.95 | ✅ |
| `tsx` | `useState` | yes | yes | 0.95 | ✅ |
| `twig` | `{% forx %}` | no | no | 1.00 | ✅ |
| `twig` | `{% for %}` | yes | yes | 1.00 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 1.00 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | 0.95 | ✅ |
| `v` | `println` | yes | yes | 1.00 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.95 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.95 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 1.00 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 1.00 | ✅ |
| `vhdl` | `processx` | no | no | 1.00 | ✅ |
| `vhdl` | `process` | yes | yes | 1.00 | ✅ |
| `vue` | `<templatex>` | no | no | 0.95 | ✅ |
| `vue` | `<template>` | yes | yes | 0.95 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.95 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.99 | ✅ |

### `Qwen3.6-35B-A3B-Uncensored-Heretic`

204/204 answered, 0 missed.

| Language | Name | Real? | Model said | Confidence | Correct |
| :--- | :--- | :--- | :--- | ---: | :---: |
| `abap` | `WRITEx` | no | no | 0.95 | ✅ |
| `abap` | `WRITE` | yes | yes | 0.95 | ✅ |
| `actionscript` | `tracex` | no | no | 0.95 | ✅ |
| `actionscript` | `trace` | yes | yes | 0.95 | ✅ |
| `ada` | `Put_Linex` | no | no | 0.95 | ✅ |
| `ada` | `Put_Line` | yes | yes | 0.95 | ✅ |
| `apex` | `Database.queryx` | no | no | 0.95 | ✅ |
| `apex` | `Database.query` | yes | yes | 0.95 | ✅ |
| `asciidoc` | `= Titlex` | no | no | 1.00 | ✅ |
| `asciidoc` | `= Title` | yes | yes | 1.00 | ✅ |
| `assembly` | `movx` | no | no | 0.95 | ✅ |
| `assembly` | `mov` | yes | yes | 0.99 | ✅ |
| `bash` | `readx` | no | no | 1.00 | ✅ |
| `bash` | `read` | yes | yes | 1.00 | ✅ |
| `blade` | `@foreachx` | no | no | 0.95 | ✅ |
| `blade` | `@foreach` | yes | yes | 0.95 | ✅ |
| `c` | `memcpyx` | no | no | 1.00 | ✅ |
| `c` | `memcpy` | yes | yes | 1.00 | ✅ |
| `cairo` | `felt252x` | no | no | 0.95 | ✅ |
| `cairo` | `felt252` | yes | yes | 1.00 | ✅ |
| `clojure` | `mapx` | no | no | 0.95 | ✅ |
| `clojure` | `map` | yes | yes | 1.00 | ✅ |
| `cobol` | `DISPLAYx` | no | no | 0.95 | ✅ |
| `cobol` | `DISPLAY` | yes | yes | 0.95 | ✅ |
| `coffeescript` | `->x` | no | no | 0.95 | ✅ |
| `coffeescript` | `->` | yes | yes | 0.95 | ✅ |
| `cpp` | `std::vectorx` | no | no | 1.00 | ✅ |
| `cpp` | `std::vector` | yes | yes | 1.00 | ✅ |
| `crystal` | `Array#mapx` | no | no | 0.95 | ✅ |
| `crystal` | `Array#map` | yes | yes | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Selectx` | no | no | 1.00 | ✅ |
| `csharp` | `System.Linq.Enumerable.Select` | yes | yes | 1.00 | ✅ |
| `css` | `display: flexx` | no | no | 1.00 | ✅ |
| `css` | `display: flex` | yes | yes | 1.00 | ✅ |
| `dart` | `List.mapx` | no | no | 0.95 | ✅ |
| `dart` | `List.map` | yes | yes | 0.99 | ✅ |
| `ejs` | `<% %>x` | no | no | 0.95 | ✅ |
| `ejs` | `<% %>` | yes | yes | 0.95 | ✅ |
| `elixir` | `Enum.mapx` | no | no | 0.95 | ✅ |
| `elixir` | `Enum.map` | yes | yes | 0.99 | ✅ |
| `elm` | `List.mapx` | no | no | 0.95 | ✅ |
| `elm` | `List.map` | yes | yes | 0.95 | ✅ |
| `erb` | `<% %>x` | no | no | 0.95 | ✅ |
| `erb` | `<% %>` | yes | yes | 0.95 | ✅ |
| `erlang` | `lists:mapx` | no | no | 0.95 | ✅ |
| `erlang` | `lists:map` | yes | yes | 1.00 | ✅ |
| `fortran` | `allocatex` | no | no | 0.95 | ✅ |
| `fortran` | `allocate` | yes | yes | 0.95 | ✅ |
| `freemarker` | `<#listx>` | no | no | 1.00 | ✅ |
| `freemarker` | `<#list>` | yes | yes | 1.00 | ✅ |
| `fsharp` | `List.mapx` | no | no | 0.95 | ✅ |
| `fsharp` | `List.map` | yes | yes | 1.00 | ✅ |
| `gdscript` | `printx` | no | no | 0.95 | ✅ |
| `gdscript` | `print` | yes | yes | 0.95 | ✅ |
| `gleam` | `list.mapx` | no | no | 0.95 | ✅ |
| `gleam` | `list.map` | yes | yes | 1.00 | ✅ |
| `go` | `fmt.Printlnx` | no | no | 1.00 | ✅ |
| `go` | `fmt.Println` | yes | yes | 1.00 | ✅ |
| `graphviz` | `digraphx` | no | no | 0.95 | ✅ |
| `graphviz` | `digraph` | yes | yes | 1.00 | ✅ |
| `groovy` | `eachx` | no | no | 0.95 | ✅ |
| `groovy` | `each` | yes | yes | 0.95 | ✅ |
| `haml` | `%divx` | no | no | 0.95 | ✅ |
| `haml` | `%div` | yes | yes | 0.95 | ✅ |
| `handlebars` | `{{#eachx}}` | no | no | 0.95 | ✅ |
| `handlebars` | `{{#each}}` | yes | yes | 0.95 | ✅ |
| `haskell` | `mapx` | no | no | 0.95 | ✅ |
| `haskell` | `map` | yes | yes | 0.99 | ✅ |
| `html` | `<a hrefx>` | no | no | 1.00 | ✅ |
| `html` | `<a href>` | yes | yes | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.mapx` | no | no | 1.00 | ✅ |
| `java` | `java.util.stream.Stream.map` | yes | yes | 1.00 | ✅ |
| `javascript` | `Array.prototype.mapx` | no | no | 1.00 | ✅ |
| `javascript` | `Array.prototype.map` | yes | yes | 1.00 | ✅ |
| `jinja` | `{% forx %}` | no | no | 0.95 | ✅ |
| `jinja` | `{% for %}` | yes | yes | 0.95 | ✅ |
| `json` | `nullx` | no | no | 1.00 | ✅ |
| `json` | `null` | yes | yes | 1.00 | ✅ |
| `jsx` | `React.createElementx` | no | no | 0.95 | ✅ |
| `jsx` | `React.createElement` | yes | yes | 0.95 | ✅ |
| `julia` | `pushx!` | no | no | 0.95 | ✅ |
| `julia` | `push!` | yes | yes | 1.00 | ✅ |
| `kotlin` | `listOfx` | no | no | 1.00 | ✅ |
| `kotlin` | `listOf` | yes | yes | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actualx` | no | no | 1.00 | ✅ |
| `kotlin-multiplatform` | `expect/actual` | yes | yes | 1.00 | ✅ |
| `latex` | `\sectionx` | no | no | 1.00 | ✅ |
| `latex` | `\section` | yes | yes | 1.00 | ✅ |
| `liquid` | `{% ifx %}` | no | no | 0.95 | ✅ |
| `liquid` | `{% if %}` | yes | yes | 0.95 | ✅ |
| `lisp` | `mapcarx` | no | no | 0.95 | ✅ |
| `lisp` | `mapcar` | yes | yes | 1.00 | ✅ |
| `livescript` | `->x` | no | no | 0.95 | ✅ |
| `livescript` | `->` | yes | yes | 0.95 | ✅ |
| `lua` | `table.insertx` | no | no | 1.00 | ✅ |
| `lua` | `table.insert` | yes | yes | 1.00 | ✅ |
| `markdown` | `## headingx` | no | no | 1.00 | ✅ |
| `markdown` | `## heading` | yes | yes | 1.00 | ✅ |
| `matlab` | `zerosx` | no | no | 1.00 | ✅ |
| `matlab` | `zeros` | yes | yes | 1.00 | ✅ |
| `mermaid` | `graph TDx` | no | no | 0.95 | ✅ |
| `mermaid` | `graph TD` | yes | yes | 1.00 | ✅ |
| `mint` | `componentx` | no | no | 0.95 | ✅ |
| `mint` | `component` | yes | yes | 0.95 | ✅ |
| `mojo` | `fnx` | no | no | 0.95 | ✅ |
| `mojo` | `fn` | yes | yes | 1.00 | ✅ |
| `move` | `vectorx` | no | no | 0.95 | ✅ |
| `move` | `vector` | yes | yes | 1.00 | ✅ |
| `mustache` | `{{#sectionx}}` | no | no | 0.95 | ✅ |
| `mustache` | `{{#section}}` | yes | yes | 0.95 | ✅ |
| `nim` | `seqx` | no | no | 0.95 | ✅ |
| `nim` | `seq` | yes | yes | 1.00 | ✅ |
| `nunjucks` | `{% forx %}` | no | no | 0.95 | ✅ |
| `nunjucks` | `{% for %}` | yes | yes | 0.95 | ✅ |
| `objective-c` | `NSArrayx` | no | no | 0.95 | ✅ |
| `objective-c` | `NSArray` | yes | yes | 0.99 | ✅ |
| `ocaml` | `List.mapx` | no | no | 0.95 | ✅ |
| `ocaml` | `List.map` | yes | yes | 1.00 | ✅ |
| `odin` | `fmt.printlnx` | no | no | 0.95 | ✅ |
| `odin` | `fmt.println` | yes | yes | 1.00 | ✅ |
| `orgmode` | `* Headingx` | no | no | 0.95 | ✅ |
| `orgmode` | `* Heading` | yes | yes | 1.00 | ✅ |
| `pascal` | `writelnx` | no | no | 0.95 | ✅ |
| `pascal` | `writeln` | yes | yes | 0.95 | ✅ |
| `perl` | `pushx` | no | no | 0.95 | ✅ |
| `perl` | `push` | yes | yes | 0.99 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 0.95 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 0.95 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINE` | yes | yes | 0.95 | ✅ |
| `prolog` | `findallx` | no | no | 0.95 | ✅ |
| `prolog` | `findall` | yes | yes | 1.00 | ✅ |
| `pug` | `extendsx` | no | no | 0.95 | ✅ |
| `pug` | `extends` | yes | yes | 0.95 | ✅ |
| `purescript` | `mapx` | no | no | 0.95 | ✅ |
| `purescript` | `map` | yes | yes | 0.95 | ✅ |
| `python` | `functools.reducex` | no | no | 1.00 | ✅ |
| `python` | `functools.reduce` | yes | yes | 1.00 | ✅ |
| `qsharp` | `Qubitx` | no | no | 0.95 | ✅ |
| `qsharp` | `Qubit` | yes | yes | 0.95 | ✅ |
| `r` | `data.framex` | no | no | 1.00 | ✅ |
| `r` | `data.frame` | yes | yes | 1.00 | ✅ |
| `reasonml` | `List.mapx` | no | no | 0.95 | ✅ |
| `reasonml` | `List.map` | yes | yes | 0.95 | ✅ |
| `rescript` | `Belt.Array.mapx` | no | no | 0.95 | ✅ |
| `rescript` | `Belt.Array.map` | yes | yes | 0.95 | ✅ |
| `rmarkdown` | ````{rx}` | no | no | 1.00 | ✅ |
| `rmarkdown` | ````{r}` | yes | yes | 1.00 | ✅ |
| `rst` | `.. code-blockx::` | no | no | 1.00 | ✅ |
| `rst` | `.. code-block::` | yes | yes | 1.00 | ✅ |
| `ruby` | `Enumerable#mapx` | no | no | 1.00 | ✅ |
| `ruby` | `Enumerable#map` | yes | yes | 1.00 | ✅ |
| `rust` | `Vec::pushx` | no | no | 1.00 | ✅ |
| `rust` | `Vec::push` | yes | yes | 1.00 | ✅ |
| `scala` | `List.mapx` | no | no | 0.95 | ✅ |
| `scala` | `List.map` | yes | yes | 0.99 | ✅ |
| `scheme` | `mapx` | no | no | 0.95 | ✅ |
| `scheme` | `map` | yes | yes | 1.00 | ✅ |
| `slim` | `.classx` | no | no | 0.95 | ✅ |
| `slim` | `.class` | yes | yes | 0.95 | ✅ |
| `smalltalk` | `dox:` | no | no | 0.95 | ✅ |
| `smalltalk` | `do:` | yes | yes | 0.95 | ✅ |
| `solidity` | `mappingx` | no | no | 0.95 | ✅ |
| `solidity` | `mapping` | yes | yes | 0.95 | ✅ |
| `sql` | `GROUP BYx` | no | no | 1.00 | ✅ |
| `sql` | `GROUP BY` | yes | yes | 1.00 | ✅ |
| `svelte` | `{#eachx}` | no | no | 0.95 | ✅ |
| `svelte` | `{#each}` | yes | yes | 0.95 | ✅ |
| `swift` | `Array.mapx` | no | no | 1.00 | ✅ |
| `swift` | `Array.map` | yes | yes | 1.00 | ✅ |
| `tex` | `\defx` | no | no | 0.95 | ✅ |
| `tex` | `\def` | yes | yes | 1.00 | ✅ |
| `thymeleaf` | `th:textx` | no | no | 1.00 | ✅ |
| `thymeleaf` | `th:text` | yes | yes | 1.00 | ✅ |
| `toml` | `[tablex]` | no | no | 1.00 | ✅ |
| `toml` | `[table]` | yes | yes | 1.00 | ✅ |
| `tsql` | `TOPx` | no | no | 0.95 | ✅ |
| `tsql` | `TOP` | yes | yes | 0.95 | ✅ |
| `tsx` | `useStatex` | no | no | 0.95 | ✅ |
| `tsx` | `useState` | yes | yes | 0.95 | ✅ |
| `twig` | `{% forx %}` | no | no | 0.95 | ✅ |
| `twig` | `{% for %}` | yes | yes | 0.95 | ✅ |
| `typescript` | `Array.prototype.reducex` | no | no | 1.00 | ✅ |
| `typescript` | `Array.prototype.reduce` | yes | yes | 1.00 | ✅ |
| `typst` | `#letx` | no | no | 0.95 | ✅ |
| `typst` | `#let` | yes | yes | 1.00 | ✅ |
| `v` | `printlnx` | no | no | 0.95 | ✅ |
| `v` | `println` | yes | yes | 1.00 | ✅ |
| `vba` | `MsgBoxx` | no | no | 0.95 | ✅ |
| `vba` | `MsgBox` | yes | yes | 0.95 | ✅ |
| `velocity` | `#foreachx` | no | no | 1.00 | ✅ |
| `velocity` | `#foreach` | yes | yes | 1.00 | ✅ |
| `verilog` | `always @(posedgex)` | no | no | 0.95 | ✅ |
| `verilog` | `always @(posedge)` | yes | yes | 0.95 | ✅ |
| `vhdl` | `processx` | no | no | 0.95 | ✅ |
| `vhdl` | `process` | yes | yes | 0.95 | ✅ |
| `vue` | `<templatex>` | no | no | 0.95 | ✅ |
| `vue` | `<template>` | yes | yes | 0.95 | ✅ |
| `yaml` | `anchorsx (&)` | no | no | 1.00 | ✅ |
| `yaml` | `anchors (&)` | yes | yes | 1.00 | ✅ |
| `zig` | `std.ArrayListx` | no | no | 0.95 | ✅ |
| `zig` | `std.ArrayList` | yes | yes | 0.99 | ✅ |

### `gemma-4-26B-A4B-it-heretic`

204/204 answered, 0 missed.

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
| `elm` | `List.mapx` | no | no | 1.00 | ✅ |
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
| `gdscript` | `printx` | no | no | 1.00 | ✅ |
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
| `pascal` | `writeln` | yes | yes | 1.00 | ✅ |
| `perl` | `pushx` | no | no | 1.00 | ✅ |
| `perl` | `push` | yes | yes | 1.00 | ✅ |
| `php` | `array_mapx` | no | no | 1.00 | ✅ |
| `php` | `array_map` | yes | yes | 1.00 | ✅ |
| `plantuml` | `@startumlx` | no | no | 1.00 | ✅ |
| `plantuml` | `@startuml` | yes | yes | 1.00 | ✅ |
| `plsql` | `DBMS_OUTPUT.PUT_LINEx` | no | no | 1.00 | ✅ |
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
| `smalltalk` | `dox:` | no | no | 1.00 | ✅ |
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
| `tsql` | `TOPx` | no | no | 1.00 | ✅ |
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
| `vba` | `MsgBoxx` | no | no | 1.00 | ✅ |
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
