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
    
    for item_name, item_label in config_data.items():
        section = f"""
  - name: 'zh-about-{item_name}'
    label: '{item_label}'
    folder: 'content/zh/{item_name}'
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
config_data = {
    "item_name": "item_label",
    "history": "歷史",
    "values": "核心價值"
}

# Generate the YAML file
generate_hugo_yaml(config_data, "config.yml")
