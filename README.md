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

    $ bash hanzi_webm2webp 跳.webm

The resulting image, `跳.webp`, can be loaded into Anki.
