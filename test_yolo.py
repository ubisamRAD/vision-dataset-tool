#!/usr/bin/env python3
"""
YOLO 모델 추론 테스트 스크립트

사용법:
  # 단일 이미지 추론
  python3 test_yolo.py --model runs/detect/train/weights/best.pt --source image.jpg

  # 폴더 내 이미지 일괄 추론
  python3 test_yolo.py --model runs/detect/train/weights/best.pt --source frames_video/

  # 결과를 파일로 저장
  python3 test_yolo.py --model runs/detect/train/weights/best.pt --source image.jpg --save
"""

import argparse
import os
import torch
from ultralytics import YOLO


def detect_device(requested: str) -> str:
    """사용 가능한 최적 디바이스를 자동 감지한다."""
    if requested:
        return requested
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return "xpu"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def main():
    parser = argparse.ArgumentParser(description="YOLO 모델 추론 테스트 도구")
    parser.add_argument("--model", type=str, required=True,
                        help="학습된 모델 경로 (.pt)")
    parser.add_argument("--source", type=str, required=True,
                        help="추론할 이미지 또는 폴더 경로")
    parser.add_argument("--conf", type=float, default=0.5,
                        help="신뢰도 임계값 (기본: 0.5)")
    parser.add_argument("--save", action="store_true",
                        help="결과 이미지 저장")
    parser.add_argument("--save-dir", type=str, default="test_results",
                        help="결과 저장 디렉토리 (기본: test_results)")
    parser.add_argument("--device", type=str, default="",
                        help="추론 디바이스 (기본: 자동감지 xpu>cuda>cpu)")
    args = parser.parse_args()

    if not os.path.isfile(args.model):
        print(f"[ERROR] 모델 파일을 찾을 수 없습니다: {args.model}")
        return

    device = detect_device(args.device)

    print(f"[INFO] 모델: {args.model}")
    print(f"[INFO] 소스: {args.source}")
    print(f"[INFO] 디바이스: {device}")
    print(f"[INFO] 신뢰도 임계값: {args.conf}")

    model = YOLO(args.model)
    results = model(args.source, conf=args.conf, device=device, verbose=False)

    total_detections = 0
    for i, r in enumerate(results):
        src_name = os.path.basename(r.path)
        num_det = len(r.boxes)
        total_detections += num_det

        if num_det > 0:
            for box in r.boxes:
                cls = r.names[int(box.cls)]
                conf = float(box.conf)
                xyxy = box.xyxy[0].tolist()
                print(f"  [{src_name}] {cls}: {conf:.2f} "
                      f"at [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}]")
        else:
            print(f"  [{src_name}] no detection")

        if args.save:
            os.makedirs(args.save_dir, exist_ok=True)
            save_path = os.path.join(args.save_dir, f"result_{src_name}")
            r.save(save_path)

    print(f"\n[DONE] {len(results)}장 추론 완료, 총 {total_detections}건 감지")
    if args.save:
        print(f"[INFO] 결과 이미지 저장: {args.save_dir}/")


if __name__ == "__main__":
    main()
