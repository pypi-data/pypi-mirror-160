import logging
import json
import os
from .sascodes import extract_lib_template, extract_authdomains_template
from .core import AbstractSAS

logging.getLogger(__name__)


def extract_libraries(sasobjsp_user: str,
                      sasobjsp_pass: str,
                      sasobjsp_host: str,
                      sasobjsp_port: str,
                      appserver: str,
                      metadata_server: str,
                      metadata_port: str,
                      metadata_user: str,
                      metadata_password: str,
                      metadata_repo: str,
                      java: str,
                      sas_session: AbstractSAS = None) -> list:

    get_all_libs_query = extract_lib_template.substitute(metadata_server=metadata_server,
                                                         metadata_port=metadata_port,
                                                         metadata_user=metadata_user,
                                                         metadata_password=metadata_password,
                                                         metadata_repo=metadata_repo)
    if not sas_session:
        sas_session = AbstractSAS(sasobjsp_port=sasobjsp_port,
                                  sasobjsp_host=sasobjsp_host,
                                  sasobjsp_user=sasobjsp_user,
                                  sasobjsp_pass=sasobjsp_pass,
                                  appserver=appserver,
                                  java=java)
    sas_session.submit(get_all_libs_query)
    df = sas_session.read_dataset(libname='WORK', tablename='Libraries_final')
    jsons = json.loads(df.to_json(orient='records'))
    return jsons


def extract_authdomains(sasobjsp_user: str,
                          sasobjsp_pass: str,
                          sasobjsp_host: str,
                          sasobjsp_port: str,
                          appserver: str,
                          metadata_server: str,
                          metadata_port: str,
                          metadata_user: str,
                          metadata_password: str,
                          metadata_repo: str,
                          java: str,
                          sas_session: AbstractSAS = None) -> list:

    get_all_authdomains_query = extract_authdomains_template.substitute(metadata_server=metadata_server,
                                                         metadata_port=metadata_port,
                                                         metadata_user=metadata_user,
                                                         metadata_password=metadata_password,
                                                         metadata_repo=metadata_repo)
    if not sas_session:
        sas_session = AbstractSAS(sasobjsp_port=sasobjsp_port,
                                  sasobjsp_host=sasobjsp_host,
                                  sasobjsp_user=sasobjsp_user,
                                  sasobjsp_pass=sasobjsp_pass,
                                  appserver=appserver,
                                  java=java)
    sas_session.submit(get_all_authdomains_query)
    df = sas_session.read_dataset(libname='WORK', tablename='Libraries_final')
    jsons = json.loads(df.to_json(orient='records'))
    return jsons
