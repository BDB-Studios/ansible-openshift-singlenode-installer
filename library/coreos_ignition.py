#!/usr/bin/python3

from ansible.module_utils.basic import *
import json

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
        print(self.params)
        self._write_contents()

    def _write_contents(self):
        with open(self.params.path) as file:
            data = json.loads(file)
            print(data)
            data[self.params.section][self.params.subsection].append(self.params.content)
            json.dump(data, file)

        file.close()


if __name__ == '__main__':
    CoreosIgnition()
