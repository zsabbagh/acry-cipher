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
parser.add_argument('-r', '--rules', help='pre-rules to apply', type=str, default='')
parser.add_argument('-x', '--exclude', help='exclude character as space', type=str, default='')
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
bigram = ['th','he','in','er','an','re','on','at','en','nd','ti','es','or','te','of','ed','is','it','al','ar','st','to','nt','ng','se','ha','as','ou','io','he','le','in','ve','er','co','an','me','re','de','on','hi','at','ri','en','ro','nd','ic','ti','ne','es','ea','or','ra','te','ce']
trigrams = ['the', 'and', 'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for', 'ent', 'ion', 'ter', 'was']
expected_frequency = [0.072, 0.013, 0.024, 0.037, 0.112, 0.02, 0.018, 0.054, 0.061, 0.001, 0.007, 0.035, 0.021, 0.058, 0.066, 0.017, 0.001, 0.053, 0.056, 0.08, 0.024, 0.009, 0.021, 0.001, 0.017, 0.001, 0.120]
expected_frequency = [0.0] * 10 + expected_frequency + [0.0]
for i in range(len(alpha)):
    expected_frequency[i] = [alpha[i], expected_frequency[i]]
expected_frequency = sorted(expected_frequency, key=lambda x : x[1], reverse=True)

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
    for c in chars:
        i = alpha.index(c)
        ls[i] = chars[c] / float(len(text))
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

def printcol(s, colour, end=''):
    print('\033[' + str(colour) + 'm' + s + '\033[0m', end=end)

def parse_rules(rules, inp):
    inp = inp.split(',')
    new = []
    for e in inp:
        e = e.split('-')
        if len(e) > 1:
            rules[e[0].upper()] = e[1].lower()
            new.append(e[0].upper())

def stats(text: str) -> None:
    """
        Statistical approach
    """
    fqs = get_freqtable(text)
    freqs = []
    for i in range(len(alpha)):
        freqs.append([alpha[i], fqs[i]])
    freqs = sorted(freqs, key=lambda x : x[1], reverse=True)[:len(frequency)]
    # Try to exclude one of the tops which should be space
    rules = {}
    for a in alpha:
        rules[a] = a
    parse_rules(rules, args.rules)
    while True:
        print()

        text = list(text)
        for i in range(len(text)):
            if text[i].upper() != rules[text[i].upper()]:
                text[i] = rules[text[i].upper()]
        text = ''.join(text)

        printcol("\n[ min frequency ] " + str(args.min), 9)

        fqs = get_freq(text)
        print("\n[ characters ]")
        for i in range(len(freqs)):
            print('\t' + freqs[i][0] + ': ' + str(round(freqs[i][1], 3)),end=',\texpected ')
            print(expected_frequency[i][0] + ': ' + str(round(expected_frequency[i][1], 3)))
        print()

        bis = get_freq(text, seq=2, min_freq=args.min/3, exclude=args.exclude)
        tris = get_freq(text, seq=3, min_freq=args.min/3, exclude=args.exclude)
        print("\n-- bigrams --")
        print(bigram)
        print(bis)
        print("\n-- trigrams --")
        print(trigrams)
        print(tris)
        for c in text[:args.length]:
            if c == args.exclude:
                print(' ', end='')
                continue
            if c in alpha:
                print('\033[31m' + c +'\033[0m', end="")
            else:
                print('\033[33m' + c + '\033[0m', end="")
        print()
        # One of the trigrams is most likely THE (or AND)
        print("\n--- Rules applied ---")
        for k in rules:
            if rules[k].islower():
                print(k + '-' + rules[k], end=',')
        print()
        inp = input('\nreplace? [x-y replaces x with y, comma delimits, no ends]\n')
        if inp != 'no':
            parse_rules(rules, inp)
        else:
            break
    
    

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
    if args.exclude:
        ls = list(map(len, text.split(args.exclude)))
        print('Average word length: ')
        print(sum(ls) / float(len(ls)))
    if args.path == '2':
        vigenere(text, args.vigenere, key_len=args.keylen)
    else:
        stats(text)

if __name__ == "__main__":
    main()
