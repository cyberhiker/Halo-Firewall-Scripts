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
Usage:
  fwparse.py [-o FILE]
  fwparse.py [-s FILE]
  fwparse.py [(-q -o FILE)]
  fwparse.py [-dhv]

Options:
  -o FILE     Set an output file
  -s FILE     Reference a settings file
  -d          Displays Debug Output
  -h          This Screen
  -v          Displays Version
```

That's it.
