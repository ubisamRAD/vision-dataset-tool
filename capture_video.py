#!/usr/bin/env python3
"""
웹캠 영상 촬영 스크립트
- 웹캠을 열어 실시간 미리보기를 표시합니다.
- 's' 키: 녹화 시작/중지 토글
- 'q' 키: 종료
- 녹화된 영상은 output/ 디렉토리에 저장됩니다.
"""

import cv2
import os
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="웹캠 영상 촬영 도구")
    parser.add_argument("--camera", type=int, default=0, help="카메라 인덱스 (기본: 0)")
    parser.add_argument("--width", type=int, default=640, help="영상 너비 (기본: 640)")
    parser.add_argument("--height", type=int, default=480, help="영상 높이 (기본: 480)")
    parser.add_argument("--fps", type=int, default=30, help="FPS (기본: 30)")
    parser.add_argument("--output-dir", type=str, default="output", help="저장 디렉토리 (기본: output)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("[ERROR] 카메라를 열 수 없습니다. 카메라 연결을 확인하세요.")
        print("  - WSL2에서는 USB 카메라 패스스루 설정이 필요합니다.")
        print("  - 또는 Windows에서 직접 실행하세요.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    cap.set(cv2.CAP_PROP_FPS, args.fps)

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"[INFO] 카메라 열림: {actual_w}x{actual_h} @ {actual_fps:.1f}fps")
    print("[INFO] 's' = 녹화 시작/중지, 'q' = 종료")

    recording = False
    writer = None
    video_path = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] 프레임을 읽을 수 없습니다.")
                break

            # 녹화 상태 표시
            display = frame.copy()
            if recording:
                cv2.circle(display, (30, 30), 10, (0, 0, 255), -1)
                cv2.putText(display, "REC", (50, 38),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                writer.write(frame)

            cv2.imshow("Capture (s=record, q=quit)", display)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                if not recording:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    video_path = os.path.join(args.output_dir, f"video_{timestamp}.mp4")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    writer = cv2.VideoWriter(video_path, fourcc, actual_fps,
                                             (actual_w, actual_h))
                    recording = True
                    print(f"[REC] 녹화 시작: {video_path}")
                else:
                    recording = False
                    writer.release()
                    writer = None
                    print(f"[STOP] 녹화 중지: {video_path}")

            elif key == ord('q'):
                break

    finally:
        if writer is not None:
            writer.release()
            print(f"[STOP] 녹화 저장됨: {video_path}")
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] 종료")


if __name__ == "__main__":
    main()
