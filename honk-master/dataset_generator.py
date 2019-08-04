#!/usr/bin/env python3
import pyaudio
import argparse
import hashlib
import wave
import os
def main(flags):
    os.chdir(flags.p)
    if not os.path.exists(flags.k):
        os.mkdir(flags.k)
    os.chdir(flags.k)
    RATE=16000
    CHUNK=1000
    FORMAT=pyaudio.paInt16
    RECORD_SECONDS=2
    _audio=pyaudio.PyAudio()
    for i in range(0,flags.n):
        stream = _audio.open(format=pyaudio.paInt16,
                             channels = 1,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        print("开始录制第%d条语音，请说话"% i)
        frames = []
        for j in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("录音结束")
        stream.stop_stream()
        stream.close()
        hashcode=hashlib.sha224(b''.join(frames)).hexdigest()[0:8]
        wf=wave.open(hashcode+"__nohash__.wav",'wb')
        wf.setnchannels(1)
        wf.setsampwidth(_audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("保存完毕,请按回车进行下一轮录制")
        str=input();


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--k",type=str,default="",help="the keyword")
    parser.add_argument("--p",type=str,default=".",help="the path of dataset")
    parser.add_argument("--n",type=int,default=10,help="the number of wav files")
    flags = parser.parse_args()
    if flags.k=="":
        print("keyword can not be empty!" )
        exit();
    main(flags)    

