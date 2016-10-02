'''
tests for the various ways we might want to add things to an xml file.
'''
from os import unlink
import xml.etree.ElementTree as ET
import tempfile
import xml.dom.minidom

from .. import xml_helpers
from . import utils

def test_add_element():
    # make an xml
    xml_root = ET.Element('root')
    xml_parent = ET.SubElement(xml_root, 'parent')
    ET.SubElement(xml_parent, 'child', attrib={'Name':'1'})
    raw_xml = ET.tostring(xml_root)
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="    ", newl='\n')
    f = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # make some new children
    xml_child_2 = ET.Element('child', attrib={'Name':'2'})
    xml_child_3 = ET.Element('child', attrib={'Name':'3'})

    # add the children
    xml_helpers.add(file_path=f.name, elements=[xml_child_2, xml_child_3], parent_element_tag='parent')

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    utils.get_xml_from_file(f.name, debug=False, always_open=False)

    # close the file
    f.close()
    unlink(f.name)

    # test
    assert(len(new_xml_root.findall('parent/child')) == 3)

def test_replace_child_elements():
    # make an xml
    xml_root = ET.Element('root')
    xml_parent = ET.SubElement(xml_root, 'parent')
    ET.SubElement(xml_parent, 'child', attrib={'Name':'1'})
    raw_xml = ET.tostring(xml_root)
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="    ", newl='\n')
    f = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # make some new children
    xml_child_2 = ET.Element('child', attrib={'Name':'2'})
    xml_child_3 = ET.Element('child', attrib={'Name':'3'})

    # add the children
    xml_helpers.replace_children(file_path=f.name, elements=[xml_child_2, xml_child_3], parent_element_tag='parent')

    utils.get_xml_from_file(f.name, debug=False, always_open=False)

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)

    # test
    assert(len(new_xml_root.findall('parent/child')) == 2)

def test_remove_elements():
    # make an xml
    xml_root = ET.Element('root')
    xml_parent = ET.SubElement(xml_root, 'parent')
    ET.SubElement(xml_parent, 'child', attrib={'Name':'1'})
    ET.SubElement(xml_parent, 'child', attrib={'Name':'2'})
    ET.SubElement(xml_parent, 'child', attrib={'Name':'3'})
    raw_xml = ET.tostring(xml_root)
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="    ", newl='\n')
    f = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # add the children
    xml_helpers.remove(file_path=f.name, tag_matches='child', attrib_matches=[{'Name':'2'}, {'Name':'3'}])

    utils.get_xml_from_file(f.name, debug=False, always_open=True)

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)

    # test
    assert(len(new_xml_root.findall('parent/child')) == 1)
