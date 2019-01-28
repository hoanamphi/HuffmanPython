#####################################################
#  Introduction à la cryptographie  	###
#   Codes de Huffman             		###
####################################################

from heapq import *

#  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z']

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008]


def frequences():
    table = {}
    n = len(caracteres)
    for i in range(n):
        table[caracteres[i]] = proba[i]
    return table


F = frequences()

#  la classe Arbre


class Arbre:
    def __init__(self, lettre, gauche=None, droit=None):
        self.gauche = gauche
        self.droit = droit
        self.lettre = lettre

    def estFeuille(self):
        return self.gauche is None and self.droit is None

    def estVide(self):
        return self is None

    def __lt__(self, other):
        return self.lettre < other.lettre

    def __str__(self):
        return '<' + str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'


#  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(frequences):
    tas = []
    for i in frequences:
        tas.append((frequences[i], i, Arbre(i)))
    heapify(tas)
    while len(tas) > 1:
        gauche = heappop(tas)
        droite = heappop(tas)
        New_Arbre = Arbre("", gauche[2], droite[2])
        heappush(tas, (gauche[0]+droite[0], "", New_Arbre))
    return heappop(tas)[2]

#  Ex.2  construction du code d'Huffamn


def parcours(arbre, prefixe, code):
    if arbre.estFeuille():
        code[arbre.lettre] = prefixe
    else:
        parcours(arbre.gauche, prefixe+"0", code)
        parcours(arbre.droit, prefixe+"1", code)


def code_huffman(arbre):
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre, '', code)
    return code


#  Ex.3  encodage d'un texte contenu dans un fichier


def encodage(dico, fichier):
    f = open(fichier, "r")
    text = f.read()
    f.close()

    for lettre in text:
        if not(lettre in dico):
            dico[lettre] = 1/len(text)
        else:
            dico[lettre] = dico[lettre]+1/len(text)

    arbre = arbre_huffman(dico)
    code = code_huffman(arbre_huffman(dico))
    new_text = ""
    for lettre in text:
        new_text += code[lettre]

    text_chunks = [new_text[i: i + 8] for i in range(0, len(new_text), 8)]
    if len(new_text) % 8 != 0:
        text_chunks[len(text_chunks)-1] = text_chunks[len(text_chunks)-1] + (8-(len(new_text) % 8))*"0"

    byte_rep = bytes(int(j, 2) for j in text_chunks)

    compressed_f = open('compressed.bit', 'wb')
    compressed_f.write(byte_rep)
    compressed_f.close()

    return arbre, text_chunks, (8-(len(new_text) % 8))


dico = {}
(arbre, text_encoded, bourrage) = encodage(dico, "leHorla.txt")

#  Ex.4  décodage d'un fichier compresse


def decodage(arbre, fichierCompresse, bourrage):
    compressed_f = open(fichierCompresse, "rb")
    byte = compressed_f.read()
    compressed_f.close()

    og_code = str(bin(int(byte.hex(), 16)))[2:]
    code = og_code[:len(og_code)-bourrage+1]

    texte = ""
    while len(code) != 0:
        (lettre, code) = parcours_inverse(arbre, code)
        texte += lettre

    f = open("decompressed.txt", "w")
    f.write(texte)
    f.close()

    return texte, og_code


def parcours_inverse(arbre, code):
    if arbre.estFeuille():
        return arbre.lettre, code
    else:
        if len(code) > 1:
            if code[0] == "0":
                return parcours_inverse(arbre.gauche, code[1:])
            else:
                return parcours_inverse(arbre.droit, code[1:])
        else:
            if code[0] == "0":
                return arbre.lettre, ""
            else:
                return arbre.lettre, ""


(texte, code) = decodage(arbre, "compressed.bit", bourrage)
print((len(text_encoded), len(code)))
