"""
    Cipher cracker
"""
import sys
import copy
import os
import re
import time # .sleep(), .time(), .time_ns()
import argparse
import numpy as np

alpha = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_#')
parser = argparse.ArgumentParser(prog = 'crack', description = 'Crack the ciphers of ACry course', epilog = 'Cracking the cipher.')
parser.add_argument('path', help='the cipher to crack')      # option that takes a value
parser.add_argument('-v', '--verbose', help='verbosity', action='store_true')
parser.add_argument('-s', '--seq', help='count sequence of n chars', type=int, default=0)
parser.add_argument('-q', '--question', help='ask to continue', action='store_true')
parser.add_argument('-f', '--freq', nargs='?', const=2, default=0,  help='frequency table', type=int) 
parser.add_argument('--vigenere',  nargs='?', const=129, help='vigenere', default=0, type=int) 
parser.add_argument('--bigram', nargs='?', default='bigram.data',  help='bigram frequency table', type=str)
parser.add_argument('-l', '--length', help='demo text length', default=100, type=int)
parser.add_argument('-k', '--keylen', help='key length', default=12, nargs='?', const=12, type=int)
parser.add_argument('--min', help='minimum frequency', default=0.01, type=float)
args = parser.parse_args()

frequency = " ETAOINSHRDLCUMWFGYPBVKJXQZ\n"
alphafreq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
bigram = ['TH','HE','IN','ER','AN','RE','ON','AT','EN','ND','TI','ES','OR','TE','OF','ED','IS','IT','AL','AR','ST','TO','NT','NG','SE','HA','AS','OU','IO','HE','LE','IN','VE','ER','CO','AN','ME','RE','DE','ON','HI','AT','RI','EN','RO','ND','IC','TI','NE','ES','EA','OR','RA','TE','CE']
trigrams = ['THE']

def counter(d, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1

def get_freq(text, seq=1, min_freq=0.00, exclude='') -> list:
    """
        Get characters in a list ordered by frequency
    """
    chars = {}
    for i in range(0, len(text)):
        if i-seq+1 >= 0:
            t = text[i-seq+1:i+1]
            if (exclude and exclude not in t) or not exclude:
                counter(chars, t)
    ls = []
    for c in chars:
        ls.append([c, chars[c] / float(len(text))])
    ls = sorted(ls, key=lambda x : x[1], reverse=True)
    if min_freq > 0:
        ls = filter(lambda x : float(x[1]) >= min_freq, ls)
    ls = [x[0] for x in ls]
    return ls

def get_freqtable(text) -> list:
    """
        Get characters in a list ordered by frequency
    """
    chars = {}
    for i in range(0, len(text)):
        counter(chars, text[i])
    ls = [0.0] * len(alpha)
    return ls

def intersect_elems(what: str, elems: list):
    res = []
    for e in elems:
        if what in e:
            res.append(e)
    return res

def gramalysis(fqs, bis, tris):
    mapper = {}
    for a in alpha:
        mapper[a] = None
    for tri in tris:
        for trigram in trigrams:
            # Let's assume tri = trigram
            for i in range(3):
                mapper[tri[i]] = trigram[i]
            # We now have our THE
            for bi in bis:
                pass

def printcol(s, colour):
    print('\033[' + str(colour) + 'm' + s + '\033[0m', end="")

def stats(text: str) -> None:
    """
        Statistical approach
    """
    fqs = get_freq(text)
    # Try to exclude one of the tops which should be space
    mapper = {}
    for a in alpha:
        mapper[a] = a
    for c in fqs:
        print()
        bis = get_freq(text, seq=2, min_freq=args.min)
        tris = get_freq(text, seq=3, min_freq=args.min)
        printcol("\nmin frequency = " + str(args.min), 7)
        print("\n-- bigrams --")
        print(bigram)
        print(bis)
        print("\n-- trigrams --")
        print(trigrams)
        print(tris)
        if args.verbose:
            for c in text[:args.length]:
                if c in alpha:
                    print('\033[31m' + c +'\033[0m', end="")
                else:
                    print('\033[33m' + c + '\033[0m', end="")
            print()
        # One of the trigrams is most likely THE (or AND)
        inp = input('\nreplace? [x-y replaces x with y, comma delimits, no ends]\n')
        if inp != 'no':
            inp = inp.split(',')
            new = []
            for e in inp:
                e = e.split('-')
                if len(e) > 1:
                    mapper[e[0].upper()] = e[1].lower()
                    new.append(e[0].upper())
            text = list(text)
            for i in range(len(text)):
                if text[i].upper() != mapper[text[i].upper()]:
                    text[i] = mapper[text[i].upper()]
            text = ''.join(text)
        else:
            break
    print("\n--- Rules applied ---")
    for k in mapper:
        print(k + '-' + mapper[k], end=',')
    

def find_keylen(text: str, max_len: int) -> int:
    occ = []
    for i in range(max_len):
        occ.append([i, 0])
        for j in range(len(text)-i):
            if text[i+j] == text[j]:
                occ[i][1] += 1
        occ[i] = [i, occ[i][1]]
    occ = sorted(occ, key=lambda x : x[1], reverse=True)
    keys = copy.deepcopy(occ)
    for i in range(1, max_len):
        for j in range(1, max_len):
            if i != j and (j % i) == 0:
                keys[i][1] += occ[j][1]
    keys = sorted(keys, key=lambda x : x[1])
    key_len = keys[-1][0] if keys[-1][0] != 0 else keys[-2][0]
    return key_len

def vigenere(text: str, max_len: int = 1000, key_len: int = 0) -> None:
    # First find key length
    if not max_len:
        max_len = len(text)
    if not key_len:
        key_len = find_keylen(text, max_len)
    print('Chosen key length is ', key_len)
    # Add modulo
    mods = [[]] * key_len
    for i in range(len(text)):
        mods[i % key_len].append(text[i])
    mods = list(map(''.join, mods))
    freqs = list(map(get_freq, mods))
    # For each mod, check frequency and deviation from 
    # Space starts frequency, then it is ABC... etc
    frequency = [0.072, 0.013, 0.024, 0.037, 0.112, 0.02, 0.018, 0.054, 0.061, 0.001, 0.007, 0.035, 0.021, 0.058, 0.066, 0.017, 0.001, 0.053, 0.056, 0.08, 0.024, 0.009, 0.021, 0.001, 0.017, 0.001]
    space = 0.120
    # Assume numbers do not occur often, neither newline
    frequency = np.array([0.0] * 10 + frequency + space + [0.0])
    # Go through all characters
    for i in range(key_len):
        mod = mods[i]
        for shift in range(len(alpha)):
            pass

def main():
    text = ''.join(open(args.path, 'r').read().rstrip().split('\n'))
    if args.path == '2':
        vigenere(text, args.vigenere, key_len=args.keylen)
    else:
        stats(text)

if __name__ == "__main__":
    main()
