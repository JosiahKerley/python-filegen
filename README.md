FileGen
=======

Universal file generation toolbox


About
=====

FileGen uses Jinja templates and YAML to generate files.


Usage
=====

```
filegen -t template.jn2 -p params.yml > mynewfile.txt
```

Help
====
```
usage: filegen [-h] --template TEMPLATE_PATH --parameters
               [PARAM_PATHS [PARAM_PATHS ...]] [--debug]
               [--ignore-command-error] [--version]
```
