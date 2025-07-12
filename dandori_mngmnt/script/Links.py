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


