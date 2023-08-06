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

#### Quintet Counting

The major API is `tally_sinlge_quintet` returning a list of length 15 containing the empirical
counts of the 15 ADR unrooted quintet topology among the tree-set in $O(k)$ time:

```python
# get counts of the ADR unrooted quintet topologies on taxa '1','2','3','4','5'. Taxa order matters.
treeset.tally_single_quintet(('1','2','3','4','5'))
# obviously you might want to convert it to numpy arrays

# normalize by the number of genes in the tree-set
new_tree_dist = np.asarray(treeset.tally_single_quintet(q_taxa)) / len(treeset)
```