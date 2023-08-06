pub mod lca;
use exposure::TreeSet;
pub use lca::*;
pub mod exposure;
use pyo3::prelude::*;

// /// Formats the sum of two numbers as string.
// #[pyfunction]
// fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
//     Ok((a + b).to_string())
// }

/// A Python module implemented in Rust.
#[pymodule]
fn table_five(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<TreeSet>()?;
    Ok(())
}
