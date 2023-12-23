import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

basePath = sys.argv[1]
extention = sys.argv[2]

# 이미지를 그레이스케일로 읽기
image = cv2.imread(f"{basePath}_original{extention}", cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, dsize=(256, 256))  # 이미지 사이즈를 256x256 픽셀로 조정

# Laplacian을 위한 커널 생성
edge_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])  # Laplacian 커널 정의

# 블러링을 위한 커널 생성
blur_kernel = (
    np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.float32) / 9
)  # 3x3 커널, 요소 값은 1/9로 정규화

# 원본 이미지 표시
fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1x3 서브플롯 생성
axes[0].imshow(image, cmap="gray")  # 첫 번째 서브플롯에 원본 이미지 표시
axes[0].set_title("Original Image")  # 타이틀 설정
axes[0].axis("off")  # 축 숨김

# 이미지 사이즈 조정
new_height, new_width = int(image.shape[0] * 0.5), int(image.shape[1] * 0.5)
resized_image = cv2.resize(image, (new_width, new_height))  # 이미지 크기를 절반으로 조정
cv2.imwrite(f"{basePath}_gray.jpg", resized_image)  # 그레이스케일 이미지 저장


# 필터링 연산을 수행하는 함수
def filtering_animation(image, edge_kernel, blur_kernel):
    edge_output = np.zeros_like(image)  # 출력 이미지를 원본과 같은 크기의 0으로 초기화
    blur_output = np.zeros_like(image)  # 출력 이미지를 원본과 같은 크기의 0으로 초기화
    height, width = image.shape  # 이미지의 높이와 너비 추출

    # 엣지 필터링 애니메이션을 위한 서브플롯 설정
    im_edge = axes[1].imshow(image, cmap="gray")
    axes[1].set_title("Edge Filtering Animation")
    axes[1].axis("off")

    # 블러 필터링 애니메이션을 위한 서브플롯 설정
    im_blur = axes[2].imshow(image, cmap="gray")
    axes[2].set_title("Blur Filtering Animation")
    axes[2].axis("off")

    def update(frame):
        nonlocal edge_output, blur_output
        i, j = divmod(frame, width - len(edge_kernel) + 1)  # 이미지를 순회하기 위한 인덱스 계산

        # 엣지 감지 연산
        window = image[i : i + len(edge_kernel), j : j + len(edge_kernel)]
        edge_output[i, j] = np.sum(window * edge_kernel)

        # 블러링 연산
        blur_window = image[i : i + len(blur_kernel), j : j + len(blur_kernel)]
        blur_output[i, j] = np.sum(blur_window * blur_kernel)

        # 이미지 업데이트
        im_edge.set_array(edge_output)
        im_blur.set_array(blur_output)

        # 이미지 저장
        cv2.imwrite(f"{basePath}_edge.jpg", edge_output)
        cv2.imwrite(f"{basePath}_blur.jpg", blur_output)

    frames = (height - len(edge_kernel) + 1) * (
        width - len(edge_kernel) + 1
    )  # 프레임 수 계산
    anim = FuncAnimation(fig, update, frames=frames, interval=10)  # 애니메이션 생성
    anim.save(f"{basePath}_result.gif", writer="imagemagick")  # 애니메이션 저장


# 함수 호출하여 애니메이션 실행
filtering_animation(resized_image, edge_kernel, blur_kernel)
