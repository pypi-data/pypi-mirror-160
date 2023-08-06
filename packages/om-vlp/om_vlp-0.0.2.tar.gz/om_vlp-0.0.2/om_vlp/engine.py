#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import mmcv
import torch
from om_vlp.model.utils import token_wise_similarity
from torchvision.datasets.folder import pil_loader
from .tokenizer import SimpleTokenizer
from torchvision.transforms import (
    Resize,
    CenterCrop,
    ToTensor,
    Normalize,
    InterpolationMode,
    Compose,
)
from om_vlp.model.builder import build_model

class Wukong(object):
    def __init__(self, config, checkpoint):
        self.config = mmcv.Config.fromfile(config)
        self.config.model.pretrained = checkpoint
        self.model = build_model(self.config.model).cuda()
        self.model.eval()
        self.input_resolution = self.model.visual.input_resolution
        self.transform = self.img_transform(self.model.visual.input_resolution)
        self.tokenizer = SimpleTokenizer()
        self.loader = pil_loader
    
    def img_transform(self, n_px):
        mean = (0.48145466, 0.4578275, 0.40821073)
        std = (0.26862954, 0.26130258, 0.27577711)
        transform = [
            Resize(n_px, interpolation=InterpolationMode.BICUBIC),
            CenterCrop(n_px),
            lambda img: img.convert("RGB"),
            ToTensor(),
            Normalize(mean, std),
        ]
        return Compose(transform)

    @torch.no_grad()
    def texts(self, texts):
        texts = self.tokenizer.tokenize(texts).cuda()
        text_batch_size = 1024
        text_features = []

        for i in range((len(texts) // text_batch_size) + 1):
            text = texts[i * text_batch_size: (i + 1) * text_batch_size]
            if len(text):
                text_features_ = self.model.encode_text(text)
                text_features_ = self.model.process_text_features(text_features_, text)
                text_features.append(text_features_)
        text_features = torch.cat(text_features)
        return text_features

    def images(self, imgs):
        image_features = self.model.encode_image(torch.stack([self.transform(self.loader(x)).cuda() for x in imgs]))
        image_features = self.model.process_img_features(image_features)
        return image_features
 
    def sims(self, image_features, text_features):
        logits = token_wise_similarity(image_features, text_features).softmax(dim=-1)
        return logits



if __name__ == "__main__":
    X = Wukong(config="configs/wukong_vit_b/wukong_vit_b.py",checkpoint="vit_b.pth")
    t = X.texts(["a","b","c"])
    i = X.images(["/mnt/soco1/img/ILSVRC/Data/CLS-LOC/val/n01631663/ILSVRC2012_val_00027028.JPEG"])
    print (i.shape)
    print (t.shape)
    print (X.sims(i,t))


