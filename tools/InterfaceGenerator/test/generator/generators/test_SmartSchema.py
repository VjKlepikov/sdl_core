import collections
import sys
import os.path

projectRootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(projectRootDir)

import unittest

from generator.generators.SmartSchema import SmartSchema
from generator import Model

expected_result_full_comment = """/**
 * @brief Enumeration Test Name.
 *
 * Description Line1
 * Description Line2
 *
 * Design Line1
 *
 * @note Issue1
 * @note Issue2
 * @note Issue3
 *
 * @todo Do1
 * @todo Do2
 */"""

expected_result_enum_element1 = """/**
 * @brief InternalName.
 */
InternalName = 10"""

expected_result_enum_element2 = """/**
 * @brief NO_VALUE_ELEMENT.
 *
 * Description Line1
 * Description Line2
 *
 * Design Line1
 */
NO_VALUE_ELEMENT"""

expected_result_enum_elements1 = """/**
 * @brief name1.
 *
 * Design Line1
 *
 * @todo Do1
 * @todo Do2
 */
name1 = 1,

/**
 * @brief internal_name2.
 *
 * Description Line1
 * Description Line2
 *
 * @note Issue1
 * @note Issue2
 * @note Issue3
 */
internal_name2"""

expected_result_enum1 = """/**
 * @brief Enumeration Enum1.
 *
 * @todo Do1
 * @todo Do2
 */
enum Enum1
{
    /**
     * @brief name1.
     *
     * Design Line1
     *
     * @todo Do1
     * @todo Do2
     */
    name1 = 1,

    /**
     * @brief internal_name2.
     *
     * Description Line1
     * Description Line2
     *
     * @note Issue1
     * @note Issue2
     * @note Issue3
     */
    internal_name2
};
"""

expected_result_enum2 = """/**
 * @brief Enumeration E2.
 */
enum E2
{
    /**
     * @brief val_1.
     */
    val_1,

    /**
     * @brief val_2.
     */
    val_2 = 100,

    /**
     * @brief val_3.
     */
    val_3
};
"""

description = ["Description Line1", "Description Line2"]
design_description = ["Design Line1"]
issues = ["Issue1", "Issue2", "Issue3"]
todos = ["Do1", "Do2"]
        
class TestSmartSchema(unittest.TestCase):
    
    def test_generate_comment(self):
        smart_schema_generator = SmartSchema()
                
        enum = Model.Enum("Test Name", description, design_description, issues, todos)
        self.assertEqual(smart_schema_generator._generate_comment(enum),
                         expected_result_full_comment, 
                         "Full comment for enum is invalid")

    def test_generate_enum_element(self):
        smart_schema_generator = SmartSchema()
        
        enum_element1 = Model.EnumElement("Element1",
                                          None, None, None, None, "InternalName", "10")
        self.assertEqual(smart_schema_generator._generate_enum_element(enum_element1),
                         expected_result_enum_element1,
                         "Short commented enum element with internal name is invalid")
        
        enum_element2 = Model.EnumElement("NO_VALUE_ELEMENT",
                                          description, design_description, None,
                                          None, None, None)
        self.assertEqual(smart_schema_generator._generate_enum_element(enum_element2),
                        expected_result_enum_element2,
                        "Enum element with no value is invalid")
        
    def test_generate_enum_elements(self):
        smart_schema_generator = SmartSchema()
        
        elements = [Model.EnumElement("name1", None, design_description, None, todos, None, "1"),
                    Model.EnumElement("name2", description, None, issues, None, "internal_name2", None)]        
        self.assertEqual(smart_schema_generator._generate_enum_elements(elements),
                         expected_result_enum_elements1,
                         "Simple enum elements are invalid")
        
    def test_generate_enum(self):
        smart_schema_generator = SmartSchema()
        
        elements1 = collections.OrderedDict()
        elements1["name1"] = Model.EnumElement("name1", None, design_description, None, todos, None, "1")
        elements1["name2"] = Model.EnumElement("name2", description, None, issues, None, "internal_name2", None)
        
        enum1 = Model.Enum("Enum1", None, None, None, todos, None, elements1)
        self.assertEqual(smart_schema_generator._generate_enum(enum1),
                         expected_result_enum1,
                         "Simple enum is invalid")
        
        elements2 = collections.OrderedDict() 
        elements2["xxx"] = Model.EnumElement("xxx", None, None, None, None, "val_1", None)
        elements2["yyy"] = Model.EnumElement("yyy", None, None, None, None, "val_2", "100")
        elements2["zzz"] = Model.EnumElement("val_3", None, None, None, None, None, None)
        
        enum2 = Model.Enum("E2", None, None, None, None, None, elements2)
        self.assertEqual(smart_schema_generator._generate_enum(enum2),
                         expected_result_enum2,
                         "Long enum is invalid")
        
        self.assertEqual(smart_schema_generator._generate_enums([enum1, enum2]), 
                         "{0}\n{1}".format(expected_result_enum1, expected_result_enum2)
                         ,"Generated enums are invalid")
        
    def test_full_generation(self):
        smart_schema_generator = SmartSchema()
        
        elements1 = collections.OrderedDict()
        elements1["name1"] = Model.EnumElement("name1", None, design_description, None, todos, None, "1")
        elements1["name2"] = Model.EnumElement("name2", description, None, issues, None, "internal_name2", None)
        
        enum1 = Model.Enum("Enum1", None, None, None, todos, None, elements1)
        
        elements2 = collections.OrderedDict() 
        elements2["xxx"] = Model.EnumElement("xxx", None, None, None, None, "val_1", None)
        elements2["yyy"] = Model.EnumElement("yyy", None, None, None, None, "val_2", "100")
        elements2["zzz"] = Model.EnumElement("val_3", None, None, None, None, None, None)
        
        enum2 = Model.Enum("E2", None, None, None, None, None, elements2)
        
        enums = collections.OrderedDict()
        enums["Enum1"] = enum1
        enums["Enum2"] = enum2
        
        functions = collections.OrderedDict()
        functions["Function1"] = Model.Function("Function1", elements1["name1"], elements1["name2"], None, None, None, None, None, None)
        functions["Function2"] = Model.Function("Function2", elements2["xxx"], elements2["yyy"], None, None, None, None, None, None)
        
        interface = Model.Interface(enums, None, functions, {"param1" : "value1", "param2" : "value2"})
        
        smart_schema_generator.generate(interface, "Test.xml", "XXX::YYY::ZZZ", "/home/eftin/gen_test")

if __name__ == '__main__':
    unittest.main()
