
# Ldap2Mattermost scripts

## Requirements

- Python 3
- ldap3
- json

## users2mattermost.py

Copy the users2mattermost.cfg.sample to users2mattermost.cfg
Edit it to match your LDAP environment and attributes.

## Run it

```bash
# python users2mattermost.py
```

## Bulk import the users into Mattermost

```bash
root@mattermost:/opt/mattermost/bin# ./platform import bulk -c /etc/mattermost/config.json /root/bulk.jsonl --apply
[2018/04/11 09:33:16 CEST] [INFO] Loaded system translations for 'en' from '/opt/mattermost/i18n/en.json'
[2018/04/11 09:33:16 CEST] [INFO] Server is initializing...
[2018/04/11 09:33:16 CEST] [INFO] Pinging SQL master database
Running Bulk Import. This may take a long time.

Finished Bulk Import.
```