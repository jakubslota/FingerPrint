import os
import finger


def inDatabase(fin):
    max_score = 0
    result = ["Brak w bazie", 0]
    names = (os.listdir('finger'))
    for x in names:
        fingers = (os.listdir('finger/' + x))
        for y in fingers:
            score = finger.finger(fin, ('finger/' + x + '/' + y), 2)
            if score >= 30 and score > max_score:
                result[0] = x
                result[1] = score
                if score == 100:
                    return result
    return result
