admin-panel-generate.py

sections 
categories 

label ? 

UI on pic 

categories-labels-items

files name 

  - name: 'zh-items-beer'
    label: '啤酒'
    folder: 'content/zh/items/酒單/啤酒'
    create: true
    # adding a nested object will show the collection folder structure

    fields: 
      - { label: '品項標題', name: 'title', widget: 'string' }
      - { label: '價格', name: 'price', widget: 'list' }
      - { label: '副標題簡介描述', name: 'description', widget: 'string',required: false }
      - { label: '未上架', name: 'draft', widget: 'boolean', default: false}
      - { label: '上架順序', name: 'weight', widget: 'number', default: 10}
      - { label: '照片', name: 'image', widget: 'image', media_folder: '../../../../../static/images', public_folder: 'images' ,required: false }
      - { label: '文字', name: 'body', widget: 'string' }
      - { label: '種類', name: 'categories', widget: 'list', required: false }
      - { label: '標籤', name: 'tags', widget: 'list', required: false }
      - { label: '發布日期', name: 'date', widget: 'datetime' }
    # adding a meta object with a path property allows editing the path of entries
    # moving an existing entry will move the entire sub tree of the entry to the new location
