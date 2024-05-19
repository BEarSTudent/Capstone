from src import *
from flask import Flask, request
import json
import base64
from io import BytesIO
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import cv2
import os
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def save_image():
    if request.method == 'POST':
        # json 형식으로 요청해야한다.
        json_data = request.get_json()
        dict_data = json.loads(json.dumps(json_data))
        
        '''
        ==========================================
                        json info
        ==========================================
        person_transfer_bool *  : 인물 포함 이미지 변환을 요청했는지 유무. True = 인물포함 변환. False = 인물 제외 변환.
        encoding_type *         : 이미지 encoding 형식. ex).jpg, .png
        content_target_name *   : 최종적으로 유저가 이미지 변환을 요구하는 이미지
        content_target_image *  : 위의 이미지 데이터
        content_source_name     : 유저가 배경화면과 content_target_image와의 합성을 원했을 경우. None에서 이미지 이름을 받아온다
        content_source_image    : 위의 이미지 데이터
        style_name *            : 변환할 스타일 이미지 이름
        style_image *           : 위의 이미지 데이터
        
            * : 값이 항상 존재해야한다는 의미
        '''
        person_transfer_bool = dict_data['segmentation']
        encoding_type = dict_data['encoding_type']
        content_target_name = dict_data['content_target_name']
        content_target_image = dict_data['content_target_image']
        content_target_image = Image.open(BytesIO(base64.b64encode(content_target_image)))
        
        hd_width = 1280
        # 타겟 이미지 크기 추출
        width, height = content_target_image.size
        if width < height:
            decay_rate = round(hd_width/height, 2)
        else:
            decay_rate = round(hd_width/width, 2)
        
        # FHD보다 이미지가 작거나 같은 경우
        if decay_rate >= 1 :
            decay_rate = 1    
        width, height = int(width * decay_rate), int(height * decay_rate)
        
        # 이미지 크기 변환
        content_target_image = content_target_image.resize((width, height))
        content_target_image.save(f"{content_path}{content_target_name}")
        
        content_source_name = dict_data['content_source_name']
        content_source_image = None
        # 유저가 이미지와 배경화면 합성을 요구한 경우
        if type(content_source_name) is str:
            content_source_image = dict_data['content_source_image']
            content_source_image = Image.open(BytesIO(base64.b64encode(content_source_image)))
            content_source_image = content_source_image.resize((width, height))
            content_source_image.save(f'{content_path}{content_source_name}')
            
        # select, dall_e, custom
        style_image = dict_data['style_image']
        # 제공하는 스타일을 적용하는 경우
        if style_image == "":
            style_name = dict_data['style_name']
            style_image = Image.open(f'{style_path}{style_name}')
        # 커스텀 이미지(DALL-E, User Image)를 이용하는 경우
        else:
            style_image = Image.open(BytesIO(base64.b64encode(style_image)))
        style_image = style_image.resize(((width, height)))
        # 배경이미지을 넣지 않은 경우
        if content_source_image is None:
            return processing(encoding_type, person_transfer_bool, 
                              content_target_image, content_target_name, style_image)
        # 배경이미지을 넣은 경우
        else:
            return processing(encoding_type, person_transfer_bool, 
                              content_target_image, content_target_name, style_image, 
                              content_source_image, content_source_name)

# 이미지 변환 작업
def processing(encoding_type:str, person_transfer_bool:bool, 
               content_target_image:Image, content_target_name:str, 
               style_image:Image, content_source_image=None,content_source_name=None):
    '''
    현재 GPU 성능으로 보았을 때 Transfer의 가능한 이미지 크기가 약 HD 정도로 추정
    따라서 필연적으로 target_image보다 화질 저하가 발생한다.
    따라서 변환하는 이미지의 크기는 HD크기를 넘지 않는다.
    '''
    # 텐서 변환
    loader = transforms.Compose([
                transforms.ToTensor()])
    # PIL 이미지로 변환
    unloader = transforms.ToPILImage()
    style_image = loader(style_image).unsqueeze(0)
    # 배경이미지를 선택하지 않은 경우
    if content_source_image is None:
        content_image = loader(content_target_image).unsqueeze(0)
        image = transfer.run_style_transfer(content_img=content_image, style_img=style_image)
        image = unloader(image.squeeze(0))
        
        # 인물 변환
        if person_transfer_bool:
            result = image 
        else:
            mask = segmenter.run(content_target_name)
            reverse_mask = np.where(mask == 0, 1, 0).astype(np.uint8)

            image = image * reverse_mask
            content_mask = content_target_image * mask
            result = image + content_mask

    # 배경 이미지를 선택한 경우
    else:
        mask = segmenter.run(content_source_name)
        reverse_mask = np.where(mask == 0, 1, 0).astype(np.uint8)
        
        # 인물 변환
        if person_transfer_bool:
            content_target_masked = content_target_image * reverse_mask
            content_source_masked = content_source_image * mask
            content_image = content_target_masked + content_source_masked
            content_image = loader(Image.fromarray(content_image)).unsqueeze(0)
            image = transfer.run_style_transfer(content_img=content_image, style_img=style_image)
            result = unloader(image.squeeze(0))
            
        else:
            content_target_image = loader(content_target_image).unsqueeze(0)
            image = transfer.run_style_transfer(content_img=content_image, style_img=style_image)
            image = unloader(image.squeeze(0))
            
            image = image * reverse_mask
            content_mask = content_target_image * mask
            result = image + content_mask
    
    result.astype(np.uint8)
    # result = Image.fromarray(result.astype(np.uint8))
    # result.save(f"./data/result/result_{content_target_name}")
    
    _, result = cv2.imencode(encoding_type, result)
    b64_string = base64.b64decode(result).decode('utf-8')
    file = {"img:": b64_string}
    return file
    
if __name__ == "__main__":
    content_path = parent_path + "/data/content/"
    style_path = parent_path + "/data/style/"
    transfer = Transfer()
    segmenter = Segmenter()
    
    app.run(host='0.0.0.0', port=2120, debug=True)