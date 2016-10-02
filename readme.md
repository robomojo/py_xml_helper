# py_xml_helper
Python module for cleanly editing existing xml files.

This aims to be a light-weight alternative to other solutions out there.

# Why bother?
Sometimes you just want to edit a living xml file, without screwing everything up.
You don't need to understand everything that's going on the file. Xml files can get hairy with namespaces and other complicated things, and this might just save you that hassle.
You don't want to erase any human hand-edits and comments accidently, nor do you want to write extra code just to parse them correctly.
You don't always need to know why an xml file is structured a certain way - if you can get lucky and find your parent element, get in, and get out.
You will probably be happy having a clean diff when you're done. 

# Testing
All the tests are made for the nose testing framework.
