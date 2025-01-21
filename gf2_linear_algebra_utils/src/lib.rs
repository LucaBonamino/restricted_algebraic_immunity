mod matrix;
use pyo3::prelude::*;


/// A Python module implemented in Rust.
#[pymodule]
fn gf2_linear_algebra_utils(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<matrix::Matrix>()?;
    Ok(())
}
