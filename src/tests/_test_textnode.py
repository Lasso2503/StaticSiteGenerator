import unittest

from textnode import *


class TestTextNode(unittest.TestCase):    
    '''
    def test_bold_text_conversion(self):
        test_text_node = TextNode("Hello, world!", "bold")
        result_node = text_node_to_html_node(test_text_node)
        assert result_node.to_html() == "<b>Hello, world!</b>", "Failed to convert plain text"
    def test_url_conversion(self):
        test_text_node = TextNode("9gag", "link", '9gag.com')
        result_node = text_node_to_html_node(test_text_node)
        assert result_node.to_html() == '<a href="9gag.com">9gag</a>', "Failed to convert plain text"
    def test_img_conversion(self):
        # Given a TextNode for an image with alt text "Funny Cat" and URL "http://example.com/cat.png"
        test_text_node = TextNode("Funny Cat", "img", 'http://example.com/cat.png')
        
        # When converting the TextNode to an HTMLNode
        result_node = text_node_to_html_node(test_text_node)
        
        # Then the HTML representation should match an <img> tag with the correct src and alt attributes
        expected_html = '<img src="http://example.com/cat.png" alt="Funny Cat"/>'
        self.assertEqual(result_node.to_html(), expected_html, "Failed to convert image text")
    
    def test_split_nodes_delimiter_basic(self):
        input_nodes = [TextNode("This is some example text with `code`", "text")]
        expected_output = [
            TextNode("This is some example text with ", "text"),
            TextNode("code", "code")
        ]
        delimiter = "`"
        text_type = "code"
        
        output_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        print(output_nodes)
        assert output_nodes == expected_output, f"Expected output did not match: {expected_output}"
        
    def test_split_nodes_delimiter_unbalanced_delimiter(self):
        input_nodes = [TextNode("This has an unbalanced `delimiter", "text")]
        delimiter = "`"
        text_type = "code"
        # Expecting a ValueError due to unmatched delimiters
        with self.assertRaises(ValueError):
            split_nodes_delimiter(input_nodes, delimiter, text_type)

    def test_split_nodes_delimiter_text_after_delimiter(self):
        input_nodes = [TextNode("Here is `code` followed by text", "text")]
        delimiter = "`"
        text_type = "code"

        expected_output = [
            TextNode("Here is ", "text"),
            TextNode("code", text_type),
            TextNode(" followed by text", "text")  # This validates handling text after the delimiter
        ]

        output_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        assert output_nodes == expected_output, f"Expected output did not match: {expected_output}"  
        

    def test_single_link(self):
        # Setup: create an old_nodes list with a single TextNode containing one link
        old_nodes = [TextNode("Check out this [link](https://example.com)! or this link [link](http://example.com) tralala", "text")]
            
        # Execution: call your function with the old_nodes
        new_nodes_list = split_nodes_link(old_nodes)
            
        # Verification: Verify the results are as expected
        self.assertEqual(len(new_nodes_list), 5, "Should split into three nodes")
        self.assertEqual(new_nodes_list[0].text, "Check out this ", "Incorrect first part")
        self.assertEqual(new_nodes_list[1].text, "link",  "Incorrect link text")
        self.assertEqual(new_nodes_list[1].url, "https://example.com", "Incorrect link URL")
        self.assertEqual(new_nodes_list[3].url, "http://example.com", "Incorrect link URL")
        self.assertEqual(new_nodes_list[1].text_type, "link", "Incorrect node type for link")
        self.assertEqual(new_nodes_list[4].text, " tralala", "Incorrect last part")
        

    def test_two_images(self):
        # Setup: create an old_nodes list with a single TextNode containing one link
        old_nodes = [TextNode("![imag**e*&](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) poedelewpoepsie", "text")]
            
        # Execution: call your function with the old_nodes
        new_nodes_list = split_nodes_image(old_nodes)
            
        # Verification: Verify the results are as expected
        self.assertEqual(len(new_nodes_list), 3, "Should split into 5 nodes")
        #self.assertEqual(new_nodes_list[0].text, "This is text with an ", "Incorrect first part")
        self.assertEqual(new_nodes_list[0].text, "imag**e*&",  "Incorrect link text")
        self.assertEqual(new_nodes_list[0].url, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png", "Incorrect link IMG")
        self.assertEqual(new_nodes_list[1].url, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png", "Incorrect link IMG2")
        self.assertEqual(new_nodes_list[0].text_type, "image", "Incorrect node type for link")
        self.assertEqual(new_nodes_list[2].text, " poedelewpoepsie", "Incorrect last part")
        

    def test_image_with_nested_markdown_in_alt_text(self):
        # Setup: create an old_nodes list with a single TextNode containing an image
        # The alt text includes Markdown formatting for italics
        old_nodes = [TextNode('Start text ![image with *italic* alt text](https://example.com/image.png) end text', 'text')]
        
        # Execution: call your function with the old_nodes
        new_nodes_list = split_nodes_image(old_nodes)
        
        # Verification: Check if the function correctly handled the Markdown in alt text
        self.assertEqual(len(new_nodes_list), 3, "Should split into three nodes")
        self.assertIn("image with *italic* alt text", new_nodes_list[1].text, "Alt text with nested Markdown was not handled correctly")
        self.assertEqual(new_nodes_list[1].url, "https://example.com/image.png", "Image URL handling issue")
        self.assertTrue("Start text " in new_nodes_list[0].text and " end text" in new_nodes_list[2].text, "Text surrounding the image was not correctly identified")
        '''

    def test_basic_markdown_elements(self):
        # Example test for basic elements
        text = "This is **bold text** with an *italic* word, a `code block`, an ![image1](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/image1.png), and a [link1](https://boot.dev). Here's another ![image2](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/image2.png) followed by [link2](https://example.com) and **another piece of bold text**."
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word, a ", "text"),
            TextNode("code block", "code"),
            TextNode(", an ", "text"),
            TextNode("image1", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/image1.png"),
            TextNode(", and a ", "text"),
            TextNode("link1", "link", "https://boot.dev"),
            TextNode(". Here's another ", "text"),
            TextNode("image2", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/image2.png"),
            TextNode(" followed by ", "text"),
            TextNode("link2", "link", "https://example.com"),
            TextNode(" and ", "text"),
            TextNode("another piece of bold text", "bold"),
            TextNode(".", "text")
        ]


        result = text_to_textnodes(text)
        
        self.assertEqual(result, expected)
        
    

if __name__ == "__main__":
    unittest.main()
