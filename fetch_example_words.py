#!/usr/bin/env python3


import numpy as np
from argparse import ArgumentParser


def load_table(fname):
    dtype = [
        ('traditional', 'U8'),
        ('simplified', 'U8'),
        ('function', 'U7'),
        ('pinyin', 'U26'),
        ('meaning', 'U351'),
        ('frequency', 'u4')
    ]
    d = np.genfromtxt(
        fname,
        delimiter='\t',
        skip_header=1,
        comments=None, # Some meanings contain "#"
        dtype=dtype
    )
    return d


def find_example_words(table, character):
    idx = [character in row['simplified'] for row in table]
    words = table[idx]
    words = [w for w in words if len(w['simplified']) > 1]
    return words


def main():
    parser = ArgumentParser(
        description='Look up words containing the given character.',
        add_help=True
    )
    parser.add_argument('character', type=str, help='Character to look up.')
    parser.add_argument(
        '--max',
        type=int,
        default=None,
        help='Max # of words to return'
    )
    parser.add_argument(
        '--minimal',
        action='store_true',
        help='Only return the simplified word and the corresponding pinyin.'
    )
    args = parser.parse_args()

    # Load the table
    fname = 'data/chinese_words_fixed.txt'
    d = load_table(fname)

    # Find example words
    words = find_example_words(d, args.character)

    # Display the results
    if args.max is not None:
        words = words[:args.max]

    if args.minimal:
        for w in words:
            print(w['simplified'], w['pinyin'])
    else:
        for w in words:
            print(w)

    return 0


if __name__ == '__main__':
    main()

