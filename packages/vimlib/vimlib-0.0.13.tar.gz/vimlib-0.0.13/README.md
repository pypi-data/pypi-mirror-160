[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PyPI](https://img.shields.io/pypi/v/vimlib?color=darkred)](https://pypi.org/project/vimlib/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vimlib?label=Python%20Version&logo=python&logoColor=yellow)](https://pypi.org/project/vimlib/)
[![PyPI - License](https://img.shields.io/pypi/l/vimlib?color=green)](https://github.com/AceofSpades5757/vimlib/blob/main/LICENSE)

[![Read the Docs](https://img.shields.io/readthedocs/vimlib)](https://vimlib.readthedocs.io/en/latest/)

A friendly interface for interacting with Vim using Python.

# Installation

`pip install vimlib`

**Recommended**: Using your chosen virtual environment, that's been setup for
Vim, or Neovim, to use, install `vimlib` using that.

Examples:

- `~/vimfiles/.venv/bin/pip.exe install --upgrade vimlib`
- `cd ~/vimfiles && poetry install vimlib`
<!--
-

```sh
cd ~/vimfiles \
&& python3 -m venv .venv \
&& ~/vimfiles/.venv/bin/pip.exe install --upgrade vimlib
```

-->

# Usage

## Current

`vimlib` offers a convenient way to interact with the current environment, much
like Vim's built-in current object.

```python
from pyvim import current
```

## Echo

`vimlib` offers a convenient way to print to Vim's stdout in a colorful, and
flexible, manner.

```python
import pyvim


# Print to STDOUT
pyvim.echo("Hello!")
# Print with chosen highlight group
pyvim.echo("Hello!", "PyVimSuccess")  # Built-In Green
pyvim.echo("Hello!", "PyVimCaution")  # Built-In Yellow
pyvim.echo("Hello!", "PyVimDanger")   # Built-In Red
```

## Highlight Groups

`vimlib` offers a convenient way to interact with highlight groups.

```python
from pyvim import current


# Boolean. Check if a highlight group is available
has_highlight = 'MyHighlightGroup' in pyvim.current.highlights
```

## Visual Selection

`vimlib` offers a convenient way to interact with highlighted text. Also
highlights the most recent highlighted text.

```python
from pyvim import current


# String with the current, or last, selection.
# Support basic, linewise, and block visual highlights
selection = pyvim.current.selection
```

## Utilities

`vimlib` offers convenient utilities.

### System Commands

_Note: Chaining will stack `<CR>` and other tokens._

```python
from pyvim.utilities import wrap_vim_command


wrapped_command: str = wrap_vim_command(
    command="!py %",
    silent=True,
    clear=True,
)

print(wrapped_command)
# ":<C-U>silent !py %<CR>
```

Examples

```python
>>> print(wrap_vim_command('w'))
:<C-u>w<CR>
```

```python
>>> print(wrap_vim_command('w!', silent=True))
:<C-u>silent w!<CR>
```

## Mappings

`vimlib` offers a convenient way to interact Vim mappings.

```python
>>> import pyvim
>>>
>>>
>>> # Set <Leader>r to write current buffer to disk.
>>> # Equivalent to `:nmap <Leader>r :<C-u>silent w<CR>` in Vim.
>>> set_mapping('nmap', '<Leader>r', ':<C-u>silent w<CR>')
```

## Function

**WARNING: Non-Working**

`vimlib` offers a convenient way to interact Vim functions.

```python
import pyvim


vim_function = pyvim.Function(
    name="Foo",
    arguments=None,
    optional_arguments=True,
    overwrite=True,
)

result = vim_function(...)
```

## Job

**WARNING: Non-Working**

`vimlib` offers a convenient way to interact Vim jobs and channels.

```python
import pyvim


vim_job = pyvim.Job(
    cmd='python -m http.server',
)

vim_job.stop()
vim_job.status
```

## Registers

`vimlib` offers a convenient way to interact Vim registers.

```python
>>> import pyvim.Register
```
