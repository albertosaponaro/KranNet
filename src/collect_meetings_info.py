import re
import json
import os
from collections import Counter
from lxml import etree


# TODO - add argument parser

# Strip namespace from tag
def strip_namespace(tag):
    return tag.split('}')[-1] if '}' in tag else tag

# Travers the DOM tree recursively
def traverse_tree(element, meeting_dict, update_id):
    xmlns='http://www.w3.org/XML/1998/namespace'
    skip_meeting = False

    # Regular expression pattern to match the year (four digits)
    pattern = r'\b\d{4}\b'
    
    # TODO - save elements we want to save else continue the traverse
    if strip_namespace(element.tag) == 'meeting':
            
            if element.text is not None: # sanity check
                if element.attrib.get(f'{{{xmlns}}}lang') == 'de':
                    update_id[0] +=1
                    
                    # extract year
                    match = re.search(pattern, element.text)

                    if match:
                        year = match.group()
                        
                        # Initialize new meeting
                        meeting_dict['id'].append(update_id[0])
                        meeting_dict['year'].append(year)
                        meeting_dict['title'].append(element.text)
                        meeting_dict['speakers'].append([])

                        skip_meeting = False
                    else: 
                        skip_meeting = True


    if strip_namespace(element.tag) == 'note' and not skip_meeting:
         
         if element.text is not None: # sanity check
              if element.attrib.get(f'type') == 'speaker':
                   
                   # update list of spekers
                   meeting_dict['speakers'][-1].append(element.text)
                   
    for child in element:
        traverse_tree(child, meeting_dict, update_id)
def main():
    """
    Collects meeting informations from the Corpus (XML) and save them into a JSON object.
    """
    tree = etree.parse('../datasets/Kranjska-xml/Corpus-Kranjska.xml')
    tree.xinclude()
    root = tree.getroot()

    update_id = [0]

    meeting_dict = {
        'id': [],
        'title': [],
        'year': [],
        'speakers': []
    }

    traverse_tree(root, meeting_dict, update_id)

    # Count how many times a speaker speechs during a meeting
    # TODO - Make separate function for readability
    speakers_counter = []
    for meeting in meeting_dict['speakers']:
        speakers_counter.append(dict(Counter(meeting)))

    meeting_dict['speakers'] = speakers_counter

    
    # Save in JSON
    # TODO - Make separate function for readability
    data = meeting_dict

    # Define the filename for the JSON file
    fname = "../cache/out.json"
    dir = os.path.dirname(fname)

    # Check directory
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Write the dictionary to a JSON file
    with open(fname, "w") as json_file:
        json.dump(data, json_file)
    


if __name__ == '__main__':
    main()

    
