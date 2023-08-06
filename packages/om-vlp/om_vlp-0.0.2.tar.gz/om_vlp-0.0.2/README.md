# om-vlp

## How to install
```
pip install om-vlp
```

## Download model
```
Wukong ViT-L: https://drive.google.com/file/d/1NHRR_zFD-iJ_OQEmxJq054cobgTkjraC/view?usp=sharing
Wukong Vit-B: https://drive.google.com/file/d/1eM7IggHjMJqguPiGRUyIFP-fFhPl5sJz/view?usp=sharing
```

## Examples
```
from om_vlp.engine import Wukong
X = Wukong(config="om_vlp/configs/wukong_vit_b/wukong_vit_b.py",checkpoint="vit_b.pth")
t = X.texts(["a","b","c"])
i = X.images(["/mnt/soco1/img/ILSVRC/Data/CLS-LOC/val/n01631663/ILSVRC2012_val_00027028.JPEG"])
print (X.sims(i,t))
```
