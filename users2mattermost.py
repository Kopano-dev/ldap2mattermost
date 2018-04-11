#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import ldap3
import json

versiontemplate = \
    """{
      "type": "version",
      "version": 1
    }"""

usertemplate = \
    """{
      "type": "user",
      "user": {
        "username": "",
        "email": "",
        "nickname": "",
        "first_name": "",
        "last_name": "",
        "position": "",
        "roles": "system_user"
      }
    }"""

ldap_server = '192.168.10.41'
bind_dn = 'cn=admin,dc=farmer,dc=lan'
bind_pass = 'kopano'
search_base = 'ou=users,dc=farmer,dc=lan'
ldap_attributes = ['uid', 'givenname', 'sn', 'mail', 'cn', 'title']
ldap_filter = '(kopanoAccount=1)'


def main():
    server = ldap3.Server(ldap_server)
    connection = ldap3.Connection(server, bind_dn, bind_pass, auto_bind=True)
    connection.search(
        search_base=search_base,
        search_filter=ldap_filter,
        attributes=ldap_attributes)

    with open('bulk.jsonl', 'w') as output:

        vt = json.loads(versiontemplate)
        output.write(json.dumps(vt))

        for i in connection.response:

            mm = json.loads(usertemplate)
            mm['user']['username'] = i['attributes']['uid'][0]
            mm['user']['first_name'] = i['attributes']['givenname'][0]
            mm['user']['last_name'] = i['attributes']['sn'][0]
            mm['user']['email'] = i['attributes']['mail'][0]
            mm['user']['nickname'] = i['attributes']['cn'][0]
            if len(i['attributes']['title']):
                mm['user']['position'] = i['attributes']['title'][0]
            output.write('\n' + json.dumps(mm))


if __name__ == "__main__":
    main()
