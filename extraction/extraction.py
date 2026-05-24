import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import cv2

class Extraction:
    def __init__(self):
        base_model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.feature_extractor = nn.Sequential(*list(base_model.children())[:-1])
        self.feature_extractor.eval()

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def feature(self, file_path: str) -> list[float]:
        """
        소의 특징값을 추출합니다.
        :param file_path: 사진이 저장된 위치입니다.
        :return: 소의 특징에 대한 백터값을 list[float] 형식으로 반환합니다.
        """
        img_bgr = cv2.imread(str(file_path))
        if img_bgr is None:
            raise FileNotFoundError(f"⚠️ 이미지를 로드할 수 없습니다: {file_path}")

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        tensor_img = self.transform(pil_img).unsqueeze(0)

        with torch.no_grad():
            features = self.feature_extractor(tensor_img)
            result =  torch.flatten(features, start_dim=1).squeeze(0).numpy()
            return result.astype(float).tolist()
