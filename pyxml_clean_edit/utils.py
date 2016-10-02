import xml.etree.ElementTree as ET
import xml.dom.minidom

def get_parsed_xml(xml_object, leading_space=None):
    leading_space = '' if leading_space == None else leading_space
    str_xml = ''
    raw_xml = ET.tostring(xml_object, encoding='UTF-8')
    prettyXml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent='  ', newl='\n').split('\n')[1:-1]
    for string in prettyXml:
        str_xml = '{PREVIOUS}{INDENT}{NEW}\n'.format(PREVIOUS=str_xml, INDENT=leading_space, NEW=string)
    return str_xml

class EnumInsertionMode(object):
    Start=0
    End=1

class SourceLines(object):
    def __init__(self):
        self.start = None
        self.startline = None
        self.end = None
        self.endline = None
        self.insertion_mode = EnumInsertionMode.Start
    def is_valid(self):
        return self.start is not None and self.end is not None
    def get_insertion_index(self):
        if self.insertion_mode == EnumInsertionMode.Start:
            return self.start + 1
        elif self.insertion_mode == EnumInsertionMode.End:
            return self.end

def get_sourcelines_of_element(file_path, element_tag):
    srclines = SourceLines()
    currentline = 0
    with open(file_path, 'r') as f:
        for line in f.readlines():
            # TODO: make work for dense xml
            FOUND_CHILD = line.find('<{0}'.format(element_tag)) > -1
            SINGLE_LINE_ELEMENT = line.find('/>') > -1
            CLOSING_TAG = line.find('</{0}>'.format(element_tag)) > -1
            if FOUND_CHILD:
                srclines.start = currentline
                srclines.startline = line
                if SINGLE_LINE_ELEMENT:
                    srclines.end = currentline
                    srclines.endline = line
            if CLOSING_TAG:
                srclines.end = currentline
                srclines.endline = line
            currentline += 1
    if not srclines.is_valid():
        raise StandardError('Could not determine source lines for element tag')
    return srclines

def get_leading_whitespace(line):
    whitespaceCount = len(line) - len(line.lstrip())
    string = ' '
    val = []
    for i in range(0, whitespaceCount):
        val.append(string)
    return ''.join(val)

def guard(file_path, parent_element_tag):
    '''
    Standard guard exceptions for all user functions
    '''
    # ensure we have the parent element tag
    if not is_valid(file_path):
        raise StandardError('Can not parse xml file.')
    # ensure it has the parent element tag in it somewhere
    if not contains(file_path, element_tag=parent_element_tag):
        raise StandardError('Can not find parent element tag')

def contains(file_path, element_tag=None):
    '''
    '''
    xml_root = ET.parse(file_path).getroot()
    with open(file_path, 'r') as f:
        for line in f.readlines():
            FOUND_CHILD = line.find('<{0}'.format(element_tag)) > -1
            if FOUND_CHILD:
                return True
    return False


def is_valid(file_path):
    '''
    '''
    try:
        xml_root = ET.parse(file_path).getroot()
        return True
    except ET.ParseError:
        return False
