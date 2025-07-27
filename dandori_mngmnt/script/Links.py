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

MERMAID_CONFIG = """
---
config:
    theme: 'dark'
---
flowchart TB
    classDef OPEN fill:#6C757D,stroke:#FFFFFF,stroke-width:0px,color:#FFFFFF
    classDef IN_PROGRESS fill:#0d6efd,stroke:#FFFFFF,stroke-width:0px,color:#FFFFFF
    classDef WAIT fill:#ffc107,stroke:#FFFFFF,stroke-width:0px,color:#FFFFFF,color:#000000
    classDef DONE fill:#198754,stroke:#FFFFFF,stroke-width:0px,color:#FFFFFF

"""

def get_relationship_list():
    """
    Get a sorted list of all unique relationship types.
    Returns:
        list: Sorted list of relationship strings.
    """
    link_list = []
    for links in LINK_LIST:
        for link in links:
            link_list.append(link)
    
    link_list = list(set(link_list))
    
    return sorted(link_list)

def get_pair_relationship(relationship: str):
    """
    Get the paired relationship for a given relationship.
    Args:
        relationship (str): The relationship to find the pair for.
    Returns:
        str or bool: The paired relationship, or False if not found.
    """
    if (relationship not in get_relationship_list()):
        return False
    else:
        for links in LINK_LIST:
            if (relationship in links):
                for link in links:
                    if (link != relationship):
                        return link

def remove_duplicated_relationship(links: list):
    """
    Remove duplicated or mirrored relationships from the links list.
    Args:
        links (list): List of link dictionaries.
    Returns:
        list: Cleaned list with duplicates removed.
    """
    remove_list = []
    # Find duplicated relationship
    for idx, link in enumerate(links):
        if (idx in remove_list):
            continue
        else:
            for link_list in LINK_LIST:
                if (link["relationship"] in link_list):
                    for temp_idx, temp_link in enumerate(links):
                        if (
                            temp_link["TargetTaskID"] == link["TargetTaskID"]
                            and
                            temp_link["SourceTaskID"] == link["SourceTaskID"]
                            and
                            temp_link["relationship"] in link_list
                            and
                            idx != temp_idx
                        ):
                            remove_list.append(temp_idx)
                        elif (
                            temp_link["TargetTaskID"] == link["SourceTaskID"]
                            and
                            temp_link["SourceTaskID"] == link["TargetTaskID"]
                            and
                            temp_link["relationship"] in link_list
                            and
                            idx != temp_idx
                        ):
                            remove_list.append(temp_idx)
                    break
    
    # Delete
    remove_list = sorted(list(set(remove_list)), reverse=True)
    for remove_idx in remove_list:
        links.pop(remove_idx)
    
    return links

def generate_mermaid_command(links: list):
    """
    Generate a Mermaid diagram command string from a list of task links.
    Args:
        links (list): List of link dictionaries.
    Returns:
        str: Mermaid diagram command string.
    """
    output_command = MERMAID_CONFIG

    # Links
    links = remove_duplicated_relationship(links)

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
            output_command += "{0}:::{2} --> {1}:::{3}".format(
                link["TargetTaskID"],
                link["SourceTaskID"],
                link["TargetStatus"].replace(" ","_"),
                link["SourceStatus"].replace(" ","_")
            ) + "\n"
        if (link["relationship"] == "before"):
            output_command += "{0}:::{2} --> {1}:::{3}".format(
                link["SourceTaskID"],
                link["TargetTaskID"],
                link["TargetStatus"].replace(" ","_"),
                link["SourceStatus"].replace(" ","_")
            ) + "\n"
        if (link["relationship"] == "relate to"):
            output_command += "{0}:::{2} -- relate to -- {1}:::{3}".format(
                link["SourceTaskID"],
                link["TargetTaskID"],
                link["TargetStatus"].replace(" ","_"),
                link["SourceStatus"].replace(" ","_")
            ) + "\n"
        if (link["relationship"] == "blocks"):
            output_command += "{0}:::{2} --x {1}:::{3}".format(
                link["SourceTaskID"],
                link["TargetTaskID"],
                link["TargetStatus"].replace(" ","_"),
                link["SourceStatus"].replace(" ","_")
            ) + "\n"
        if (link["relationship"] == "is blocked by"):
            output_command += "{0}:::{2} --x {1}:::{3}".format(
                link["TargetTaskID"],
                link["SourceTaskID"],
                link["TargetStatus"].replace(" ","_"),
                link["SourceStatus"].replace(" ","_")
            ) + "\n"
    # Return the generated Mermaid command string
    return output_command




