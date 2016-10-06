'''
tests for the various ways we might want to add things to an xml file.
'''
import os
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
    f2 = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)
    with open(f2.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # make some new children
    xml_child_2 = ET.Element('child', attrib={'Name':'2'})
    xml_child_3 = ET.Element('child', attrib={'Name':'3'})

    # add the children
    xml_helpers.add(file_path=f.name, elements=[xml_child_2, xml_child_3], tag_match='parent')

    # os.system('"C:\\Program Files\\KDiff3\\kdiff3.exe" {0} {1}'.format(f2.name, f.name))

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)
    f2.close()
    unlink(f2.name)

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
    f2 = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)
    with open(f2.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # make some new children
    xml_child_2 = ET.Element('child', attrib={'Name':'2'})
    xml_child_3 = ET.Element('child', attrib={'Name':'3'})

    # add the children
    xml_helpers.replace_children(file_path=f.name, elements=[xml_child_2, xml_child_3], tag_match='parent')

    # os.system('"C:\\Program Files\\KDiff3\\kdiff3.exe" {0} {1}'.format(f2.name, f.name))

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)
    f2.close()
    unlink(f2.name)

    # test
    assert(len(new_xml_root.findall('parent/child')) == 2)

def test_replace_child_elements_with_subelement():
    # make an xml
    xml_root = ET.Element('root')
    xml_parent = ET.SubElement(xml_root, 'parent')
    xml_subparent = ET.SubElement(xml_parent, 'children')
    ET.SubElement(xml_subparent, 'child', attrib={'Name':'1'})
    ET.SubElement(xml_subparent, 'child', attrib={'Name':'2'})
    ET.SubElement(xml_subparent, 'child', attrib={'Name':'3'})
    raw_xml = ET.tostring(xml_root)
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="    ", newl='\n')
    f = tempfile.NamedTemporaryFile(delete=False)
    f2 = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)
    with open(f2.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # replace with None
    # xml_helpers.replace_children(file_path=f.name, elements=None, tag_match='parent')

    # os.system('"C:\\Program Files\\KDiff3\\kdiff3.exe" {0} {1}'.format(f2.name, f.name))

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)
    f2.close()
    unlink(f2.name)

    # test
    assert(len(new_xml_root.findall('parent/child')) == 0)

def test_replace_element():
    # make an xml
    xml_root = ET.Element('root')
    xml_parent = ET.SubElement(xml_root, 'parent')
    xml_subparent = ET.SubElement(xml_parent, 'children')
    ET.SubElement(xml_subparent, 'child', attrib={'Name':'1'})
    ET.SubElement(xml_subparent, 'child', attrib={'Name':'2'})
    ET.SubElement(xml_subparent, 'child', attrib={'Name':'3'})
    raw_xml = ET.tostring(xml_root)
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="    ", newl='\n')
    f = tempfile.NamedTemporaryFile(delete=False)
    f2 = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)
    with open(f2.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # replace with None
    xml_helpers.replace(file_path=f.name, element=ET.Element('imposter'), tag_match='child', attrib_match={'Name':'2'})

    # os.system('"C:\\Program Files\\KDiff3\\kdiff3.exe" {0} {1}'.format(f2.name, f.name))

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)
    f2.close()
    unlink(f2.name)

    # test
    assert(len(new_xml_root.findall('parent/children/child')) == 2)
    assert(len(new_xml_root.findall('parent/children/imposter')) == 1)

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
    f2 = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)
    with open(f2.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # add the children
    xml_helpers.remove(file_path=f.name, tag_matches='child', attrib_matches=[{'Name':'2'}, {'Name':'3'}])

    # os.system('"C:\\Program Files\\KDiff3\\kdiff3.exe" {0} {1}'.format(f2.name, f.name))

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)
    f2.close()
    unlink(f2.name)

    # test
    assert(len(new_xml_root.findall('parent/child')) == 1)

def test_add_element_using_subtags():
    # make an xml
    xml_root = ET.Element('root')
    xml_parent = ET.SubElement(xml_root, 'parent')
    xml_children = ET.SubElement(xml_parent, 'children')
    xml_child1 = ET.SubElement(xml_children, 'child', attrib={'Name':'1'})
    xml_child1_children = ET.SubElement(xml_child1, 'children')
    xml_child1_subchild = ET.SubElement(xml_child1_children, 'child', attrib={'Name':'1'})
    xml_child1_subchild = ET.SubElement(xml_child1_children, 'child', attrib={'Name':'2'})
    xml_child1_subchild = ET.SubElement(xml_child1_children, 'child', attrib={'Name':'3'})
    xml_child2 = ET.SubElement(xml_children, 'child', attrib={'Name':'2'})
    xml_child2_children = ET.SubElement(xml_child2, 'children')
    xml_child2_subchild = ET.SubElement(xml_child2_children, 'child', attrib={'Name':'1'})
    xml_child2_subchild = ET.SubElement(xml_child2_children, 'child', attrib={'Name':'2'})
    xml_child2_subchild = ET.SubElement(xml_child2_children, 'child', attrib={'Name':'3'})
    xml_children = ET.SubElement(xml_root, 'children')
    xml_child3 = ET.SubElement(xml_children, 'child', attrib={'Name':'1'})
    raw_xml = ET.tostring(xml_root)
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="    ", newl='\n')
    f = tempfile.NamedTemporaryFile(delete=False)
    f2 = tempfile.NamedTemporaryFile(delete=False)

    # write it
    with open(f.name, mode='w') as t_file:
        t_file.write(prettyXml)
    with open(f2.name, mode='w') as t_file:
        t_file.write(prettyXml)

    # add the children
    xml_helpers.add(file_path=f.name, elements=ET.Element('inserted'), tag_match='parent', sub_tags='children')

    # os.system('"C:\\Program Files\\KDiff3\\kdiff3.exe" {0} {1}'.format(f2.name, f.name))

    # try to find the children
    new_xml_root = ET.parse(f.name).getroot()

    # close the file
    f.close()
    unlink(f.name)
    f2.close()
    unlink(f2.name)

    # test
    assert(len(new_xml_root.findall('parent/children/inserted')) == 1)
