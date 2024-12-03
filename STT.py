import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

class SpeechToText:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'), 
            region=os.getenv('SPEECH_REGION')
        )
        self.speech_config.speech_recognition_language = "zh-CN"
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, 
            audio_config=self.audio_config
        )
        
    def listen(self):
        """监听并转换语音为文本"""
        print("请说话...")
        
        # 创建一个事件来同步识别过程
        done = False
        result_text = None

        def handle_result(evt):
            nonlocal done, result_text
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                result_text = evt.result.text
            done = True

        # 绑定事件处理器
        self.speech_recognizer.recognized.connect(handle_result)
        self.speech_recognizer.canceled.connect(lambda evt: setattr(done, True))
        
        # 开始识别
        self.speech_recognizer.start_continuous_recognition()
        
        try:
            while not done:
                import time
                time.sleep(0.1)
        finally:
            # 确保停止识别
            self.speech_recognizer.stop_continuous_recognition()
            
        if result_text:
            return result_text
        return None