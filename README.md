Displays a plot graph representing an amount of money over time.

## Usage
The program reads a CSV file containing a list of movements/transactions, with at least two columns specified: one for
the date and the other for the amount.  
Example CSV file:
```
id,date,amount
1,1/12/2023,10
2,2/12,2023,30
3,3/12,2023,-50
```
To show the plot graph, use:
```shell
money-over-time --file "/path/to/your/csv/file.csv"
```
The default column separator used is a comma ",".  
The default date format used is "%d/%m/%Y".  
The default label used for date and amount are "date" and "amount" respectively.  
All these parameters can be customized using:
```shell
money-over-time
    --file "/path/to/your/csv/file.csv"
    --separator ;
    --date_label "custom date label"
    --date_format "%Y/%m/%d"
```
It's also possible to filter out some movements based on the value of a specific column.
For example, if the CSV file contains a column named "account" and you want to filter out
all the rows which account is "debit card", you can use:
```shell
money-over-time
    --file "/path/to/your/csv/file.csv"
    --skip_label "account"
    --skip_value "debit card"
```
All string parameters for column labels are handled in a case-insensitive manner.
## Building from source
This program is compatible and tested with Python 3.10, this guide assumes you're using Linux or macOS.  
1. Download Python 3.10 using your package manager or from the official website.
2. Create a virtual environment ("myenv" may be changed based on your preferences):
    ```shell
    python3.10 -m venv myenv
    source myenv/bin/activate
    ```
3. Navigate to the repository directory, then install all pip dependencies using:
    ```shell
    pip install -r requirements.txt
    ```
4. Modify and execute the program with Python:
    ```shell
    python src/main.py
    ```

## Gallery
![Figure1](https://github.com/user-attachments/assets/3bfcfae2-c956-41bc-9c36-c3702a4fcfd2)
