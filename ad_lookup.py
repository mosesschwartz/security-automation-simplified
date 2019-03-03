import json

from ldap3 import (
    Server, Connection, ALL, NTLM, SUBTREE, ALL_ATTRIBUTES
)
import settings


def search_ad(username):
    server = Server(settings.ad_server, get_info=ALL)
    search_filter = "(&(sAMAccountName={}))".format(username)
    conn = Connection(
        server,
        user=settings.ad_user,
        password=settings.ad_password,
        authentication=NTLM,
        auto_referrals=False,
    )
    conn.bind()
    conn.search(
        search_base=settings.search_base,
        search_filter=search_filter,
        search_scope=SUBTREE,
        attributes=ALL_ATTRIBUTES,
        get_operational_attributes=True,
    )
    return json.loads(conn.response_to_json())


"""
    return {
        "entries": [
            {
                "attributes": {
                    "cn": "Moses Schwartz",
                    "title": "Staff Security Engineer",
                    "company": "Box, Inc",
                    "department": "Security Automation",
                    "employeeID": "1234",
                    "l": "Redwood City",
                    "streetAddress": "900 Jefferson Avenue",
                }
            }
        ]
    }

"""
