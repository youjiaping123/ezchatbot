import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

class TextToSpeech:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('SPEECH_KEY'), 
            region=os.getenv('SPEECH_REGION')
        )
        # 设置中文女声
        self.speech_config.speech_synthesis_voice_name = 'zh-CN-XiaoxiaoNeural'
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, 
            audio_config=self.audio_config
        )

    def speak(self, text):
        """将文本转换为语音"""
        try:
            result = self.speech_synthesizer.speak_text_async(text).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True
            else:
                print(f"语音合成失败: {result.reason}")
                return False
        except Exception as e:
            print(f"语音合成错误: {str(e)}")
            return False