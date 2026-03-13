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
from ultralytics import YOLO


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
    args = parser.parse_args()

    # 기본 모델 설정
    if not args.model:
        if args.task == "segment":
            args.model = "yolov8n-seg.pt"
        else:
            args.model = "yolov8n.pt"

    print(f"[INFO] 태스크: {args.task}")
    print(f"[INFO] 모델: {args.model}")
    print(f"[INFO] 데이터: {args.data}")
    print(f"[INFO] 에포크: {args.epochs}, 이미지 크기: {args.imgsz}, 배치: {args.batch}")

    model = YOLO(args.model)

    train_args = {
        "data": args.data,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
    }

    if args.name:
        train_args["name"] = args.name

    if args.task == "segment":
        results = model.train(**train_args)
    else:
        results = model.train(**train_args)

    print(f"\n[DONE] 학습 완료!")
    print(f"[INFO] best 모델: {model.trainer.best}")
    print(f"[INFO] 결과 디렉토리: {model.trainer.save_dir}")


if __name__ == "__main__":
    main()
