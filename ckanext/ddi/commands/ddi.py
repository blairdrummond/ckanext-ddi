import ckan.lib.cli
import sys
import json
from pprint import pprint

from ckanext.ddi.importer import ddiimporter
from ckanext.ddi.plugins import get_ddi_config

import logging
log = logging.getLogger(__name__)


class DdiCommand(ckan.lib.cli.CkanCommand):
    '''Command to handle DDI data

    Usage:

        # General usage
        paster --plugin=ckanext-ddi <command> -c <path to config file>

        # Show this help
        paster --plugin=ckanext-ddi ddi help

        # Show current configuration
        paster --plugin=ckanext-ddi ddi config

        # Import datasets
        paster --plugin=ckanext-ddi ddi import <path_or_url> <license>

    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        # load config
        self._load_config()
        options = {
            'import': self.importCmd,
            'config': self.configCmd,
            'help': self.helpCmd,
        }

        try:
            cmd = self.args[0]
            options[cmd](*self.args[1:])
        except KeyError:
            self.helpCmd()
            sys.exit(1)

    def helpCmd(self):
        print(self.__doc__)

    def configCmd(self):
        config_dict = get_ddi_config()
        pprint(json.loads(json.dumps(config_dict)))

    def importCmd(self, path_or_url=None, license=None):
        if path_or_url is None:
            print("Argument 'path_or_url' must be set")
            self.helpCmd()
            sys.exit(1)
        try:
            importer = ddiimporter.DdiImporter()
            if path_or_url.startswith('http:'):
                importer.run(
                    url=path_or_url,
                    params={
                        'license': license
                    }
                )
            else:
                importer.run(
                    file_path=path_or_url,
                    params={
                        'license': license
                    }
                )
        except Exception:
            import traceback
            traceback.print_exc()
