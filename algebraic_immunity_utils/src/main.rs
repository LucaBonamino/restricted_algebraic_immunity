use std::fs::File;
use std::io::{Write, BufWriter};
use itertools::Itertools;
use ndarray::Array2;

// Generate binary strings of length `n` in graded lexicographic order
fn generate_binary_strings(n: usize) -> Vec<String> {
    let mut binary_strings = Vec::new();

    // Iterate over the number of 1's (graded order)
    for ones_count in 0..=n {
        // Generate all combinations of positions for the 1's
        for comb in (0..n).combinations(ones_count) {
            // Create the binary string with the selected positions as 1
            let mut bin_str = vec!['0'; n];
            for &i in &comb {
                bin_str[i] = '1';
            }
            binary_strings.push(bin_str.into_iter().collect());
        }
    }

    binary_strings
}

fn str_ops(s1: &str, s2: &str) -> i32 {
    s1.chars()
        .zip(s2.chars())
        .map(|(c1, c2)| {
            let base = c1.to_digit(10).unwrap() as i32;
            let exp = c2.to_digit(10).unwrap() as i32;
            base.pow(exp as u32)
        })
        .product()
}

fn generate_matrix(n: usize) -> Array2<i32> {
    let binary_strings = generate_binary_strings(n);
    let matrix_size = 2_usize.pow(n as u32);
    let mut matrix = Array2::<i32>::zeros((binary_strings.len(), matrix_size));

    for (idx, bin_str) in binary_strings.iter().enumerate() {
        let str_inv: String = bin_str.chars().rev().collect(); // Invert the string her
        for i in 0..matrix_size {
            let bin_i = format!("{:0width$b}", i, width = n);
            matrix[(idx, i)] = str_ops(&bin_i, &str_inv);
        }
    }
    matrix
}


fn pretty_print_matrix(matrix: &Array2<i32>) {
    for row in matrix.rows() {
        for val in row {
            print!("{:5} ", val);
        }
        println!();
    }
}

fn save_large_bit_matrix_bin(matrix: &Array2<i32>, filename: &str) {
    let rows = matrix.nrows() as u32;
    let cols = matrix.ncols() as u32;

    let mut file = BufWriter::new(File::create(filename).expect("Failed to create file"));

    file.write_all(&rows.to_le_bytes()).expect("Failed to write rows");
    file.write_all(&cols.to_le_bytes()).expect("Failed to write cols");

    let data = matrix.as_slice().expect("Failed to convert matrix to slice");
    for value in data {
        file.write_all(&value.to_le_bytes()).expect("Failed to write matrix data");
    }
}

fn main() {
    let size = 16;
    let matrix = generate_matrix(size);
    let filename = format!("large_bit_matrix_{}.bin", size);
    save_large_bit_matrix_bin(&matrix, &filename);

}
