# Firewall Scripts for CloudPassage Halo
Repository of scripts for doing Firewall Rule reporting with the Halo API.  This is intended give a quick way of dumping firewall rules into a text format for parsing, slicing and dicing.  Output is pipe (|) delimited.

## Install

```
git clone https://github.com/cyberhiker/halo-fw-scripts
cd cp-fwparse
pip install -r requirements.txt
```

## Running

```
Usage: fwparse.py
  [-o FILE]          Output to a specified file.
  [-s FILE]          Specify a settings file.
  [(-q -o FILE)]     Quietly, must specify -o
  (-d | --debug)     Loudly, Debug mode
  (-h | --help)      Show this screen.
  (-v | --version)   Show version.
```

That's it.
