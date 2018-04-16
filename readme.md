# Ldap2Mattermost script

## Requirements

- Python 3
- ldap3 (install with pip3)
- json (install with pip3)

## users2mattermost.py

Copy the users2mattermost.cfg.sample to users2mattermost.cfg
Edit it to match your LDAP environment and attributes.

### Running the script

```bash
# python3 users2mattermost.py
```

This will write a file called bulk.jsonl this file will contain the users which need to be added to mattermost.

## Bulk importing the users into Mattermost

### Validate the bulk.jsonl file

```bash
root@mattermost:/opt/mattermost/bin# ./platform import bulk -c /etc/mattermost/config.json /root/bulk.jsonl
[2018/04/11 15:10:21 CEST] [INFO] Loaded system translations for 'en' from '/opt/mattermost/i18n/en.json'
[2018/04/11 15:10:21 CEST] [INFO] Server is initializing...
[2018/04/11 15:10:21 CEST] [INFO] Pinging SQL master database
Running Bulk Import Data Validation.
** This checks the validity of the entities in the data file, but does not persist any changes **
Use the --apply flag to perform the actual data import.

Validation complete. You can now perform the import by rerunning this command with the --apply flag.
```

### Import the bulk.jsonl file after validation

```bash
root@mattermost:/opt/mattermost/bin# ./platform import bulk -c /etc/mattermost/config.json /root/bulk.jsonl --apply
[2018/04/11 09:33:16 CEST] [INFO] Loaded system translations for 'en' from '/opt/mattermost/i18n/en.json'
[2018/04/11 09:33:16 CEST] [INFO] Server is initializing...
[2018/04/11 09:33:16 CEST] [INFO] Pinging SQL master database
Running Bulk Import. This may take a long time.

Finished Bulk Import.
```