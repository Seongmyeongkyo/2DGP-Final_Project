import os
import sys

# 실행 파일(exe)로 실행 중인지, 일반 Python 스크립트로 실행 중인지 확인
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행 파일인 경우
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 일반 Python 스크립트로 실행되는 경우
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOUND_FILES = {
    'background': os.path.join(BASE_DIR, 'sound', 'Background.wav'),
    'exit': os.path.join(BASE_DIR, 'sound', 'exit.wav'),
}