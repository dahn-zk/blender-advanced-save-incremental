contributions are welcome if you can follow and tolerate certain unconventional code style quirks.

### bpy.props

code reliability is more important than conciseness for this project, this is why Python typings are used heavily to
reduce chances for accidental bugs in code maintenance.

unfortunately, the Blender API requires defining Custom Properties as annotations, which breaks the Python typings
system. if a custom property is defined like `p: bpy.props...` then it breaks static type checkers and detects dynamic
usages everywhere, which also slows down refactorings.

let's say we have a `split` method defined anywhere in the code at any level (module, class, doesn't matter) not related
to `str.split` in any way. when we access our `p` property it's type will be detected as `None` because Blender does not
provide normal Python module to rely on, and `fake-bpy-module` does not extract the correct annotations for each of
the `bpy.props.*`. so until Blender finally makes the normal module to use, we define getters like `p_get(self) -> ...`
with the correct typing where needed.

also function arguments inside a typing dont render well in some IDEs, so they are extracted to a separate `*_def`
values.

### misc

- typings MUST be anywhere where possible
- sometimes classes and variables can end with base class or type like `*Operator` or even `*OperatorProps` which is not
  PEP-friendly and makes the code look like enterprise Java, but it also can make the code more readable and clearer
- get/set/update/etc should usually end the function name if it operates on an object(s). English is subject-verb-object
  language but in the context of programming and especially OOP i find [SOV][SOV] order more intuitive to read/write and
  think in, but in places where a more procedural than object-oriented style is used, SVO is appropriate

[SOV]: https://en.wikipedia.org/wiki/Subject%E2%80%93object%E2%80%93verb_word_order