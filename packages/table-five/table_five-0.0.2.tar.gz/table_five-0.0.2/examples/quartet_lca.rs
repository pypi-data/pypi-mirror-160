use fifteen::TreeCollectionWithLCA;
use ogcat::ogtree::TreeCollection;

// extern crate fifteen;
pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let collection = TreeCollection::from_newick("res/quartet.nwk")?;
    let wrapped = TreeCollectionWithLCA::from_tree_collection(collection);
    println!("{:?}", wrapped);
    Ok(())
}
