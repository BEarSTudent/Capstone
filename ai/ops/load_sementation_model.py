import mmcv
from mmseg.apis import inference_segmentor, init_segmentor, show_result_pyplot
from mmseg.core.evaluation import get_palette
from mmcv.runner import load_checkpoint
from mmseg.core import get_classes
import cv2
import os.path as osp

def main():
    pretrain_weight = "segmentation/released/upernet_augreg_adapter_base_512_160k_ade20k.pth.tar"
    configs = "segmentation/configs/ade20k/upernet_augreg_adapter_base_512_160k_ade20k.py"
    palette = "ade20k"
    checkpoint = "checkpoint"
    
    model = init_segmentor(configs, checkpoint=None, device='cuda:0')
    checkpoint = load_checkpoint(model, checkpoint, map_location='cpu')
    if 'CLASSES' in checkpoint.get('meta', {}):
        model.CLASSES = checkpoint['meta']['CLASSES']
    else:
        model.CLASSES = get_classes(palette)
    
    return model

if __name__ == '__main__':
    main()