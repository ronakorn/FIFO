import json
from pathlib import Path
root=Path('/home/user/fifo-wealth-os-web/messages')
for locale in ('en','th'):
    target=root/f'{locale}.json'
    data=json.loads(target.read_text(encoding='utf-8'))
    for patch_name in ('core','advanced','upload'):
        patch=json.loads((Path('/home/user')/f'patch_{patch_name}_{locale}.json').read_text(encoding='utf-8'))
        def merge(base, extra):
            for key,value in extra.items():
                if key in base and isinstance(base[key],dict) and isinstance(value,dict): merge(base[key],value)
                else: base[key]=value
        merge(data,patch)
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('merged locale patches')