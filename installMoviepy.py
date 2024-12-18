import os
import sys
import subprocess

def run_command(command):
    """ 명령어 실행 및 에러 처리 """
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {command}")
        print(f"Command returned non-zero exit status {e.returncode}.")
        sys.exit(1)

def install_dependencies():
    """ 필요한 패키지 및 라이브러리 설치 """
    print("Updating system and installing required packages...")
    
    # 루트 권한이 없는 경우 오류 방지
    if os.geteuid() != 0:
        print("Error: This script must be run with root privileges. Use 'sudo' or run as root.")
        sys.exit(1)

    # 시스템 패키지 업데이트 및 설치
    run_command("apt-get update -qq")
    run_command("apt-get install imagemagick -y -qq")
    run_command("apt-get install ffmpeg -y -qq")

    # moviepy 설치
    print("Installing moviepy...")
    run_command("pip install moviepy[optional] -q")

    # ImageMagick 권한 설정
    print("Configuring ImageMagick policy...")
    run_command("sed -i '/<policy domain=\"path\" rights=\"none\" pattern=\"@*\"/d' /etc/ImageMagick-6/policy.xml")

    # 나눔고딕 폰트 설치
    print("Installing Nanum font...")
    run_command("apt-get install -y fonts-nanum")
    run_command("fc-cache -fv")

if __name__ == "__main__":
    install_dependencies()
    print("All dependencies installed successfully!")
