# SLURMstressor

Python script to generate Simplified Local Internet Number Resource Management with the RPKI [(SLURM)](https://tools.ietf.org/html/rfc8416) files to test RPKI validators and routers.

## Usage
```
makeSLURM.py --help
usage: makeSLURM.py [-h] [--comment] count

Generate a SLURM files with <COUNT> number of prefix assertions

positional arguments:
  count       the number of assertions to generate

optional arguments:
  -h, --help  show this help message and exit
  --comment   include comment in entry (default is to no comment)
  ```
