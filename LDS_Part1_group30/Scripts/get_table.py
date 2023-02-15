import os
import csv
from shutil import copyfile


def get_quarter(month):

    month = int(month)
    if month in range(1,4):
        return 1

    elif month in range(4,7):
        return 2

    elif month in range(7,10):
        return 3
    else:
        return 4

# ritorna un dizionario con chiave il nome del paese e come valore il nome della lingua
# usando come file country_list.csv
def get_languages():
    f_languages= open('country_list.csv', 'r')
    reader_lang= csv.DictReader(f_languages)
    lang_dict= dict()

    for row in reader_lang:

        if row['country_name'] not in lang_dict:
            if row['lang_name'] == None:
                row['lang_name'] = '?'

            lang_dict[row['country_name'].lower()] = row['lang_name']

    f_languages.close()
    return lang_dict

# ritorna un dizionario con chiave il country_id e come valore una lista
# contenente il nome del continente e il nome della lingua
def define_countries():

    f_countries = open('countries.csv', 'r')
    first= True
    languages= get_languages()
    country_dict = dict()
    reader= csv.reader(f_countries)

    for row in reader:
        if first:
            code_idx= row.index('country_code')
            cont_name_idx= row.index('continent')
            name_idx = row.index('country_name')
            first = False

        else:
            if row[code_idx] not in country_dict:
                try:
                    country_dict[row[code_idx]] = [row[cont_name_idx], languages[row[name_idx].lower()]]

                #
                except KeyError:
                    country_dict[row[code_idx]] = [row[cont_name_idx], '?']


    f_countries.close()
    return country_dict

def define_table(name_ifile, name_ofile, lst_cols, lst_idx  ):

    ifile = open(name_ifile, 'r')
    ofile = open(name_ofile, 'w', newline='')

    # avvio il reader per il file di input
    reader = csv.reader(ifile)
    writer = csv.writer(ofile)

    first = True
    collections = set()

    for row in reader:

        # se sono nell'header
        if first:

            # una volta selezionati gli id che mi interessano
            # li scrivo nel file di output
            writer.writerow([row[idx] for idx in lst_cols])
            first = False

        # inizio a scrivere nel file di output
        else:
            # poiche voglio evitare di scrivere duplicati, se la mia tupla di
            # indici non e presente nell'ofile scrivila, altrimenti passa

            t_ids = tuple([row[idx] for idx in lst_idx])
            if t_ids not in collections:
                collections.add(t_ids)
                # scrivi solo i valori della riga per gli attributi desiderati
                writer.writerow([row[idx] for idx in lst_cols])

    ifile.close()
    ofile.close()

def transform_match_table(NAME_IFILE):
    # creo una versione copiata e temporanea del file match.csv
    # infine leggo da temp.csv e riscrivo da zero su match.csv
    copyfile(NAME_IFILE, 'temp.csv')
    ifile = open('temp.csv', 'r')
    ofile = open(NAME_IFILE, 'w', newline='')

    first = True
    reader = csv.reader(ifile)
    writer = csv.writer(ofile)

    for row in reader:

        if first:
            match_col_idx= row.index('match_num')
            tourn_col_idx= row.index('tourney_id')
            row[match_col_idx] = 'match_id'
            writer.writerow(row)
            first = False

        else:
            row[match_col_idx] = row[tourn_col_idx] + '-' + row[match_col_idx]
            writer.writerow(row)


    ifile.close()
    ofile.close()

def transform_date_table(NAME_IFILE):
    # creo una versione copiata e temporanea del file date.csv
    # infine leggo da temp.csv e riscrivo da zero su date.csv
    copyfile(NAME_IFILE, 'temp.csv')
    ifile = open('temp.csv', 'r')
    ofile = open(NAME_IFILE, 'w', newline='')

    first= True
    cols= ['day','month','year','quarter']
    reader = csv.reader(ifile)
    writer = csv.writer(ofile)

    for row in reader:
        if first:
            row[0] = 'date_id'
            row.extend(cols)
            writer.writerow(row)
            first = False

        else:
            date= row[0]
            year = date[:4]
            month= date[4:6]
            day= date[6:]
            quarter= get_quarter(month)

            date= [row[0], day,month,year,quarter]
            writer.writerow(date)

    ifile.close()
    ofile.close()

def transform_geo_table(NAME_IFILE):
    # creo una versione copiata e temporanea del file date.csv
    # infine leggo da temp.csv e riscrivo da zero su date.csv
    copyfile(NAME_IFILE, 'temp.csv')
    ifile = open('temp.csv', 'r')
    ofile = open(NAME_IFILE, 'w', newline='')


    first = True
    name_cols= ['country_loc', 'continent', 'language']
    country_codes= set()
    country_dict = define_countries()

    reader= csv.reader(ifile)
    writer= csv.writer(ofile)

    for row in reader:
        if first:
            writer.writerow(name_cols)
            first= False

        else:
            for code in row:
                # questa condizione mi serve per evitare di avere duplicati nella tabella finale
                if code not in country_codes:
                    country_codes.add(code)

                    # potrebbero esistere righe in tennis.csv con un codice paese inesistente
                    # per esempio potrebbe esserci un typo o un missing value
                    try:
                        writer.writerow((code, country_dict[code][0], country_dict[code][1] ))

                    except KeyError:
                        writer.writerow((code, '?', '?'))

    ifile.close()
    ofile.close()

def define_player_table(NAME_IFILE, NAME_OFILE):

    ifile = open(NAME_IFILE, 'r')
    ofile = open(NAME_OFILE, 'w', newline='')

    # avvio il reader per il file di input
    reader = csv.DictReader(ifile)
    writer = csv.writer(ofile)

    first = True
    players = set()
    name_cols = ['winner_id', 'winner_ioc', 'winner_name', 'winner_hand',
                 'winner_ht', 'winner_age', 'tourney_date']

    for row in reader:
        # se sono nell'header
        if first:
            first= False
            pass

        else:
            # poiche voglio evitare di scrivere duplicati, se la mia tupla di
            # indici non e presente nell'ofile scrivila, altrimenti passa

            p_idx = row['winner_id']
            if p_idx not in players:
                players.add(p_idx)
                # scrivi solo i valori della riga per gli attributi desiderati
                writer.writerow([row[col] for col in name_cols])

    ifile.close()


    ifile= open(NAME_IFILE, 'r')
    reader = csv.DictReader(ifile)

    first = True
    name_cols = ['loser_id', 'loser_ioc', 'loser_name', 'loser_hand',
                 'loser_ht', 'loser_age', 'tourney_date']

    for row in reader:
        # se sono nell'header
        if first:
            first = False
            pass

        else:
            # poiche voglio evitare di scrivere duplicati, se la mia tupla di
            # indici non e presente nell'ofile scrivila, altrimenti passa

            p_idx = row['loser_id']
            if p_idx not in players:
                players.add(p_idx)
                # scrivi solo i valori della riga per gli attributi desiderati
                writer.writerow([row[col] for col in name_cols])

    ifile.close()
    ofile.close()

def transform_player_table(NAME_IFILE):
    from math import floor
    # creo una versione copiata e temporanea del file date.csv
    # infine leggo da temp.csv e riscrivo da zero su date.csv
    copyfile(NAME_IFILE, 'temp.csv')
    ifile = open('temp.csv', 'r')
    ofile = open(NAME_IFILE, 'w', newline='')

    # la mia assunzione per determinare il sesso e che il nome determina il sesso
    m_file= open('male_players.csv', 'r')
    f_file= open('female_players.csv', 'r')
    male_names= set()
    female_names= set()

    # registro tutti i nomi maschili
    reader = csv.DictReader(m_file)
    for row in reader:
        if row['name'] not in male_names:
            male_names.add(row['name'])
    m_file.close()

    # registro tutti i nomi femminili
    reader = csv.DictReader(f_file)
    for row in reader:
        if row['name'] not in female_names:
            female_names.add(row['name'])
    f_file.close()

    # siccome potrebbero esistere dei nomi bisex, allora sara
    # l'intersezione dei due insiemi
    bisex_names= male_names.intersection(female_names)

    # si guarda il nome del giocatore se e bisex, se lo e:
    #   - si riaprono i due file e si cerca il nome e il cognome di quella persona


    reader= csv.reader(ifile)
    writer = csv.writer(ofile)

    # scrivo l'header del file in output
    writer.writerow(('player_id', 'country_id', 'name', 'sex',
                         'hand', 'ht', 'byear'))

    for row in reader:
        # dal file temp prendo il nome e lo splitto in modo da avere
        # il nome e il cognome del giocatore separati
        name_surname= row[2].split()
        name= name_surname[0]
        surname= name_surname[1]

        ######################################## definisco il sesso #####################################################

        # controllo se il nome e bisex
        if name in bisex_names:
            # se lo e, controllo se il giocatore e nella lista di giocatori maschi, altrimenti e femmina
            m_file= open('male_players.csv', 'r')
            players= csv.DictReader(m_file)
            for player in players:
                if ( (name == player['name'] ) and (surname == player['surname']) ):
                    sex = 'M'

                else:
                    sex = 'F'

        elif name in male_names:
            sex = 'M'
        else:
            sex= 'F'
        m_file.close()
        # definisco l'anno di nascita
        try:
            t_year= int(row[6][0:4] )           # prendo la data del torneo, prendo i primi 4 caratteri che e l'anno e lo casto in int
            age = floor(float(row[5]))                   # prendo l'eta media e la casto in intero
            b_year= t_year - age

            # scrivo la riga
            writer.writerow( (row[0], row[1], row[2], sex, row[3], row[4], b_year) )

        # poiche esistono giocatori senza il dato 'eta media' devo gestire questo caso
        # assegnando dei missing values
        except ValueError:
            #print('t_year = ' ,row[6], 'age = ', row[5] )
            writer.writerow((row[0], row[1], row[2], sex, row[3], row[4], '?'))

    ifile.close()
    ofile.close()

def clean_missing(NAME_IFILE):
    copyfile(NAME_IFILE, 'temp.csv')
    ifile = open('temp.csv', 'r')
    ofile = open(NAME_IFILE, 'w', newline='')

    first = True
    reader = csv.reader(ifile)
    writer = csv.writer(ofile)

    for row in reader:
        if first:
            header = row
            writer.writerow(header)
            first = False

        else:
            row = ['?' if x == '' else x for x in row]
            if len(row) < len(header):
                row.append('?')

            writer.writerow(row)

    ifile.close()
    ofile.close()


NAME_IFILE= 'tennis.csv'

tournament_name = 'tournament.csv'
match_name = 'match.csv'
date_name = 'date.csv'
geo_name = 'geography.csv'
player_name = 'player.csv'

# definisco la tabella tournament
define_table(NAME_IFILE, tournament_name, [0,5,1,2,3,4,47,48], [0])
print('tournament.csv created')

# definisco la tabella match
define_table(NAME_IFILE, match_name, [0,6,7,14,21,22,23,24,25,26,
                                      27,28,29,30,31,32,33,34,
                                      35,36,37,38,39,40,41,42,
                                      43,44,45,46], [0,6])
transform_match_table(match_name)
print('match.csv created')

# definisco la tabella date
define_table(NAME_IFILE, date_name, [5],[5])
transform_date_table(date_name)
print('date.csv created')

# definisco la tabella geography
define_table(NAME_IFILE, geo_name, [12,19], [12,19])
transform_geo_table(geo_name)
print('geography.csv created')

# definisco la tabella player
define_player_table(NAME_IFILE, player_name)
transform_player_table(player_name)
print('player.csv created')


clean_missing(match_name)
print('match.csv cleaned')

clean_missing(tournament_name)
print('tournament.csv cleaned')

clean_missing(date_name)
print('date.csv cleaned')

clean_missing(geo_name)
print('geography.csv cleaned')

clean_missing(player_name)
print('player.csv cleaned')

os.remove('temp.csv')
