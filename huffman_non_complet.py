#####################################################
#  Introduction à la cryptographie  	###
#   Codes de Huffman             		###
####################################################

from heapq import *
from pickle import *


# La classe Arbre
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
def frequences(dico, texte):

    for lettre in texte:
        if not(lettre in dico):
            dico[lettre] = 1/len(texte)
        else:
            dico[lettre] = dico[lettre]+1/len(texte)

    return dico


def encodage(dico, fichier, destination):
    f = open(fichier, "r")
    text = f.read()
    f.close()

    frequences(dico, text)

    arbre = arbre_huffman(dico)
    code = code_huffman(arbre_huffman(dico))
    new_text = ""
    for lettre in text:
        new_text += code[lettre]

    text_chunks = [new_text[i: i + 8] for i in range(0, len(new_text), 8)]
    bourrage = (8 - (len(new_text) % 8))
    if len(new_text) % 8 != 0:
        text_chunks[len(text_chunks)-1] = text_chunks[len(text_chunks)-1] + bourrage*"0"

    byte_rep = bytes(int(j, 2) for j in text_chunks)

    compressed_f = open(destination, 'wb')

    dump(arbre, compressed_f)
    dump(bourrage, compressed_f)

    compressed_f.write(byte_rep)
    compressed_f.close()

    return code


#  Ex.4  décodage d'un fichier compresse
def decodage(fichierCompresse):
    compressed_f = open(fichierCompresse, "rb")

    arbre = load(compressed_f)
    bourrage = load(compressed_f)
    byte = compressed_f.read()
    compressed_f.close()

    og_code = str(bin(int(byte.hex(), 16)))[2:]
    if len(og_code) % 8 != 0:
        og_code = (8 - (len(og_code) % 8))*"0" + og_code
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


if __name__ == "__main__":
    dico = {}
    code = encodage(dico, "leHorla.txt", "compressed.bit")

    (texte, text_encod) = decodage("compressed.bit")
    print(code)
    print(texte)
