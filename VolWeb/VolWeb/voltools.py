import volatility3, datetime, hashlib, io, tempfile, json, os, subprocess, vt
from typing import Dict, Type, Union, Any, List, Tuple
from volatility3.framework import contexts, interfaces
from volatility3 import plugins
from volatility3.framework.plugins import construct_plugin
from volatility3.framework import automagic, constants
from volatility3.cli import text_renderer
from volatility3.framework.renderers import format_hints
from .keyconfig import Secrets


class GraphException(Exception):
    """Class to allow filtering of the graph generation errors"""


def file_handler(output_dir):
    class CLIFileHandler(interfaces.plugins.FileHandlerInterface):
        """The FileHandler from Volatility3 CLI"""

        def _get_final_filename(self):
            """Gets the final filename"""
            if output_dir is None:
                raise TypeError("Output directory is not a string")
            os.makedirs(output_dir, exist_ok=True)

            pref_name_array = self.preferred_filename.split('.')
            filename, extension = os.path.join(output_dir, '.'.join(pref_name_array[:-1])), pref_name_array[-1]
            output_filename = f"{filename}.{extension}"

            counter = 1
            if os.path.exists(output_filename):
                os.remove(output_filename)
            return output_filename

    class CLIDirectFileHandler(CLIFileHandler):
        """We want to save our files directly to disk"""

        def __init__(self, filename: str):
            fd, self._name = tempfile.mkstemp(suffix='.vol3', prefix='tmp_', dir=output_dir)
            self._file = io.open(fd, mode='w+b')
            CLIFileHandler.__init__(self, filename)
            for item in dir(self._file):
                if not item.startswith('_') and not item in ['closed', 'close', 'mode', 'name']:
                    setattr(self, item, getattr(self._file, item))

        def __getattr__(self, item):
            return getattr(self._file, item)

        @property
        def closed(self):
            return self._file.closed

        @property
        def mode(self):
            return self._file.mode

        @property
        def name(self):
            return self._file.name

        def close(self):
            """Closes and commits the file (by moving the temporary file to the correct name"""
            # Don't overcommit
            if self._file.closed:
                return

            self._file.close()
            output_filename = self._get_final_filename()
            os.rename(self._name, output_filename)

    return CLIDirectFileHandler


# Inspired by the JsonRenderer class.
class DictRendererPsTree(text_renderer.CLIRenderer):
    """Directly inspired by the JsonRenderer rendered
        Return : Dict of the plugin result.
    """
    _type_renderers = {
        format_hints.HexBytes: text_renderer.quoted_optional(text_renderer.hex_bytes_as_text),
        interfaces.renderers.Disassembly: text_renderer.quoted_optional(text_renderer.display_disassembly),
        format_hints.MultiTypeData: text_renderer.quoted_optional(text_renderer.multitypedata_as_text),
        bytes: text_renderer.optional(lambda x: " ".join([f"{b:02x}" for b in x])),
        datetime.datetime: lambda x: x.isoformat() if not isinstance(x, interfaces.renderers.BaseAbsentValue) else None,
        'default': lambda x: x
    }

    name = 'JSON'
    structured_output = True

    def get_render_options(self) -> List[interfaces.renderers.RenderOption]:
        pass

    def render(self, grid: interfaces.renderers.TreeGrid):
        final_output: Tuple[Dict[str, List[interfaces.renderers.TreeNode]], List[interfaces.renderers.TreeNode]] = (
            {}, [])

        def visitor(
                node: interfaces.renderers.TreeNode, accumulator: Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]
        ) -> Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
            # Nodes always have a path value, giving them a path_depth of at least 1, we use max just in case
            acc_map, final_tree = accumulator
            node_dict: Dict[str, Any] = {'__children': []}
            depth = "*" * max(0, node.path_depth - 1) + ("" if (node.path_depth <= 1) else " ")
            node_dict['level'] = depth
            for column_index in range(len(grid.columns)):
                column = grid.columns[column_index]
                renderer = self._type_renderers.get(column.type, self._type_renderers['default'])
                data = renderer(list(node.values)[column_index])
                if isinstance(data, interfaces.renderers.BaseAbsentValue):
                    data = None
                node_dict[column.name] = data
            if node.parent:
                acc_map[node.parent.path]['__children'].append(node_dict)
            else:
                final_tree.append(node_dict)
            acc_map[node.path] = node_dict

            return (acc_map, final_tree)

        if not grid.populated:
            grid.populate(visitor, final_output)
        else:
            grid.visit(node=None, function=visitor, initial_accumulator=final_output)

        return final_output[1]


# Inspired by the JsonRenderer class.
class DictRenderer(text_renderer.CLIRenderer):
    _type_renderers = {
        format_hints.HexBytes: text_renderer.quoted_optional(text_renderer.hex_bytes_as_text),
        interfaces.renderers.Disassembly: text_renderer.quoted_optional(text_renderer.display_disassembly),
        format_hints.MultiTypeData: text_renderer.quoted_optional(text_renderer.multitypedata_as_text),
        bytes: text_renderer.optional(lambda x: " ".join([f"{b:02x}" for b in x])),
        datetime.datetime: lambda x: x.isoformat() if not isinstance(x, interfaces.renderers.BaseAbsentValue) else None,
        'default': lambda x: x
    }

    name = 'JSON'
    structured_output = True

    def get_render_options(self) -> List[interfaces.renderers.RenderOption]:
        pass

    def render(self, grid: interfaces.renderers.TreeGrid):
        final_output: Tuple[Dict[str, List[interfaces.renderers.TreeNode]], List[interfaces.renderers.TreeNode]] = (
            {}, [])

        def visitor(
                node: interfaces.renderers.TreeNode, accumulator: Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]
        ) -> Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
            # Nodes always have a path value, giving them a path_depth of at least 1, we use max just in case
            acc_map, final_tree = accumulator
            node_dict: Dict[str, Any] = {'__children': []}
            for column_index in range(len(grid.columns)):
                column = grid.columns[column_index]
                renderer = self._type_renderers.get(column.type, self._type_renderers['default'])
                data = renderer(list(node.values)[column_index])
                if isinstance(data, interfaces.renderers.BaseAbsentValue):
                    data = None
                node_dict[column.name] = data
            if node.parent:
                acc_map[node.parent.path]['__children'].append(node_dict)
            else:
                final_tree.append(node_dict)
            acc_map[node.path] = node_dict

            return acc_map, final_tree

        if not grid.populated:
            grid.populate(visitor, final_output)
        else:
            grid.visit(node=None, function=visitor, initial_accumulator=final_output)

        return final_output[1]


def memory_image_hash(dump_path):
    """Compute memory image signature.
    Args:
        dump_path: A string indicating the image file path

    Returns:
        A dict of different types of hash computed
    """
    blocksize = 65536  # Read the file in 64kb chunks.
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    try:
        with open(dump_path, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                md5.update(buf)
                sha1.update(buf)
                sha256.update(buf)
                buf = afile.read(blocksize)
        signatures = {'md5': format(md5.hexdigest()), 'sha1': format(sha1.hexdigest()),
                      'sha256': format(sha256.hexdigest())}
    except:
        signatures = {'md5': 'Error', 'sha1': 'Error', 'sha256': 'Error'}
    return signatures


def file_sha256(path):
    """Compute memory image signature.
    Args:
        path: A string indicating the file path
    Returns:
        sh256 of the file
    """
    blocksize = 65536  # Read the file in 64kb chunks.
    sha256 = hashlib.sha256()
    try:
        with open(path, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                sha256.update(buf)
                buf = afile.read(blocksize)
        return format(sha256.hexdigest())
    except:
        return 'error'


def generate_network_graph(data):
    graph_data = {'nodes': [], 'edges': []}
    for entry in data:
        node_data_1 = {'id': entry['LocalAddr'], 'Involved_PIDs': [entry['PID']], 'Owner(s)': [entry['Owner']],
                       'Local_Ports': [entry['LocalPort']], 'State': entry['State']}
        node_data_2 = {'id': entry['ForeignAddr'], 'Involved_PIDs': [entry['PID']], 'Owner(s)': [entry['Owner']],
                       'Local_Ports': [entry['ForeignPort']], 'State': entry['State']}
        edge_data = {'from': entry['LocalAddr'], 'to': entry['ForeignAddr']}
        if not graph_data['nodes']:
            graph_data['nodes'].append(node_data_1)

        is_present = False
        for item in graph_data['nodes']:
            if node_data_1['id'] == item['id']:
                is_present = True
                break
        if not is_present:
            graph_data['nodes'].append(node_data_1)
        else:
            if entry['PID'] not in item['Involved_PIDs']:
                item['Involved_PIDs'].append(entry['PID'])
            if entry['LocalPort'] not in item['Local_Ports']:
                item['Local_Ports'].append(entry['LocalPort'])
            if entry['Owner'] not in item['Owner(s)']:
                item['Owner(s)'].append(entry['Owner'])

        is_present = False
        for item in graph_data['nodes']:
            if node_data_2['id'] == item['id']:
                is_present = True
                break

        if not is_present:
            graph_data['nodes'].append(node_data_2)
        else:
            if entry['PID'] not in item['Involved_PIDs']:
                item['Involved_PIDs'].append(entry['PID'])
            if entry['ForeignPort'] not in item['Local_Ports']:
                item['Local_Ports'].append(entry['ForeignPort'])
            if entry['Owner'] not in item['Owner(s)']:
                item['Owner(s)'].append(entry['Owner'])

        if edge_data not in graph_data['edges']:
            graph_data['edges'].append(edge_data)

    return graph_data


def vt_check_file_hash(hash):
    client = vt.Client(Secrets.VT_API_KEY)
    try:
        file = client.get_object("/files/" + hash)
        client.close()
        result = file.last_analysis_stats
        result.update({'SHA256': file.sha256})
        try:
            result.update({'meaningful_name': file.meaningful_name})
        except:
            pass
        try:
            result.update({'crowdsourced_yara_results': file.crowdsourced_yara_results})
        except:
            pass
        try:
            result.update({'sandbox_verdicts': file.sandbox_verdicts})
        except:
            pass
        return result, "success"
    except vt.error.APIError as e:
        client.close()
        return None, e.message
    except:
        client.close()
        return None, "Unknown Error"


def build_timeline(data):
    timeline = []
    nb_event = 1
    actual_date = ""
    try:
        saved_date = data[0]["Created Date"]
    except:
        raise GraphException('Could not generate timeline graph')
    for i in data:
        try:
            actual_date = str(i["Created Date"])
            if actual_date != saved_date:
                timeline.append([saved_date, nb_event])
                saved_date = actual_date
                nb_event = 1
            else:
                nb_event += 1
        except:
            raise GraphException('Could not generate timeline graph')
    return timeline
