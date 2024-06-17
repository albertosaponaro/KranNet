import re
from collections import Counter
from lxml import etree
import utils



def strip_namespace(tag):
    """
    Strip namespace from tag
    """
    return tag.split('}')[-1] if '}' in tag else tag

def speaker_counter(meeting_dict):
    """
    Count how many times a speaker speechs during a meeting
    """
    speakers_counter = []
    for meeting in meeting_dict['speakers']:
        speakers_counter.append(dict(Counter(meeting)))

    meeting_dict['speakers'] = speakers_counter

    return meeting_dict

def traverse_tree(element, meeting_dict, update_id):
    """
    Travers the DOM tree recursively
    """
    xmlns='http://www.w3.org/XML/1998/namespace'
    skip_meeting = False

    # Regular expression pattern to match the year (four digits)
    pattern = r'\b\d{4}\b'
    
    
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
    input_file, output_file = utils.parse_arguments()

    print('Load the Corpus DOM tree...')
    tree = etree.parse(input_file)
    tree.xinclude()
    root = tree.getroot()

    update_id = [0]

    meeting_dict = {
        'id': [],
        'title': [],
        'year': [],
        'speakers': []
    }

    # Travers the corpus to extract meetings infos
    print('Travers XML DOM tree...')
    traverse_tree(root, meeting_dict, update_id)

    # Count how many times a speaker speechs during a meeting
    meeting_dict = speaker_counter(meeting_dict)

    utils.save_dict_to_json(meeting_dict, output_file)



if __name__ == '__main__':
    main()

    
