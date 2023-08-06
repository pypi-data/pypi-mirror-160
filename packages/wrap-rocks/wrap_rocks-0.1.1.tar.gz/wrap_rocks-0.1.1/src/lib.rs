use rocksdb::{DB, DBCompressionType, Options};
use pyo3::prelude::*;
extern crate rocksdb;
extern crate core;



#[pyfunction]
fn put(path: String, inserts: Vec<Vec<String>>) -> u64 {
    let mut options = Options::default();
    options.create_if_missing(true);
    options.set_compression_type(DBCompressionType::None);
    let db = DB::open(&options, path).unwrap();
    let mut batch = rocksdb::WriteBatch::default();
    let mut counter: u64 = 0;
    for pair in inserts.iter() {
        batch.put(pair[0].as_bytes(), pair[1].as_bytes());
        counter += 1
    }
    match db.write(batch) {
        Ok(_) => counter,
        Err(_) => 0
    }
}

#[pyfunction]
fn get(path: String, keys: Vec<String>) -> Vec<String> {
    let mut options = Options::default();
    options.create_if_missing(true);
    options.set_compression_type(DBCompressionType::None);
    let db = DB::open(&options, path).unwrap();
    let byte_keys: Vec<&[u8]> = keys.iter().map(|x| x.as_bytes()).collect();
    let packed_results = db.multi_get(byte_keys.iter());
    let mut unpacked_results: Vec<String> = Vec::with_capacity(keys.capacity());
    for pack in packed_results.iter() {
        match pack {
            Ok(Some(value)) => unpacked_results.push(String::from_utf8(value.to_vec()).unwrap()),
            Ok(None) => unpacked_results.push( String::from("")),
            Err(_) => unpacked_results.push(String::from("error")),
        }
    }
    return unpacked_results;
}
/// A Python module implemented in Rust.
#[pymodule]
fn wrap_rocks(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(put, m)?)?;
    m.add_function(wrap_pyfunction!(get, m)?)?;
    Ok(())
}