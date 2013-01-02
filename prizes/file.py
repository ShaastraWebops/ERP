def handle_uploaded_file(f):
    print "HELLO"
    with open(f, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            print row
