#!/usr/bin/python3

from ansible.module_utils.basic import *
import json
import ast

DOCUMENTATION = '''
---
module: coreos_ignition
short_description: Adds elements to a pre-generated ignition file
description:
    - Adds elements to a pre-generated ignition file
options:
    path:
      description
        - The full path of the ignition file
      required: true
    section:
      description
        - The section we are adding this to
      required: true
    subsection:
      description
        - The subsection we are adding this to
      required: true
    content:
      description
        - The JSON block, as a string we wish to add
      required: true

'''
EXAMPLES = '''
# Add a file to our coreos ignition
- coreos_ignition:
    path: /tmp/coreos.ign
    section: "storage"
    subsection: "files"
    content: "{'path':'/tmp/foo', 'contents': { 'source': 'foo'} , 'mode': 420}"
'''


class CoreosIgnition(object):

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                path=dict(default='/openshift/iso/iso.ign'),
                section=dict(required=True, type='str'),
                subsection=dict(required=True, type='str'),
                content=dict(required=True, type='str')
            )
        )

        self.params = self.module.params
        self._write_contents()
        self.module.exit_json(changed=False)

    def _write_contents(self):
        raw = open(self.params['path'])
        data = json.load(raw)
        dict = ast.literal_eval(self.params['content'])
        data[self.params['section']][self.params['subsection']].append(dict)
        with open(self.params['path'], 'w') as outfile:
            json.dump(data, outfile)

        outfile.close()

        self.module.exit_json(changed=True, meta={"Result": self.params['content']})


if __name__ == '__main__':
    CoreosIgnition()
