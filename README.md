## Introduction
A tool to manage and analyze financial records.  
It's helpful to whoever tracks financial movements because of the two main features:
1. `plot`: displays a plot graph showing the amount of money over time.
2. `diff`: tracks all accountability errors between a source set of financial records and a reference file (for example between a manually updated CSV/XLSX file and the bank document with all the actual records).

This program can read both CSV and XLSX files, which are going to be referenced as "record files" in this document.  
It's required that record files contain column headers in the first rows, which must include a column to indicate when movements occurred and another one with the amount: the date format and the name of such columns are arbitrary and can be later specified when using this program.  
Example records file:
```
id,date,amount
1,1/12/2023,10
2,2/12,2023,30
3,3/12,2023,-50
```
## Usage
#### Case sensitiveness
When specifying the label of the date and amount column, the parameters are handled in a case-insensitive manner.
#### Default parameters
There are the default values used when their respective parameters are not specified:  
- Column delimiter: ",";
- Date format: "%d/%m/%Y";  
- Date label: "date";
- Amount label: "amount".

### Plot
To show the graph, use the `plot` command:
```shell
money-over-time plot --file "/path/to/your/csv/or/xlsx/file.csv"
```
Optional parameters can be customized using:
```shell
money-over-time \
    --file "/path/to/your/csv/or/xlsx/file.csv" \
    --separator ";" \
    --date_label "custom date label" \
    --date_format "%Y/%m/%d"
```
It's also possible to filter out some movements based on the value of a specific column.
For example, if the records file contains a column named "account" and you want to filter out
all the rows which account is "debit card", you can use:
```shell
money-over-time \
    --file "/path/to/your/csv/or/xlsx/file.csv" \
    --skip_label "account" \
    --skip_value "debit card"
```
### Diff
The `diff` command requires a source records file to be compared against a reference one.
## Building from source
This program is compatible and tested with Python 3.10 and this guide assumes you're using Linux or macOS.
1. Download Python 3.10 using your package manager or from the official website.
2. Navigate to the repository directory.
3. Create a virtual environment:
    ```shell
    python3.10 -m venv venv
    source venv/bin/activate
    ```
4. Install all pip dependencies using:
    ```shell
    pip install -r requirements.txt
    ```
5. Modify and execute the program with Python:
    ```shell
    python -m src.main
    ```
6. Run the unit tests with:
   ```shell
    python -m unittest discover -s test
    ```

## Gallery
![Figure1](https://github.com/user-attachments/assets/3bfcfae2-c956-41bc-9c36-c3702a4fcfd2)
