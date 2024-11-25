from diffusers import StableDiffusionPipeline
import torch

class Generation:
    def __init__(self, model_id = "runwayml/stable-diffusion-v1-5", cuda:bool = False):
        # Diffusion 모델 불러오기
        self.model_id = model_id
        if cuda:
            self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
            self.pipe = self.pipe.to("cuda")
        else:
            self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id)
            self.pipe = self.pipe.to("cpu")
    
    def processing(self, prompt):
        image = self.pipe(prompt).images[0]
        
        return image