# Language corpus

The 102 languages probed by [`hallucination-test.py`](../../scripts/measure/hallucination-test.py), grouped by kind. For each, the `real` column is a genuine, well-known API or feature; the harness derives a fabricated twin by appending `x` to the last word (e.g. `functools.reduce` → `functools.reducex`) and asks the model which is real. The corpus is in [`../../data/languages.json`](../../data/languages.json).

Total: **102 languages**, 204 probes per model.

## compiled (34)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| ABAP | `.abap` | `WRITE` |
| ActionScript | `.as` | `trace` |
| Ada | `.adb` | `Put_Line` |
| Apex | `.cls` | `Database.query` |
| Assembly | `.s` | `mov` |
| C | `.c` | `memcpy` |
| C# | `.cs` | `System.Linq.Enumerable.Select` |
| C++ | `.cpp` | `std::vector` |
| COBOL | `.cob` | `DISPLAY` |
| CoffeeScript | `.coffee` | `->` |
| Crystal | `.cr` | `Array#map` |
| Dart | `.dart` | `List.map` |
| Elixir | `.ex` | `Enum.map` |
| Fortran | `.f90` | `allocate` |
| Go | `.go` | `fmt.Println` |
| Groovy | `.groovy` | `each` |
| Java | `.java` | `java.util.stream.Stream.map` |
| Kotlin | `.kt` | `listOf` |
| Kotlin Multiplatform | `.kt` | `expect/actual` |
| LiveScript | `.ls` | `->` |
| Mint | `.mint` | `component` |
| Mojo | `.mojo` | `fn` |
| Nim | `.nim` | `seq` |
| Objective-C | `.m` | `NSArray` |
| Odin | `.odin` | `fmt.println` |
| Pascal | `.pas` | `writeln` |
| Q# | `.qs` | `Qubit` |
| ReScript | `.res` | `Belt.Array.map` |
| Rust | `.rs` | `Vec::push` |
| Scala | `.scala` | `List.map` |
| Swift | `.swift` | `Array.map` |
| TypeScript | `.ts` | `Array.prototype.reduce` |
| V | `.v` | `println` |
| Zig | `.zig` | `std.ArrayList` |

## template (19)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Blade | `.blade.php` | `@foreach` |
| EJS | `.ejs` | `<% %>` |
| ERB | `.erb` | `<% %>` |
| FreeMarker | `.ftl` | `<#list>` |
| Haml | `.haml` | `%div` |
| Handlebars | `.hbs` | `{{#each}}` |
| Jinja | `.j2` | `{% for %}` |
| JSX | `.jsx` | `React.createElement` |
| Liquid | `.liquid` | `{% if %}` |
| Mustache | `.mustache` | `{{#section}}` |
| Nunjucks | `.njk` | `{% for %}` |
| Pug | `.pug` | `extends` |
| Slim | `.slim` | `.class` |
| Svelte | `.svelte` | `{#each}` |
| Thymeleaf | `.html` | `th:text` |
| TSX | `.tsx` | `useState` |
| Twig | `.twig` | `{% for %}` |
| Velocity | `.vm` | `#foreach` |
| Vue | `.vue` | `<template>` |

## interpreted (12)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| GDScript | `.gd` | `print` |
| JavaScript | `.js` | `Array.prototype.map` |
| Julia | `.jl` | `push!` |
| Lua | `.lua` | `table.insert` |
| MATLAB | `.m` | `zeros` |
| Perl | `.pl` | `push` |
| PHP | `.php` | `array_map` |
| Python | `.py` | `functools.reduce` |
| R | `.r` | `data.frame` |
| Ruby | `.rb` | `Enumerable#map` |
| Smalltalk | `.st` | `do:` |
| VBA | `.bas` | `MsgBox` |

## functional (11)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Clojure | `.clj` | `map` |
| Common Lisp | `.lisp` | `mapcar` |
| Elm | `.elm` | `List.map` |
| Erlang | `.erl` | `lists:map` |
| F# | `.fs` | `List.map` |
| Gleam | `.gleam` | `list.map` |
| Haskell | `.hs` | `map` |
| OCaml | `.ml` | `List.map` |
| PureScript | `.purs` | `map` |
| ReasonML | `.re` | `List.map` |
| Scheme | `.scm` | `map` |

## docs (8)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| AsciiDoc | `.adoc` | `= Title` |
| LaTeX | `.tex` | `\section` |
| Markdown | `.md` | `## heading` |
| Org-mode | `.org` | `* Heading` |
| reStructuredText | `.rst` | `.. code-block::` |
| RMarkdown | `.rmd` | ````{r}` |
| TeX | `.tex` | `\def` |
| Typst | `.typ` | `#let` |

## blockchain (3)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Cairo | `.cairo` | `felt252` |
| Move | `.move` | `vector` |
| Solidity | `.sol` | `mapping` |

## data (3)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| JSON | `.json` | `null` |
| TOML | `.toml` | `[table]` |
| YAML | `.yaml` | `anchors (&)` |

## diagram (3)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Graphviz | `.dot` | `digraph` |
| Mermaid | `.mmd` | `graph TD` |
| PlantUML | `.puml` | `@startuml` |

## query (3)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| PL/SQL | `.pls` | `DBMS_OUTPUT.PUT_LINE` |
| SQL | `.sql` | `GROUP BY` |
| T-SQL | `.sql` | `TOP` |

## hdl (2)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Verilog | `.v` | `always @(posedge)` |
| VHDL | `.vhd` | `process` |

## logic (1)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Prolog | `.pl` | `findall` |

## markup (1)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| HTML | `.html` | `<a href>` |

## shell (1)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| Bash | `.sh` | `read` |

## style (1)

| Language | File | Genuine API / feature |
| :--- | :--- | :--- |
| CSS | `.css` | `display: flex` |
