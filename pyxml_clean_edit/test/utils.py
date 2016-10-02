import xml.etree.ElementTree as ET
import xml.dom.minidom

def get_xml_from_file (file_path, debug=None, always_open=None):
    '''
    Parse temp file into xml variable, with some test convenience. 
    Args:
        file_path: path to valid xml file
    Kwargs:
        debug: file will be opened if the xml cannot be parsed.
        always_open: always open the file.
    '''
    always_open = False if always_open == None else always_open
    debug = False if debug == None else debug
    open_file = False
    xml_root = None
    try:
        xml_root = ET.parse(file_path).getroot()
    except ET.ParseError:
        # open the file
        open_file = True
    if (open_file and debug) or always_open:
        import os
        os.system('notepad.exe {0}'.format(file_path))
    return xml_root
