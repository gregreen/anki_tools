# anki_tools
Various small tools to use alongside Anki.

## Looking up a Chinese word

The script `explore_word.py` can be used to look up the definition, example sentences and historical usage frequency (normalized by 的) of a Chinese word:

    $ python3 explore_word.py 普通话
    
This will open up a number of web pages in a browser window.

## Generating a Chinese character stroke-order diagram

In order to generate a stroke-order diagram, first start up a local server:

    $ python3 -m http.server

Then, to generate a diagram for a character (we'll use 跳), load up the following website on the local server (which we assume to be `http://0.0.0.0:8000`):

    $ google-chrome http://0.0.0.0:8000/render_hanzi.html?w=1024&b=4096&c=跳

This will prompt you to download a `.webm` video. Anki can't handle `.webm` graphics, so we convert it to `.webp`:

    $ bash hanzi_webm2webp.sh 跳.webm

The resulting image, `跳.webp`, can be loaded into Anki.

## Looking up example words for a Chinese character

There is a script to find the most common example words (in Mandarin) for any given Chinese character:

    $ python3 fetch_example_words.py 我 --max 2 --minimal

This will return:

    我们 wǒmen
    我国 wǒguó

This script makes use of a frequency list of Mandarin words, compiled by Keh-Jiann Chen and the CKIP Group of Academia Sinica. The source list is available [here](https://web.archive.org/web/20120610034235/http://childes.psy.cmu.edu/morgrams/chinese-xls.zip). Slight modifications/corrections were made to the source list, including the addition of simplified characters and corrections to the pinyin transliterations (e.g., "iou" was changed to "iu," and "ue" was changed to "üe" in various places).
