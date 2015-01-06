import csv


def read_twitter_data(file_name):
    with open(file_name, "rb") as f_obj:
        data = csv_reader(f_obj)
    
    return data

def csv_reader(file_obj):
    """
    Read a csv file
    """
    #total = sum( 1 for x in csv.reader(file_obj) )
    #print total
    reader = csv.reader(file_obj)
    first = False
    data = []
    header = []
    for row in reader:
        if len(header) == 0:
            header = row
        else:
            i = 0
            tweet = {}
            while i < len(row):
                tweet[header[i]] = row[i]
                i = i + 1
            data.append(tweet)
        

    return data