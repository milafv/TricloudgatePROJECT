# demo.py


import sys
sys.path.insert(0, '.')
from stage1_parser.tosca_parser import TOSCAParser

parser = TOSCAParser()


# Demo 1 
print()
print("Demo 1: Simple blueprint , 1 compute node")

result = parser.parse('sample_tosca_files/simple_test.yaml')
if result:
    nodes = result['node_templates']
    print("Result: SUCCESS")
    print("Nodes found:", len(nodes))
    for name, data in nodes.items():
        print(f"  - {name}: {data['type']}")



# Demo 2
print()
print("Demo 2: Medium blueprint , compute + storage")
result2 = parser.parse('sample_tosca_files/medium_test.yaml')
if result2:
    nodes2 = result2['node_templates']
    print("Result: SUCCESS")
    print("Nodes found:", len(nodes2))
    for name, data in nodes2.items():
        print(f"  - {name}: {data['type']}")



# Demo 3
print()
print("Demo 3: Complex blueprint , all 3 categories")
result3 = parser.parse('sample_tosca_files/complex_test.yaml')
if result3:
    nodes3 = result3['node_templates']
    print("Result: SUCCESS")
    print("Nodes found:", len(nodes3))
    for name, data in nodes3.items():
        print(f"  - {name}: {data['type']}")



# Demo 4 
print()
print("Demo 4: File that does not exist")
result4 = parser.parse('fake_file.yaml')
if result4 is None:
    print("Result: REJECTED")
    print("Error:", parser.get_errors()[0])



# Demo 5
print()
print("Demo 5: Wrong file type")
result5 = parser.parse('some_file.txt')
if result5 is None:
    print("Result: REJECTED")
    print("Error:", parser.get_errors()[0])


