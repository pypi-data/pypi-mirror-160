import os

# Default Java
java_linux = '/usr/bin/java'  # fetch it from env vars???
java_windows = 'java'

# SAS globals...
all_obj_types = ['DeployedFlow', 'DeployedJob', 'ExternalFile', 'Folder',
                     'Library', 'Role', 'Server', 'StoredProcess', 'Table',
                     'User', 'Job']


#**********************************
# Default platfrom settings
###################################
# SASMA
###################################
sasma_sasobjsp_host = 'vs246.imb.ru'
sasma_sasobjsp_port = '8591'
sasma_workspace = 'SASApp_DI - Workspace Server'
##################################
# SAS Scoring
###################################
sascs_sasobjsp_host = 'vs2458.imb.ru'
sascs_sasobjsp_port = '8591'
sascs_workspace = 'DRKR - Workspace Server'
sascs_sasapp_workspace = 'SASApp - Workspace Server'
sascs_alloved_appservers = [sascs_workspace, sascs_sasapp_workspace]
#**********************************
sasvs235_sasobjsp_host = 'vs235.imb.ru'
sasvs235_sasobjsp_port = '8591'
sasvs235_drkr_workspace = 'DRKR - Workspace Server'
sasvs235_sasapp_workspace = 'SASApp - Workspace Server'
sasvs235_drkr_pm_workspace = 'DRKR_PM - Workspace Server'
sasvs235_drkr_fdp_workspace = 'DRKR_FDP - Workspace Server'
sasvs235_drkr_scu_workspace = 'DRKR_SCU - Workspace Server'
sasvs235_drkr_rt_workspace = 'DRKR_RT - Workspace Server'
sasvs235_drkr_rwo_workspace = 'DRKR_RWO - Workspace Server'
sasvs235_alloved_appservers = [sasvs235_drkr_workspace, sasvs235_sasapp_workspace, sasvs235_drkr_pm_workspace,
                               sasvs235_drkr_fdp_workspace, sasvs235_drkr_scu_workspace, sasvs235_drkr_rt_workspace,
                               sasvs235_drkr_rwo_workspace]
#**********************************
sasvs221_sasobjsp_host = 'vs221.imb.ru'
sasvs221_sasobjsp_port = '8591'
sasvs221_drkr_workspace = 'DRKR - Workspace Server'
sasvs221_sasapp_workspace = 'SASApp - Workspace Server'
sasvs221_dsur_workspace = 'DSUR - Workspace Server'
sasvs221_dfpc_workspace = 'DFPC - Workspace Server'
sasvs221_aso_workspace = 'ASO - Workspace Server'
sasvs221_alloved_appservers = [sasvs221_drkr_workspace, sasvs221_dsur_workspace, sasvs221_dfpc_workspace,
                               sasvs221_aso_workspace]
##################################
# SAS OA
###################################
sasoa_sasobjsp_host = 'vs990.imb.ru'
sasoa_sasobjsp_port = '8591'
sasoa_sasapp_workspace = 'SASApp - Workspace Server'
###################################
# HashicorpVault settings variables
###################################
hvac_url = 'https://hvault.intranet'
hvac_token_env_var = 'HVAC_TOKEN'
hvac_token = os.environ.get(hvac_token_env_var, default=None)
hvac_role_id_env_var = 'HVAC_ROLE_ID'
hvac_role_id = os.environ.get(hvac_role_id_env_var, default=None)
hvac_secret_env_var = 'HVAC_SECRET_ID'
hvac_secret_id = os.environ.get(hvac_secret_env_var, default=None)
hvac_connections_path = 'Data_Science/dlake/airflow/connections/'
hvac_connections_mountpoint = 'CDO/'
