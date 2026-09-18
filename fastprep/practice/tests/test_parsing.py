"""Unit tests for the value parser, comparator and node encodings."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import parsing
from parsing import ParseError, parse_value, compare_output, format_value


class TestScalars(unittest.TestCase):
    def test_int_and_long(self):
        self.assertEqual(parse_value("5", "int"), 5)
        self.assertEqual(parse_value("-12", "int"), -12)
        self.assertEqual(parse_value("10", "long"), 10)
        self.assertIsInstance(parse_value("10", "long"), int)

    def test_java_long_suffix(self):
        """Seen once in the bank: xperi-count-integer-sequences."""
        self.assertEqual(parse_value("9000606388L", "long"), 9000606388)

    def test_real(self):
        self.assertEqual(parse_value("1.5", "double"), 1.5)
        self.assertEqual(parse_value("3.89", "float"), 3.89)
        self.assertEqual(parse_value("230.0", "float"), 230.0)
        self.assertIsInstance(parse_value("2", "double"), float)

    def test_boolean(self):
        self.assertIs(parse_value("true", "boolean"), True)
        self.assertIs(parse_value("false", "boolean"), False)

    def test_string_quoted_and_bare(self):
        self.assertEqual(parse_value('"hit"', "String"), "hit")
        self.assertEqual(parse_value("East", "String"), "East")          # bare output
        self.assertEqual(parse_value('"1e2"', "String"), "1e2")          # not a number
        self.assertEqual(parse_value('"2C 2D 3F"', "String"), "2C 2D 3F")  # suffix-looking

    def test_char(self):
        self.assertEqual(parse_value('"J"', "char"), "J")
        self.assertEqual(parse_value("b", "char"), "b")                  # bare output

    def test_string_none_is_not_null(self):
        self.assertEqual(parse_value('["None"]', "String[]"), ["None"])


class TestArrays(unittest.TestCase):
    def test_int_array(self):
        self.assertEqual(parse_value("[16,17,4,3]", "int[]"), [16, 17, 4, 3])
        self.assertEqual(parse_value("[]", "int[]"), [])
        self.assertEqual(parse_value("", "int[]"), [])

    def test_nested(self):
        self.assertEqual(parse_value("[[0,7],[1,4]]", "int[][]"), [[0, 7], [1, 4]])
        self.assertEqual(parse_value("[[[1,3],[5,7]],[[2,4]]]", "int[][][]"),
                         [[[1, 3], [5, 7]], [[2, 4]]])

    def test_string_arrays(self):
        self.assertEqual(parse_value('["a","b"]', "String[]"), ["a", "b"])
        self.assertEqual(parse_value('[["v1","Maple"]]', "String[][]"), [["v1", "Maple"]])
        self.assertEqual(parse_value('[["1","0"],["0","1"]]', "char[][]"), [["1", "0"], ["0", "1"]])

    def test_generic_lists(self):
        self.assertEqual(parse_value("[1,2,3]", "List<Integer>"), [1, 2, 3])
        self.assertEqual(parse_value('[["java"], ["python", "sql"]]', "List<List<String>>"),
                         [["java"], ["python", "sql"]])

    def test_float_array_with_int_literals(self):
        v = parse_value("[[3, -1], [-2, 3]]", "float[][]")
        self.assertEqual(v, [[3.0, -1.0], [-2.0, 3.0]])
        self.assertIsInstance(v[0][0], float)

    def test_whitespace_tolerated(self):
        self.assertEqual(parse_value("[1.2, 4.3, 5.8]", "float[]"), [1.2, 4.3, 5.8])

    def test_bad_value_raises(self):
        with self.assertRaises(ParseError):
            parse_value("[1,2", "int[]")
        with self.assertRaises(ParseError):
            parse_value('["a"]', "int[]")


class TestNodes(unittest.TestCase):
    def test_linked_list_round_trip(self):
        head = parse_value("[1,2,3,4,5]", "ListNode")
        self.assertEqual(head.val, 1)
        self.assertEqual(parsing.encode_linked_list(head), [1, 2, 3, 4, 5])
        self.assertIsNone(parse_value("[]", "ListNode"))

    def test_list_of_lists(self):
        lists = parse_value("[[1,4,5],[1,3,4],[2,6]]", "ListNode[]")
        self.assertEqual([parsing.encode_linked_list(l) for l in lists],
                         [[1, 4, 5], [1, 3, 4], [2, 6]])
        self.assertEqual(parse_value("[[],[3]]", "ListNode[]")[0], None)

    def test_tree_round_trip(self):
        root = parse_value("[3,9,20,null,null,15,7]", "TreeNode")
        self.assertEqual(root.val, 3)
        self.assertEqual(root.left.val, 9)
        self.assertEqual(root.right.left.val, 15)
        self.assertEqual(parsing.encode_tree(root), [3, 9, 20, None, None, 15, 7])

    def test_tree_nulls_do_not_consume_children(self):
        """[1,null,2,3] means: root 1, no left, right 2, whose left is 3."""
        root = parse_value("[1,null,2,3]", "TreeNode")
        self.assertIsNone(root.left)
        self.assertEqual(root.right.val, 2)
        self.assertEqual(root.right.left.val, 3)
        self.assertEqual(parsing.encode_tree(root), [1, None, 2, 3])

    def test_empty_tree(self):
        self.assertIsNone(parse_value("[]", "TreeNode"))
        self.assertEqual(parsing.encode_tree(None), [])

    def test_cycle_does_not_hang(self):
        a = parsing.ListNode(1); b = parsing.ListNode(2)
        a.next = b; b.next = a
        self.assertEqual(parsing.encode_linked_list(a), [1, 2, "<cycle>"])


class TestComparison(unittest.TestCase):
    def test_exact_int(self):
        ok, got, exp = compare_output(4, "4", "int")
        self.assertTrue(ok); self.assertEqual((got, exp), ("4", "4"))
        self.assertFalse(compare_output(5, "4", "int")[0])

    def test_float_tolerance(self):
        self.assertTrue(compare_output(0.8807970779778824, "0.8807970779778823", "double")[0])
        self.assertFalse(compare_output(0.88, "0.8807970779778823", "double")[0])

    def test_nested_lists(self):
        self.assertTrue(compare_output([[540, 570], [585, 600]], "[[540,570],[585,600]]", "int[][]")[0])
        self.assertFalse(compare_output([[540, 570]], "[[540,570],[585,600]]", "int[][]")[0])

    def test_order_matters(self):
        self.assertFalse(compare_output([2, 1], "[1,2]", "int[]")[0])

    def test_tuple_counts_as_list(self):
        self.assertTrue(compare_output((1, 2), "[1,2]", "int[]")[0])

    def test_returned_node_is_encoded(self):
        head = parse_value("[1,2,3]", "ListNode")
        self.assertTrue(compare_output(head, "[1,2,3]", "ListNode")[0])
        root = parse_value("[3,9,20,null,null,15,7]", "TreeNode")
        self.assertTrue(compare_output(root, "[3,9,20,null,null,15,7]", "TreeNode")[0])

    def test_bool_is_not_one(self):
        self.assertFalse(compare_output(1, "true", "boolean")[0])
        self.assertTrue(compare_output(True, "true", "boolean")[0])

    def test_string_output_display(self):
        ok, got, exp = compare_output("East", '"East"', "String")
        self.assertTrue(ok); self.assertEqual(got, '"East"')

    def test_none_result_fails_cleanly(self):
        self.assertFalse(compare_output(None, "[1,2]", "int[]")[0])


class TestTypeGrammar(unittest.TestCase):
    def test_element_type(self):
        self.assertEqual(parsing.element_type("int[]"), "int")
        self.assertEqual(parsing.element_type("int[][]"), "int[]")
        self.assertEqual(parsing.element_type("List<List<String>>"), "List<String>")
        self.assertIsNone(parsing.element_type("int"))
        self.assertIsNone(parsing.element_type("ListNode[]"))     # atomic on purpose

    def test_depth_and_base(self):
        self.assertEqual(parsing.depth("int[][][]"), 3)
        self.assertEqual(parsing.base_type("List<List<Integer>>"), "Integer")
        self.assertEqual(parsing.base_type("char[][]"), "char")


if __name__ == "__main__":
    unittest.main(verbosity=2)
