import subprocess
import os
from typing import List
import json
from static import *


def prepare(input_file: str, duration: int, media_dir: str, targets: List[List]) -> None:
    cmd = f'ffmpeg -y -t {duration} -i {input_file}'

    # convert input file to different resolutions and frame rates
    for res, frame_rate in targets:
        # create the directory if it doesn't exists
        output_dir = media_dir + f'/{res}{frame_rate}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        gen_config_file(output_dir, res, frame_rate, duration)

        output_video = output_dir + '/srcvideo.yuv'
        output_audio = output_dir + '/srcaudio.wav'
        cmd += f' -s {resolutions[res]} -r {frame_rate} {output_video}'
        cmd += f' {output_audio}'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = log_dir + '/convert.log'
    cmd += f' > {log_file} 2>&1'

    subprocess.run(cmd, shell=True)


def gen_config_file(path: str, res: str, frame_rate: int, duration: int) -> None:
    sender = path + '/sender.json'
    receiver = path + '/receiver.json'

    width, height = resolutions[res].split(':')

    with open(sender_example, 'r') as f:
        sender_config = json.load(f)

    sender_config['serverless_connection']['autoclose'] = duration
    sender_config['video_source']['video_file']['width'] = int(width)
    sender_config['video_source']['video_file']['height'] = int(height)
    sender_config['video_source']['video_file']['fps'] = frame_rate
    #sender_config['video_source']['video_file']['file_path'] = 'srcvideo.yuv'
    #sender_config['audio_source']['audio_file']['file_path'] = 'srcaudio.wav'

    with open(sender, 'w') as f:
        json.dump(sender_config, f, indent=4)


    with open(receiver_example, 'r') as f:
        receiver_config = json.load(f)

    receiver_config['serverless_connection']['autoclose'] = duration
    #receiver_config['save_to_file']['audio']['file_path'] = 'outaudio.wav'
    #receiver_config['save_to_file']['video']['file_path'] = 'outvideo.yuv'
    receiver_config['save_to_file']['video']['width'] = int(width)
    receiver_config['save_to_file']['video']['height'] = int(height)
    receiver_config['save_to_file']['video']['fps'] = frame_rate

    with open(receiver, 'w') as f:
        json.dump(receiver_config, f, indent=4)
