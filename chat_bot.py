from openai import OpenAI
import os
from dotenv import load_dotenv
from TTS import TextToSpeech
from STT import SpeechToText
import json

# 加载环境变量
load_dotenv()

class ChatBot:
    def __init__(self):
        # 基础配置
        self.bot_config = {
            "id": "8S_CKtD8Bq3T0y8h1QbK1",
            "avatar": "gpt-bot",
            "name": "新的聊天",
            "lang": "cn",
            "builtin": False,
            "createdAt": 1733243019631
        }
        
        # 模型配置
        self.model_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.5,
            "top_p": 1,
            "max_tokens": 4000,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "sendMemory": True,
            "historyMessageCount": 4,
            "compressMessageLengthThreshold": 1000,
            "enableInjectSystemPrompts": True,
            "template": "{{input}}",
            "size": "1024x1024",
            "quality": "standard",
            "style": "vivid"
        }

        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE')
        )
        
        # 初始化消息历史
        self.messages = []
        self.history_message_count = self.model_config["historyMessageCount"]
        
        # 初始化语音模块
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        
    def add_message(self, role, content):
        """添加消息到对话历史，并保持历史消息数量在限制范围内"""
        self.messages.append({"role": role, "content": content})
        
        # 保持历史消息数量在限制范围内
        if len(self.messages) > self.history_message_count * 2:  # 乘2是因为每轮对话包含用户和助手各一条消息
            self.messages = self.messages[-self.history_message_count * 2:]
        
    def chat(self, user_input):
        """与用户进行对话"""
        # 添加用户输入到消息历史
        self.add_message("user", user_input)
        
        try:
            # 调用API获取回复
            response = self.client.chat.completions.create(
                model=self.model_config["model"],
                messages=self.messages,
                temperature=self.model_config["temperature"],
                top_p=self.model_config["top_p"],
                max_tokens=self.model_config["max_tokens"],
                presence_penalty=self.model_config["presence_penalty"],
                frequency_penalty=self.model_config["frequency_penalty"]
            )
            
            # 获取助手的回复
            assistant_response = response.choices[0].message.content
            
            # 将助手的回复添加到消息历史
            self.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            return "抱歉，我遇到了一些问题，请稍后再试。"
    
    def save_config(self, filename="bot_config.json"):
        """保存配置到文件"""
        config = {
            **self.bot_config,
            "modelConfig": self.model_config,
            "context": self.messages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def load_config(self, filename="bot_config.json"):
        """从文件加载配置"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.bot_config.update(config)
                self.model_config.update(config.get("modelConfig", {}))
                self.messages = config.get("context", [])

def main():
    chatbot = ChatBot()
    print(f"欢迎使用 {chatbot.bot_config['name']}！")
    print("输入 'quit' 或 'exit' 结束对话")
    print("输入 'voice' 开始语音输入")
    print("输入 'text' 切换回文本输入")
    
    input_mode = "text"
    
    try:
        while True:
            try:
                if input_mode == "text":
                    user_input = input("\n你: ")
                    if user_input.lower() == "voice":
                        input_mode = "voice"
                        print("已切换到语音输入模式")
                        continue
                else:  # voice mode
                    user_input = chatbot.stt.listen()
                    if user_input:
                        print(f"\n你: {user_input}")
                    else:
                        print("未能识别语音，请重试")
                        continue
                        
                if user_input.lower() in ['quit', 'exit']:
                    print("谢谢使用，再见！")
                    break
                elif user_input.lower() == 'text':
                    input_mode = "text"
                    print("已切换到文本输入模式")
                    continue
                    
                response = chatbot.chat(user_input)
                print(f"\nAI助手: {response}")
                
                # 如果在语音模式下，播放语音回复
                if input_mode == "voice":
                    chatbot.tts.speak(response)
                    
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"\n发生错误: {str(e)}")
                continue
                
    finally:
        # 保存配置和对话历史
        chatbot.save_config()

if __name__ == "__main__":
    main() 