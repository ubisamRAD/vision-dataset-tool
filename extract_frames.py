#!/usr/bin/env python3
"""
영상에서 프레임을 추출하여 이미지 파일로 저장하는 스크립트

사용법:
  python3 extract_frames.py output/video_20260313_120000.mp4
  python3 extract_frames.py output/video_20260313_120000.mp4 --interval 5 --format png
"""

import cv2
import os
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="영상 프레임 추출 도구")
    parser.add_argument("video", type=str, help="입력 영상 파일 경로")
    parser.add_argument("--interval", type=int, default=10,
                        help="프레임 추출 간격 (N 프레임마다 1장 저장, 기본: 10)")
    parser.add_argument("--max-frames", type=int, default=0,
                        help="최대 추출 프레임 수 (0=무제한, 기본: 0)")
    parser.add_argument("--output-dir", type=str, default="",
                        help="이미지 저장 디렉토리 (기본: frames_<영상이름>)")
    parser.add_argument("--format", type=str, default="jpg", choices=["jpg", "png"],
                        help="이미지 포맷 (기본: jpg)")
    parser.add_argument("--quality", type=int, default=95,
                        help="JPEG 품질 0-100 (기본: 95)")
    parser.add_argument("--resize", type=str, default="",
                        help="리사이즈 (예: 640x480)")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"[ERROR] 영상 파일을 찾을 수 없습니다: {args.video}")
        return

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"[ERROR] 영상 파일을 열 수 없습니다: {args.video}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps if fps > 0 else 0

    print(f"[INFO] 영상 정보: {width}x{height}, {fps:.1f}fps, "
          f"{total_frames}프레임, {duration:.1f}초")
    print(f"[INFO] {args.interval}프레임 간격으로 추출 "
          f"→ 약 {total_frames // args.interval}장 예상")

    # 출력 디렉토리
    if args.output_dir:
        output_dir = args.output_dir
    else:
        video_name = Path(args.video).stem
        output_dir = f"frames_{video_name}"
    os.makedirs(output_dir, exist_ok=True)

    # 리사이즈 파싱
    resize = None
    if args.resize:
        try:
            rw, rh = args.resize.split("x")
            resize = (int(rw), int(rh))
        except ValueError:
            print(f"[ERROR] 리사이즈 형식이 잘못되었습니다: {args.resize} (예: 640x480)")
            return

    # 프레임 추출
    frame_idx = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % args.interval == 0:
            if resize:
                frame = cv2.resize(frame, resize)

            filename = f"frame_{saved_count:05d}.{args.format}"
            filepath = os.path.join(output_dir, filename)

            if args.format == "jpg":
                cv2.imwrite(filepath, frame,
                            [cv2.IMWRITE_JPEG_QUALITY, args.quality])
            else:
                cv2.imwrite(filepath, frame)

            saved_count += 1

            if saved_count % 50 == 0:
                print(f"  ... {saved_count}장 저장 완료")

            if args.max_frames > 0 and saved_count >= args.max_frames:
                print(f"[INFO] 최대 프레임 수({args.max_frames})에 도달")
                break

        frame_idx += 1

    cap.release()
    print(f"\n[DONE] 총 {saved_count}장 저장 → {output_dir}/")
    print(f"[TIP] Roboflow에 업로드할 준비가 되었습니다!")


if __name__ == "__main__":
    main()
