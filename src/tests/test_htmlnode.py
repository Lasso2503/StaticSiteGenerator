import unittest
from htmlnode import *
from markdown_extractor import *


class TestHTMLNode(unittest.TestCase):
    '''
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
         
    def test_block_type_paragraph(self):
        paragraph_text = "This is a test paragraph."
        expected_output = "<p>This is a test paragraph.</p>"

        paragraph_html_node = block_type_paragraph(paragraph_text)
        actual_output = paragraph_html_node.to_html()

        assert actual_output == expected_output, "The paragraph block did not convert correctly."

    def test_block_type_blockquote(self):
        blockquote_text = "This is a test blockquote."
        expected_output = "<blockquote>This is a test blockquote.</blockquote>"

        blockquote_html_node = block_type_blockquote(blockquote_text)
        actual_output = blockquote_html_node.to_html()

        assert actual_output == expected_output, "The blockquote block did not convert correctly."

    def test_block_type_ul(self):
        list_items = ["- First item", "- Second item", "- Third item"]
        expected_output = "<ul><li>First item</li><li>Second item</li><li>Third item</li></ul>"

        ul_html_node = block_type_ul(list_items)
        actual_output = ul_html_node.to_html()

        assert actual_output == expected_output, "The UL block did not convert correctly."

    def test_block_type_code(self):
        code_content = "print('Hello, world!')"
        expected_output = "<pre><code>print('Hello, world!')</code></pre>"

        code_html_node = block_type_code(code_content)
        actual_output = code_html_node.to_html()

        assert actual_output == expected_output

    def test_block_type_heading(self):
        heading_text = "## This is a test heading"
        expected_output = "<h2>This is a test heading</h2>"

        heading_html_node = block_type_heading(heading_text)
        actual_output = heading_html_node.to_html()

        assert actual_output == expected_output, "The heading block did not convert correctly."
    '''

    def test_paragraph(self):
        # Define a simple paragraph block
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")

    def test_heading(self):
        # Define a heading block
        self.assertEqual(block_to_block_type("# This is a heading"), "heading")

    def test_code(self):
        # Define a code block
        self.assertEqual(block_to_block_type("```\nprint('Hello, world!')\n```"), "code")

    def test_quote(self):
        # Define a quote block
        self.assertEqual(block_to_block_type("> This is a quote."), "blockquote")

    def test_unordered_list(self):
        # Define an unordered list block
        self.assertEqual(block_to_block_type("* List item 1\n* List item 2"), "unordered_list")

    def test_ordered_list(self):
        # Define an ordered list block
        self.assertEqual(block_to_block_type("1. List item 1\n2. List item 2"), "ordered_list")

    def test_all_block_types(self):
        # Test heading
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        # Test paragraph
        self.assertEqual(block_to_block_type("Just a simple paragraph."), "paragraph")
        # Test code
        self.assertEqual(block_to_block_type("```\nCode block\n```"), "code")
        # Test blockquote
        self.assertEqual(block_to_block_type("> This is a quote."), "blockquote")
        # Test unordered list
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        # Test ordered list
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), "ordered_list")
        
if __name__ == "__main__":
    unittest.main()
