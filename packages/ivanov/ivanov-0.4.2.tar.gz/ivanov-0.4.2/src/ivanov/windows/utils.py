import logging
import re
import subprocess

logger = logging.getLogger(__name__)


def get_odbc_sources() -> list:
    sources = []
    process = subprocess.run(['powershell', 'Get-OdbcDsn'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    stdout = process.stdout
    stderr = process.stderr
    rc = process.returncode
    if rc == 0:
        logger.info(f'Successfully got odbc sources')
        logger.debug(f'stdout: "{stdout}"')
        pattern = r'^Name\s+:\s(?P<DSN_NAME>.*)$\n^DsnType\s+:\s(?P<DSN_TYPE>.*)$\n^Platform\s+:\s(?P<DSN_PLATFORM>.*)$\n^DriverName\s+:\s(?P<DSN_DRIVER_NAME>.*)$\n^Attribute\s+:\s(?P<DSN_ATTRIBUTE>.*)$'
        matches = re.finditer(pattern, string=stdout, flags=re.MULTILINE | re.VERBOSE)
        for match in matches:
            source = match.groupdict()
            logger.debug(f'Founded match: {source}')
            sources.append(source)
        logger.debug(f'Parse results: {sources}')
        return sources
    else:
        logger.error(f'Getting list of ODBC failed. Stderr: "{stderr}"')
        return sources


def kill_pid(pid: str):
    process = subprocess.run(['taskkill', '/PID', pid, '/T', '/F'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    stdout = process.stdout
    stderr = process.stderr
    rc = process.returncode
    return {"rc": rc, "stdout": stdout, "stderr": stderr}


def disable_scheduled_task(task_name: str = None):
    logger.info(f'Unscheduling of scheduled task {task_name} requested')
    process = subprocess.run(['powershell', 'Disable-ScheduledTask', '-TaskName', task_name], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    stdout = process.stdout
    stderr = process.stderr
    rc = process.returncode
    if rc == 0:
        logger.info(f'Successfully unscheduled "{task_name}"')
        logger.debug(f'stdout: "{stdout}"')
        return {'rc': 0}
    else:
        logger.error(f'Unscheduling of task {task_name} failed. Stderr: "{stderr}"')
        return {'rc': rc}


def enable_scheduled_task(task_name: str = None):
    logger.info(f'Enabling of scheduled task {task_name} requested')
    process = subprocess.run(['powershell', 'Enable-ScheduledTask', '-TaskName', task_name], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    stdout = process.stdout
    stderr = process.stderr
    rc = process.returncode
    if rc == 0:
        logger.info(f'Successfully scheduled "{task_name}"')
        logger.debug(f'stdout: "{stdout}"')
        return {'rc': 0}
    else:
        logger.error(f'Enabling of task {task_name} failed. Stderr: "{stderr}"')
        return {'rc': rc}


def delete_scheduled_task(task_name: str = None):
    logger.info(f'Deletion of scheduled task {task_name} requested')
    process = subprocess.run(['powershell', 'Unregister-ScheduledTask', '-TaskName', task_name, '-Confirm:$false'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    stdout = process.stdout
    stderr = process.stderr
    rc = process.returncode
    if rc == 0:
        logger.info(f'Successfully deleted scheduled task "{task_name}"')
        logger.debug(f'stdout: "{stdout}"')
        return {'rc': 0}
    else:
        logger.error(f'Deletion of scheduled task {task_name} failed. Stderr: "{stderr}"')
        return {'rc': rc}


def parse_handle_out(handle_output: str) -> list:
    logger.debug(f'Started handle output parser')
    blockers = []
    pattern = r'^(?P<executable>\S+)\s+pid:\s(?P<pid>\d+)\s+type:\s(?P<type>\w+)\s+(?P<user>\S+)\s+(?P<handle>\w+):\s(?P<path>.*)$'
    matches = re.finditer(pattern, string=handle_output, flags=re.MULTILINE | re.VERBOSE)
    for match in matches:
        blocker = match.groupdict()
        logger.debug(f'Founded match: {blocker}')
        blockers.append(blocker)
    logger.debug(f'Parse results: {blockers}')
    return blockers


def unlock(path: str, handle_exe_path: str) -> dict:
    logger.info(f'Unlock of {path} requested')
    process = subprocess.run([handle_exe_path, '-u', path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
    stdout = process.stdout
    stderr = process.stderr
    rc = process.returncode
    if rc == 0:
        logger.info(f'Successfully got list of processes, that uses "{path}"')
        logger.debug(f'stdout: "{stdout}"')
        logger.debug(f'Starting output parsing')
        blockers = parse_handle_out(handle_output=stdout)
        for blocker in blockers:
            logger.debug(f'Unblocking {blocker}')
            process = subprocess.run([handle_exe_path, '-c', blocker['handle'], '-p', blocker['pid'], '-y'],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                     timeout=60)
            stdout = process.stdout
            stderr = process.stderr
            rc = process.returncode
            if rc == 0:
                logger.info(f'Process {blocker["pid"]} successfully killed.')
                logger.debug(f'stdout: "{stdout}"')
            else:
                logger.error(f'Unable to close handle for pid {blocker["pid"]}')
                logger.error(f'Following error occurred: "{stderr}"')
                break
        else:
            return {"rc": rc, "stdout": stdout, "stderr": stderr}
    else:
        logger.error(f'Unable to ger list of processes, that uses f"{path}"')
        logger.error(f'Following error occurred: "{stderr}"')
    return {"rc": rc, "stdout": stdout, "stderr": stderr}


def execute_xmla(xmla_query: str,  catalog: str, adomdclientdll: str, server: str) -> dict:
    if adomdclientdll:
        import clr
        clr.AddReference(adomdclientdll)
        clr.AddReference("System.Data")
        from Microsoft.AnalysisServices.AdomdClient import AdomdConnection
    else:
        logger.critical(f'AdomdClient.dll is required...')
        return {'rc': 1}
    logger.info(f'Starting to execute xmla query on {server}')
    logger.debug(f'Opening connection to {server}, catalog {catalog}')
    try:
        logger.debug(f'Initiating conn object')
        conn = AdomdConnection(f"Data Source={server};Catalog={catalog};")
        logger.debug(f'Conn object created, opening connection...')
        conn.Open()
        logger.debug(f'Conn opened...')
        if conn.State == 1:
            logger.info(f'Connection to {server} opened.')
        else:
            logger.error(f'Connection to {server} was not opened.')
            return {'rc': 1}
        logger.debug(f'Preparing connection to accept xmla query...')
        cmd = conn.CreateCommand()
        cmd.CommandText = xmla_query
        logger.debug(f'Xmla query is ready to be executed.')
        logger.info(f'Executing xmla query...')
        cmd.Execute()
        logger.info(f'Xmla query executed.')
        conn.Close()
        logger.info(f'Connection to {server} closed.')
        return {'rc': 0}
    except Exception as error:  # I know, i know...
        logger.error(f'Query executed with error: {str(error)}')
        return {'rc': 1, 'exception': str(error)}