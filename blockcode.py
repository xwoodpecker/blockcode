import math
import numpy as np

# Funktionen
def getCode():
    clear = []
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    clear.append([a, b, c, d])
    code = []
    for c in np.array(clear):
        result = np.mod(c.dot(G), 2)
        code.append(result)
    return code


def getHamming():
    code = np.array(getCode())
    min = float("inf")
    for c in code:
        nonzero = np.count_nonzero(c)
        if (nonzero != 0) & (min > nonzero):
            min = nonzero
    return min


def getSyndromes():
    oneBitErrors = np.array(np.eye(7), int)
    syndromes = []
    for e in oneBitErrors:
        syndrome = np.mod(H.dot(e), 2)
        syndromes.append(syndrome)
    syndromes = np.array(syndromes)
    return syndromes, oneBitErrors


def verifyAndCorrect(codeWord):
    s = np.mod(H.dot(codeWord), 2)
    correct = np.array_equal(s, np.zeros(3))
    syndromes, oneBitErrors = getSyndromes()

    oneBitErrors = np.array(np.eye(7), int)
    cancorrect = canCorrect()

    correctedCodeWord = None
    if (not correct) & cancorrect:
        indices = np.where((syndromes[:, 0] == s[0]) & (syndromes[:, 1] == s[1]) & (syndromes[:, 2] == s[2]))
        correctedCodeWord = np.mod(oneBitErrors[indices[0]] + codeWord, 2)[0]
    return correct, cancorrect, correctedCodeWord


def canCorrect():
    dmin = getHamming()
    t = math.floor((dmin-1)/2)
    return t == 1


def canCorrectOld(syndromes):
    # old approach checking if syndromes are unique
    syndromes_ca = np.ascontiguousarray(syndromes)
    unique = np.unique(syndromes_ca.view(
        [('', syndromes_ca.dtype)] * syndromes_ca.shape[1]))  # format it so unique compares the subarrays
    unique = unique.view(syndromes_ca.dtype).reshape(
        (unique.shape[0], syndromes_ca.shape[1]))  # back to original format
    can_correct = (len(unique) == len(syndromes))


def userChoice():
    print("\nAktuelle Generator Matrix: ")
    for i in range(4):
        print(G[i])
    print("\n[0] Generatormatrix setzen")
    print("[1] Liste aller Codewoerter anzeigen")
    print("[2] Hamming-Distanz berechnen")
    print("[3] Syndrome zu allen Fehlervektoren berechnen")
    print("[4] Wort auf Korrektheit prüfen und ggf. korrigieren")
    print("[q] Beenden.")
    return input("Bitte einen Menuepunkt auswaehlen\n")

def generateH():
    C = G[np.ix_([0, 1, 2, 3], [4, 5, 6])]
    C_Transposed = np.transpose(C)
    return np.append(C_Transposed, np.array(np.eye(3), int), axis=1)

# Hauptprogramm

# default matrix G
G = np.array([
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1]
])

H = generateH()

choice = ''
print("Default Generatormatrix gesetzt")

while choice != 'q':
    choice = userChoice()
    if choice == '0':
        repeat = True
        while repeat:
            try:
                matrix = np.zeros((4, 7))
                print("Zeilenweise Eingabe mit Leerzeichen zur Trennung:")
                for i in range(4):
                    matrix[i] = input().split(" ")
                G = matrix
                H = generateH()
                repeat = False
            except Exception:
                print("Bitte erneut versuchen")
    elif choice == '1':
        print("Codewoerter:")
        code = np.array(getCode())
        for i in range(0, code.shape[0]):
            print(code[i])
    elif choice == '2':
        print("Minimale Hamming-Distanzge dmin = ", getHamming())
    elif choice == '3':
        print("1-Bit-Fehlervektoren - Syndrome:")
        syndromes, oneBitErrors = getSyndromes()
        for i in range(0, syndromes.shape[0]):
            print(oneBitErrors[i], " - ", syndromes[i])
    elif choice == '4':
        repeat = True
        while repeat:
            try:
                print("Bitte Codewort eingeben mit Leerzeichen zur Trennung:")
                codeWord = input().split(" ")
                codeWord = np.array(codeWord, int)
                if len(codeWord) != 7:
                    raise Exception
                repeat = False
            except Exception:
                print("Bitte erneut versuchen")
        correct, can_correct, correctedCodeWord = verifyAndCorrect(codeWord)
        if correct:
            print("Korrektes Codewort")
        elif not can_correct:
            print("Kann nicht korrigiert werden")
        else:
            print("Korrigiertes Codewort: ", correctedCodeWord)
    elif choice == 'q':
        print("Anwendung beendet.")
    else:
        print("\nKein gueltiger Menuepunkt.\n")
