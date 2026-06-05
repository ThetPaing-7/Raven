# File Combiner & Header Validator

A Python utility for:

* Combining multiple CSV or Excel files into a single dataset.
* Comparing file headers against a master template.
* Detecting column mismatches before consolidation.
* Tracking source files and worksheet names during combination.

---

## Features

### Combine Files

* Supports CSV and Excel files.
* Combines data from multiple files into a single CSV output.
* Adds the source filename to every record.
* Adds worksheet names when combining multi-sheet Excel files.

### Header Validation

* Uses a master file as the template.
* Compares headers from all files in a folder.
* Detects:

  * Missing columns
  * Extra columns
  * Incorrect column order
  * Different column counts

---

# Installation

## Windows

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## macOS / Linux

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Required Packages

```bash
pip install pandas openpyxl xlrd
```

---

# Functions

## combine_files()

Combine multiple CSV or Excel files into a single CSV file.

### Parameters

| Parameter      | Type    | Default    | Description                                    |
| -------------- | ------- | ---------- | ---------------------------------------------- |
| folder_path    | str     | Required   | Folder containing files to combine             |
| output_file    | str     | "combined" | Name of the output file                        |
| extension      | str     | "xlsx"     | File extension to search for                   |
| sheets         | str/int | "all"      | Excel sheet to read. Use "all" for every sheet |
| header_include | int     | 0          | Row to use as the header                       |

### Returns

```python
pandas.DataFrame
```

A combined DataFrame containing data from all processed files.

### Example

```python
combine_files(
    folder_path="data",
    output_file="combined_result",
    extension="xlsx"
)
```

---

## check_header()

Compare the header structure of all files against a master file.

### Parameters

| Parameter   | Type    | Default  | Description                       |
| ----------- | ------- | -------- | --------------------------------- |
| folder_path | str     | Required | Folder containing files           |
| master_file | str     | Required | Template file used for comparison |
| rows        | int     | 1        | Number of header rows to compare  |
| sheet_name  | str/int | 0        | Sheet name or index to compare    |

### Returns

```python
None
```

This function prints validation results directly to the console.

### Output

The function reports:

* Header matches
* Header mismatches
* Column count differences
* Missing columns
* Extra columns
* Incorrect column order

### Example

```python
check_header(
    folder_path="data",
    master_file="template.xlsx",
    rows=1
)
```

---

# Example Workflow

### Step 1: Validate headers

```python
check_header(
    folder_path="input_files",
    master_file="template.xlsx"
)
```

### Step 2: Combine files

```python
combine_files(
    folder_path="input_files",
    output_file="final_output",
    extension="xlsx"
)
```

---

# Output Example

Combined file:

```text
source_file,name,age,city
file1.xlsx,John,25,Tokyo
file2.xlsx,Sarah,30,Osaka
```

For multi-sheet Excel files:

```text
source_file,sheet_name,name,age
file1.xlsx,Employees,John,25
file1.xlsx,Managers,Sarah,30
```
