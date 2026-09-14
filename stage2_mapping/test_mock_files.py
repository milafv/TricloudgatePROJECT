import json
import os

def load_json(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File is missing: {filepath}")
    with open(filepath, "r") as f:
        return json.load(f)

def check_catalog(catalog):
    expected_categories = ["compute", "storage", "network"]
    for cat in expected_categories:
        assert cat in catalog, f"Missing category '{cat}' in catalog"
    print("Catalog categories present:", list(catalog.keys()))

    compute_entry = catalog["compute"]["tosca.nodes.Compute"]
    assert "aws" in compute_entry and "azure" in compute_entry
    print("Compute entry has aws + azure sub-entries. OK.")

def check_ir(ir_data):

    assert "blueprint_id" in ir_data, "Missing blueprint_id"
    assert "nodes" in ir_data and len(ir_data["nodes"]) > 0, "Missing or empty nodes list"
    print(f"Blueprint ID: {ir_data['blueprint_id']}")
    print(f"Number of nodes: {len(ir_data['nodes'])}")
    for node in ir_data["nodes"]:
        print(f"  - {node['node_id']} ({node['type']})")

def main():
    catalog = load_json("service_catalog.json")
    ir_data = load_json("mock_ir_output.json")

    check_catalog(catalog)
    print()
    check_ir(ir_data)

    print("\nAll mock files loaded and validated successfully.")

if __name__ == "__main__":
    main()