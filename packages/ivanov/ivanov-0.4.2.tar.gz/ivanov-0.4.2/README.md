# Ivanov
###========================
##TL; DR: All sh*t in one place!
###========================

# What for?
- Connect to SAS MA
- Connect to SASCS
- Connect to SAS Scoring
- SAS SPK object extraction
- Get vault secrets
- SAP BO blx parsing
- A lot's of other things (hidden inside)

##Examples:
### Connection to SAS MA
```
from ivanov import SASMA
sasma = SASMA(user='user@domain', password='may_be_empty_in_jupiter')
sasma.endsas() # do not forget to close session!
```
### Connection to SAS CS
```
from ivanov import SASCSS
sascs = SASCS(user='user@domain', password='may_be_empty_in_jupiter')
sascs.endsas() # do not forget to close session!
```
### Connection to SAS Scoring on vs221
```
from ivanov import SASScoringVS221
sas_vs221 = SASScoringVS221(user='user@domain', password='secret', appserver='SASApp - Workspace Server')
sas_vs221.endsas() # do not forget to close session!
```

### Connection to SAS Scoring on vs235
```
from ivanov import SASScoringVS235
sas_vs235 = SASScoringVS235(user='user@domain', password='secret', appserver='SASApp - Workspace Server')
sas_vs235.endsas() # do not forget to close session!
```

### Connection to SAS OA on vs235
```
from ivanov import SASOA
sas_vs990 = SASOA(user='user@domain', password='secret')
sas_vs990.endsas() # do not forget to close session!
```

## Current status:
- [x] Check SAS MA connection
- [x] Check SAS CS connection
- [x] Check SAS Scoring vs235 connection
- [x] Check SAS Scoring vs221 connection
- [ ] Check SAS OA (vs990) connection
- [ ] Check BO BLX parsing
- [ ] Check SAS Support funcs...
- [ ] Check vault integrations

