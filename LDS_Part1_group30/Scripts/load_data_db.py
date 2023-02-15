import csv
import pyodbc

def get_header(strings):

    strings = [str(value) for value in strings]
    new_string = str()
    first = True

    for string in strings:
        if first:
            new_string += string
            first = False
        else:
            new_string += ', ' + string

    return new_string

def get_sql_params(h):
    n = len(h)
    first = True
    params = str()

    for i in range(n):
        if first:
            first = False
            params = '?'

        else:
            params += ', ' + '?'

    return params


def load_csv(name_ifile, cnn, name_table):

    ifile = open(name_ifile, 'r')
    reader = csv.reader(ifile)
    cursor = cnn.cursor()
    first = True
    for row in reader:
        if first:

            sql = "INSERT INTO " + name_table + " (" + get_header(row) + ") " + "VALUES( " + get_sql_params(row) + " )"
            print(sql)
            first = False

        else:
            print(row)
            cursor.execute(sql, (row[::]))

    cnxn.commit()
    ifile.close()


###### setting the connection to the db and the cursor
server = 'lds.di.unipi.it'
database = 'Group_30_DB'
username = 'Group_30'
password = '295R5QAG'
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
cnxn = pyodbc.connect(connectionString)


load_csv('date.csv', cnxn, '[Group_30_DB].[Group_30].[Date]')
load_csv('tournament_cleaned.csv', cnxn, '[Group_30_DB].[Group_30].[Tourney]')
load_csv('geography_cleaned.csv', cnxn, '[Group_30_DB].[Group_30].[Geography]')
load_csv('player_cleaned.csv', cnxn, '[Group_30_DB].[Group_30].[Player]')
load_csv('match_cleaned.csv', cnxn, '[Group_30_DB].[Group_30].[Match]')