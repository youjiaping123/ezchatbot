import pyaudio
import wave
import time

def test_microphone():
    """测试麦克风录音功能"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "test_recording.wav"

    print("开始麦克风测试...")
    
    try:
        p = pyaudio.PyAudio()
        
        # 获取默认输入设备信息
        default_input = p.get_default_input_device_info()
        print(f"\n默认输入设备: {default_input['name']}")
        
        # 列出所有可用的音频输入设备
        print("\n可用的输入设备:")
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                print(f"设备 {i}: {dev_info['name']}")

        # 开始录音
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

        print("\n* 录音中...")
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            # 显示录音进度
            print(f"录音进度: {(i+1)/(RATE/CHUNK*RECORD_SECONDS)*100:.1f}%", end='\r')

        print("\n* 录音完成!")

        # 停止录音
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 保存录音文件
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"\n录音已保存到 {WAVE_OUTPUT_FILENAME}")
        return True

    except Exception as e:
        print(f"\n麦克风测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_microphone() 