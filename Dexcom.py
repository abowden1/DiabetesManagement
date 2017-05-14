import pandas as pd
import csv
import os
import xml.etree.ElementTree as ET

from Database import create_db_table
from sqlalchemy import create_engine


def main():
    csv = input('Enter CSV File Path: ')

    # checks if file already exists and creates if not
    if not os.path.isfile(csv):
        xml = input('Enter XML File Path: ')
        create_csv(csv)
        convert_xml(xml, csv)

    df = pd.DataFrame.from_csv(csv, index_col=2)
    df.rename(columns={'Value' : 'GlucoseVal'}, inplace=True)

    insert_to_database(df)
    print(df.head())
    return


def convert_xml(xml, csv):
    tree = ET.parse(xml)
    root = tree.getroot()
    glucose_readings = root.find('GlucoseReadings')

    # pulls values from <Glucose> and writes them to a CSV file
    for element in glucose_readings:
        values = element.attrib
        data = values['Value'], values['DisplayTime'], values['InternalTime']
        write_csv(data, csv)
    return


def write_csv(data, path):
    # appends all data to the existing CSV
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)


def create_csv(file):
    headers = ['Value', 'DisplayTime', 'InternalTime']
    # writes the above values to a blank CSV to act as the column names for future manipulation
    with open(file, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)


def create_df(data):
    df = pd.DataFrame.from_csv(csv)
    return df


def insert_to_database(data):
    db = input('Enter path to DB: ')
    if not os.path.isfile(db):
        create_db_table(db)

    engine = create_engine('sqlite:///%s' % db)
    data.to_sql('glucose_val', con=engine, if_exists='append')

if __name__ == '__main__':
    main()