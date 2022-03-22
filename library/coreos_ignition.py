#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
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
    state:
      description
        - Do we add or remove this block
      choices: [ 'present', 'absent' ]
      required: false
author:
    - Brett Minnie (@brettminnie)
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
        self.arguments = dict(
            path=dict(
                default='/openshift/iso/iso.ign'
            ),
            section=dict(
                required=True,
                type='str'
            ),
            subsection=dict(
                required=True,
                type='str'
            ),
            content=dict(
                required=True,
                type='str'
            ),
            state=dict(
                default='present',
                choices=['absent', 'present']
            )
        )

        self.module = AnsibleModule(
            argument_spec=self.arguments
        )

        self.params = self.module.params
        self.json_data = self.__load_json()
        self.result = dict(
            changed=False,
            original_message='',
            message=''
        )

    def run_module(self):
        if self._is_present():
            self._change_contents()
        elif not self._is_present():
            self._remove_content()

        self.__write_json()

        self.module.exit_json(**self.result)

    def _is_present(self):
        """
        Checks to see if our state is present
        :return: boolean
        """
        return str(self.params['state']).lower() == 'present'

    def __load_json(self):
        raw = open(self.params['path'])
        data = json.load(raw)
        raw.close()
        return data

    def __write_json(self):
        with open(self.params['path'], 'w') as outfile:
            json.dump(self.json_data, outfile)
        outfile.close()

    def _content_exists(self):
        try:
            if self.params['subsection'] in self.json_data[self.params['section']]:
                return True
        except KeyError:
            pass
        return False

    def _remove_content(self):
        if self._content_exists():
            del(self.json_data[self.params['section']][self.params['subsection']])

    def _change_contents(self):
        content_dictionary = ast.literal_eval(self.params['content'])
        if not self._content_exists():
            self.json_data[self.params['section']][self.params['subsection']].append(content_dictionary)
        else:
            self.result['original_message'] = str(self.json_data[self.params['section']][self.params['subsection']])
            self.json_data[self.params['section']][self.params['subsection']].update(content_dictionary)
        self.result['changed'] = True
        self.result['message'] = str(content_dictionary)


def main():
    module = CoreosIgnition()
    module.run_module()


if __name__ == '__main__':
    main()
