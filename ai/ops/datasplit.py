import os
import random

def datasplit() -> int:
    # 학습할 데이터 폴더
    train_image_root_path = os.path.join("../data/HumanSegmentationDataset")
    ImageSets_path = train_image_root_path + "/ImageSets"
    
    if not os.path.exists(ImageSets_path):
        os.mkdir(ImageSets_path)
    else:
        if os.path.exists(ImageSets_path+"/train.txt"):
            print("already exisits")
            return 1
        
    # 이미지 데이터와 어노테이션 데이터
    image_list = os.listdir(train_image_root_path + "/Training_Images/")

    # 이미지 이름 불러오기
    image_name = list()
    for image in image_list:
        if image.count(".") == 1:
            name = image.split('.')[0]
            image_name.append(name)
        else:
            for k in range(len(image) - 1, 0, -1):
                if image[k] == '.':
                    image_name.append(image[:k])
                    break

    # 이미지 섞고 train set, test set 나누기
    point = int(len(image_name) * 0.7)

    random.seed(123456)
    random.shuffle(image_name)

    train_image = image_name[:point]
    test_image = image_name[point:]
    with open(ImageSets_path + "/train.txt", 'w') as f:
        for image in train_image:
            f.write(image + "\n")
    f.close()
    
    with open(ImageSets_path + "/test.txt", 'w') as f:
        for image in test_image:
            f.write(image + "\n")
    f.close()
    
    return 0