mod exposure;
mod lca;
pub use lca::*;
use ogcat::ogtree::TreeCollection;
// extern crate fifteen;
pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let collection = TreeCollection::from_newick("res/avian.tre")?;
    let wrapped = TreeCollectionWithLCA::from_tree_collection(collection);
    let (one, two, three, four, five) =
        wrapped.translate_taxon_names(("PYGAD", "COLLI", "TINMA", "CUCCA", "MANVI"));
    for (e, i) in wrapped.lca.iter().enumerate() {
        println!("==========");
        let quintet = [
            i.rev[one],
            i.rev[two],
            i.rev[three],
            i.rev[four],
            i.rev[five],
        ];
        let r = i.retrieve_topology(&quintet);
        if r.is_none() {
            println!("******");
            println!("{} {:?}", e + 1, i.retrieve_topology(&quintet));
        } else {
            println!("{} {:?}", e + 1, r);
        }
        break;
    }
    Ok(())
}
