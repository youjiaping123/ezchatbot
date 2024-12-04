import pyaudio
import wave
import os

def test_speaker():
    """测试扬声器播放功能"""
    print("开始扬声器测试...")
    
    # 首先检查是否存在测试音频文件
    test_file = "test_recording.wav"
    if not os.path.exists(test_file):
        print(f"未找到测试音频文件: {test_file}")
        print("请先运行麦克风测试生成测试音频")
        return False

    try:
        # 初始化PyAudio
        p = pyaudio.PyAudio()

        # 获取默认输出设备信息
        default_output = p.get_default_output_device_info()
        print(f"\n默认输出设备: {default_output['name']}")
        
        # 列出所有可用的音频输出设备
        print("\n可用的输出设备:")
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info['maxOutputChannels'] > 0:
                print(f"设备 {i}: {dev_info['name']}")

        # 打开测试音频文件
        wf = wave.open(test_file, 'rb')

        # 打开音频流
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                       channels=wf.getnchannels(),
                       rate=wf.getframerate(),
                       output=True)

        print("\n* 开始播放...")
        
        # 读取数据
        data = wf.readframes(1024)
        
        # 播放音频
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        print("* 播放完成!")

        # 清理资源
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        return True

    except Exception as e:
        print(f"\n扬声器测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_speaker() 