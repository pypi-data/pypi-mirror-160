def armstrong():
    print("Plz enter a number upto which u want a list of armstrong number")
    a=input()
    count=0
    for i in str(a):
        count = count + int(i) ** len(str(a))
    if int(a) == count:
        print("it is armstrong")
    else:
        print("it is not armstrong")
armstrong()

