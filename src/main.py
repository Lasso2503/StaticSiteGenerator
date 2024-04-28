import os
import shutil
from markdown_utils import *
from markdown_extractor import *


def delete_and_create_new_public(public_dir_path):
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
    os.makedirs(public_dir_path, exist_ok=True) 

def copy_contents(src_path, dest_path):
    # Ensure the destination directory exists (create if not)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        
    items = os.listdir(src_path)
    for item in items:
        item_src_path = os.path.join(src_path, item)
        item_dest_path = os.path.join(dest_path, item)
        
        if os.path.isfile(item_src_path):
            # If it's a file, copy it to the destination
            shutil.copy(item_src_path, item_dest_path)
        elif os.path.isdir(item_src_path):
            # If it's a directory, recursively call this function
            copy_contents(item_src_path, item_dest_path)
'''
def generate_page(from_path, template_path, dest_path):
    print('Generate page process initiated...standby...')
    
    with open(os.path.join(from_path, "index.md")) as my_file:
        content = my_file.read()
    with open(os.path.join(template_path, "template.html")) as my_file:
        html_template = my_file.read()

    converted_html = markdown_to_html(content)    
    title = extract_title(content)   
    html_with_title = html_template.replace("{{ Title }}", title)   
    final_html = html_with_title.replace("{{ Content }}", converted_html)
   
    # Extract the directory from dest_path
    directory = os.path.dirname(dest_path)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(final_html)
'''


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if os.path.isdir(dir_path_content):
        for item in os.listdir(dir_path_content):
            new_path = os.path.join(dir_path_content, item)
            generate_pages_recursive(new_path, template_path, dest_dir_path)
    elif dir_path_content.endswith("md"):
        with open(dir_path_content) as my_file:
            content = my_file.read()
        with open(template_path) as my_file:
            html_template = my_file.read()
            converted_html = markdown_to_html(content)   
            title = extract_title(content)

            html_with_title = html_template.replace("{{ Title }}", title)   
            final_html = html_with_title.replace("{{ Content }}", converted_html)
            base_content_dir = "content"
           
            relative_path = os.path.relpath(dir_path_content, start=base_content_dir)
            
            change_to_html = relative_path.replace(".md", ".html")
            
            destination = os.path.join(dest_dir_path, change_to_html)
           
            whole_path = os.path.dirname(destination)
            if not os.path.isdir(whole_path):
                os.makedirs(whole_path, exist_ok=True)
            
            with open(destination, 'w') as file:
                file.write(final_html)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    content_path = os.path.join(project_root, 'content')
    template_path = os.path.join(project_root, 'template.html')
    static_src_path = os.path.join(project_root, 'static')
    public_dest_path = os.path.join(project_root, 'public')
    
    delete_and_create_new_public(public_dest_path)  # Note the adjustment to take path as argument
    # Now providing the correct template path and ensuring it points directly to the 'template.html'
    generate_pages_recursive(content_path, template_path, public_dest_path)
    # Copy static contents correctly
    copy_contents(static_src_path, public_dest_path)
    

    
    
# Ensure the main() function is called when the script is executed directly
if __name__ == "__main__":
    main()