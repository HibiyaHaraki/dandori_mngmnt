#
# July 2025. Created by Hibiya Haraki
#
# Links.py
#

LINK_LIST = [
    ["contains" , "is contained by"],
    ["after"    , "before"         ],
    ["relate to", "relate to"      ],
    ["blocks"   , "is blocked by"  ]
]

def get_relationship_list():
    link_list = []
    for links in LINK_LIST:
        for link in links:
            link_list.append(link)
    
    link_list = list(set(link_list))
    
    return sorted(link_list)

def get_pair_relationship(relationship:str):
    # Check input
    if (relationship not in get_relationship_list()):
        return False
    else:
        for links in LINK_LIST:
            if (relationship in links):
                for link in links:
                    if (link != relationship):
                        return link

def generate_mermaid_command(links:list):
    output_command = """
---
config:
    theme: 'dark'
---
"""
    output_command += "flowchart TB" + "\n"

    # Convert Node Name
    for link in links:
        if ("TASK" not in str(link["SourceTaskID"])):
            link["SourceTaskID"] = "TASK/" + str(link["SourceTaskID"])
        if ("TASK" not in str(link["TargetTaskID"])):
            link["TargetTaskID"] = "TASK/" + str(link["TargetTaskID"])
        
    # Create Subgraph
    subgraphs = {}
    for link in links:
        if (link["relationship"] == "contains"):
            if (link["SourceTaskID"] in subgraphs.keys()):
                subgraphs[link["SourceTaskID"]].append(link["TargetTaskID"])
                subgraphs[link["SourceTaskID"]] = list(set(subgraphs[link["SourceTaskID"]]))
            else:
                subgraphs[link["SourceTaskID"]] = [link["TargetTaskID"]]

        if (link["relationship"] == "is contained by"):
            if (link["TargetTaskID"] in subgraphs.keys()):
                subgraphs[link["TargetTaskID"]].append(link["SourceTaskID"])
                subgraphs[link["TargetTaskID"]] = list(set(subgraphs[link["TargetTaskID"]]))
            else:
                subgraphs[link["TargetTaskID"]] = [link["SourceTaskID"]]
    
    for subgraph in subgraphs.keys():
        output_command += "subgraph {}".format(subgraph) + "\n"
        for node in subgraphs[subgraph]:
            output_command += "{}".format(node) + "\n"
        output_command += "end" + "\n"
    
    # Add connection
    for link in links:
        if (link["relationship"] == "after"):
            output_command += "{0}-->{1}".format(link["TargetTaskID"],link["SourceTaskID"]) + "\n"
        if (link["relationship"] == "before"):
            output_command += "{0}-->{1}".format(link["SourceTaskID"],link["TargetTaskID"]) + "\n"
        if (link["relationship"] == "relate to"):
            output_command += "{0}-- relate to --{1}".format(link["SourceTaskID"],link["TargetTaskID"]) + "\n"
        if (link["relationship"] == "blocks"):
            output_command += "{0} --x {1}".format(link["SourceTaskID"],link["TargetTaskID"]) + "\n"
        if (link["relationship"] == "is blocked by"):
            output_command += "{0} --x {1}".format(link["TargetTaskID"],link["SourceTaskID"]) + "\n"
    
    print(output_command)
    return output_command




