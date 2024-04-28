import re
from htmlnode import *

in_code_block = False

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)   
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)    
    return matches

def markdown_to_blocks(markdown):  
    pattern = r'^(?:- |\* |\+ |\d+\.)' 
    lines = markdown.split('\n')     
    block_list = []
    temp_block_string = ''
    for list_item in lines:
        placeholder = re.sub(r'\n\s*\n', '\n', list_item, flags=re.MULTILINE)
        x = placeholder.strip()  
        if re.search(pattern, x, re.MULTILINE):                            
            temp_block_string += x + "\n"
        else:      
            if temp_block_string != '': 
                temp_block_string  = temp_block_string.rstrip('\n')              
                block_list.append(temp_block_string)  
                temp_block_string = '' 
            block_list.append(x)
    if temp_block_string != '':
        temp_block_string  = temp_block_string.rstrip('\n')                            
        block_list.append(temp_block_string)  
    filtered_result = [line for line in block_list if line]
    
    return filtered_result

def block_to_block_type(block_text):    
    if block_text.startswith("```"):        
        return "code block delimiter"    
    else:

        block_type_heading = "heading"
        block_type_paragraph = "paragraph"        
        block_type_blockquote = "blockquote"
        block_type_unordered_list = "unordered_list"
        block_type_ordered_list = "ordered_list"

        if re.match(r'^#{1,6}\s', block_text):
            return block_type_heading        
        if re.match(r"^>", block_text):       
            return block_type_blockquote
        if re.match(r"^(?:\*|-)\s", block_text):         
            return block_type_unordered_list
        if re.match(r"^\d+\.\s", block_text):          
            return block_type_ordered_list
        return block_type_paragraph
    
def block_type_paragraph(value):
    return HTMLNode(tag='p', value=value)

def block_type_blockquote(value):    
    modified_value = re.sub(r'^>\s*', '', value)    
    return HTMLNode(tag='blockquote', value=modified_value)

def block_type_ul(list_items):
    children = []
    pattern = re.compile(r'^\s*[*-]\s+')
    for item in list_items:
        cleaned_item = pattern.sub('', item)
        children.append(HTMLNode(tag='li', value=cleaned_item))
    return HTMLNode(tag='ul', children=children)

def block_type_ol(list_items):
    children = []
    pattern = re.compile(r'^\d+\.\s+')
    for item in list_items:
        cleaned_item = pattern.sub('', item)
        children.append(HTMLNode(tag='li', value=cleaned_item))
    return HTMLNode(tag='ol', children=children)


def block_type_code(code_content):   
    code_node = HTMLNode(tag='code', value=code_content)
    return HTMLNode(tag='pre', children=[code_node])




def block_type_heading(heading_text):
    # Counting the number of '#' characters at the start
    num_hashes = len(heading_text) - len(heading_text.lstrip('#'))
    
    # Determining the tag based on the count
    tag = f'h{num_hashes}'
    
    # Removing '#' characters and leading spaces from the heading text
    value = heading_text.lstrip('#').strip()
    
    return HTMLNode(tag=tag, value=value)

def markdown_to_html(markdown):
    #applying bold and italic
    pattern_bold1 = r'(\*\*(.*?)\*\*)'
    pattern_bold2 = r'(__(.+?)__)'
    pattern_italic1 = r'(\*(.*?)\*)'
    pattern_italic2 = r'(_(.+?)_)'
    replace_bold = r'<strong>\2</strong>'
    replace_italic = r'<em>\2</em>'
    markdown = re.sub(pattern_bold1, replace_bold, markdown)
    markdown = re.sub(pattern_bold2, replace_bold, markdown)
    markdown = re.sub(pattern_italic1, replace_italic, markdown)
    markdown = re.sub(pattern_italic2, replace_italic, markdown)  

    html_nodes = []  # To hold all HTMLNode objects created from the markdown
    blocks = markdown_to_blocks(markdown)  # Break down the markdown
    in_code_block = False
    code_block_lines = ''
    for block in blocks:
      
        block_type = block_to_block_type(block)  # Determine the block's type
        
        images = extract_markdown_images(block)
        links = extract_markdown_links(block)
        for alt_text, img_url in images:
            img_tag = f'<img src="{img_url}" alt="{alt_text}">'
            block = block.replace(f'![{alt_text}]({img_url})', img_tag)
        for link_text, link_url in links:
            link_tag = f'<a href="{link_url}">{link_text}</a>'
            block = block.replace(f'[{link_text}]({link_url})', link_tag)


        # Depending on the block type, call the appropriate function        
        if block_type == 'heading':
            node = block_type_heading(block)
        elif block_type == 'blockquote':            
            node = block_type_blockquote(block)
        elif block_type == 'unordered_list':
            # Unordered list might require splitting the block into list items                       
            items = block.split('\n')                   
            node = block_type_ul(items)
        elif block_type == 'ordered_list':
            # Similar splitting for ordered lists            
            items = block.split('\n')                    
            node = block_type_ol(items)
        elif block_type == "code block delimiter":            
            in_code_block = not in_code_block  # Toggle the state
            if not in_code_block:  # Exiting a code block
                # Process code_block_lines                
                node = block_type_code(code_block_lines)
                code_block_lines = []  # Reset for the next code block
           
        elif in_code_block:            
            code_block_lines += block + '\n'
        elif block_type == 'paragraph':           
            node = block_type_paragraph(block)
        else:
            # Fallback for unhandled types, you might adjust this part
            node = block_type_paragraph(block) # Using paragraph as a default might not always be appropriate

        html_nodes.append(node)  # Add the created HTMLNode to the list
    
    # Finally, assemble all HTMLNodes into a single parent HTMLNode
    parent_node = HTMLNode(tag="div", children=html_nodes)  # Assuming HTMLNode can take a list of children

    # Assuming HTMLNode has a method to convert itself into an HTML string
    return parent_node.to_html()  # Convert the entire structure to a single HTML string