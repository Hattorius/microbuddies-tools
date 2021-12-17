
def calculateSubstringPercentage(string, substring):
    subsubstrings = []
    for fromN in range(len(substring)):
        subsubstringTemp = ""
        for character in substring[fromN:]:
            subsubstringTemp += character
            subsubstrings.append(subsubstringTemp)
    subsubstrings = list(set(subsubstrings))
    matches = 0
    for subsubstring in subsubstrings:
        if subsubstring in string:
            matches += 1
    extra = 1
    if len(substring) > 10:
        extra = 1 + len(substring)/100*3
    return (matches / len(subsubstrings))*100*extra
