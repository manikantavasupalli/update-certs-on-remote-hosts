#!/bin/bash
export PATH=$PATH:/usr/local/bin/
/Users/mvasupalli/Library/Python/3.6/bin/fab -f fabfile.py -R "test" -i "$HOME/patching/id_rsa_splunk" -P --set component="aci_all"  starter
