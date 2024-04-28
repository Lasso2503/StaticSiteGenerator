import unittest
from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = LeafNode(
            "div",
            "Hello, world!",
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
    
    def test_leaf_node_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph.")
        expected_html = "<p>This is a paragraph.</p>"
        self.assertEqual(node.to_html(), expected_html)
       
        

if __name__ == "__main__":
    unittest.main()
    