Displays a plot graph representing an amount of money over time.

## Building
This program is compatible and tested with Python 3.10.  
Install all pip dependencies using:
```
pip install -r requirements.txt
```
## Usage
The program reads a CSV file containing a list of movements/transactions, with at least two columns specified: one for
the date and the other for the amount.  
Example CSV file:
```csv
id,date,amount
1,1/12/2023,10
2,2/12,2023,30
3,3/12,2023,-50
```
To show the plot graph, use:
```
python3 src/main.py --file "/path/to/your/csv/file"
```
The default column separator used is a comma ",".  
The default date format used is "%d/%m/%Y".  
The default label used for date and amount are "date" and "amount" respectively.  
All these parameters can be customized using:
```
python3 src/main.py
    --file "/path/to/your/csv/file"
    --separator ;
    --date_label "custom date label"
    --date_format "%Y/%m/%d"
```
It's also possible to filter out some movements based on the value of a specific column.
For example, if the CSV file contains a column named "account" and you want to filter out
all the rows which account is "debit card", you can use:
```
python3 src/main.py
    --file "/path/to/your/csv/file"
    --skip_label "account"
    --skip_value "debit card"
```
All string parameters for column labels are handled in a case-insensitive manner.
## Gallery
![Figure_1](https://github.com/Ciro23/money-over-time/assets/38884767/3e3c8e1e-1fa6-48f7-aef7-b5315f97965b)
