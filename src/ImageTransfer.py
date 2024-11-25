from .Transfer_module import Transfer_module
from .Segmentation_module import Segmenter
import os, gc, torch
from PIL import Image
import torchvision.transforms as transforms
import numpy as np

# content path 폴더 생성
if not os.path.exists("src/content"):
    os.makedirs("src/content")

class Transfer:
    def __init__(self):
        # 모델 불러오기
        self.transfer = Transfer_module()
        self.segmenter = Segmenter()

    # 이미지 변환 작업
    def processing(self, data:dict):
        '''
        현재 GPU 성능으로 보았을 때 Transfer의 가능한 이미지 크기가 약 HD 정도로 추정
        따라서 필연적으로 target_image보다 화질 저하가 발생한다.
        따라서 변환하는 이미지의 크기는 HD크기를 넘지 않는다.
        
        ==========================================
                         data info
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
        person_transfer_bool = data['person_transfer_bool']
        content_target_image = data['content_target_image']
        content_target_name = data['content_target_name']
        content_source_image = data['content_source_image']
        style_image = data['style_image']
        
        # 텐서 변환
        loader = transforms.Compose([
                    transforms.ToTensor()])
        # PIL 이미지로 변환
        unloader = transforms.ToPILImage()
        print("style image size: ", style_image.size)
        style_image = loader(style_image).unsqueeze(0)
        
        # 오류 발생 시 True로 변함 
        exception = False
        try:
            # 배경이미지를 선택하지 않은 경우
            if content_source_image is None:
                print("content_target_image size: ", content_target_image.size)
                content_image = loader(content_target_image).unsqueeze(0)
                print(content_image.shape, "\n", style_image.shape)
                image = self.transfer.run_style_transfer(content_img=content_image, style_img=style_image, num_steps=300)
                image = unloader(image.squeeze(0))
                
                # 인물 변환
                if person_transfer_bool:
                    mask = self.segmenter.run(content_target_name)
                    reverse_mask = np.where(mask == 0, 1, 0).astype(np.uint8)

                    image = image * reverse_mask
                    content_mask = content_target_image * mask
                    result = image + content_mask
                    
                else:
                    result = np.array(image)

            # 배경 이미지를 선택한 경우
            else:
                mask = self.segmenter.run(content_target_name)
                reverse_mask = np.where(mask == 0, 1, 0).astype(np.uint8)
                content_target_masked = content_target_image * mask
                
                # 인물 변환
                if person_transfer_bool:
                    content_source_image = loader(content_source_image).unsqueeze(0)
                    image = self.transfer.run_style_transfer(content_img=content_source_image, style_img=style_image, num_steps=300)
                    image = unloader(image.squeeze(0))
                    
                    content_source_masked = image * reverse_mask
                    result = content_target_masked + content_source_masked
                else:
                    content_source_masked = content_source_image * reverse_mask
                    content_image = content_target_masked + content_source_masked
                    content_image = loader(Image.fromarray(content_image)).unsqueeze(0)
                    image = self.transfer.run_style_transfer(content_img=content_image, style_img=style_image, num_steps=300)
                    result = np.array(unloader(image.squeeze(0)))
                
            result.astype(np.uint8)
            result = Image.fromarray(result)
            
        except Exception as e:
            exception = True
        
        # 임시로 저장한 이미지 삭제
        if os.path.exists(f'src/content/{content_target_name}'):
            os.remove(f'src/content/{content_target_name}')

        # Garbage collector
        gc.collect()
        torch.cuda.empty_cache()
        
        if exception:
            raise Exception
        
        return result