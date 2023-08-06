import os.path
import os
import subprocess
import zipfile
import xml.etree.ElementTree as ET
import saspy
import logging
import tempfile
from datetime import datetime
from ..globals import all_obj_types
from sys import platform


logging.getLogger(__name__)

if platform == "linux" or platform == "linux2":
    from ..globals import java_linux as java
else:
    from ..globals import java_windows as java


def create_saspyconn(sasobjsp_host, sasobjsp_port, appserver, java=java):
    logging.debug(f'Creating temporary sascfg file...')
    saspy_conn = tempfile.NamedTemporaryFile(mode='w+', delete=False)  # needed to manually deleted after, to be compitable with win
    saspy_conn.write(f"""SAS_config_names=['sasconnection']
SAS_config_options = {{'lock_down': False,
                    'verbose'  : True,
                    'prompt'   : True
                    }}
SAS_output_options = {{'output' : 'html5'}} 
sasconnection = {{'java'      : '{java}',
            'iomhost'   : ['{sasobjsp_host}'],
            'iomport'   : {sasobjsp_port},
            'appserver' : '{appserver}',
            'encoding': 'cyrillic',
            'options' : ["-fullstimer"]
            }}""")
    saspy_conn.seek(0)
    saspy_conn.close()
    logging.debug(f'Created temporary sascfg file.')
    return saspy_conn


class AbstractSAS(saspy.SASsession):
    def __init__(self, sasobjsp_user,
                       sasobjsp_pass,
                       sasobjsp_host,
                       sasobjsp_port,
                       appserver,
                       java=java,
                       **kwargs):
        logging.debug('Initializing Abstract SAS class')
        self.sasobjsp_host = sasobjsp_host
        self.sasobjsp_port = sasobjsp_port
        self.sasobjsp_user = sasobjsp_user
        self.sasobjsp_pass = sasobjsp_pass
        self.appserver = appserver
        self.java = java
        logging.debug('Generating saspy conn file')
        self.saspy_conn = create_saspyconn(sasobjsp_host=self.sasobjsp_host,
                                           sasobjsp_port=self.sasobjsp_port,
                                           appserver=self.appserver,
                                           java=self.java)
        logging.debug(f'Generated saspy conn file {self.saspy_conn.name}')
        super(AbstractSAS, self).__init__(cfgfile=self.saspy_conn.name,
                                           cfgname='sasconnection',
                                           omruser=self.sasobjsp_user,
                                           omrpw=self.sasobjsp_pass)
        logging.info(f'Pid in sas server side({self.sasobjsp_host}) is  {self.SASpid}')
        print(f'Pid in sas server side({self.sasobjsp_host}) is  {self.SASpid}')

    def read_dataset(self, tablename: str, libname: str = 'WORK'):
        """
        Read data From SAS. Data is returned is in the form of Pandas DataFrame.
        :param libname: library, is which table is stored
        :param tablename: name of the table, you want to read
        :return: pd.Dataframe
        """
        df = self.sasdata2dataframe(table=tablename, libref=libname)
        return df

    def write_dataset(self, df, tablename: str, libname: str = 'WORK'):
        """
        Writes dataframe To SAS.
        :param df: dataframe to write
        :param tablename: table, in which you want to write data.
        :param libname: library, in which you want to write data.
        :return:
        """
        result = self.dataframe2sasdata(df=df, table=tablename, libref=libname)
        return result

    def show_libs(self):
        libs = self.assigned_librefs()
        return libs

    def run_script(self, script):
        if script:
            pass
        return self.submit(code=script)

    def endsas(self):
        os.unlink(self.saspy_conn.name)  # need to do it manually for win systems
        super(AbstractSAS, self).endsas()


def get_obj_from_deploymap(root):
    extracted_objects = []
    meta_id = root.attrib.get('Id', root.text)
    obj_name = root.attrib.get('Name', root.text)
    obj_type = root.attrib.get('PublicType', root.text)
    desc = root.attrib.get('Desc', root.text)
    path = root.attrib.get('Path', root.text)
    if meta_id and path:
        meta_object = {'METADATA_ID': meta_id,
                       'OBJECT_TYPE': obj_type,
                       'OBJECT_NAME': obj_name,
                       'OBJECT_PATH': path,
                       'META_OBJ_DESC': desc}
        extracted_objects.append(meta_object)
    for elem in root.getchildren():
        extracted_objects = extracted_objects + get_obj_from_deploymap(elem)
    return extracted_objects


def get_objects_from_spk(spk_path, object_types=None):
    """
    Extracts information about metadata objects from spk
    :param spk_path: path (str) to spk
    :param object_types: list of objects types (str), needed to be extracted.
    If not provided - defaults to ['DeployedFlow', 'DeployedJob',
    'ExternalFile', 'Folder', 'Library', 'Role', 'Server', 'StoredProcess',
    'Table', 'User']
    :return: dict with keys: 'Success' - indicating the success of operation and
    'Objects', containing dict with specified metadata object keys, containing
    list of path's --- FIX THAT DESCRIPTION!!!
    """
    logging.info(f"Object extraction from {spk_path} started.")
    errors = []
    warnings = []
    all_obj_types = ['DeployedFlow', 'DeployedJob', 'ExternalFile', 'Folder',
                     'Library', 'Role', 'Server', 'StoredProcess', 'Table',
                     'User', 'Job', 'PhysicalTable', 'Tree', 'SASLibrary']
    if not object_types:
        object_types = all_obj_types
    extracted_objects = {i: [] for i in object_types}
    logging.debug(f"Objects to extract: {extracted_objects}")
    logging.debug(f"Opening file {spk_path}")
    try:
        spk = zipfile.ZipFile(spk_path)
        if 'DeployMap.xml' in spk.namelist():
            deploymap = ET.parse(spk.open('DeployMap.xml'))
            root = deploymap.getroot()
            extracted_objects = get_obj_from_deploymap(root)
            logging.info(f"List of objects extracted successfully.")
            spk.close()
        else:
            spk.close()
            raise FileNotFoundError
    except Exception as e:
        logging.error(f"Errors during extraction: {str(e)}")
        errors.append(str(e))
    finally:
        return {'Completed': True,
                'Warnings': warnings,
                'Errors': errors,
                'Log': None,
                'Objects': extracted_objects}


def check_sas_code(sas_script_path: str = None,
                   sas_script:str = None,
                   log_path: str = None) -> dict:
    """
    Sas code checking. Implements various sas scripth checks
    (drop database includes, etc.)
    :param sas_script_path: path to sas log file (str)
    :param log_path: path to validation log file (str)
    :return: dict with key 'Success', indicating the results of validation.
    """
    logging.info(f"Checking of script {sas_script_path} stated.")
    validation_log_lines = []
    validation_status = False
    try:
        if sas_script_path:
            with open(sas_script_path, 'r') as f:
                sas_script = f.read()
                ### checks....
                pass
        elif sas_script:
            pass
        else:
            raise ValueError
        validation_log_lines += 'Validated\n'
        validation_status = True
        logging.info(f"Script validated successfully.")
    except Exception as e:
        validation_log_lines += str(e)
        logging.critical(f"Script did not passed validation.")
    finally:
        logging.debug(f"Writing log to {log_path}")
        with open(log_path, 'a') as logfile:
            logfile.writelines(validation_log_lines)
        return {'Success': validation_status}


def import_spk(sas_conn_file_path, spk_path, log_path, import_package_jar_path,
               target='/',
               safe_mode=True):
    """
    Importing or checking import of spk to target platform
    :param sas_conn_file_path: path (str) to sas .swa connection profile of
    target platform
    :param spk_path: path(str) to spk
    :param log_path: path (str) to logfile
    :param target: metadata root path (str) to import data. Defaults to '/',
    rarely changes to something else.
    :param import_package_jar_path: path (str) to
    ImportPackage or ImportPackage.exe If not provided - platform and global vars
    are used to determine which path to use.
    :param safe_mode: (bool) - Flag, indicating if spk is being imported,
    or just checking (-noexecute flag)
    :return: dict with key 'Success', results of import or check, key 'Warnings',
    indicating if there were warnings during the process
    """
    logging.info(f"Import of {spk_path} started.")
    logging.debug(f"'Check mode' is set to {safe_mode}")
    import_log_lines = []
    warnings = []
    errors = []
    command = ['-profile', sas_conn_file_path, '-package', spk_path, '-target',
               target, '-log', log_path, '-preservePaths', ]
    if platform == "linux" or platform == "linux2":
        command.append('-disableX11')
    command.insert(0, import_package_jar_path)
    if safe_mode:
        logging.debug(f"Launching in -noexecute mode.")
        command.append('-noexecute')
    try:
        logging.debug(f"'Command to be run: {command}")
        import_process = subprocess.run(command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        if import_process.returncode == 0:
            logging.info(f"Import process finished successfully")
        elif import_process.returncode == 4:
            logging.warning(f"Import process finished with Warnings")
            warnings.append(f"Warning during SPK Import. Check log.")
        else:
            logging.error(f"Import process finished Errors")
            errors.append(f"Import finished with errors. Check log.")
        log = SPK_Import_Log(log_file_path=log_path)
        log.parse()
        warnings = log.warnings
        errors = log.errors
    except Exception as e:
        import_log_lines += str(e)
        logging.error(f"Import process finished ERRORS! {str(e)}")
        errors.append(f"Errors while performing import: {str(e)}")
    finally:
        logging.info(f"Log will be written to {log_path}")
        with open(log_path, 'a+') as logfile:
            logfile.writelines(import_log_lines)
        return {'Completed': True,
                'Warnings': warnings,
                'Errors': errors,
                'Log': log_path}


def check_import(sas_conn_file_path,
                 spk_path,
                 import_package_jar_path,
                 log_path,
                 target='/'):
    """
    Spk import check, calls import_spk with key "safe_mode=True".
    Writes logs to provided log file.
    :param sas_conn_file_path: path (str) to sas .swa connection profile of
    target platform
    :param spk_path: path(str) to spk
    :param log_path: path (str) to logfile
    :param target: metadata root path (str) to import data. Defaults to '/',
    rarely changes to something else.
    :param import_package_jar_path: path (str) to
    ImportPackage \ ImportPackage.exe If not provided - platform and global vars
    are used to determine which path to use.
    :return: dict with key 'Success', results of import \ check, key 'Warnings',
    indicating if there were warnings during the process
    """
    logging.info(f"Import check of {spk_path} started.")
    check_result = import_spk(sas_conn_file_path=sas_conn_file_path,
                              spk_path=spk_path,
                              log_path=log_path,
                              target=target,
                              import_package_jar_path=import_package_jar_path,
                              safe_mode=True)
    return check_result


def launch_sas_code(sasobjsp_host: str,
                    sasobjsp_port: str,
                    sasobjsp_user: str,
                    sasobjsp_pass: str,
                    sas_script: str = None,
                    sas_script_path: str = None,
                    sas_appserver: str = 'SASApp - Workspace Server',
                    log_path: str = None):
    if sas_script and sas_script_path:
        logging.error(f"You cannot specify 'sas script' an 'sas_script_path' simultaneously")
        raise SyntaxError
    execution_status = False
    execution_log_lines = []
    try:
        if sas_script_path:
            logging.info(f"Launching of script {sas_script_path} started.")
            with open(sas_script_path, 'r') as f:
                sas_script = f.read()
                execution_log_lines += 'The following script obtained from file:\n'
                execution_log_lines += sas_script
        logging.info(f"Starting sas session...")
        sas = AbstractSAS(sasobjsp_user=sasobjsp_user, sasobjsp_pass=sasobjsp_pass,
                          sasobjsp_host=sasobjsp_host, sasobjsp_port=sasobjsp_port, appserver=sas_appserver)
        code = sas.submit(sas_script)
        sas.endsas()
        execution_log_lines += code['LOG']
        execution_status = True
    except Exception as e:
        logging.error(f"Error while executing script. {str(e)}")
        execution_log_lines += str(e)
    finally:
        logging.info(f"Log will be written to {log_path}")
        if log_path:
            with open(log_path, 'a') as log:
                log.writelines(execution_log_lines)
        return {'Success': execution_status}


def redeploy_jobs(objects_list,
                  serverusername,
                  serverpassword,
                  execution_log_path,
                  sas_conn_file_path,
                  deploy_dir,
                  deployjob_jar_path,
                  deploytype='REDEPLOY',
                  metarepository='Foundation',
                  appservername='SASApp',
                  display='localhost:99'):
    """
    Launches redeploy or deploy process of given objects on given platform.
    Writes results to log.
    :param objects_list: (list) of path's (str) of metata objects, being
    deployed or redeployed
    :param serverusername: (str) username for app server
    :param serverpassword: (str) password for app server
    :param execution_log_path: path (str) to log file
    :param sas_conn_file_path: path (str) to sas .swa connection file
    :param deploytype: DEPLOY or REDEPLOY (str), indicates the type of action.
    :param deploy_dir: (str) - path where to deploy .sas code
    :param metarepository: (str) Name of repository, where deploy or redeploy is
    happening. Defaults to 'Foundation'.
    :param appservername: (str) name of App server, to perform action. Defaults
    to 'SASApp'.
    :param deployjob_jar_path: path (str) to DeployJobs \ DeployJobs.exe If not
    provided - platform and global vars
    are used to determine which path to use.
    :param display: (str) 'DISPLAY' env variable, that is needed to be provided
    to perform action on linux platform.
    Defaults to 'localhost:99' since we have xvfb launched as service.
    :return: dict with key 'Success', results of redeploy, key 'Warnings',
    indicating if there were warnings during the process
    """
    logging.info(f"Redeploy process started")
    execution_log_lines = []
    execution_status = False
    warnings = False
    env = os.environ.copy()
    env['DISPLAY'] = display
    command = ['-profile', sas_conn_file_path, '-deploytype', deploytype,
               '-objects', *objects_list, '-sourcedir',
               deploy_dir, '-metarepository', metarepository, '-appservername',
               appservername, '-serverusername', serverusername,
               '-serverpassword', serverpassword, '-log', execution_log_path]
    command.insert(0, deployjob_jar_path)
    logging.debug(f"Command to be executed: {command}")
    try:
        redeploy_process = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if redeploy_process.returncode == 0:
            logging.info(f"Redeploy process finished successfully.")
            execution_status = True
        elif redeploy_process.returncode == 4:
            execution_status = True
            warnings = True
            logging.warning(f"Redeploy process finished with warnings.")
            # execution_log_lines += redeploy_process.stdout
        else:
            # execution_log_lines += redeploy_process.stderr
            logging.error(f"Redeploy process finished with Errors! Check log!")
    except Exception as e:
        logging.error(f"Errors while performing redeploy {str(e)}")
        execution_log_lines += str(e)
    finally:
        logging.info(f"Log will be written to {execution_log_path}")
        with open(execution_log_path, 'a+') as log:
            log.writelines(execution_log_lines)
        return {'Success': execution_status, 'Warnings': warnings}


def export_objects(objects_list, log_path, sas_conn_file_path,
                   export_package_jar_path,
                   package_path):
    """
    Launches meta objects export process
    :param objects_list: list of metadata path strings
    :param log_path: path to lig file (it will be created by export process)
    :param sas_conn_file_path: path to .swa file with connection description
    :param export_package_jar_path: path to ExportPackage binary
    :param package_path: path to spk file, that will be created.
    :return: dict with key 'Success', results of export process, key 'Warnings',
    indicating if there were warnings during the process
    """
    execution_log_lines = []
    env = os.environ.copy()
    execution_status = False
    warnings = False
    logging.info(f"Starting metadata export process.")
    command = ['-profile', sas_conn_file_path, '-package', package_path,
               '-objects', *objects_list, '-log', log_path]
    if platform == "linux" or platform == "linux2":
        command.append('-disableX11')
    command.insert(0, export_package_jar_path)
    logging.debug(f"Command to be executed: {command}")
    try:
        export_process = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(80 * '*')
        if export_process.returncode == 0:
            logging.info(f"Objects succesfully exported to {package_path}.")
            execution_status = True
        elif export_process.returncode == 4:
            # print(f'Export process finished with warnings.')
            execution_status = True
            warnings = True
            logging.warning(f"Warnings during export process. Check log: {log_path}")
            # logging.info(f"Objects exported to {package_path}.")
            # execution_log_lines += redeploy_process.stdout
        else:
            logging.error(f"Errors during export process. Check log: {log_path}")
            # execution_log_lines += redeploy_process.stderr
            # print(f'Export process finished with ERRORS.')
    except Exception as e:
        execution_log_lines += str(e)
        logging.error(f"Export process finished with ERRORS: {str(e)}")
    finally:
        logging.info(f"Log will be written to: {log_path}")
        with open(log_path, 'a') as log:
            log.writelines(execution_log_lines)
        return {'Success': execution_status, 'Warnings': warnings}


def backup_metadata(backup_script_path, comment, sas_conn_file_path, log_path):
    """
    Launches metadata backup
    :param backup_script_path: path to sas-backup-metadata script
    :param comment: comment(str) to be written on backup
    :param sas_conn_file_path: path to .swa file with connection description
    :param log_path: path to lig file
    :return: dict with key 'Success', results of backup process,
    key 'Backup_name', containing the backup name
    """
    logging.info(f"Full metadata backup started")
    execution_log_lines = []
    env = os.environ.copy()
    backup_name = None
    warnings = []
    errors = []
    command = [backup_script_path, '-comment', comment,
               '-profile', sas_conn_file_path, '-log', log_path]
    logging.debug(f"Command to run: {command}")
    try:
        backup_process = subprocess.run(command, env=env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        if backup_process.returncode == 0:
            backup_name = str(backup_process.stdout).split()[2]
            logging.info(f"Backup {backup_name} completed successfully.")
        elif backup_process.returncode == 4:
            logging.warning(f"Warnings during backup.")
            warnings.append(f"There is a warning...")
        else:
            logging.error(f"Backup NOT completed!")
            errors.append(f"Errors during backup.")
        execution_log_lines += f"{80 * '='}\n"
        execution_log_lines += f"Captured output (May contain more data...)\n"
        execution_log_lines += f"{80 * '='}\n"
        execution_log_lines += str(backup_process.stdout)
    except Exception as e:
        logging.error(f"Errors during backup process! {str(e)}")
        execution_log_lines += str(e)
        errors.append(f"Errors while performing backup.")
    finally:
        logging.info(f"Log will be written to {log_path}")
        with open(log_path, 'a+') as log:
            log.writelines(execution_log_lines)
        return {'Completed': True,
                'Warnings': warnings,
                'Errors': errors,
                'Log': log_path,
                'Backup_name': backup_name}


def recover_metadata(recover_script_path, backup_name, comment,
                     sas_conn_file_path, log_path):
    """
    Launches metadata restore
    :param recover_script_path: path to sas-recover-metadata script
    :param backup_name: name of backup (actually, name of folder)
    :param comment: comment(str) to be written on restore
    :param sas_conn_file_path: path to .swa file with connection description
    :param log_path: path to lig file
    :return: dict with key 'Success', results of restore process,
    key 'Backup_name', containing the backup name
    """
    logging.info(f"Metadata recovery from backup {backup_name} started.")
    execution_log_lines = []
    env = os.environ.copy()
    warnings = []
    errors = []
    command = [recover_script_path, backup_name, '-comment', comment,
               '-profile', sas_conn_file_path, '-log', log_path]
    logging.info(f"Command to run: {command}")
    try:
        backup_process = subprocess.run(command, env=env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        execution_log_lines += f"{80 * '='}\n"
        execution_log_lines += f"Captured output (May contain more data...)\n"
        execution_log_lines += f"{80 * '='}\n"
        execution_log_lines += str(backup_process.stdout)
        if backup_process.returncode == 0:
            logging.info(f"Restore from backup {backup_name} finished successfully")
        elif backup_process.returncode == 4:
            warnings.append(f"There is a warning.")
            logging.warning(f"Restore from backup {backup_name} finished with warnings")
        else:
            restore_success = False
            logging.error(f"Restore from backup {backup_name} not finished!")
            errors.append(f"Restore from backup {backup_name} not finished!")
    except Exception as e:
        restore_success = False
        execution_log_lines += str(e)
        logging.error(f"Restore from backup {backup_name} not finished. ERRORS: {str(e)}")
        errors.append(f"Restore from backup {backup_name} not finished. ERRORS: {str(e)}")
    finally:
        logging.info(f"Log file will be written to {log_path}")
        with open(log_path, 'a+') as log:
            log.writelines(execution_log_lines)
        return {'Completed': True,
                'Warnings': warnings,
                'Errors': errors,
                'Log': log_path}


def export_object_relations(report_process_file, sas_relationship_reporter_path, object, user, host, password, port='7980'):
    logging.info(f"Object {object} relations export started.")
    reports = []
    warnings = []
    errors = []
    env = os.environ.copy()
    report_types = ['lineage', 'impact', 'directDependencies', 'indirectDependencies']  # this should be cofigurable!!!!
    for report in report_types:
        logging.info(f"Generating {report} report.")
        command = [sas_relationship_reporter_path, '-report', report, object, '-user', user,
                '-host', host, '-password', password, '-port', port, '-format', 'CSV']
        logging.debug(f"Command to be launched: {command}")
        report_process = subprocess.run(command, env=env,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
        report_process_file_name = f"{object.split('/')[-1]}_{report}_report_{datetime.now().strftime(r'%Y_%m_%d-%H:%M:%S')}.csv"
        # report_process_file = os.path.join(config['SETTINGS']['storage'], report_process_file_name)
        with open(report_process_file, 'wb') as s:
            s.write(report_process.stdout)
        logging.info(f"Report written to file {report_process_file}")
        reports.append(report_process_file)
        if report_process.returncode == 0:
            logging.info(f"Loaded {report} report about {object}.")
        elif report_process.returncode == 4:
            warnings.append(f'Warnings during genetating {report} report.')
            logging.warning(f"Warnings during {report} report about {object}")
        else:
            errors.append(f'Errors during genetating {report} report.')
            logging.error(f"Errors during {report} report about {object}")
    return {'Completed': True,
            'Reports': reports,
            'Warnings': warnings,
            'Errors': errors,
            'Log': None}


def load_object_report(loader_process_log ,sas_relationship_loader_path, object, user, host, password, port='7980'):
    logging.info(f"Relationship analyze for {object} started.")
    env = os.environ.copy()
    warnings = []
    errors = []
    command = [sas_relationship_loader_path, object, '-user', user,
               '-host', host, '-password', password, '-port', port]
    logging.debug(f"Command to be executed: {command}")
    loader_process = subprocess.run(command, env=env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    loader_process_log_name = f"{object.split('/')[-1]}_info_load_{datetime.now().strftime(r'%Y_%m_%d-%H:%M:%S')}.log"
    # loader_process_log = os.path.join(config['SETTINGS']['storage'], loader_process_log_name)
    with open(loader_process_log, 'wb') as s:
        s.write(loader_process.stdout)
    logging.debug(f"Log was written to {loader_process_log}")
    if loader_process.returncode == 0:
        logging.info(f"Loaded info about {object}.")
    elif loader_process.returncode == 4:
        warnings.append(f"Warnings during loading info about {object}")
        logging.warning(f"Warnings during loading info about {object}")
    else:
        errors.append(f"Errors during loading info about {object}")
        logging.error(f"Errors during loading info about {object}")
    return {'Completed': True,
            'Warnings': warnings,
            'Errors': errors,
            'Log': loader_process_log}


def get_sas_objects(sas_list_objects_path, connection_file, start_folfer='/', sort='path'):
    extracted_objects = []
    warnings = []
    errors = []
    objects_xml = tempfile.NamedTemporaryFile(mode='w+', delete=True)
    env = os.environ.copy()
    command = [sas_list_objects_path, '-folderTree', start_folfer, '-sort', sort,
               '-profile', connection_file, '-format', 'xml']
    logging.debug(f"Running {command}")
    export_process = subprocess.run(command, env=env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    with open(objects_xml.name, 'wb') as s:
        s.write(export_process.stdout)
    mapping = ET.parse(objects_xml.name)
    root = mapping.getroot()
    format = '%Y-%m-%dT%H:%M:%SZ'  # move to config???
    for tag in root.findall('Object'):
        metapath = tag.get('Path', '')
        name = tag.get('Name', '')
        type = tag.get('Type', '')
        typelabel = tag.get('TypeLabel', '')
        description = tag.get('Description', '')
        creation_dttm = tag.get('Created', '')
        if creation_dttm:
            try:
                creation_dttm = datetime.strptime(creation_dttm, format)
            except ValueError as error:
                creation_dttm = ''
        modify_dttm = tag.get('Modified', '')
        if modify_dttm:
            try:
                modify_dttm = datetime.strptime(modify_dttm, format)
            except ValueError as error:
                modify_dttm = ''
        created_by = tag.get('CreatedBy', '')
        modified_by = tag.get('ModifiedBy', '')
        meta_object = {'METADATA_ID': '',
                        'OBJECT_TYPE': type,
                        'OBJECT_NAME': name,
                        'OBJECT_PATH': metapath,
                        'META_OBJ_DESC': description,
                        'CREATION_DTTM':creation_dttm,
                        'MODIFY_DTTM':modify_dttm,
                        'CREATED_BY':created_by,
                        'MODIFIED_BY':modified_by,
                        'TYPELABEL':typelabel}
        print(f"{meta_object}")
        extracted_objects.append(meta_object)
    return {'Completed': True,
            'Warnings': warnings,
            'Errors': errors,
            'Log': None,
            'Objects': extracted_objects}
