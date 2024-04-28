import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_html_generation(self):
        # Create a tree of HTML nodes
        inner_node = ParentNode("div", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
        ])
        root_node = ParentNode("p", [
            inner_node,
            LeafNode("i", "Italic text"),
        ])

        expected_html = "<p><div><b>Bold text</b>Normal text</div><i>Italic text</i></p>"
        self.assertEqual(root_node.to_html(), expected_html)

    def test_odd_edge_case(self):
        # Create some LeafNodes
        leaf_with_no_tag_and_empty_value = LeafNode(None, '')
        leaf_with_html_like_value = LeafNode(None, '<span>Fake HTML</span>')
        leaf_with_tag = LeafNode("b", "Bold text")

        # Create a ParentNode that contains these LeafNodes
        parent_node = ParentNode("div", [
            leaf_with_no_tag_and_empty_value,
            leaf_with_html_like_value,
            leaf_with_tag,
        ])

        # What we expect to get back
        expected_html = "<div><span>Fake HTML</span><b>Bold text</b></div>"

        # This tests how it handles empty values and values that look like HTML but are not.
        self.assertEqual(parent_node.to_html(), expected_html)

    

    def test_complex_properties(self):
        complex_children = [
            LeafNode("a", "Click here", {"href": "http://example.com", "data-custom": "value"}),
            LeafNode("img", None, {"src": "http://example.com/image.png", "onerror": "alert('XSS')"}),
            LeafNode("span", "Stylish text", {"style": "color:red; font-weight:bold;"}),
        ]
        parent_node = ParentNode("div", complex_children)
        expected_html = """<div><a href="http://example.com" data-custom="value">Click here</a><img src="http://example.com/image.png" onerror="alert('XSS')<span style="color:red; font-weight:bold;">Stylish text</span>"""
    

    

if __name__ == '__main__':
    unittest.main()