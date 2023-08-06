import traceback
from ...core_interface import invoke_core_method
from ... import common_utils
from ...utils.logger import Logger
import os
logger = Logger()


def get_module_details(data):
    try:
        module_details = {}
        stack_trace = traceback.extract_stack()
        mapped_stack_trace = list(
            map(common_utils.map_stack_trace, stack_trace))
        filtered_stack_trace = list(filter(lambda stackTrace: (
            'protectonce' not in stackTrace.get(
                'fileName', '') and 'frozen' not in stackTrace.get('fileName', '')
            and 'pythonFiles' not in stackTrace.get('fileName', '')), mapped_stack_trace))
        filtered_stack_trace.reverse()
        module_details['stackTrace'] = filtered_stack_trace
        try:
            if data['result']:
                module_details['version'] = data['result'].__version__
                module_details['name'] = data['result'].__name__
                module_details['modulePath'] = data['result'].__file__
                notification_data = {
                    'key': "BOM.usedModule",
                    'args': [module_details]
                }
                library_path = os.path.dirname(os.__file__)
                if not library_path in module_details['modulePath']:
                    invoke_core_method("notify", notification_data)
        except Exception as e:
            pass
    except Exception as e:
        logger.info() and logger.write(
            'bom_handler.get_module_details failed with error : ' + str(e))
