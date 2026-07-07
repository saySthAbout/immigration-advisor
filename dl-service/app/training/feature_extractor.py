"""사전학습된 MobileNetV3-Small을 고정된 특징 추출기로 사용.

문서 이미지가 MIDV500 원본 클래스별 30장씩(4개국 4클래스, 총 120장)밖에 없어서
CNN을 처음부터 학습시키면 바로 과적합한다 - 대신 ImageNet으로 사전학습된
백본의 마지막 분류층 이전 특징(576차원)만 뽑아서 그 위에 작은 sklearn
분류기를 올린다. easyocr 자체가 이미 PyTorch에 의존하므로 이 방식은
서빙 이미지에 별도 무거운 의존성을 추가하지 않는다.
"""

import torch
from PIL import Image
from torchvision import transforms
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

_weights = MobileNet_V3_Small_Weights.DEFAULT
_model = mobilenet_v3_small(weights=_weights)
_model.classifier = torch.nn.Identity()  # 마지막 분류층 제거 -> 특징 벡터만 출력
_model.eval()

_transform = _weights.transforms()


def extract_features(image: Image.Image) -> list[float]:
    tensor = _transform(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        features = _model(tensor)
    return features.squeeze(0).tolist()
