# Vision Dataset Tool

웹캠으로 물체를 촬영하고, 프레임을 추출한 뒤, Roboflow에서 라벨링하고, YOLO 모델을 학습하는 도구입니다.

---

## 목차

1. [전체 흐름](#전체-흐름)
2. [사전 준비](#사전-준비)
3. [Step 1: 웹캠으로 물체 영상 촬영 (Windows)](#step-1-웹캠으로-물체-영상-촬영-windows)
4. [Step 2: 영상에서 프레임(이미지) 추출 (Windows)](#step-2-영상에서-프레임이미지-추출-windows)
5. [Step 3: Roboflow에 이미지 업로드 및 라벨링](#step-3-roboflow에-이미지-업로드-및-라벨링)
6. [Step 4: 데이터셋 다운로드 (Linux/WSL2)](#step-4-데이터셋-다운로드-linuxwsl2)
7. [Step 5: YOLO 모델 학습 (Linux/WSL2)](#step-5-yolo-모델-학습-linuxwsl2)
8. [Step 6: 모델 추론 테스트 (Linux/WSL2)](#step-6-모델-추론-테스트-linuxwsl2)
9. [파일 구조](#파일-구조)
10. [문제 해결](#문제-해결)

---

## 전체 흐름

```
[Windows]  Step 1. 웹캠으로 물체 영상 촬영        ← capture_video.py
[Windows]  Step 2. 영상에서 프레임(이미지) 추출     ← extract_frames.py
[브라우저]  Step 3. Roboflow에 이미지 업로드 및 라벨링
[Linux]    Step 4. Roboflow에서 데이터셋 다운로드
[Linux]    Step 5. YOLO 모델 학습                  ← train_yolo.py
[Linux]    Step 6. 모델 추론 테스트                 ← test_yolo.py
```

> **왜 Windows와 Linux를 나눠서 사용하나요?**
> - **Windows**: 노트북 웹캠에 직접 접근 가능하고, Roboflow에 이미지를 드래그 앤 드롭으로 업로드하기 편합니다.
> - **Linux/WSL2**: ROS 2 Humble 환경(Python 3.10)에서 YOLO 모델을 학습하고 로봇 패키지와 함께 사용합니다.
> - 학습된 모델(`.pt` 파일)은 **OS에 무관하게** 어디서든 사용 가능합니다.

---

## 사전 준비

### 1. Windows에 Python 설치

ROS 2 Humble과 동일한 Python 3.10 버전을 설치합니다.

1. 아래 링크에서 **Windows installer (64-bit)** 를 다운로드합니다.
   - https://www.python.org/downloads/release/python-31011/
   - 페이지 맨 아래 **Files** 섹션에서 `Windows installer (64-bit)` 클릭

2. 설치 프로그램을 실행합니다.
   - **중요: 반드시 "Add python.exe to PATH" 체크박스를 선택하세요!**
   - 체크하지 않으면 터미널에서 `python` 명령이 동작하지 않습니다.
   - `Install Now` 클릭

3. 설치 확인 — **PowerShell을 새로 열고** 아래 명령을 실행합니다:
   ```powershell
   python --version
   ```
   `Python 3.10.11` 이 출력되면 성공입니다.

   > **만약 다른 Python 버전이 나온다면:**
   > 여러 버전이 설치된 경우 `py -3.10 --version`으로 확인하고,
   > 기본 버전을 변경하려면 `setx PY_PYTHON 3.10` 실행 후 PowerShell을 재시작하세요.

4. OpenCV 설치:
   ```powershell
   pip install opencv-python
   ```

### 2. Linux/WSL2에 패키지 설치

WSL2 터미널에서:

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install opencv-python ultralytics roboflow
```

> **torch 호환성 에러가 발생하면:**
> ```bash
> pip install --force-reinstall torch torchvision
> ```

### 3. 이 저장소 클론

```bash
# Linux/WSL2에서
git clone <이 저장소 URL>
cd vision_dataset_tool
```

Windows 바탕화면에도 복사해두면 촬영/추출이 편합니다:
```powershell
# PowerShell에서
copy -Recurse \\wsl$\Ubuntu\home\<사용자명>\vision_dataset_tool C:\Users\<사용자명>\Desktop\vision_dataset_tool
```

### 4. Roboflow 계정 생성

1. https://roboflow.com 접속
2. **Sign Up** 클릭 → Google 계정 또는 이메일로 가입 (무료)
3. 가입 후 **Settings** → **API Key** 를 메모해 둡니다 (Step 4에서 사용)

---

## Step 1: 웹캠으로 물체 영상 촬영 (Windows)

### 1-1. 스크립트 실행

Windows PowerShell을 열고:

```powershell
cd C:\Users\<사용자명>\Desktop\vision_dataset_tool
python capture_video.py
```

실행하면 웹캠 미리보기 창이 뜹니다.

### 1-2. 녹화

| 키 | 동작 |
|----|------|
| `s` | 녹화 시작 / 중지 (토글) |
| `q` | 프로그램 종료 |

1. 웹캠 미리보기 창이 뜨면, 인식하고 싶은 **물체를 손에 들고** 카메라 앞에 위치시킵니다.
2. `s` 키를 눌러 **녹화를 시작**합니다 — 화면 왼쪽 위에 빨간 `REC` 표시가 나타납니다.
3. 물체를 **천천히 움직이면서** 10~30초간 촬영합니다.
4. `s` 키를 눌러 **녹화를 중지**합니다.
5. 영상을 더 찍고 싶으면 `s`를 다시 눌러 추가 녹화합니다.
6. 모든 촬영이 끝나면 `q` 키로 종료합니다.

녹화된 영상은 `output\` 폴더에 `video_YYYYMMDD_HHMMSS.mp4` 형식으로 저장됩니다.

### 1-3. 좋은 데이터셋을 위한 촬영 팁

YOLO 모델의 성능은 **학습 데이터의 품질**에 크게 좌우됩니다. 아래 팁을 따르면 더 좋은 모델을 만들 수 있습니다.

| 팁 | 설명 |
|----|------|
| **다양한 각도** | 물체를 천천히 회전시키며 촬영 (위, 아래, 옆, 대각선) |
| **다양한 거리** | 카메라에 가까이/멀리 이동하며 촬영 |
| **다양한 배경** | 2~3가지 다른 배경 (책상, 바닥, 벽 앞 등) |
| **다양한 조명** | 밝은 곳, 어두운 곳에서 각각 촬영 |
| **짧은 영상 여러 개** | 5분짜리 1개보다 10~30초짜리 여러 개가 좋음 |
| **최소 100장 이상** | 추출 후 이미지 100장 이상을 목표로 촬영 |

### 1-4. 옵션

```powershell
# 외장 웹캠 사용 (기본 카메라가 아닌 경우)
python capture_video.py --camera 1

# 해상도 변경 (기본: 640x480)
python capture_video.py --width 1280 --height 720

# FPS 변경 (기본: 30)
python capture_video.py --fps 15
```

---

## Step 2: 영상에서 프레임(이미지) 추출 (Windows)

### 2-1. 촬영된 영상 확인

```powershell
dir output
```

출력 예시:
```
video_20260313_153441.mp4
video_20260313_154012.mp4
```

### 2-2. 프레임 추출 실행

```powershell
python extract_frames.py output\video_20260313_153441.mp4
```

출력 예시:
```
[INFO] 영상 정보: 640x480, 30.0fps, 660프레임, 22.0초
[INFO] 10프레임 간격으로 추출 → 약 66장 예상
  ... 50장 저장 완료

[DONE] 총 66장 저장 → frames_video_20260313_153441/
[TIP] Roboflow에 업로드할 준비가 되었습니다!
```

추출된 이미지는 `frames_video_20260313_153441\` 폴더에 저장됩니다.

### 2-3. 옵션

```powershell
# 5프레임마다 1장 추출 (더 많은 이미지 — 기본: 10)
python extract_frames.py output\video_20260313_153441.mp4 --interval 5

# 최대 200장까지만 추출
python extract_frames.py output\video_20260313_153441.mp4 --interval 5 --max-frames 200

# 640x640으로 리사이즈 (YOLO 입력 크기에 맞춤)
python extract_frames.py output\video_20260313_153441.mp4 --resize 640x640

# PNG 포맷으로 저장 (기본: JPG)
python extract_frames.py output\video_20260313_153441.mp4 --format png
```

### 2-4. 추출 장수 가이드

| 목적 | 권장 이미지 수 | `--interval` 설정 |
|------|---------------|-------------------|
| 빠른 테스트 | 50~100장 | 15~20 |
| 기본 학습 | 150~300장 | 5~10 |
| 고품질 학습 | 500장 이상 | 3~5 |

> **이미지가 너무 적으면?** 모델이 제대로 학습되지 않습니다. **최소 100장 이상**을 권장합니다.
> 10장으로도 동작은 하지만, 중복 감지나 미감지가 발생할 수 있습니다.

---

## Step 3: Roboflow에 이미지 업로드 및 라벨링

### 3-1. 프로젝트 생성

1. https://roboflow.com 에 로그인합니다.
2. 왼쪽 메뉴에서 **Projects** 탭을 클릭합니다.
3. **New Project** 를 클릭합니다.
4. 아래와 같이 설정합니다:
   - **Project Name**: 원하는 이름 입력 (예: `find-bottles`)
   - **Project Type**: `Object Detection` 선택
     - 세그멘테이션이 필요하면 `Instance Segmentation` 선택
   - **What are you detecting?**: 감지할 물체 이름 입력 (예: `bottle`)
5. **Create Project** 클릭

### 3-2. 이미지 업로드

1. 프로젝트에 들어가면 이미지 업로드 화면이 나타납니다.
2. Windows 파일 탐색기에서 `frames_video_...\` 폴더를 열고 이미지를 **드래그 앤 드롭**합니다.
3. **무료 플랜은 한 번에 10장 제한**이므로 여러 번 나눠서 업로드합니다.
4. 업로드가 완료될 때까지 기다립니다.

### 3-3. 라벨링 (Annotation)

모델이 "이게 어떤 물체인지" 배우려면, 각 이미지에서 **물체의 위치를 표시**해줘야 합니다.

#### 수동 라벨링

1. 업로드된 이미지를 클릭하면 라벨링 도구가 열립니다.
2. 왼쪽 도구에서 **Bounding Box** (사각형) 도구를 선택합니다.
3. 이미지에서 물체를 **드래그하여 사각형으로 감쌉니다**.
4. 클래스 이름을 입력합니다 (예: `bottle`).
5. **Save** 를 클릭하고 다음 이미지로 넘어갑니다.
6. 모든 이미지에 대해 반복합니다.

#### 자동 라벨링 (Auto-Label)

Roboflow의 Auto-Label 기능을 사용하면 자동으로 라벨링할 수 있습니다.

1. 이미지 목록에서 **Auto-Label** 또는 **Run on all images** 버튼을 클릭합니다.
2. 자동 라벨링이 완료되면 결과를 확인합니다.
3. 잘못된 라벨이 있으면 수동으로 수정합니다.

> **주의**: Auto-Label은 Roboflow **Rapid** 모델을 사용합니다.
> Rapid 모델은 `.pt` 파일로 추출할 수 없으므로, 자체 모델이 필요하면 **Step 5에서 직접 학습**해야 합니다.

### 3-4. 데이터셋 버전 생성

라벨링이 완료되면 데이터셋 버전을 생성합니다.

1. 프로젝트 페이지에서 **Generate** 탭으로 이동합니다.
2. 설정:
   - **Train/Valid/Test Split**: 70% / 20% / 10% (권장)
   - **Preprocessing**:
     - Auto-Orient: 켜기
     - Resize: 640x640
   - **Augmentation** (데이터 증강, 선택):
     - Flip: Horizontal
     - Rotation: ±15°
     - Brightness: ±15%
3. **Generate** 를 클릭합니다.

> **Augmentation이란?** 원본 이미지를 회전, 반전, 밝기 조절 등으로 변형하여
> 학습 데이터를 늘리는 기법입니다. 이미지 수가 적을 때 특히 효과적입니다.

---

## Step 4: 데이터셋 다운로드 (Linux/WSL2)

여기서부터는 **WSL2 터미널**에서 진행합니다.

### 4-1. Roboflow API Key 확인

1. Roboflow 웹사이트 → **Settings** (왼쪽 하단 톱니바퀴) → **API Key**
2. API Key를 복사합니다.

### 4-2. 워크스페이스/프로젝트 정보 확인

Roboflow 웹에서 프로젝트 URL을 확인합니다. URL 형식:
```
https://app.roboflow.com/<워크스페이스>/<프로젝트>/<버전>
```

예시: `https://app.roboflow.com/my-workspace/find-bottles/1`
- 워크스페이스: `my-workspace`
- 프로젝트: `find-bottles`
- 버전: `1`

### 4-3. 데이터셋 다운로드

```bash
cd ~/vision_dataset_tool

python3 << 'EOF'
from roboflow import Roboflow

# 아래 값을 본인 정보로 변경하세요
API_KEY = "YOUR_API_KEY"           # Roboflow API Key
WORKSPACE = "YOUR_WORKSPACE"       # 워크스페이스 이름
PROJECT = "YOUR_PROJECT"           # 프로젝트 이름
VERSION = 1                        # 버전 번호

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)
version = project.version(VERSION)
dataset = version.download("yolov8")

print(f"\n다운로드 완료: {dataset.location}")
print(f"data.yaml 경로: {dataset.location}/data.yaml")
EOF
```

다운로드가 완료되면 아래와 같은 폴더 구조가 생성됩니다:

```
<프로젝트이름>-<버전>/
├── data.yaml          ← 학습에 필요한 설정 파일
├── train/
│   ├── images/        ← 학습용 이미지
│   └── labels/        ← 학습용 라벨
├── valid/
│   ├── images/        ← 검증용 이미지
│   └── labels/        ← 검증용 라벨
└── test/
    ├── images/        ← 테스트용 이미지
    └── labels/        ← 테스트용 라벨
```

---

## Step 5: YOLO 모델 학습 (Linux/WSL2)

### 5-1. 학습 실행

```bash
cd ~/vision_dataset_tool

# 학습 스크립트 사용 (권장)
python3 train_yolo.py --data <다운로드된 폴더>/data.yaml --epochs 100
```

실제 예시:
```bash
python3 train_yolo.py --data Find-bottles-2-2/data.yaml --epochs 100
```

### 5-2. 학습 옵션

| 옵션 | 설명 | 기본값 | 권장값 |
|------|------|--------|--------|
| `--data` | data.yaml 경로 | (필수) | - |
| `--epochs` | 학습 반복 횟수 | 100 | 이미지 100장 이하: 150, 이상: 100 |
| `--batch` | 배치 크기 | 16 | 메모리 부족 시 4 또는 8 |
| `--imgsz` | 입력 이미지 크기 | 640 | 640 |
| `--model` | 베이스 모델 | yolov8n.pt | 아래 표 참고 |
| `--task` | detect 또는 segment | detect | 프로젝트 타입에 맞춰 선택 |
| `--name` | 실험 이름 | 자동 | 구분이 필요할 때 지정 |

#### 베이스 모델 선택 가이드

| 모델 | 크기 | 속도 | 정확도 | 용도 |
|------|------|------|--------|------|
| `yolov8n.pt` | 6MB | 가장 빠름 | 보통 | 임베디드/실시간 |
| `yolov8s.pt` | 22MB | 빠름 | 좋음 | 일반 용도 (권장) |
| `yolov8m.pt` | 50MB | 보통 | 높음 | 정확도 중시 |
| `yolov8l.pt` | 84MB | 느림 | 매우 높음 | 고성능 GPU 환경 |

> **CPU에서 학습하는 경우**: `yolov8n.pt` (nano)를 사용하세요. 다른 모델은 너무 느립니다.
> GPU가 있으면 `yolov8s.pt` 이상을 권장합니다.

### 5-3. 학습 결과 확인

학습이 완료되면 아래 경로에 결과가 저장됩니다:

```
runs/detect/train/
├── weights/
│   ├── best.pt        ← 가장 성능 좋은 모델 (이걸 사용)
│   └── last.pt        ← 마지막 에포크 모델
├── results.png        ← 학습 그래프
├── confusion_matrix.png
└── ...
```

### 5-4. 학습 결과 해석

학습 로그 마지막에 출력되는 지표:

| 지표 | 의미 | 좋은 값 |
|------|------|---------|
| **mAP50** | IoU 50% 기준 평균 정밀도 | 0.9 이상 |
| **mAP50-95** | IoU 50~95% 기준 평균 정밀도 | 0.7 이상 |
| **Precision** | 감지한 것 중 실제 맞는 비율 | 0.8 이상 |
| **Recall** | 실제 물체 중 감지된 비율 | 0.8 이상 |

> **성능이 낮으면?**
> - 이미지 수를 늘리세요 (가장 효과적)
> - 다양한 각도/배경/조명으로 촬영하세요
> - Augmentation을 추가하세요
> - epoch 수를 늘리세요

---

## Step 6: 모델 추론 테스트 (Linux/WSL2)

### 6-1. 스크립트로 테스트

```bash
# 단일 이미지 추론
python3 test_yolo.py --model runs/detect/train/weights/best.pt --source test_image.jpg

# 폴더 내 이미지 일괄 추론
python3 test_yolo.py --model runs/detect/train/weights/best.pt --source frames_video_20260313_153441/

# 결과 이미지 저장 (test_results/ 폴더에 감지 결과가 그려진 이미지 저장)
python3 test_yolo.py --model runs/detect/train/weights/best.pt --source test_image.jpg --save

# 신뢰도 임계값 변경 (기본: 0.5)
python3 test_yolo.py --model runs/detect/train/weights/best.pt --source test_image.jpg --conf 0.3
```

출력 예시:
```
[INFO] 모델: runs/detect/train/weights/best.pt
[INFO] 소스: frames_video_20260313_153441/
[INFO] 신뢰도 임계값: 0.5
  [frame_00000.jpg] bottle: 1.00 at [510, 230, 595, 467]
  [frame_00005.jpg] bottle: 1.00 at [488, 215, 580, 472]
  [frame_00010.jpg] bottle: 0.97 at [420, 198, 512, 450]
  ...

[DONE] 66장 추론 완료, 총 66건 감지
```

### 6-2. Python 코드에서 직접 사용

```python
from ultralytics import YOLO

# 모델 로드
model = YOLO("runs/detect/train/weights/best.pt")

# 이미지 추론
results = model("test_image.jpg", conf=0.5)

# 결과 확인
for box in results[0].boxes:
    class_name = results[0].names[int(box.cls)]  # 클래스 이름 (예: "bottle")
    confidence = float(box.conf)                   # 신뢰도 (0~1)
    x1, y1, x2, y2 = box.xyxy[0].tolist()        # 바운딩 박스 좌표
    print(f"{class_name}: {confidence:.2f} at [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")

# 결과 이미지 저장
results[0].save("result.jpg")

# 결과 이미지 표시 (GUI 환경 필요)
results[0].show()
```

### 6-3. ROS 2에서 사용하기

학습된 `.pt` 파일은 ROS 2 패키지에서 바로 사용할 수 있습니다:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO


class YoloDetectorNode(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.model = YOLO('/path/to/best.pt')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        results = self.model(cv_image, conf=0.5, verbose=False)
        for box in results[0].boxes:
            cls = results[0].names[int(box.cls)]
            conf = float(box.conf)
            self.get_logger().info(f'Detected {cls}: {conf:.2f}')
```

---

## 파일 구조

```
vision_dataset_tool/
├── capture_video.py      # [Windows] 웹캠 영상 촬영
├── extract_frames.py     # [Windows] 영상 → 이미지 프레임 추출
├── train_yolo.py         # [Linux]   YOLO 모델 학습
├── test_yolo.py          # [Linux]   YOLO 모델 추론 테스트
├── requirements.txt      # Python 패키지 의존성
├── README.md             # 이 문서
├── .gitignore
│
├── output/               # (git 제외) 촬영된 영상
├── frames_*/             # (git 제외) 추출된 이미지
└── runs/                 # (git 제외) 학습 결과
    └── detect/train/weights/
        └── best.pt       # 학습된 모델
```

---

## 문제 해결

### 환경 설정

| 문제 | 원인 | 해결 |
|------|------|------|
| `python`이 안 됨 (Windows) | PATH 미등록 | Python 재설치 시 "Add to PATH" 체크. 또는 `py`, `python3`으로 시도 |
| 여러 Python 버전이 충돌 | py launcher 기본 버전 불일치 | `setx PY_PYTHON 3.10` 실행 후 PowerShell 재시작 |
| `pip install` 에러 | pip 버전 낮음 | `python -m pip install --upgrade pip` |
| torch 호환성 에러 | torch/torchvision 버전 불일치 | `pip install --force-reinstall torch torchvision` |

### 촬영 및 추출

| 문제 | 원인 | 해결 |
|------|------|------|
| 카메라가 안 열림 (WSL2) | WSL2에서 웹캠 직접 접근 불가 | Windows에서 촬영 스크립트 실행 |
| 카메라가 안 열림 (Windows) | 다른 앱이 카메라 점유 중 | 카메라 사용 중인 앱 종료 후 재시도. `--camera 1` 시도 |
| 추출 이미지가 너무 비슷함 | interval이 너무 작음 | `--interval`을 높이기 (10~20) |
| 추출 이미지가 흐림 | 빠르게 움직여서 모션 블러 발생 | 촬영 시 물체를 천천히 움직이기 |

### Roboflow

| 문제 | 원인 | 해결 |
|------|------|------|
| 한 번에 10장만 업로드 가능 | 무료 플랜 제한 | 여러 번 나눠서 업로드 |
| `.pt` 파일 다운로드 안 됨 | Rapid 모델은 추출 불가 | 데이터셋 export 후 로컬에서 학습 (Step 5) |
| 데이터셋 버전이 없음 | Generate를 아직 안 함 | Roboflow에서 데이터셋 버전 생성 필요 |

### 학습 및 추론

| 문제 | 원인 | 해결 |
|------|------|------|
| 학습이 너무 느림 | CPU 학습 + 큰 모델 | `yolov8n.pt` (nano) 사용, batch 크기 줄이기 |
| 감지를 아예 못 함 | 학습 데이터 부족 | 이미지 수 늘리기 (최소 100장), epoch 늘리기 |
| 중복 감지 (같은 물체 여러 번) | 학습 데이터 부족 또는 conf 낮음 | `--conf 0.5` 이상으로 올리기, 이미지 추가 |
| 엉뚱한 것을 감지 (False Positive) | 학습 데이터 다양성 부족 | 다양한 배경/조명에서 촬영, augmentation 추가 |
| Linux에서 `.pt` 로드 에러 | ultralytics 버전 불일치 | `pip install ultralytics --upgrade` |
