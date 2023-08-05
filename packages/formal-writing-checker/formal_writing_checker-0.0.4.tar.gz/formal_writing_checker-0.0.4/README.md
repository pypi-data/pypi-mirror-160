# Formal Writing Checker

A script for raising some warnings to you when writing formal documents.

Warnings are raised for:

- sentence length: 30 words (can be changed)
- passive voice
- rare terms? NOT IMPLEMENTED


## Installation

You can install this package from:
- PyPI: `pip install formal-writing-checker`
- GitHub: `pip install git+https://github.com/MartinoMensio/formal-writing-checker.git`

This package requires the `en_core_web_lg` from spacy, which you can install with one of the following:
- `formal-writing-checker-install`
- `python -m spacy download en_core_web_lg`

## Usage

Once installed, the script is available as

```bash
formal-writing-checker "Let's say I am told to check this sentence. Why am I using the passive voice anyways?"

# Or use a text file as input
cat > example_long_text.txt <<EOF
On offering to help the blind man, the man who then stole his car, had not, at that precise moment, had any evil intention, quite the contrary, what he did was nothing more than obey those feelings of generosity and altruism which, as everyone knows, are the two best traits of human nature and to be found in much more hardened criminals than this one, a simple car-thief without any hope of advancing in his profession, exploited by the real owners of this enterprise, for it is they who take advantage of the needs of the poor.
EOF

cat example_long_text.txt | formal-writing-checker

# or in a pipe after any other command (e.g. to take as input a latex files)
detex example_latex.tex | formal-writing-checker
```

## Options

The behaviour can be customised with the following options (can be seen with `formal-writing-checker --help`):

```text
  -m, --max-sentence-length INTEGER
                                  Maximum sentence length  [default: 30]
  -s, --use-statistical-sentencizer
                                  Use statistical sentencizer instead
                                  of rule-based sentencizer  [default: False]

  -l, --ignore-sentence-length    Disable passive voice check  [default:
                                  False]

  -p, --ignore-passive-voice      Disable passive voice check  [default:
                                  False]
```


### Deploy utils
```bash
python setup.py sdist
# upload to pypi
twine upload dist/formal_writing_checker-0.0.4.tar.gz