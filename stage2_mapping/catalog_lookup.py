import json
import os


def load_catalog(catalog_path="service_catalog.json"):
    if not os.path.exists(catalog_path):
        raise FileNotFoundError(f"Catalog file not found: {catalog_path}")
    with open(catalog_path, "r") as f:
        return json.load(f)


def lookup_node_type(tosca_type, provider, catalog):

    for category, types_in_category in catalog.items():
        if tosca_type in types_in_category:
            provider_entry = types_in_category[tosca_type].get(provider)
            if provider_entry is not None:
                return {
                    "found": True,
                    "category": category,
                    "entry": provider_entry
                }
            else:
                return {
                    "found": False,
                    "category": category,
                    "entry": None
                }

    return {
        "found": False,
        "category": None,
        "entry": None
    }


if __name__ == "__main__":
    catalog = load_catalog("service_catalog.json")

    test_cases = [
        ("tosca.nodes.Compute", "aws"),
        ("tosca.nodes.Compute", "azure"),
        ("tosca.nodes.Storage.ObjectStorage", "aws"),
        ("tosca.nodes.network.Network", "azure"),
        ("tosca.nodes.Container.Application.Docker", "aws"),
    ]

    for tosca_type, provider in test_cases:
        result = lookup_node_type(tosca_type, provider, catalog)
        print(f"{tosca_type} + {provider} -> found={result['found']}, category={result['category']}")