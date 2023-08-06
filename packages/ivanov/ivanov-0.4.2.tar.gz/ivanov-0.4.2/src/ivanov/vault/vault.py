import hvac
import certifi
import logging
import os
from urllib.parse import parse_qsl, unquote, urlparse
from ..globals import hvac_url, hvac_token, hvac_secret_id, hvac_role_id, hvac_connections_path, \
    hvac_connections_mountpoint, hvac_token_env_var, hvac_secret_env_var, hvac_role_id_env_var

logging.getLogger(__name__)


def get_hvac_client(hvac_url: str = hvac_url,
                    namespace: str = None,
                    token: str = hvac_token,
                    hvac_role_id: str = hvac_role_id,
                    hvac_secret_id: str = hvac_secret_id,
                    ldap_login: str = None,
                    ldap_password: str = None,
                    verify=True,
                    **kwargs):
    if not token:
        token = os.environ.get(hvac_token_env_var, default=None)
    if not hvac_role_id:
        hvac_role_id = os.environ.get(hvac_role_id_env_var, default=None)
    if not hvac_secret_id:
        hvac_secret_id = os.environ.get(hvac_secret_env_var, default=None)
    try:
        if token:
            client = hvac.Client(url=hvac_url, token=token, namespace=namespace, verify=verify)
        elif hvac_role_id and hvac_secret_id:
            client = hvac.Client(url=hvac_url, namespace=namespace, verify=verify)
            client.auth.approle.login(hvac_role_id, hvac_secret_id, use_token=True)
        elif ldap_login and ldap_password:
            client = hvac.Client(url=hvac_url, namespace=namespace, verify=verify)
            client.auth.ldap.login(username=ldap_login, password=ldap_password)
        else:
            print(f"Something is missing, cannot authentificate.")
            raise ValueError
    except ConnectionError as e:
        print(f"Connection error. Probably, you don't have correct certificates/chain for {hvac_url}.\n"
              f"Certificates are located at {certifi.where()}\n"
              f"You can also use REQUESTS_CA_BUNDLE env variable to point to correct certs.\n"
              f"Full error: {str(e)}\n"
              f"Also, if you are some kind of naughty boy/girl/whatever you can pass verify=False as one of the args\n"
              f"Which is, obviously, very bad. Added it just for testing.\n")
        return
    return client


def _normalize_conn_type(conn_type):
    if conn_type == 'postgresql':
        conn_type = 'postgres'
    elif '-' in conn_type:
        conn_type = conn_type.replace('-', '_')
    return conn_type


def _parse_netloc_to_hostname(uri_parts):
    """Parse a URI string to get correct Hostname."""
    hostname = unquote(uri_parts.hostname or '')
    if '/' in hostname:
        hostname = uri_parts.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = unquote(hostname)
    return hostname


def _parse_from_uri(uri: str):
    uri_parts = urlparse(uri)
    conn_type = uri_parts.scheme
    conn_type = _normalize_conn_type(conn_type)
    host = _parse_netloc_to_hostname(uri_parts)
    quoted_schema = uri_parts.path[1:]
    schema = unquote(quoted_schema) if quoted_schema else quoted_schema
    login = unquote(uri_parts.username) if uri_parts.username else uri_parts.username
    password = unquote(uri_parts.password) if uri_parts.password else uri_parts.password
    port = uri_parts.port
    extra = ''
    if uri_parts.query:
        query = dict(parse_qsl(uri_parts.query, keep_blank_values=True))
        if '__extra__' in query:
            extra = query['__extra__']
        else:
            extra = query
    return {'conn_type': conn_type,
            'host': host,
            'schema': schema,
            'login': login,
            'password': password,
            'port': port,
            'extra': extra}


def get_secret_from_vault(vault_path: str, vault_mount_point: str, client: hvac.Client = None, **kwargs):
    if not client:
        client = get_hvac_client(**kwargs)
    creds = client.secrets.kv.v2.read_secret_version(path=vault_path, mount_point=vault_mount_point)
    creds = creds['data']['data']
    key = list(creds.keys())[0]  # EXTREMELY DANGER!
    value = list(creds.values())[0]  # EXTREMELY DANGER!
    return key, value


def get_connection_from_vault(connection_id: str,
                              connections_path: str = hvac_connections_path,
                              mount_point=hvac_connections_mountpoint,
                              client: hvac.Client = None, **kwargs):
    if not client:
        client = get_hvac_client(**kwargs)
    conn_path = f"{connections_path}/{connection_id}"
    response = client.secrets.kv.v2.read_secret_version(path=conn_path, mount_point=mount_point)
    conn_uri = response['data']['data']['conn_uri']
    return _parse_from_uri(conn_uri)
