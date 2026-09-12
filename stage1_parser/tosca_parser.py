# tosca_parser.py
# Milaf Alajlan
# Component: TOSCA Parser
# Status: done i guess

import yaml
import os


# Supported TOSCA versions
SUPPORTED_VERSIONS = [
    "tosca_2_0",
    "tosca_simple_yaml_1_3",
    "tosca_simple_yaml_1_2"
]


class TOSCAParser:
    """
    Reads and validates TOSCA 2.0 YAML blueprint files
    Checks file structure, TOSCA version, and node fields
    """

    def __init__(self):
        # stores error messages from the last parse
        self.errors = []
        # stores non-fatal warnings
        self.warnings = []

    def parse(self, file_path):
        """
        Reads a TOSCA YAML file and returns its contents as a dictionary.
        Returns None if any validation check fails.
        """

        self.errors = []
        self.warnings = []

        print(f"[TOSCAParser] Reading file: {file_path}")

        # check if the file exists
        if not os.path.exists(file_path):
            self._add_error(f"File not found: '{file_path}'")
            return None

        # check if it is a yaml file
        if not file_path.endswith('.yaml') and not file_path.endswith('.yml'):
            self._add_error(f"Wrong file type — must be .yaml or .yml")
            return None

        # try to read and parse the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self._add_error(f"Could not read file: {str(e)}")
            return None

        # check the file actually has content
        if content is None:
            self._add_error("File is empty")
            return None

        # check it has the node_templates section
        if 'node_templates' not in content:
            self._add_error("File has no node_templates section")
            return None

        # check TOSCA version compatibility
        if not self._check_version(content):
            return None

        # validate each node has required fields
        if not self._validate_nodes(content):
            return None

        node_count = len(content['node_templates'])
        print(f"[TOSCAParser] Found {node_count} node(s) — full validation passed")

        if self.warnings:
            for w in self.warnings:
                print(f"[TOSCAParser] WARNING: {w}")

        return content

    def _check_version(self, content):
        """
        Checks that the TOSCA version in the file is supported

        """

        version = content.get('tosca_definitions_version', None)

        if version is None:
            self.warnings.append("No tosca_definitions_version found — assuming TOSCA 2.0")
            return True

        if version not in SUPPORTED_VERSIONS:
            self._add_error(
                f"Unsupported TOSCA version: '{version}'. "
                f"Supported versions are: {SUPPORTED_VERSIONS}"
            )
            return False

        print(f"[TOSCAParser] TOSCA version: {version} — supported")
        return True

    def _validate_nodes(self, content):
        """
        Checks that every node in node_templates has the required fields.
        Every node must have a type field at least
        """

        nodes = content.get('node_templates', {})

        if len(nodes) == 0:
            self._add_error("node_templates section is empty — at least one node is required")
            return False

        for node_name, node_data in nodes.items():

            # every node must be a dictionary
            if not isinstance(node_data, dict):
                self._add_error(
                    f"Node '{node_name}' has invalid format — must be a YAML mapping"
                )
                return False

            # every node must have a type field
            if 'type' not in node_data:
                self._add_error(
                    f"Node '{node_name}' is missing required 'type' field"
                )
                return False

            # warn if node has no properties
            if 'properties' not in node_data:
                self.warnings.append(
                    f"Node '{node_name}' has no properties defined"
                )

        print(f"[TOSCAParser] All {len(nodes)} node(s) have required fields")
        return True

    def _add_error(self, message):
        self.errors.append(message)
        print(f"[TOSCAParser] ERROR: {message}")

    def get_errors(self):
        return self.errors

    def get_warnings(self):
        return self.warnings

    def had_errors(self):
        return len(self.errors) > 0