# money-over-time

## Introduction

A tool to manage and analyze financial records.  
It's helpful to whoever tracks financial movements because of the two main features:

1. `plot`: displays a plot graph showing the amount of money over time.
2. `diff`: tracks all accounting errors between a source set of financial records and a reference file (for example
between a manually updated CSV/XLSX file and the document exported from the bank website with all the actual records).

This program can read both CSV and XLSX files, which are going to be referenced as "record files" in this document.  
It's required that record files contain column headers in the first row, which must include a column to indicate when
movements occurred and another one with the changed amount: the date format and the name of such columns are arbitrary
as they can be later customized when using this program.  

Example records file:

```csv
id,date,amount,account
1,1/12/2023,10,cash
2,2/12,2023,30,cash
3,3/12,2023,-50,debit card
```

## How to run

This program is compatible and tested with Python 3.11 and this guide assumes you're using Linux or macOS (other Python
versions should also be compatible, but warnings may be shown).

1. Download Python 3.11 from your package manager, [pyenv](https://github.com/pyenv/pyenv), or the official website.
2. Navigate to the repository directory.
3. Create a virtual environment:

    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Install all pip dependencies using:

    ```shell
    pip install -r requirements.txt
    ```

5. Execute the program with Python:

    ```shell
    python -m mot
    ```

## Usage

### Plot

To show the graph, use the `plot` command:

```shell
python -m mot plot --file "/path/to/your/csv/or/xlsx/file.csv"
```

Optional arguments can be customized using:

```shell
python -m mot plot \
    --file "/path/to/your/csv/or/xlsx/file.csv" \
    --delimiter ";" \
    --date-format "%Y/%m/%d" \
    --date-label "custom date label" \
    --amount-label "custom amount label"
```

It's also possible to filter in or out some movements based on the value of a specific column.
For example, if the records file contains a column named "account" and you want to filter out
all the rows which account is "debit card", you can use:

```shell
python -m mot plot \
    --file "/path/to/your/csv/or/xlsx/file.csv" \
    --filter-label "account" \
    --filter-value "debit card"
    --filter-mode "out"
```

### Diff

The `diff` command requires a source records file to be compared against a reference one:

```shell
python -m mot diff \
    --source-file "/path/to/your/csv/or/xlsx/source-file.csv" \
    --reference-file "/path/to/your/csv/or/xlsx/reference-file.csv"
```

Optional arguments can be customized using:

```shell
python -m mot diff \
    --source-file "/path/to/your/csv/or/xlsx/source-file.csv" \
    --reference-file "/path/to/your/csv/or/xlsx/reference-file.csv" \
    --source-delimiter ";" \
    --source-date-format "%Y/%m/%d" \
    --source-date-label "custom date label" \
    --source-amount-label "custom amount label" \
    --reference-delimiter ";" \
    --reference-date-format "%Y/%m/%d" \
    --reference-date-label "custom date label" \
    --reference-amount-label "custom amount label"
```

It's also possible to filter in or out some movements from the source records file based on the value of a specific column.  
For example, if the source records file contains a column named "account" and you want to filter out
all the rows except the ones which account is "debit card", you can use:

```shell
python -m mot diff \
    --source-file "/path/to/your/csv/or/xlsx/source-file.csv" \
    --reference-file "/path/to/your/csv/or/xlsx/reference-file.csv" \
    --filter-label "account" \
    --filter-value "debit card"
    --filter-mode "in"
```

---

### Case sensitiveness

When specifying the label of the date and amount columns, the values are handled in a case-insensitive manner.

### Default arguments

These are the default values used when their respective arguments are not specified:

- Cells delimiter: ",";
- Date format: "%d/%m/%Y";  
- Date label: "date";
- Amount label: "amount".

### Troubleshooting

Add the `-v` or `--verbose` argument to print a more detailed error message in case of problems.

## Gallery

### Example output for Plot command

![Figure1](https://github.com/user-attachments/assets/3bfcfae2-c956-41bc-9c36-c3702a4fcfd2)

### Example output for Diff command

![Figure2](https://github.com/user-attachments/assets/895514df-5591-44b3-8921-428b1d031f50)
