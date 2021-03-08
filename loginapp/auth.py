from random import randint

import ldap3


def connect_server(server_uri, user_dc, password):
    """

    :param server_uri: LDAP Server URI
    :param user_dc: User DC
    :param password: Password
    :return: LDAP conenction
    """
    server = ldap3.Server(server_uri, get_info=ldap3.ALL)
    connection = ldap3.Connection(server, user=user_dc, password=password)
    return connection


def authenticate(server_uri, base, username, password):
    """

    :param server_uri: LDAP Server URI
    :param base: LDAP base
    :param username: Username
    :param password: Password
    :return: boolean
    """
    user_dc = "uid=" + username + ',' + base
    connection = connect_server(server_uri, user_dc, password)

    if not connection.bind():  # This is authenticate operation
        return False
    else:
        return True


def add_user(server_uri, username, password):
    """
    :param server_uri: LDAP Server Uri
    :param username: Username
    :param password: Password
    :return: String: response
    """
    connection = connect_server(server_uri, "cn=admin,dc=example,dc=com", "login")
    connection.bind()

    connection.add('uid={},ou=users,dc=example,dc=com'.format(username),
                   ['account', 'posixAccount', ],
                   {'cn': '{}'.format(username),
                    'uidNumber': randint(1, 10000),
                    'userPassword': '{}'.format(password),
                    'gidNumber': 100,
                    'homeDirectory': '/home/{}'.format(username)})

    print(connection)
    res = connection.result

    return res['description']  # success, entryAlreadyExists

# server_uri = 'ldap://127.0.0.53'
#
#
# server = ldap3.Server(server_uri, get_info=ldap3.ALL)
# user_dc = "cn=admin,dc=example,dc=com"
# password = "login"
# connection = ldap3.Connection(server, user_dc, password)
#
# print(connection.bind())
# print(connection.result)
#
# username = 'killl'
# password = '123'
#
# #
# print(connection.result)
