import csv
 
#----------------------------------------------------------------------
def csv_reader(file_obj):
    """
    Read a csv file
    """
    #total = sum( 1 for x in csv.reader(file_obj) )
    #print total
    reader = csv.reader(file_obj)
    ct = 0
    idx = 0
    ct2 = 0
    words_ctr = {}
    retweets = {}
    videos = {}
    #['tweet_id', 'in_reply_to_status_id', 'in_reply_to_user_id', 'timestamp', 'source', 'text', 'retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp', 'expanded_urls']
    for row in reader: #row[5] is the text field
        if idx == 0:
            print row
        link  = row[-1]
        if "spot" not in link: continue
        if link not in videos:
            videos[link] = 1
        else:
            videos[link] += 1
        #if idx < 10: print words
        idx += 1

    things =  words_ctr.items()
    things.sort(key=lambda x: -1*x[1])
    rt = retweets.items()
    rt.sort(key=lambda x: -1*x[1])

    v = videos.items()
    v.sort(key=lambda x: -1*x[1])
    print rt
    i = 0
    while i < 10:
        print v[i][0], v[i][1]
        i = i  +1

    '''
    i = 0
    for row in reader:

        i += 1

    print i
    '''


#----------------------------------------------------------------------
if __name__ == "__main__":

    xd = {1:'2'}
    print xd.items()
    csv_path = "leonardo.csv"
    with open(csv_path, "rb") as f_obj:
        csv_reader(f_obj)