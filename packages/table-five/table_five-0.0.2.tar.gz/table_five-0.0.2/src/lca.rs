use halfbrown::{hashmap, HashMap};
use ndarray::{array, Array, ArrayBase, Ix2, ShapeBuilder};
use ogcat::ogtree::{TaxonSet, Tree, TreeCollection};
use smallvec::{smallvec, SmallVec};

/// normalize a bipartition on 5 taxa
fn bip(b: u8) -> u8 {
    (0b11111 ^ b).min(b)
}

fn reorder_bips(a: u8, b: u8) -> (u8, u8) {
    if a < b {
        (a, b)
    } else {
        (b, a)
    }
}

/// gives the ADR quintet index of two bipartitions (must be normalized, but can be unordered)
fn bips_to_adr_ix(bip1: u8, bip2: u8) -> u8 {
    let (bip1, bip2) = reorder_bips(bip1, bip2);
    match (bip1, bip2) {
        (0b11, 0b111) => 0,
        (0b101, 0b111) => 1,
        (0b110, 0b111) => 2,
        (0b11, 0b1011) => 3,
        (0b1001, 0b1011) => 4,
        (0b1010, 0b1011) => 5,
        (0b101, 0b1101) => 6,
        (0b1001, 0b1101) => 7,
        (0b1100, 0b1101) => 8,
        (0b110, 0b1110) => 9,
        (0b1010, 0b1110) => 10,
        (0b1100, 0b1110) => 11,
        (0b11, 0b1100) => 12,
        (0b101, 0b1010) => 13,
        (0b110, 0b1001) => 14,
        (_, _) => panic!("Invalid bipartitions"),
    }
}

#[derive(Debug)]
pub struct TreeLCA {
    /// a mapping of taxa id to euler tour id (i.e, ix of first appearance)
    pub rev: Vec<u32>,
    /// contains node ids
    pub euler_tour: Vec<u32>,
    /// depths of nodes
    pub depths: Vec<u32>,
    /// sparse table, only containing the indices (not actual minimum depths)
    pub sparse_table: Array<u32, Ix2>,
}

impl TreeLCA {
    /// return the LCA (by euler ID and its depth) of two taxa (not by the canonical taxon ID but by euler tour first appearance)
    pub fn lca(&self, lhs: u32, rhs: u32) -> (u32, u32) {
        let (u, v) = if lhs < rhs { (lhs, rhs) } else { (rhs, lhs) };
        let min_ix = self.rmq(u, v);
        (min_ix as u32, self.depths[min_ix as usize])
    }

    /// range minimum query on the depths array (inclusive range), returns the ix of the minimum depth
    pub fn rmq(&self, l: u32, r: u32) -> usize {
        let j = Self::lg2(r - l + 1) as usize;
        let ix1 = self.sparse_table[[j, l as usize]] as usize;
        let ix2 = self.sparse_table[[j, (r - (1 << j) + 1) as usize]] as usize;
        // println!("looking up {:?}", [j, l as usize]);
        // println!("looking up {:?}", [j, (r - (1 << j) + 1) as usize]);
        let ix = if self.depths[ix1] <= self.depths[ix2] {
            ix1
        } else {
            ix2
        };
        ix
    }

    /// fast log2 implemention TODO: make it fast
    #[inline]
    pub fn lg2(u: u32) -> u32 {
        //(u as f64).log2() as u32
        u32::BITS - u.leading_zeros() - 1
    }

    pub fn lg2_usize(u: usize) -> u32 {
        usize::BITS - u.leading_zeros() - 1
    }

    pub fn mk_bip(u: u8, v: u8) -> u8 {
        bip(0b00000 | (1 << (4 - u)) | (1 << (4 - v)))
    }

    pub fn mk_bip3(x: u8, y: u8, z: u8) -> u8 {
        bip(0b00000 | (1 << (4 - x)) | (1 << (4 - y)) | (1 << (4 - z)))
    }

    pub fn retrieve_topology(&self, eids: &[u32; 5]) -> Option<u8> {
        let mut v: SmallVec<[(u8, u8, u32, u32); 14]> = smallvec![];
        let mut bips: SmallVec<[u8; 2]> = smallvec![];
        for i in 0..4u8 {
            for j in i + 1..5u8 {
                let (nid, depth) = self.lca(eids[i as usize], eids[j as usize]);
                v.push((i, j, nid, depth));
            }
        }
        let mut cur_deepest_pair = (v[0].0, v[0].1);
        let mut cur_depth = v[0].3;
        let mut cur_deepest_lca = v[0].2;
        let mut cur_deep_mult: HashMap<u32, u8> = hashmap! {self.euler_tour[cur_deepest_lca as usize] => 1};
        // println!("{:?}", v);
        for (i, j, nid, depth) in v.iter().skip(1) {
            if *depth > cur_depth {
                cur_deep_mult.clear();
                cur_deepest_pair = (*i, *j);
                cur_depth = *depth;
                cur_deepest_lca = *nid;
                cur_deep_mult.insert(self.euler_tour[cur_deepest_lca as usize], 1);
            } else if *depth == cur_depth {
                let mut mult = cur_deep_mult.entry(self.euler_tour[*nid as usize]).or_insert(0);
                *mult += 1;
            }
        }
        // println!("deepest pair: {:?}", cur_deepest_pair);
        // println!("cur_deep_mult {:?}", cur_deep_mult);
        if cur_deep_mult.values().any(|it| *it > 1) {
            // println!("early return");
            return None;
        }
        drop(cur_deep_mult);
        bips.push(Self::mk_bip(cur_deepest_pair.0, cur_deepest_pair.1));
        for i in 0..5u8 {
            if i == cur_deepest_pair.0 || i == cur_deepest_pair.1 {
                continue;
            }
            let (nid, depth) = self.lca(eids[i as usize], cur_deepest_lca);
            v.push((i, 5, nid, depth));
        }
        // println!("v2: {:?}", v);
        let mut lookable = v
            .iter()
            .filter(|it| {
                it.0 != cur_deepest_pair.0
                    && it.1 != cur_deepest_pair.1
                    && it.0 != cur_deepest_pair.1
                    && it.1 != cur_deepest_pair.0
            })
            .peekable();
        // println!(
        //     "lookable: {:?}",
        //     v.iter()
        //         .filter(|it| it.0 != cur_deepest_pair.0
        //             && it.1 != cur_deepest_pair.1
        //             && it.0 != cur_deepest_pair.1
        //             && it.1 != cur_deepest_pair.0)
        //         .collect::<Vec<_>>()
        // );
        let mut next_deepest_pair = (lookable.peek().unwrap().0, lookable.peek().unwrap().1);
        let mut next_depth = lookable.peek().unwrap().3;
        let mut next_deepest_lca = lookable.peek().unwrap().2;
        let mut next_deep_mult: HashMap<u32, u8> =
            // if next_deepest_pair.0 != 5 && next_deepest_pair.1 != 5 {
                hashmap! {self.euler_tour[next_deepest_lca as usize] => 1}
            // } else {
                // hashmap! {}
            // }
            ;
        for (i, j, nid, depth) in lookable.skip(1) {
            if *depth > next_depth {
                next_deep_mult.clear();
                next_deepest_pair = (*i, *j);
                next_deepest_lca = *nid;
                next_depth = *depth;
                // if next_deepest_pair.0 != 5 && next_deepest_pair.1 != 5 {
                next_deep_mult.insert(self.euler_tour[next_deepest_lca as usize], 1);
                // }
            } else if *depth == next_depth {
                // if *i != 5 && *j != 5 {
                let mut mult = next_deep_mult.entry(self.euler_tour[*nid as usize]).or_insert(0);
                *mult += 1;
                // }
            }
        }
        
        if next_deep_mult.values().any(|it| *it > 1) {
            // println!("X next_deep_mult: {:?}", next_deep_mult);
            return None;
        } else {
            // println!("OK, next_deep_mult: {:?}", next_deep_mult);
        }
        match next_deepest_pair {
            (a, 5) => {
                // let rest: SmallVec<[usize; 2]> = eids
                //     .iter()
                //     .enumerate()
                //     .filter(|(i, it)| {
                //         *i != a as usize
                //             && *i != cur_deepest_pair.0 as usize
                //             && *i != cur_deepest_pair.1 as usize
                //     })
                //     .map(|it| it.0)
                //     .collect();
                bips.push(Self::mk_bip3(a, cur_deepest_pair.0, cur_deepest_pair.1));
            }
            (u, v) => {
                bips.push(Self::mk_bip(u, v));
            }
        }
        // println!("match result: {:?}", bips_to_adr_ix(bips[0], bips[1]));
        Some(bips_to_adr_ix(bips[0], bips[1]))
    }
}

fn euler_dfs(
    tree: &Tree,
    node: u32,
    depth: u32,
    rev: &mut [u32],
    depths: &mut [u32],
    euler: &mut [u32],
    timer: &mut usize,
) {
    // println!("{}", node);
    euler[*timer] = node;
    depths[*timer] = depth;
    if tree.taxa[node as usize] >= 0 {
        rev[tree.taxa[node as usize] as usize] = *timer as u32;
    }
    *timer += 1;
    for i in tree.children(node as usize) {
        euler_dfs(tree, i as u32, depth + 1, rev, depths, euler, timer);
        euler[*timer] = node;
        depths[*timer] = depth;
        *timer += 1;
    }
}

pub fn construct_lca(taxa: &TaxonSet, tree: &Tree) -> TreeLCA {
    let mut rev = vec![0; taxa.len()];
    let mut depths = vec![0; 2 * tree.taxa.len()];
    let mut euler = vec![0; 2 * tree.taxa.len()];
    let n = 2 * tree.num_nodes();
    let mut timer = 0;
    euler_dfs(tree, 0, 0, &mut rev, &mut depths, &mut euler, &mut timer);
    let k = TreeLCA::lg2_usize(n) as usize;
    // sparse table
    let mut st = Array::<u32, _>::zeros((k + 1, n).f());
    for i in 0..n {
        st[[0, i]] = i as u32;
    }
    let mut j = 1;
    loop {
        if 1 << j <= n {
            let mut i = 0;
            loop {
                if i + (1 << j) - 1 < n {
                    if depths[st[[j - 1, i]] as usize]
                        < depths[st[[j - 1, i + (1 << (j - 1))]] as usize]
                    {
                        st[[j, i]] = st[[j - 1, i]];
                    } else {
                        st[[j, i]] = st[[j - 1, i + (1 << (j - 1))]];
                    }
                } else {
                    break;
                }
                i += 1;
            }
        } else {
            break;
        }
        j += 1;
    }
    TreeLCA {
        rev,
        euler_tour: euler,
        depths,
        sparse_table: st,
    }
}

#[derive(Debug)]
pub struct TreeCollectionWithLCA {
    pub collection: TreeCollection,
    pub lca: Vec<TreeLCA>,
}

impl TreeCollectionWithLCA {
    pub fn from_tree_collection(collection: TreeCollection) -> Self {
        let lcas = collection
            .trees
            .iter()
            .map(|t| construct_lca(&collection.taxon_set, t))
            .collect();
        Self {
            collection,
            lca: lcas,
        }
    }

    pub fn translate_taxon_names(
        &self,
        names: (&str, &str, &str, &str, &str),
    ) -> (usize, usize, usize, usize, usize) {
        (
            self.collection.taxon_set.retrieve(names.0),
            self.collection.taxon_set.retrieve(names.1),
            self.collection.taxon_set.retrieve(names.2),
            self.collection.taxon_set.retrieve(names.3),
            self.collection.taxon_set.retrieve(names.4),
        )
    }
}
