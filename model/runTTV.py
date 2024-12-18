import os
import sys
import subprocess
import importlib.util
import torch

# Text2Video-Zero 경로 설정
text2video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Text2Video-Zero"))
model_file_path = os.path.join(text2video_path, "model.py")

video_name=[]


def install_dependencies():
    """
    필요한 패키지 및 라이브러리 설치
    """
    try:
        # apt-get 설치
        print("Installing python3.9-distutils...")
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3.9-distutils"])

        # wget으로 get-pip.py 다운로드
        print("Downloading get-pip.py...")
        subprocess.check_call(["wget", "https://bootstrap.pypa.io/get-pip.py"])

        # Python 3.9용 pip 설치
        print("Installing pip for Python 3.9...")
        subprocess.check_call(["python3.9", "get-pip.py"])

        # requirements.txt 파일 설치
        #print("Installing packages from requirements.txt...")
        #subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        # jax와 jaxlib 업그레이드
        print("Upgrading jax and jaxlib...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "jax", "jaxlib"])

        # tomesd 설치
        print("Installing tomesd...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tomesd"])

        # 특정 버전의 huggingface_hub 설치
        #print("Installing huggingface_hub version 0.10.1...")
        #subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub==0.10.1"])

        print("All dependencies have been installed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
        sys.exit(1)


# model.py를 동적으로 가져오기
def load_model():
    spec = importlib.util.spec_from_file_location("model", model_file_path)
    model_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_module)
    return model_module.Model

Model = load_model()


def runTTVPerSec(prompt, params=None, output_dir="./", fps=4):

    """
    단일 문장을 입력받아 텍스트를 비디오로 변환하는 함수.
    파일 생성 없이 직접 실행 가능.
    
    Args:
        prompt (str): 텍스트 프롬프트.
        params (dict): 비디오 생성 파라미터.
        output_dir (str): 출력 파일 디렉토리.
        fps (int): 출력 비디오의 초당 프레임 수.
    """

    global video_name

    # 기본 파라미터 설정
    if params is None:
        params = {
            "t0": 44,
            "t1": 47,
            "motion_field_strength_x": 30,
            "motion_field_strength_y": 30,
            "video_length": 30,
        }

    # Model 인스턴스 초기화
    print("Initializing the model...")
    model = Model(device="cuda", dtype=torch.float16)

    # 출력 파일 경로 생성
    out_path = f"{output_dir}/text2video_{prompt.replace(' ', '_')}.mp4"

    video_name.append(out_path)

    # 비디오 생성
    try:
        print(f"Generating video for prompt: {prompt}")
        model.process_text2video(prompt, fps=fps, path=out_path, **params)
        print(f"Video successfully generated: {out_path}")
    except Exception as e:
        print(f"An error occurred while generating the video: {e}")

def makeOutput(prompts, output_dir="./", fps=4):
    """
    여러 문장을 입력받아 각 문장에 대해 비디오 생성 실행.
    
    Args:
        prompts (list): 텍스트 프롬프트 리스트.
        output_dir (str): 출력 파일 디렉토리.
        fps (int): 출력 비디오의 초당 프레임 수.
    """
    for prompt in prompts:
        runTTVPerSec(prompt, output_dir=output_dir, fps=fps)

def runTTV(prompts):
    output_dir = "./generated_videos"
        # 디렉토리 생성
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 비디오 생성 실행
    makeOutput(prompts, output_dir=output_dir)

    return video_name

if __name__ == "__main__":    

    install_dependencies()
    video_f_name = runTTV(prompts)
    print("Generate video files:", video_f_name)

    

