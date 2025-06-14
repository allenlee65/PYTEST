

inputnumber = int(input("Enter a number: "))
if inputnumber % 2 == 0 and inputnumber != 0:
    print("A")
elif inputnumber % 2 == 1 and  2 < inputnumber < 6:
    print("B")
elif inputnumber % 2 != 0 and 6 <= inputnumber <= 20:
    print("C")
elif inputnumber % 2 != 0 and inputnumber > 20:
    print("D")
