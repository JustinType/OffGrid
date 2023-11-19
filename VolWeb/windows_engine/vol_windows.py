import logging, jsonschema
from investigations.models import *
from windows_engine.models import *
from django.apps import apps
from VolWeb.voltools import *
from volatility3.framework.exceptions import *
from volatility3.cli import MuteProgress
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def build_context(dump_path, context, base_config_path, plugin, output_path):
    """This function is used to buid the context and construct each plugin
       Return : The contructed plugin.
    """
    available_automagics = automagic.available(context)
    plugin_config_path = interfaces.configuration.path_join(base_config_path, plugin.__name__)
    automagics = automagic.choose_automagic(available_automagics, plugin)
    context.config['automagic.LayerStacker.stackers'] = automagic.stacker.choose_os_stackers(plugin)
    context.config['automagic.LayerStacker.single_location'] = "file://" + os.getcwd() + "/" + dump_path
    constructed = construct_plugin(context, automagics, plugin, base_config_path, MuteProgress(), file_handler(output_path))
    return constructed

def dump_process(dump_path, pid, output_path):
    """Dump the process requested by the user"""
    volatility3.framework.require_interface_version(2, 0, 0)
    failures = volatility3.framework.import_files(plugins, True)
    if failures:
        logger.info(f"Some volatility3 plugin couldn't be loaded : {failures}")
    else:
        logger.info(f"Plugins are loaded without failure")
    plugin_list = volatility3.framework.list_plugins()
    base_config_path = "plugins"
    context = contexts.Context()
    context.config['plugins.Memmap.pid'] = int(pid)
    context.config['plugins.Memmap.dump'] = True

    constructed = build_context(dump_path, context, base_config_path, plugin_list['windows.memmap.Memmap'], output_path)
    if constructed:
        result = DictRenderer().render(constructed.run())
    else:
        logger.info("Error")
    artifact = {x.translate({32: None}): y
                for x, y in result[0].items()}
    return artifact['Fileoutput']



def get_handles(dump_path, pid, case_id):
    """Compute Handles for a specific PID"""
    volatility3.framework.require_interface_version(2, 0, 0)
    failures = volatility3.framework.import_files(plugins, True)
    if failures:
        logger.info(f"Some volatility3 plugin couldn't be loaded : {failures}")
    else:
        logger.info(f"Plugins are loaded without failure")
    plugin_list = volatility3.framework.list_plugins()
    base_config_path = "plugins"
    context = contexts.Context()
    context.config['plugins.Handles.pid'] = [int(pid)]
    constructed = build_context(dump_path, context, base_config_path, plugin_list['windows.handles.Handles'], output_path=None)
    if constructed:
        result = DictRenderer().render(constructed.run())
    else:
        logger.info("Error the handles could not be computed")
        return "KO"
    for artifact in result:
        artifact = {x.translate({32: None}): y
                    for x, y in artifact.items()}
        del (artifact['__children'])
        Handles(investigation_id=case_id, **artifact).save()
    return "OK"


def dump_file(dump_path, offset, output_path):
    """Dump the file requested by the user"""
    volatility3.framework.require_interface_version(2, 0, 0)
    failures = volatility3.framework.import_files(plugins, True)
    if failures:
        logger.info(f"Some volatility3 plugin couldn't be loaded : {failures}")
    else:
        logger.info(f"Plugins are loaded without failure")
    plugin_list = volatility3.framework.list_plugins()
    base_config_path = "plugins"
    context = contexts.Context()
    context.config['plugins.DumpFiles.virtaddr'] = int(offset)
    try:
        constructed = build_context(dump_path, context, base_config_path, plugin_list['windows.dumpfiles.DumpFiles'],
                                    output_path)
    except:
        logger.info("Cannot build")
    if constructed:
        result = DictRenderer().render(constructed.run())
        if len(result) < 1:
            del (context.config['plugins.DumpFiles.virtaddr'])
            context.config['plugins.DumpFiles.physaddr'] = int(offset)
            constructed = build_context(dump_path, context, base_config_path,
                                        plugin_list['windows.dumpfiles.DumpFiles'], output_path)
            result = DictRenderer().render(constructed.run())
    for artifact in result:
        artifact = {x.translate({32: None}): y
                    for x, y in artifact.items()}
    return result


def run_volweb_routine_windows(dump_path, case_id, case):
    partial_results = False
    logger.info('Starting VolWeb Engine')
    volatility3.framework.require_interface_version(2, 0, 0)
    if case.linked_isf:
        path = os.sep.join(case.linked_isf.symbols_file.name.split(os.sep)[:-2])
        volatility3.symbols.__path__.append(os.path.abspath(path))
    """Import available plugings from the native framework"""
    failures = volatility3.framework.import_files(plugins, True)
    if failures:
        logger.info(f"Some volatility3 plugin couldn't be loaded : {failures}")
    else:
        logger.info(f"Plugins are loaded without failure")
    plugin_list = volatility3.framework.list_plugins()
    base_config_path = "plugins"

    """Full list of plugins supported by VolWeb"""
    volweb_knowledge_base = {
        # Process
        'PsScan': {'plugin': plugin_list['windows.psscan.PsScan']},
        'PsTree': {'plugin': plugin_list['windows.pstree.PsTree']},
        'DeviceTree': {'plugin': plugin_list['windows.devicetree.DeviceTree']},
        'CmdLine': {'plugin': plugin_list['windows.cmdline.CmdLine']},
        'Sessions': {'plugin': plugin_list['windows.sessions.Sessions']},
        'Privs': {'plugin': plugin_list['windows.privileges.Privs']},
        'Envars': {'plugin': plugin_list['windows.envars.Envars']},
        'DllList': {'plugin': plugin_list['windows.dlllist.DllList']},
        'LdrModules': {'plugin': plugin_list['windows.ldrmodules.LdrModules']},
        # Network
        'NetScan': {'plugin': plugin_list['windows.netstat.NetStat']},
        'NetStat': {'plugin': plugin_list['windows.netscan.NetScan']},

        # Cryptography
        'Hashdump': {'plugin': plugin_list['windows.hashdump.Hashdump']},
        'Lsadump': {'plugin': plugin_list['windows.lsadump.Lsadump']},
        'Cachedump': {'plugin': plugin_list['windows.cachedump.Cachedump']},

        # Registry
        'HiveList': {'plugin': plugin_list['windows.registry.hivelist.HiveList']},
        'UserAssist': {'plugin': plugin_list['windows.registry.userassist.UserAssist']},

        # Malware analysis
        'Timeliner': {'plugin': plugin_list['timeliner.Timeliner']},
        'Malfind': {'plugin': plugin_list['windows.malfind.Malfind']},
        'SkeletonKeyCheck': {'plugin': plugin_list['windows.skeleton_key_check.Skeleton_Key_Check']},
        'FileScan': {'plugin': plugin_list['windows.filescan.FileScan']},
    }
   
    """Progress Function"""
    def update_progress(case):
        MODULES_TO_RUN = len(volweb_knowledge_base) * 2
        percentage = str(format(float(case.percentage) + float(100 / MODULES_TO_RUN), '.0f')) 
        case.percentage = percentage
        case.save()

    """STEP 0 : Clear the current signatures and compute the memory image signatures"""
    logger.info("Constructing memory image signatures...")
    ImageSignature.objects.filter(investigation_id=case_id).delete()
    signatures = memory_image_hash(dump_path)
    ImageSignature(investigation_id=case_id, **signatures).save()

    """STEP 1 : Clean database and build the basic context for each plugin"""
    NetGraph.objects.filter(investigation_id=case_id).delete()
    TimeLineChart.objects.filter(investigation_id=case_id).delete()
    for runable in volweb_knowledge_base:
        apps.get_model("windows_engine", runable).objects.filter(investigation_id=case_id).delete()
        context = contexts.Context()
        logger.info(f"Constructing context for {runable} ")
        """Add pluging argument for hivelist"""
        if runable == 'HiveList':
            context.config['plugins.HiveList.dump'] = True
        try:
            volweb_knowledge_base[runable]['constructed'] = build_context(dump_path, context, base_config_path,
                                                                          volweb_knowledge_base[runable]['plugin'],
                                                                          "Cases/files")
        except VolatilityException:
            volweb_knowledge_base[runable]['constructed'] = []
        except: 
            logger.info(f"Could not build context for {runable}" )
        update_progress(case)

    """STEP 2.1 : For each constructed plugin's context, we render the result and save it."""
    for runable in volweb_knowledge_base:
        if volweb_knowledge_base[runable]['constructed']:
            logger.info(f"Running plugin : {runable}")
            try:
                volweb_knowledge_base[runable]['result'] = DictRenderer().render(
                    volweb_knowledge_base[runable]['constructed'].run())
            except VolatilityException:
                partial_results = True
                volweb_knowledge_base[runable]['result'] = []
            except:
                logger.info(f"Could not run {runable}" )
                partial_results = True
                volweb_knowledge_base[runable]['result'] = []
        else:
            volweb_knowledge_base[runable]['result'] = []
        update_progress(case)

    """STEP 3.1 : We can now inject the results inside the database"""
    for runable in volweb_knowledge_base:
        if runable != 'PsTree' and runable != 'UserAssist' and runable != 'DeviceTree':
            for artifact in volweb_knowledge_base[runable]['result']:
                artifact = {x.translate({32: None}): y
                            for x, y in artifact.items()}
                if '__children' in artifact:
                    del (artifact['__children'])
                if 'Offset(V)' in artifact:
                    artifact['Offset'] = artifact['Offset(V)']
                    del (artifact['Offset(V)'])

                apps.get_model("windows_engine", runable)(investigation_id=case_id, **artifact).save()

    """STEP 3.2 : Construct and inject the graphs"""

    def rename_pstree(node):
        if len(node['__children']) == 0:
            node['children'] = node['__children']
            node['name'] = node['ImageFileName']
            del (node['__children'])
            del (node['ImageFileName'])
        else:
            node['children'] = node['__children']
            node['name'] = node['ImageFileName']
            del (node['__children'])
            del (node['ImageFileName'])
            for children in node['children']:
                rename_pstree(children)

    def rename_devicetree(node):
        if len(node['__children']) == 0:
            node['children'] = node['__children']
            
            node['name'] = ""
            
            if node['DeviceName']:
                node['name'] += node['DeviceName']
            if node['DeviceType']:
                node['name'] += "/" + node['DeviceType'] 
            if node['DriverName']:
                node['name'] += "/" + node['DriverName']
            del (node['__children'])
        else:
            node['children'] = node['__children']
            
            node['name'] = ""
            
            if node['DeviceName']:
                node['name'] += node['DeviceName']
            if node['DeviceType']:
                node['name'] += "/" + node['DeviceType'] 
            if node['DriverName']:
                node['name'] += "/" + node['DriverName']
        
            del (node['__children'])
            for children in node['children']:
                rename_devicetree(children)

    json_pstree_artifact = []
    json_devicetree_artifact = []
    json_netgraph_artifact = []
    json_timeline_graph_artifact = []
    if volweb_knowledge_base['PsTree']['result']:
        pstree_artifact = volweb_knowledge_base['PsTree']['result']
        for tree in pstree_artifact:
            rename_pstree(tree)
        json_pstree_artifact = json.dumps(pstree_artifact)

    if volweb_knowledge_base['DeviceTree']['result']:
        devicetree_artifact = volweb_knowledge_base['DeviceTree']['result']
        for tree in devicetree_artifact:
            rename_devicetree(tree)
        json_devicetree_artifact = json.dumps(devicetree_artifact)

    if volweb_knowledge_base['NetScan']['result'] or volweb_knowledge_base['NetStat']['result']:
        json_netgraph_artifact = json.dumps(generate_network_graph(
            volweb_knowledge_base['NetScan']['result'] + volweb_knowledge_base['NetStat']['result']))

    if volweb_knowledge_base['Timeliner']['result']:
        json_timeline_graph_artifact = json.dumps(build_timeline(volweb_knowledge_base['Timeliner']['result']))

    PsTree(investigation_id=case_id, graph=json_pstree_artifact).save()
    DeviceTree(investigation_id=case_id, graph=json_devicetree_artifact).save()
    NetGraph(investigation_id=case_id, graph=json_netgraph_artifact).save()
    TimeLineChart(investigation_id=case_id, graph=json_timeline_graph_artifact).save()

    def fill_userassist(list, case_id):
        for artifact in list:
            artifact = {x.translate({32: None}): y
                        for x, y in artifact.items()}
            apps.get_model("windows_engine", 'UserAssist')(investigation_id=case_id,
                                                           HiveOffset=artifact['HiveOffset'],
                                                           HiveName=artifact['HiveName'],
                                                           Path=artifact['Path'],
                                                           LastWriteTime=artifact['LastWriteTime'],
                                                           Type=artifact['Type'],
                                                           Name=artifact['Name'],
                                                           ID=artifact['ID'],
                                                           Count=artifact['Count'],
                                                           FocusCount=artifact['FocusCount'],
                                                           TimeFocused=artifact['TimeFocused'],
                                                           LastUpdated=artifact['LastUpdated'],
                                                           RawData=artifact['RawData']).save()
            if artifact['__children']:
                fill_userassist(artifact['__children'], case_id)

    if volweb_knowledge_base['UserAssist']['result']:
        fill_userassist(volweb_knowledge_base['UserAssist']['result'], case_id)
    return partial_results
