#!/bin/bash
export PATH=$PATH:/usr/local/bin/
/Users/mvasupalli/Library/Python/3.6/bin/fab -f fabfile.py -H "ops-zbx-prxy-01-prd404.eng.sfdc.net" -i "$HOME/patching/p_key" -P --set component="aci_all"  starter
