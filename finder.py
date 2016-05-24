from zim.plugins import PluginClass
from zim.command import Command
from zim.notebook import resolve_notebook, build_notebook

usagehelp ='''\
usage: zim --plugin linklist [OPTIONS] [Notebook]

--help, -h      Print this help
--page, -p      Check links only on the given page
'''
class LinkFinderPlugin(PluginClass):
    plugin_info = {
        'name': 'Multi-link finder',
        'description': '''\
List pages that link to another page more than once.
        ''',
        'author': 'Gergely Polonkai',
    }

class LinkFinderCommand(Command):
    options = (
        ('help',          'h', 'Print this help text and exit'),
    )

    def parse_options(self, *args):
        Command.parse_options(self, *args)

    def _all_links(self):
        for page in self.nb.index.walk():
            yield page

    def run(self):
        if self.opts.get('help'):
            print usagehelp

            return

        if len(self.args) == 0:
            # TODO: find and open the default notebook
            notebook, ns = build_notebook(nb)
            print(notebook)
        else:
            nbi = resolve_notebook(self.args[0])
            notebook, ns = build_notebook(nbi)

        self.process_subpages(notebook, None)

    def process_subpages(self, notebook, path):
        for page in notebook.get_pagelist(path):
            _links = {}

            for linktype, destination, attrs in page.get_links():
                if linktype == 'page':
                    path = notebook.resolve_path(destination,
                                                 source=page,
                                                 index=notebook.index)
                    if path.name in _links:
                        _links[path.name] += 1
                    else:
                        _links[path.name] = 1


            for page_name, count in _links.items():
                if count > 1:
                    print("{} is linked {} times from {}".format(
                        page_name, count, page.name))

            # Process subpages of this one
            self.process_subpages(notebook, page)
