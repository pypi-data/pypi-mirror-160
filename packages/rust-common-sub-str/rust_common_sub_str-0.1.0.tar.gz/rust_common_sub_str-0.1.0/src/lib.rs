use pyo3::prelude::*;

#[pyfunction]
fn find(s: &str, t: &str, threshold: usize) -> Vec<[usize; 3]> {
    let mut result = vec![];

    let source :Vec<char> = s.chars().collect();
    let target :Vec<char> = t.chars().collect();

    let source_len: usize = source.len();
    let target_len: usize = target.len();


    let mut dp = [vec![0; target_len+1], vec![0; target_len+1]];

    for i in 1..=source_len {
        for j in 1..=target_len {
            if source[i - 1] == target[j - 1] {
                dp[i % 2][j] = dp[(i - 1) % 2][j - 1] + 1;
                if dp[i % 2][j] >= threshold && (i == source_len || j == target_len) {
                    result.push([i, j, dp[i % 2][j]]);
                }
            } else {
                dp[i % 2][j] = 0;
                if dp[(i - 1) % 2][j - 1] >= threshold {
                    result.push([i - 1, j - 1, dp[(i - 1) % 2][j - 1]]);
                }
            }
        }
    }

    result
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_common_sub_str(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find, m)?)?;
    Ok(())
}
