# nbclick - Turn Jupyter notebooks into command line applications

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/nbclick.svg)](https://badge.fury.io/py/nbclick)

`nbclick` allows you to modify and run Jupyter notebooks from the commandline.
It builds on top of [nbparameterise](https://github.com/takluyver/nbparameterise) which allows
programmatic extraction and modification of parameters of Jupyter notebooks.

## Installation

`nbclick` can be installed using `pip`:

```
python -m pip install nbclick
```

It is also possible to run `nbclick` without prior installation using `pipx`:

```
pipx run --system-site-packages nbclick
```

Note that the `--system-site-packages` flag is absolutely necessary if your notebook depends
on any non-standard library Python package.

## Running nbclick

After installation, you can run `nbclick` using the commandline:

```
nbclick
```

The most important argument is the `NOTEBOOK` parameter. For a given notebook,
you can again use `--help` to display the configuration options:

```
nbclick mynotebook.ipynb --help
```

## Preparing a notebook for execution with nbclick

`nbclick` relies on `nbparameterise` to extract command line options from your
Jupyter notebook. The best way to specify customizable parameters is to place
them into the first code cell of the notebook as simple assignments:

```python
num_samples = 1000      # The number of samples to draw
outfile = "output.csv"  # The filename to store the results
```

For above case, the output of `nbclick notebook.ipynb --help` will be:

```
Usage: nbclick notebook.ipynb [OPTIONS]

Options:
  --num_samples INTEGER  The number of samples to draw  [default: 1000]
  --outfile TEXT         The filename to store the results  [default:
                         output.csv]
  --help                 Show this message and exit.
```

## Limitations

There are a few known limitations that result from upstream projects that I currently
do not plan to fix for `nbclick`:

* The number of parameter types recognized is quite small. `nbclick` is known to work
  with `int`, `float`, `bool`, `str`, `list` (of both homogeneous and heterogeneous type).
  Most notably, `nbparameterise` does not support `tuple`s.
* List parameters are restricted to fixed length (defined by their default). This results
  from `click` voluntarily chosing not to provide variable length list parameters, as it
  introduces ambiguity of the parser.
