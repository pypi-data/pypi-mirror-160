fifteen
=================

(DBA `table_five`)

Experimental library for quick quintet tallying, useful when you have a lot of quintets that somehow you don't want to count yourself.

## Usage

Binary wheels are provided on PyPI

```
python3 -m pip install table_five
```

## API

### `TreeSet`

A treeset is an efficient (i.e., fast parsing) list of tree topologies. The construction is $O(k n \lg n)$ where $k$ is the number of trees and $n$ the number of taxa due to the LCA data structure initialization.

```python
from table_five import TreeSet
trees = TreeSet("path_to_newline_delimited_newicks.tre")
```