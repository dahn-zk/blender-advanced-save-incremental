## technical

### minor

- hierarchize modules, like move operators to `ops` submodule, property data types to `data`
- move draw methods to MainPanel class as methods
- operator data is built on every `draw` call, which was fine for the first version, but with the dynamic collection
  of Save Templates, the code become messy. now `core` logic is mixed with Blender interface logic and it should be
  separated.
- `config` in `VersionTemplate` class is temporary, the values should be simply part of class validation.
- `bpyx` can be re-organized better
- it would likely be nicer to have `draw_*` methods inside a property groups, but currently there is no need for it
- `data_*` accessors and modifiers could have fewer parameters, as all the extra data is in `Preferences`. legacy code
- when defining `Callable` typings, `ParamSpec` can be useful instead, but for now we use a simple way
