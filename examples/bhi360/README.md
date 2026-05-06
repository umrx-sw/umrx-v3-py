# BHI360

Download the compiled firmware files, e.g. from 
[umrx-bhi360-fw-builds](https://github.com/umrx-sw/umrx-bhi360-fw-builds/releases)
and put it to the `./firmware` folder.

This can be done with [GitHub CLI](https://cli.github.com/) :
```bash
gh release download v0.1.0 --repo umrx-sw/umrx-bhi360-fw-builds --dir firmware
```
