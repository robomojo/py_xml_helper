import xml.etree.ElementTree as ET
import xml.dom.minidom

from . import utils
reload(utils)

def add(file_path=None, elements=None, tag_match=None, attrib_match=None):
    '''
    Add new sub-elements the found element.
    '''
    # guard against common exceptions
    utils.guard(file_path)
    # ensure arg types
    elements = utils.handle_elements(elements)
    tag_match = utils.handle_tag_match(tag_match)
    attrib_match = utils.handle_attrib_match(attrib_match)
    # get the sourcelines
    srclines = utils.get_sourcelines_of_element(file_path, tag_match, attrib_match)
    srclines.insertion_mode = utils.EnumInsertionMode.End
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # reverse elements, as we will be inserting them into the same index
    elements.reverse()
    # derive leading space from previous line
    leading_space = utils.get_leading_whitespace(lines[srclines.get_insertion_index() - 1])
    # get the clip as a list
    for xml_element in elements:
        str_element = utils.get_parsed_xml(xml_element, leading_space=leading_space)
        lines.insert(srclines.get_insertion_index(), str_element)
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))

def remove(file_path=None, tag_matches=None, attrib_matches=None):
    '''
    Remove found elements from the file.
    '''
    # guard against common exceptions
    utils.guard(file_path)
    # ensure arg types
    tag_matches = utils.handle_tag_matches(tag_matches)
    attrib_matches = utils.handle_attrib_matches(attrib_matches)
    srcline_objs = []
    for tag in tag_matches:
        for attrib in attrib_matches:
            srclines = utils.get_sourcelines_of_element(file_path, tag, attrib)
            srcline_objs.append(srclines)
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # reverse srcline_objs as we will now go and remove the lines
    srcline_objs.reverse()
    # pop all the lines inbetween start and end
    for srclines in srcline_objs:
        if srclines.is_multiline():
            del lines[srclines.start:srclines.end]
        else:
            del lines[srclines.start]
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))

def replace(file_path=None, element=None, tag_match=None, attrib_match=None):
    '''
    Replace the found element with a new element.
    '''
    # guard against common exceptions
    utils.guard(file_path)
    # ensure arg types
    tag_match = utils.handle_tag_match(tag_match)
    attrib_match = utils.handle_attrib_match(attrib_match)
    if type(element) is not ET.Element:
        raise StandardError('expecting element to be of type ET.Element')
    # get the sourcelines
    srclines = utils.get_sourcelines_of_element(file_path, tag_match, attrib_match)
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # derive leading space from target line
    leading_space = utils.get_leading_whitespace(lines[srclines.get_insertion_index()])
    # get the clip as a list
    str_element = utils.get_parsed_xml(element, leading_space=leading_space)
    # pop all the lines inbetween start and end
    if srclines.is_multiline():
        del lines[srclines.start:srclines.end]
        lines.insert(srclines.start, str_element)
    else:
        del lines[srclines.start]
        lines.insert(srclines.start, str_element)
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))

def replace_children(file_path, elements, tag_match=None, attrib_match=None):
    '''
    Replace all the child elements of the found element.
    '''
    # guard against common exceptions
    utils.guard(file_path)
    # ensure arg types
    tag_match = utils.handle_tag_match(tag_match)
    attrib_match = utils.handle_attrib_match(attrib_match)
    elements = utils.handle_elements(elements)
    # get the sourcelines
    srclines = utils.get_sourcelines_of_element(file_path, tag_match, attrib_match)
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # reverse elements, as we will be inserting them into the same index
    elements.reverse()
    # derive leading space from target line
    leading_space = utils.get_leading_whitespace(lines[srclines.get_insertion_index()])
    # pop all the lines inbetween start and end
    del lines[srclines.start+1:srclines.end]
    # get the clip as a list
    for xml_element in elements:
        str_element = utils.get_parsed_xml(xml_element, leading_space=leading_space)
        lines.insert(srclines.get_insertion_index(), str_element)
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))

def contains(file_path, tag_match=None, attrib_match=None):
    '''
    Queries the existance of a element.
    Kwargs:
        tag_match: string of tag name (<Fruit> = 'Fruit')
        attrib_match: dict of attribs (Type="Banana" = {'Type':'Banana'})
    '''
    # guard against common exceptions
    utils.guard(file_path)
    # ensure arg types
    tag_match = utils.handle_tag_match(tag_match)
    attrib_match = utils.handle_attrib_match(attrib_match)
    # get sourcelines
    srclines = utils.get_sourcelines_of_element(file_path, tag_match, attrib_match)
    return srclines.is_valid()
