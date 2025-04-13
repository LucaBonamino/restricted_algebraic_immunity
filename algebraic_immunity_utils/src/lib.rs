mod matrix;
mod restricted_ai;
use pyo3::prelude::*;


/// A Python module implemented in Rust.
#[pymodule]
fn algebraic_immunity_utils(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<matrix::Matrix>()?;
    m.add_class::<restricted_ai::RestrictedAI>()?;
    m.add_function(wrap_pyfunction!(matrix::verify, m)?)?;
    m.add_function(wrap_pyfunction!(matrix::verify_2, m)?)?;
    Ok(())
}
