## API Scripts for CloudPassage Halo
Repository of scripts for doing Firewall Rule reporting with the Halo API.  This is intended give a quick way of dumping firewall rules into a text format for parsing, slicing and dicing.  Output is pipe (|) delimited.

### Install

```
git clone https://github.com/cyberhiker/halo-scripts && \
cd halo-scripts && \
pip install -r requirements.txt
```

### Running

Be sure to put your valid API keys in the settings.yml before you start.

These command line options may or may not work.  I usually just throw the output to the screen and give it the >> treatment.

```
Usage:
  script.py [-o FILE]
  script.py [-s FILE]
  script.py [(-q -o FILE)]
  script.py [-d]
  script.py [-h]

Options:
  -o FILE     Set an output file
  -s FILE     Reference a settings file outside this directory
  -q          Quietly, must use -o
  -d          Displays Debug Output
  -h          This Screen
```

That's it.  Let me know if you have any issues ... by filing and issue.
