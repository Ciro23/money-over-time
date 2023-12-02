Displays a plot graph representing an amount of money over time.

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
python3 src/main.py --file /path/to/your/csv/file
```
The default label used for date and amount are "date" and "amount" respectively, but they can be customized
using:
```
python3 src/main.py --file /path/to/your/csv/file --date_label "custom date label" --date_format "%Y/%m/%d"
```
