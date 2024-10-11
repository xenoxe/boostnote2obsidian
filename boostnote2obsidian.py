import os
import cson
import re
import shutil

def convert_image_paths(content, image_dir, output_image_dir):

    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    images = image_pattern.findall(content)
    images = [s.removeprefix(':storage\\') for s in images] 

    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)
    
    for image in images:

        image_path = os.path.join(image_dir, image)
        if os.path.exists(image_path):

            shutil.copy(image_path, output_image_dir)
            # Remplacer le chemin dans le contenu
            new_image_path = os.path.join(output_image_dir, os.path.basename(image_path))
            content = content.replace(image, new_image_path)
    
    return content

def convert_cson_to_md(input_dir, output_dir, image_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    for filename in os.listdir(input_dir):
        if filename.endswith(".cson"):
            input_file = os.path.join(input_dir, filename)
            
            with open(input_file, 'r', encoding='utf-8') as file:
                try:

                    cson_content = cson.load(file)
                    markdown_content = cson_content.get("content", "")
                    
                    markdown_content = convert_image_paths(markdown_content, image_dir, os.path.join(output_dir, out_image_dir))
                    pattern = r'\[([^\]]+)\]\(:storage\\.*?\)'
                    markdown_content = re.sub(pattern, r'[[\1]]', markdown_content)

                    title = cson_content.get("title", "Untitled")
                    title = re.sub(r'[<>:"/\\|?*]', '', title)  
                    output_file = os.path.join(output_dir, title + ".md")
                    
                    with open(output_file, 'w', encoding='utf-8') as md_file:
                        md_file.write(markdown_content)
                    
                    print(f"Note convertie : {output_file}")
                except Exception as e:
                    print(f"Erreur lors de la conversion de {filename}: {e}")

# TO MODIFY
input_cson_dir = "./Boostnote/notes"  # Note's folder
output_md_dir = "./Obsi-export"         # Dirname where data will be exported to
image_dir = "./Boostnote/attachments"          # Boost note imges folder
out_image_dir = "img"          # dirname of your images (depends on your obsidian setup)

convert_cson_to_md(input_cson_dir, output_md_dir, image_dir)