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
        ('frequency', 'u4'),
        ('pinyin_questionable', 'u1')
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
    idx = [
        (character in row['simplified']) and (len(row['simplified'])>1)
        for row in table
    ]
    words = table[idx]
    #idx = [len(s) > 1 for s in words['simplified']]
    #words = words[idx]
    #words = [w for w in words if len(w['simplified']) > 1]
    return words


def get_reading(character, row):
    # Get pinyin syllables
    pinyin = row['pinyin'].split()
    # If # of syllables does not match # of characters, replace pinyin with ---
    if len(pinyin) != len(row['simplified']):
        pinyin = ['-' for c in row['simplified']]

    # Find character in row
    for c,p in zip(row['simplified'], pinyin):
        if c == character:
            return p

    return None


def select_multiple_readings(character, rows, min_rel_freq=0.05, safe_harbor_freq=100):
    readings = np.array([get_reading(character, d) for d in rows])

    # Get unique readings, with the order preserved
    _,idx = np.unique(readings, return_index=True)
    readings_unique = readings[np.sort(idx)]

    # Find top entry for each reading
    idx = [np.where(readings == r)[0][0] for r in readings_unique]
    #for r in np.unique(readings):
    #    idx = np.where(readings == r)[0][0]
    #    idx_sel.append(idx)
    rows_sel = rows[idx]
    readings_sel = readings[idx]
    freq_max = rows_sel['frequency'][0]
    freq = rows_sel['frequency']
    idx = (freq > freq_max*min_rel_freq) | (freq > safe_harbor_freq)
    rows_sel = rows_sel[idx]
    readings_sel = readings_sel[idx]
    return rows_sel, readings_sel


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
    parser.add_argument(
        '--include-questionable-readings',
        action='store_true',
        help='Include examples with questionable pinyin readings.'
    )
    parser.add_argument(
        '--fix-questionable-readings',
        action='store_true',
        help='Attempt to fix questionable pinyin readings.'
    )
    parser.add_argument(
        '--multiple-pronunciations',
        action='store_true',
        help='If the character is pronounced differently in different '
             'words, show an example word for each pronunciation.'
    )
    args = parser.parse_args()

    # Load the table
    fname = 'data/chinese_words_fixed.txt'
    d = load_table(fname)

    # Find example words
    rows = find_example_words(d, args.character)

    # Filter out questionable readings
    if not args.include_questionable_readings:
        idx = (rows['pinyin_questionable'] == 0)
        rows = rows[idx]

    # Get one example per reading?
    if args.multiple_pronunciations:
        rows,readings = select_multiple_readings(args.character, rows)
    else:
        readings = [get_reading(args.character,r) for r in rows]

    # Display the results
    if args.max is not None:
        rows = rows[:args.max]
        readings = readings[:args.max]

    if args.minimal:
        char_readings = ', '.join(readings)
        words_c = '、'.join([s for s in rows['simplified']])
        words_p = ', '.join([
            s.replace(' ','') + ['','*'][q]
            for s,q in zip(rows['pinyin'],rows['pinyin_questionable'])
        ])
        print(f'{args.character}|{char_readings}|{words_c}|{words_p}')
        #for r in rows:
        #    print(w['simplified'], w['pinyin'])
    else:
        for r in rows:
            print(r)

    return 0


if __name__ == '__main__':
    main()

