import os
import yaml

def generate_hugo_yaml(config_data, output_file):
    yaml_content = """
backend:
  name: git-gateway
  branch: master # Branch to update (optional; defaults to master at testing remember to change to dev )

media_folder: static/images
public_folder: images

collections:
"""
    
    for item_name, item_dir in config_data.items():
        section = f"""
  - name: 'zh-item-{item_name}'
    label: '{item_dir}'
    folder: 'content/zh/items/酒單/{item_dir}'
    create: true

    fields: 
      - {{ label: '品項標題', name: 'title', widget: 'string' }}
      - {{ label: '價格', name: 'price', widget: 'list' }}
      - {{ label: '副標題簡介描述', name: 'description', widget: 'string',required: false }}
      - {{ label: '未上架', name: 'draft', widget: 'boolean', default: false}}
      - {{ label: '上架順序', name: 'weight', widget: 'number', default: 10}}
      - {{ label: '照片', name: 'image', widget: 'image', media_folder: '../../../../../static/images', public_folder: 'images' ,required: false }}
      - {{ label: '文字', name: 'body', widget: 'string' }}
      - {{ label: '種類', name: 'categories', widget: 'list', required: false }}
      - {{ label: '標籤', name: 'tags', widget: 'list', required: false }}
      - {{ label: '發布日期', name: 'date', widget: 'datetime' }}
"""
        yaml_content += section
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(yaml_content.strip() + "\n")
    
    print(f"YAML config saved to {output_file}")

# Example key-value mapping
def generate_config_data(folder_path):
    config_data = {
        "item_name": "item_dir",
        "wisky": "威士忌",
        "gin": "琴"
    }

    # Check if the folder exists before proceeding
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return config_data  # Return empty dictionary if folder is missing

    # Loop through all items and collect only directories
    for folder_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, folder_name)  # Get full path

        # Ensure it's a folder (not a file)
        if os.path.isdir(full_path):  
            config_data[folder_name] = folder_name  # Store { "item_name": "item_dir" }

    return(config_data)

# Generate the YAML file
directories_path = "../content/zh/items/酒單"
config_data = generate_config_data(directories_path)
generate_hugo_yaml(config_data, "config.yml")
