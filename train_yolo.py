#!/usr/bin/env python3
"""
YOLO 모델 학습 스크립트

사용법:
  # 기본 학습 (detect)
  python3 train_yolo.py --data Find-bottles-2-2/data.yaml

  # 세그멘테이션 학습
  python3 train_yolo.py --data pen_dataset/data.yaml --task segment

  # 상세 옵션
  python3 train_yolo.py --data dataset/data.yaml --epochs 100 --batch 8 --model yolov8s.pt
"""

import argparse
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
    parser = argparse.ArgumentParser(description="YOLO 모델 학습 도구")
    parser.add_argument("--data", type=str, required=True,
                        help="데이터셋 data.yaml 경로")
    parser.add_argument("--task", type=str, default="detect",
                        choices=["detect", "segment"],
                        help="학습 태스크 (기본: detect)")
    parser.add_argument("--model", type=str, default="",
                        help="베이스 모델 (기본: detect=yolov8n.pt, segment=yolov8n-seg.pt)")
    parser.add_argument("--epochs", type=int, default=100,
                        help="학습 에포크 수 (기본: 100)")
    parser.add_argument("--imgsz", type=int, default=640,
                        help="이미지 크기 (기본: 640)")
    parser.add_argument("--batch", type=int, default=16,
                        help="배치 크기 (기본: 16)")
    parser.add_argument("--name", type=str, default="",
                        help="학습 실험 이름 (기본: 자동)")
    parser.add_argument("--device", type=str, default="",
                        help="학습 디바이스 (기본: 자동감지 xpu>cuda>cpu)")
    args = parser.parse_args()

    # 기본 모델 설정
    if not args.model:
        if args.task == "segment":
            args.model = "yolov8n-seg.pt"
        else:
            args.model = "yolov8n.pt"

    device = detect_device(args.device)

    print(f"[INFO] 태스크: {args.task}")
    print(f"[INFO] 모델: {args.model}")
    print(f"[INFO] 데이터: {args.data}")
    print(f"[INFO] 디바이스: {device}")
    print(f"[INFO] 에포크: {args.epochs}, 이미지 크기: {args.imgsz}, 배치: {args.batch}")

    model = YOLO(args.model)

    train_args = {
        "data": args.data,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": device,
    }

    if args.name:
        train_args["name"] = args.name

    results = model.train(**train_args)

    print(f"\n[DONE] 학습 완료!")
    print(f"[INFO] best 모델: {model.trainer.best}")
    print(f"[INFO] 결과 디렉토리: {model.trainer.save_dir}")


if __name__ == "__main__":
    main()
