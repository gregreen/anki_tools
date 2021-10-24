#!/usr/bin/env python

import webbrowser
from argparse import ArgumentParser


def open_urls(word):
    urls = [
        fr'https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={word}',
        fr'https://dict.leo.org/chinesisch-deutsch/{word}',
        fr'https://tatoeba.org/en/sentences/search?from=cmn&query="{word}"&to=',
        fr'http://jukuu.com/search.php?q={word}',
        fr'https://books.google.com/ngrams/graph?content={word}/的&year_start=1930&year_end=2008&corpus=23&smoothing=3'
    ]
    for u in urls:
        webbrowser.open(u)


def main():
    parser = ArgumentParser(
        description='Look up word on various web sites.',
        add_help=True
    )
    parser.add_argument('word', type=str, help='Word to look up.')
    args = parser.parse_args()
    open_urls(args.word)

    return 0


if __name__ == '__main__':
    main()
