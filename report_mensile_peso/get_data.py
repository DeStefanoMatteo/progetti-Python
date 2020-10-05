#! python3

# GET DATA FROM GOOGLE SHEETS

import ezsheets
import os
import os.path
import datetime
import pandas as pd

DATE_TODAY = datetime.date.today().strftime('%d/%m/%Y')
DATE_CODE = datetime.date.today().strftime('%Y%m%d')
CSV_NAME = f'weight_data_{DATE_CODE}.csv'
        

def download_data():
    ss = ezsheets.Spreadsheet('...')
    sheet = ss[0]
    rows = sheet.getRows()
    for i, row in enumerate(rows):
        if row[0] == DATE_TODAY:
            row_today = i + 1
    rows = rows[1:row_today]
    return rows


def clean_data(rows):
    for row in rows:
        # Replace empty values with None
        row[1] = None if row[1] == '' else row[1]
    # print(rows[-4:])
    return rows


def create_csv(weight_data):
    df = pd.DataFrame(weight_data, columns=['date', 'weight'])
    df.to_csv(f'data/{CSV_NAME}', index=False)


def delete_old_data():
    for file in os.listdir('data/'):
        if file != CSV_NAME:
            os.remove(f'data/{file}')
            print(f'File {file} deleted.')


def main():

    # Check if file "weight_data_{DATE_CODE}.csv" exists
    data_exist = os.path.isfile(CSV_NAME)

    # If file doesn't exist, download and clean data from Google Sheets
    if not data_exist:
        print('Downloading data from Google Sheets.')
        raw_data = download_data()
        weight_data = clean_data(raw_data)
        create_csv(weight_data)
    
    delete_old_data()

if __name__ == '__main__':
    main()
