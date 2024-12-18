import subprocess
from datetime import datetime

def run_command(command):
    """
    시스템 명령어를 실행하는 함수.
    """
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {command}\n{e}")

'''
def setup_environment():
    """
    시스템 업데이트 및 필수 패키지, 폰트 설치 및 설정.
    """
    # 시스템 업데이트 및 패키지 설치
    print("Updating system and installing required packages...")
    run_command("apt-get update -qq")
    run_command("apt-get install imagemagick -y -qq")
    run_command("apt-get install ffmpeg -y -qq")

    # moviepy 설치
    print("Installing moviepy...")
    run_command("pip install moviepy[optional] -q")

    # ImageMagick 설정 변경
    print("Configuring ImageMagick policy...")
    run_command('sudo sed -i \'/<policy domain="path" rights="none" pattern="@*"/d\' /etc/ImageMagick-6/policy.xml')

    # 나눔고딕 폰트 설치
    print("Installing Nanum font...")
    run_command("apt-get install -y fonts-nanum")

    # 폰트 캐시 갱신
    print("Refreshing font cache...")
    run_command("fc-cache -fv")

    # 설치된 폰트 확인
    print("Checking installed fonts...")
    run_command("fc-list | grep Nanum")


setup_environment()
'''

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip,CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.resize import resize

import textwrap

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip,CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.resize import resize

import textwrap

'''
video_files = ["data/video1.mp4", "data/video2.mp4", "data/video3.mp4", "data/video4.mp4", "data/video5.mp4"]
audio_files = ["data/음성1.m4a", "data/음성2.m4a", "data/음성3.m4a", "data/음성4.m4a", "data/음성5.m4a"]
subtitles = ['무허가 불법 선물거래소를 운영한 일당이 경찰에 붙잡혔습니다.', '이들은 인천과 해외에서 불법 도박장을 차리고 수익을 챙겼습니다.', '부산경찰청은 이들을 자본시장법 위반 혐의로 구속했습니다.', '일당은 6270명의 회원을 모집하고 허위 인증글로 유도했습니다.', '경찰은 이들의 범죄 수익 8억 6000만원을 환수 조치했습니다.']
'''

font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

output_width = 1080
output_height = 1920

def wrap_text(text, max_width):
    return textwrap.wrap(text, width=max_width)


def runMoviepy(video_files, audio_files, subtitles, output_label="output"):

    final_clips = []

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    for video_file, audio_file, subtitle in zip(video_files, audio_files, subtitles):
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)

        video_duration = audio.duration
        repeated_video = video.loop(duration=video_duration)

        resized_video = resize(repeated_video, width=output_width)
        padding_video = resized_video.on_color(size=(output_width, output_height), color=(0, 0, 0), pos=("center", "center"))

        wrapped_subtitles = wrap_text(subtitle, max_width=20)

        text_clips = []
        for i, line in enumerate(wrapped_subtitles):
            text_clip = TextClip(line, fontsize=50, color='white', font=font_path, stroke_color='black', stroke_width=2, align='center')
            text_clip = text_clip.set_position(('center', output_height - 300 + (i * 60)))  # 각 줄의 Y 위치 조정
            text_clip = text_clip.set_duration(video_duration)
            text_clips.append(text_clip)

        video_with_subtitle = CompositeVideoClip([padding_video] + text_clips)
        video_with_audio = video_with_subtitle.set_audio(audio)

        final_clips.append(video_with_audio)


    final_video = concatenate_videoclips(final_clips)
    final_video.write_videofile(f"{output_label}_{current_time}.mp4", codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    runMoviepy(video_files,audio_files, subtitles,output_label="output")
