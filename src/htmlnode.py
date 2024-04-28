class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []  # Ensure children is a list
        self.props = props
        if self.props is None:
            self.props = {}
    
    def to_html(self):
        # Convert properties to string of HTML attributes
        props_html = self.props_to_html()
        
        # Base case: Node with no children, only a value
        if not self.children:
            # Include properties in the opening tag
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        
        # Recursive case: Node with children
        children_html = "".join(child.to_html() for child in self.children)  # Generate HTML for children
        # Also include properties in the opening tag for consistent output
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def props_to_html(self):
        if not self.props:
            return ""
        
        a_list = []
        for key in self.props:        
            key_value_string = f'{key}="{self.props[key]}"'
            a_list.append(key_value_string)
        props = ' '.join(a_list)
        return f" {props}"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        self.value = value  
        if tag != "img" and value is None:
            raise ValueError('No value detected for in between the tag')
          
        if props is None:
            props = {}
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):        
        if self.tag == None:
            if self.value is None:
                return ''
            return self.value

        if self.value is not None and not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        elif self.tag == "img":
            prop_string = self.props_to_html()
            return f'<{self.tag}{prop_string}/>'
        else:
            prop_string = self.props_to_html()
            return f'<{self.tag}{prop_string}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        
        self.tag = tag        
        if tag is None:
            raise ValueError('No tag provided')
        super().__init__(tag=tag, props=props)
        self.children = children
        if not self.children:
            raise ValueError('No children provided')        
        
    
    def to_html(self):   
        return_string = f'<{self.tag}>'
        child_string = ''
        for child in self.children:
            child_string += child.to_html()
        return_string += child_string + f'</{self.tag}>'
        return return_string

