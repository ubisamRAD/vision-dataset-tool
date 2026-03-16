#!/usr/bin/env python3
"""
Roboflow 데이터셋 다운로드 스크립트

사용법:
  python3 download_dataset.py --api-key YOUR_KEY --workspace YOUR_WS --project YOUR_PROJECT --version 1
"""

import argparse
from roboflow import Roboflow


def main():
    parser = argparse.ArgumentParser(description="Roboflow 데이터셋 다운로드 도구")
    parser.add_argument("--api-key", type=str, required=True,
                        help="Roboflow API Key")
    parser.add_argument("--workspace", type=str, required=True,
                        help="워크스페이스 이름 (URL에서 확인)")
    parser.add_argument("--project", type=str, required=True,
                        help="프로젝트 이름 (URL에서 확인)")
    parser.add_argument("--version", type=int, default=1,
                        help="데이터셋 버전 번호 (기본: 1)")
    parser.add_argument("--format", type=str, default="yolov8",
                        help="다운로드 포맷 (기본: yolov8)")
    args = parser.parse_args()

    print(f"[INFO] 워크스페이스: {args.workspace}")
    print(f"[INFO] 프로젝트: {args.project}")
    print(f"[INFO] 버전: {args.version}")
    print(f"[INFO] 포맷: {args.format}")

    rf = Roboflow(api_key=args.api_key)
    project = rf.workspace(args.workspace).project(args.project)
    dataset = project.version(args.version).download(args.format)

    print(f"\n[DONE] 다운로드 완료: {dataset.location}")
    print(f"[INFO] data.yaml 경로: {dataset.location}/data.yaml")


if __name__ == "__main__":
    main()
