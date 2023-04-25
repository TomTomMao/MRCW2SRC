def checkDigit(string: str):
    if len(string) == 0:
        return False
    for char in string:
        if char not in [str(i) for i in range(10)]:
            return False
    else:
        return True

assert checkDigit("1234123") == True
assert checkDigit("1234123x") == False
assert checkDigit("") == False