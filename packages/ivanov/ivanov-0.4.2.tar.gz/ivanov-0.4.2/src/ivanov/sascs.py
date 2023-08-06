from .sas.core import AbstractSAS
from .globals import sascs_sasobjsp_host, sascs_sasobjsp_port, sascs_alloved_appservers, \
    sasvs235_sasobjsp_host, sasvs235_sasobjsp_port, sasvs235_alloved_appservers, \
    sasvs221_sasobjsp_host, sasvs221_sasobjsp_port, sasvs221_alloved_appservers


class SASCS(AbstractSAS):
    def __init__(self, user,
                       password,
                       sasobjsp_host=sascs_sasobjsp_host,
                       sasobjsp_port=sascs_sasobjsp_port,
                       appserver=sascs_alloved_appservers[0],
                 **kwargs):
        self.platform = 'SASCS'
        self.env_type = 'Prod'
        self.alloved_appservers = sascs_alloved_appservers
        super(SASCS, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                    **kwargs)

    def _is_appserver_valid(self, appsever):
        for existing_appserver in self.alloved_appservers:
            if existing_appserver.lower().startswith(appsever.lower()):
                return existing_appserver
        else:
            raise ValueError(f'Appserver must be one of: {self.alloved_appservers}')


class SASScoringVS235(AbstractSAS):
    def __init__(self, user,
                         password,
                         sasobjsp_host=sasvs235_sasobjsp_host,
                         sasobjsp_port=sasvs235_sasobjsp_port,
                         appserver=sasvs235_alloved_appservers[0],
                 **kwargs):
        self.platform = 'SASScoringVS235'
        self.env_type = 'Prod'
        self.alloved_appservers = sasvs235_alloved_appservers
        super(SASScoringVS235, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                    **kwargs)

    def _is_appserver_valid(self, appserver):
        for existing_appserver in self.alloved_appservers:
            if existing_appserver.lower().startswith(appserver.lower()):
                return existing_appserver
        else:
            raise ValueError(f'Appserver must be one of: {self.alloved_appservers}')


class SASScoringVS221(AbstractSAS):
    def __init__(self, user,
                         password,
                         sasobjsp_host=sasvs221_sasobjsp_host,
                         sasobjsp_port=sasvs221_sasobjsp_port,
                         appserver=sasvs221_alloved_appservers[0],
                 **kwargs):
        self.platform = 'SASScoringVS221'
        self.env_type = 'Pre-prod'
        self.alloved_appservers = sasvs221_alloved_appservers
        super(SASScoringVS221, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                              **kwargs)

    def _is_appserver_valid(self, appserver):
        for existing_appserver in self.alloved_appservers:
            if existing_appserver.lower().startswith(appserver.lower()):
                return existing_appserver
        else:
            raise ValueError(f'Appserver must be one of: {self.alloved_appservers}')
