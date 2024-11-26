import random, time

while True:
    time.sleep(1)
    try:
        s = raw_input("Print what? ")
        i = int(input("How many times? "))
        for round in xrange(i):
            print(s)
    except Exception as e:
        print("Something bad happened :(")
        print(e)
