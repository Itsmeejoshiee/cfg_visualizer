import flet as ft
import nltk
from nltk import CFG
import graphviz
from PIL import Image

# Define the grammar
grammar = CFG.fromstring("""
S -> A B C | A B | A C | B C | A | B | C
A -> 'a' A | 'A' A | 'a' | 'A'
B -> 'b' B | 'B' B | 'b' | 'B'
C -> 'c' C | 'C' C | 'c' | 'C'
""")

def generate_derivation_tree(input_string):
    if input_string == "":
        return nltk.Tree('S', [])
    parser = nltk.ChartParser(grammar)
    input_tokens = list(input_string)  # Convert input string to list of tokens
    trees = list(parser.parse(input_tokens))
    
    if not trees:
        return None
    
    return trees[0]

def tree_to_graphviz(tree):
    if tree is None:
        return None
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')

    def add_nodes(node, parent=None):
        node_id = str(id(node))
        label = node.label() if isinstance(node, nltk.Tree) else node
        dot.node(node_id, label)
        
        if parent:
            dot.edge(str(id(parent)), node_id)
        
        if isinstance(node, nltk.Tree):
            for child in node:
                add_nodes(child, node)

    add_nodes(tree)
    return dot

def render_tree_to_image(tree, filename="derivation_tree.png"):
    """Render the tree to a PNG image and save it."""
    dot = tree_to_graphviz(tree)
    if dot:
        dot.render(filename, format="png", cleanup=True)
    return filename


def main(page: ft.Page):
    page.title = "Derivation Tree Generator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  

    # Ensure the page can expand to fill the available space
    page.expand = True

    # Create a Column to center the widgets in the middle
    column = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        spacing=20,  
        expand=True  
    )

    # Add the grammar rules text at the top
    grammar_rules = (
        "Grammar Rules:\n"
        "S -> A | B | C | A B | A C | B C | A B C\n"
        "A -> 'a' A | 'A' A | 'a' | 'A'\n"
        "B -> 'b' B | 'B' B | 'b' | 'B'\n"
        "C -> 'c' C | 'c'"
    )

    column.controls.append(ft.Text(value=grammar_rules, size=14)) 
   
    row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER, 
        spacing=10,  
    )

    # Input field for the string
    input_field = ft.TextField(label="Enter a string (e.g., 'a', 'aab', 'A', 'aAB')", width=400)
    row.controls.append(input_field)

    # Button to generate the derivation tree
    generate_button = ft.ElevatedButton(text="Generate Derivation Tree", on_click=lambda e: on_generate_click(e))
    row.controls.append(generate_button)

    # Add the Row to the Column
    column.controls.append(row)

    # Output text for messages
    output_message = ft.Text("", width=400)
    column.controls.append(output_message)

    # Define the on_generate_click function
    def on_generate_click(e):
        input_string = input_field.value  
        tree = generate_derivation_tree(input_string)  

        if tree:
            output_filename = render_tree_to_image(tree) 
            output_message.value = f"Derivation tree saved as '{output_filename}'."  
        else:
            output_message.value = "No valid derivation tree could be generated."  


        output_message.update()  

    # Add the Column to the page
    page.add(column)

# Start the app
ft.app(target=main)
