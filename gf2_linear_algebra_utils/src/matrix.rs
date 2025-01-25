use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
pub struct Matrix {
    pub elements: Vec<Vec<u8>>,
}

#[pymethods]
impl Matrix {
    #[new]
    pub fn new(elements: Vec<Vec<u8>>) -> Self {
        Matrix { elements }
    }

    pub fn __repr__(&self) -> String {
        let rows: Vec<String> = self
            .elements
            .iter()
            .map(|row| format!("{:?}", row))
            .collect();
        format!("[{}]", rows.join(", "))
    }

    fn to_list(&self) -> Vec<Vec<u8>> {
        self.elements.clone()
    }
    //
    fn nrows(&self) -> usize {
        self.elements.len()
    }

    fn ncols(&self) -> usize {
        if !self.elements.is_empty() {
            self.elements[0].len()
        } else {
            0
        }
    }

    fn copy(&self) -> Self {
        self.clone()
    }

    fn get(&self, row: usize, col: usize) -> u8 {
        self.elements[row][col]
    }

    fn add_rows(&mut self, target: usize, source: usize) {
        for i in 0..self.ncols() {
            self.elements[target][i] ^= self.elements[source][i];
        }
    }

    fn swap_rows(&mut self, row1: usize, row2: usize) {
        self.elements.swap(row1, row2);
    }

    fn is_zero_row(&self, row: usize) -> bool {
        self.elements[row].iter().all(|&x| x == 0)
    }

    fn echelon_form_last_row(&mut self) -> (Self, Vec<(usize, usize)>) {
        let mut m_copy = self.copy();
        let mut last_row = m_copy.elements[m_copy.nrows() - 1].clone();
        let last_row_index = m_copy.nrows() - 1;
        let mut operations = Vec::new();

        for _ in 0..m_copy.ncols() {
            let p_index = Matrix::get_pivot(&last_row);
            if p_index.is_none() {
                // No pivot found in the last row, we need to search for a row to swap
                let mut swap_row_index: Option<usize> = None;
                for row_index in (0..m_copy.nrows() - 1).rev() {
                    if m_copy.get(row_index, row_index) == 0
                        && (row_index+1..m_copy.ncols()).any(|k| m_copy.get(row_index, k) == 1)
                    {
                        swap_row_index = Some(row_index);
                        break;
                    }
                }

                if let Some(swap_index_row) = swap_row_index {
                    // Swap the rows if necessary
                    m_copy.swap_rows(swap_index_row, swap_index_row + 1);
                    operations.push((swap_index_row, swap_index_row + 1));
                    operations.push((swap_index_row + 1, swap_index_row));
                    operations.push((swap_index_row, swap_index_row + 1));
                } else {
                    break; // Exit if no valid row swap is found
                }
            } else {
                let p_index = p_index.unwrap();

                let mut p_row: Option<Vec<u8>> = None;
                let mut j_index: Option<usize> = None;

                // Look for a row above that has the pivot at p_index
                for j in 0..m_copy.nrows() - 1 {
                    if m_copy.get(j, p_index) == 1
                        && !(0..p_index).any(|k| m_copy.get(j, k) == 1)
                    {
                        p_row = Some(m_copy.elements[j].clone());
                        j_index = Some(j);
                        break;
                    }
                }

                println!("p_row: {:?}", p_row);

                if p_row.is_none() {
                    // No row found with a pivot at p_index
                    if p_index == last_row_index {
                        let mut swap_index_row: Option<usize> = None;
                        // Look for a row to swap that is a zero row
                        for r in 0..m_copy.nrows() - 1 {
                            if m_copy.is_zero_row(r) {
                                swap_index_row = Some(r);
                                break;
                            }
                        }

                        if let Some(swap_index_row) = swap_index_row {
                            m_copy.swap_rows(last_row_index, swap_index_row);
                            operations.push((swap_index_row, last_row_index));
                            operations.push((last_row_index, swap_index_row));
                            operations.push((swap_index_row, last_row_index));
                        }
                        break; // Exit if we can't find a valid pivot
                    }

                    // Swap rows to bring the pivot to the last row
                    m_copy.swap_rows(last_row_index, p_index);
                    last_row = m_copy.elements[last_row_index].clone();
                    operations.push((p_index, last_row_index));
                    operations.push((last_row_index, p_index));
                    operations.push((p_index, last_row_index));
                } else if p_row.unwrap()[p_index] == 1 {
                    // If the pivot is found, add the pivot row to the last row
                    m_copy.add_rows(last_row_index, j_index.unwrap());
                    last_row = m_copy.elements[last_row_index].clone();
                    operations.push((last_row_index, j_index.unwrap()));
                }
            }
        }

        (m_copy, operations)
    }


    fn row_echelon_full_matrix(&self) -> (Self, Vec<(usize, usize)>) {
        let mut operations: Vec<(usize, usize)> = Vec::new();
        let mut m_copy = self.copy();

        for i in 0..usize::min(self.nrows(), self.ncols()) {
            // Find the pivot in the current column (the first 1 in column i)
            let mut pivot_row: Option<usize> = None;
            for r in i..self.nrows() {
                if m_copy.get(r, i) == 1 {
                    pivot_row = Some(r);
                    break;
                }
            }

            // If no pivot is found, skip this column
            if pivot_row.is_none() {
                continue;
            }
            let pivot_row = pivot_row.unwrap();

            // Swap the current row with the pivot row
            if pivot_row != i {
                m_copy.swap_rows(i, pivot_row);
                operations.push((i, pivot_row));
                operations.push((pivot_row, i));
                operations.push((i, pivot_row));
            }

            // Eliminate all rows below the pivot
            for j in (i + 1)..self.nrows() {
                if m_copy.get(j, i) == 1 {
                    m_copy.add_rows(j, i);
                    operations.push((j, i));
                }
            }
        }

        (m_copy, operations)
    }

    fn append_row(&mut self, v: Vec<u8>) {
        self.elements.push(v)
    }

    fn append_column(&mut self, v: Vec<u8>) {
        for i in 0..self.nrows() {
            self.elements[i].push(v[i]);
        }
    }

    fn rank(&self) -> usize {
        let mut count = 0;
        let mut pivot_columns = std::collections::HashSet::new();

        for i in 0..self.nrows() {
            let p = Matrix::get_pivot(&self.elements[i]);
            if let Some(col) = p {
                if pivot_columns.insert(col) {
                    count += 1;
                }
            }
        }
        count
    }

    fn pivots(&self){
        let rows = self.nrows();
        let cols = self.ncols();
        let mut pivots: Vec<usize> = Vec::new();

        let mut free_columns: Vec<usize> = Vec::new();
        let mut current_pivot_row = 0;

        // Identify pivot and free columns
        for col in 0..cols {
            if current_pivot_row < rows && self.elements[current_pivot_row][col] == 1 {
                pivots.push(col);
                current_pivot_row += 1;
            } else {
                free_columns.push(col);
            }
        }
        // Print the vectors
        println!("Pivot columns: {:?}", pivots);
        println!("Free columns: {:?}", free_columns);

    }

    fn kernel(&self) -> Vec<Vec<u8>> {
        let rows = self.nrows();
        let cols = self.ncols();

        let mut pivots: Vec<usize> = Vec::new();
        let mut kernel_base: Vec<Vec<u8>> = Vec::new();
        let mut free_columns: Vec<usize> = Vec::new();
        let mut current_pivot_row = 0;

        // Identify pivot and free columns
        for col in 0..cols {
            if current_pivot_row < rows && self.elements[current_pivot_row][col] == 1 {
                pivots.push(col);
                current_pivot_row += 1;
            } else {
                free_columns.push(col);
            }
        }

        // Construct kernel basis
        for &free_col in &free_columns {
            let mut kernel_vector = vec![0; cols];
            kernel_vector[free_col] = 1;

            // Backward substitution for pivot columns
            for (pivot_row, &pivot_col) in pivots.iter().enumerate().rev() {
                let mut sum = 0;
                for col in pivot_col + 1..cols {
                    sum ^= self.elements[pivot_row][col] * kernel_vector[col];
                }
                kernel_vector[pivot_col] = sum;
            }

            kernel_base.push(kernel_vector);
        }

        kernel_base
    }
}

impl Matrix {
    fn get_pivot(row: &Vec<u8>) -> Option<usize> {
        row.iter().position(|&x| x == 1)
    }
}
