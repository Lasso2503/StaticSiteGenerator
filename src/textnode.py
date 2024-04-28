from htmlnode import LeafNode
from markdown_extractor import *
import re


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        if self.url is None:
            return f"TextNode('{self.text}', '{self.text_type}')"
        return f"TextNode('{self.text}', '{self.text_type}', '{self.url}')"



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []      
    for node in old_nodes:
        if node.text_type  == "text":            
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:                
                raise ValueError("Unmatched delimiter found in text")
            for i, segment in enumerate(split_nodes):
                if segment or i % 2 != 0:  # Adds non-empty segments and any segment between delimiters
                    text_type_assign = "text" if i % 2 == 0 else text_type                    
                    new_nodes_list.append(TextNode(segment, text_type_assign))   
                    text_assign_check = text_type_assign                       
        else:           
            new_nodes_list.append(node)
    return new_nodes_list

    
def text_node_to_html_node(text_node):
    
    if text_node.text_type == 'text':
        return LeafNode('', text_node.text)
    if text_node.text_type == 'code':
        return LeafNode(text_node.text_type, text_node.text) 
    if text_node.text_type == 'italic':
        return LeafNode('i', text_node.text) 
    if text_node.text_type == 'bold':
        return LeafNode('b', text_node.text)      
    if text_node.text_type == 'link':
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if text_node.text_type == 'img':
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    raise ValueError('Unknown text_type')

def split_nodes_image(old_nodes):
    new_nodes_list = []
    pattern = r'!\[.*?\]\(.*?\)'  
    for node in old_nodes:
        img_list = extract_markdown_images(node.text)
        if not img_list:
            new_nodes_list.append(node)
        else:
            split_text  = re.split(pattern, node.text)
            count = 0
            for segment in split_text:
                if segment.strip(): 
                    new_nodes_list.append(TextNode(segment, "text")) 
                if count < len(img_list):
                    alt_text, img_url = img_list[count]
                    new_nodes_list.append(TextNode(alt_text, "image", img_url))
                    count += 1
    return new_nodes_list
                    
def split_nodes_link(old_nodes):
    new_nodes_list = []
    pattern = r'\[.*?\]\(.*?\)'     
    
    for node in old_nodes:        
        link_list = extract_markdown_links(node.text)
        if not link_list:
            new_nodes_list.append(node)
        else:
            split_text  = re.split(pattern, node.text)
            count = 0
            for segment in split_text:
                if segment.strip(): 
                    new_nodes_list.append(TextNode(segment, "text")) 
                if count < len(link_list):
                    link_text, link_url = link_list[count]
                    new_nodes_list.append(TextNode(link_text,"link", link_url))
                    count += 1
    return new_nodes_list

def text_to_textnodes(text):
    first_split_image = split_nodes_image([TextNode(text, "text")])  
    processed_nodes = []
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for list_item in first_split_image:        
        if list_item.text_type == "image":
            processed_nodes.append(list_item)
            continue
        elif re.search(link_pattern, list_item.text):            
            second_split_link = split_nodes_link([list_item])            
            processed_nodes.extend(second_split_link)
            continue
        
        processed_nodes.append(list_item)

    
    # Define a list of tuples representing the delimiters and their corresponding text types
    markdown_elements = [("**", "bold"), ("*", "italic"), ("`", "code")]

    # Iteratively process each markdown feature for the entire list of nodes
    for delimiter, text_type in markdown_elements:
        # Temporarily store the results after each iteration to use in the next
        temp_processed_nodes = []
        for node in processed_nodes:
            # Only process text nodes further
            if node.text_type == "text":
                # split_nodes_delimiter needs to work on a segment of text within the node
                # Here we assume split_nodes_delimiter can handle segments of text and split them accordingly
                more_split_nodes = split_nodes_delimiter([node], delimiter, text_type)
                temp_processed_nodes.extend(more_split_nodes)
            else:
                # If not a text node, just carry it over to the next list
                temp_processed_nodes.append(node)
        # Update processed_nodes with the latest processed list
        processed_nodes = temp_processed_nodes

    # By the end of this process, processed_nodes should contain all the nodes processed into their final forms
    return processed_nodes   