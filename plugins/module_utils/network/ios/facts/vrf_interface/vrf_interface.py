# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios vrf_interface fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vrf_interface.vrf_interface import (
    Vrf_interfaceArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_interface import (
    Vrf_interfaceTemplate,
)


class Vrf_interfaceFacts(object):
    """The ios vrf_interface facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Vrf_interfaceArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vrf_interface network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get()

        # parse native config using the Vrf_interface template
        vrf_interface_parser = Vrf_interfaceTemplate(lines=data.splitlines(), module=self._module)
        objs = list(vrf_interface_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("vrf_interface", None)

        params = utils.remove_empties(
            vrf_interface_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["vrf_interface"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts