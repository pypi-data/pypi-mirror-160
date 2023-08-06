from .sas.core import AbstractSAS
from .globals import sasoa_sasobjsp_host, sasoa_sasobjsp_port, sasoa_sasapp_workspace


class SASOA(AbstractSAS):
    def __init__(self, user,
                       password,
                       sasobjsp_host=sasoa_sasobjsp_host,
                       sasobjsp_port=sasoa_sasobjsp_port,
                       appserver=sasoa_sasapp_workspace,
                 **kwargs):
        self.platform = 'SASOA'
        self.env_type = 'Prod'
        super(SASOA, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                    **kwargs)

    def _is_appserver_valid(self, appsever):
        allowed_appservers = [sasoa_sasapp_workspace]
        for existing_appserver in allowed_appservers:
            if existing_appserver.lower().startswith(appsever.lower()):
                return existing_appserver
        else:
            raise ValueError(f'Appserver must be one of: {allowed_appservers}')

