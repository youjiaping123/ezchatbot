from test_microphone import test_microphone
from test_speaker import test_speaker
import time

def run_all_tests():
    """运行所有音频测试"""
    print("=== 开始音频设备测试 ===\n")
    
    # 测试麦克风
    print("测试1: 麦克风测试")
    print("-" * 50)
    mic_result = test_microphone()
    print("-" * 50)
    print(f"麦克风测试结果: {'通过' if mic_result else '失败'}\n")
    
    # 等待2秒
    time.sleep(2)
    
    # 测试扬声器
    print("测试2: 扬声器测试")
    print("-" * 50)
    speaker_result = test_speaker()
    print("-" * 50)
    print(f"扬声器测试结果: {'通过' if speaker_result else '失败'}\n")
    
    # 输出总结果
    print("=== 测试结果总结 ===")
    print(f"麦克风: {'✓' if mic_result else '✗'}")
    print(f"扬声器: {'✓' if speaker_result else '✗'}")
    
    if mic_result and speaker_result:
        print("\n所有测试通过！音频设备工作正常。")
    else:
        print("\n部分测试失败，请检查设备连接和系统设置。")

if __name__ == "__main__":
    run_all_tests() 