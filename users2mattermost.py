#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import configparser
import json
import ldap3


def template(get):
    versiontemplate = {'type': 'version', 'version': 1}
    usertemplate = {
        'user': {
            'username': '',
            'last_name': '',
            'email': '',
            'position': '',
            'first_name': '',
            'roles': 'system_user'
        },
        'type': 'user'
    }
    if get == 'version':
        return versiontemplate
    elif get == 'user':
        return usertemplate


def getconfig():
    config = configparser.ConfigParser()
    try:
        config.read('users2mattermost.cfg')
        ldap_server = config.get('ldap', 'server')
        bind_dn = config.get('ldap', 'bind_dn')
        bind_pass = config.get('ldap', 'bind_pass')
        search_base = config.get('ldap', 'search_base')
        ldap_attributes = config.get('ldap',
                                     'attributes').replace(' ', '').split(',')
        ldap_filter = config.get('ldap', 'filter')
        port = config.getint('ldap', 'port')
        use_ssl = config.getboolean('ldap', 'use_ssl')
        mapping = dict()
        mapping['username'] = config.get('mapping', 'username')
        mapping['first_name'] = config.get('mapping', 'first_name')
        mapping['last_name'] = config.get('mapping', 'last_name')
        mapping['email'] = config.get('mapping', 'email')
        mapping['position'] = config.get('mapping', 'position')
        return ldap_server, bind_dn, bind_pass, search_base, ldap_attributes, ldap_filter, port, use_ssl, mapping
    except Exception as e:
        exit('Configuration {}\nplease check users2mattermost.cfg'.format(e))


def main():
    ldap_server, bind_dn, bind_pass, search_base, \
        ldap_attributes, ldap_filter, port, use_ssl, mapping = getconfig()
    server = ldap3.Server(ldap_server, port=port, use_ssl=use_ssl)
    connection = ldap3.Connection(server, bind_dn, bind_pass, auto_bind=True)
    connection.search(
        search_base=search_base,
        search_filter=ldap_filter,
        attributes=ldap_attributes)

    with open('bulk.jsonl', 'w') as output:
        output.write(json.dumps(template('version')))
        for result in connection.response:
            mmuser = template('user')
            for attribute in mapping:
                if mapping[attribute] in result['attributes'] and len(
                        result['attributes'][mapping[attribute]]):
                    if attribute == 'username':
                        mmuser['user'][attribute] = result['attributes'][
                            mapping[attribute]][0].lower()
                    else:
                        mmuser['user'][attribute] = result['attributes'][
                            mapping[attribute]][0]
            output.write('\n' + json.dumps(mmuser))


if __name__ == "__main__":
    main()
