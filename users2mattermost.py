#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import configparser
import json

import ldap3

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


def getconfig():
    config = configparser.ConfigParser()
    try:
        config.read('users2mattermost.cfg')
        ldap_server = config.get('ldap', 'server')
        bind_dn = config.get('ldap', 'bind_dn')
        bind_pass = config.get('ldap', 'bind_pass')
        search_base = config.get('ldap', 'search_base')
        ldap_attributes = config.get('ldap', 'attributes').replace(' ', '').split(',')
        ldap_filter = config.get('ldap', 'filter')
        mapping = {}
        mapping['username'] = config.get('mapping', 'username')
        mapping['first_name'] = config.get('mapping', 'first_name')
        mapping['last_name'] = config.get('mapping', 'last_name')
        mapping['email'] = config.get('mapping', 'email')
        mapping['nickname'] = config.get('mapping', 'nickname')
        mapping['positition'] = config.get('mapping', 'position')

        return ldap_server, bind_dn, bind_pass, search_base, ldap_attributes, ldap_filter, mapping
    except Exception as e:
        exit('Configuration {}\nplease check users2mattermost.cfg'.format(e))


def main():
    ldap_server, bind_dn, bind_pass, search_base, \
    ldap_attributes, ldap_filter, mapping = getconfig()

    server = ldap3.Server(ldap_server)
    connection = ldap3.Connection(server, bind_dn, bind_pass, auto_bind=True)
    connection.search(
        search_base=search_base,
        search_filter=ldap_filter,
        attributes=ldap_attributes)

    with open('bulk.jsonl', 'w') as output:

        vt = json.loads(versiontemplate)
        output.write(json.dumps(vt))

        for result in connection.response:
            mmuser = json.loads(usertemplate)
            for attribute in mapping:
                if mapping[attribute] in result['attributes'] and len(result['attributes'][mapping[attribute]]):
                    mmuser['user'][attribute] = result['attributes'][mapping[attribute]][0]
            output.write('\n' + json.dumps(mmuser))

if __name__ == "__main__":
    main()
