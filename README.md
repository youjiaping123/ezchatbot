# EzChatBot - 树莓派语音聊天机器人

这是一个基于OpenAI API和Azure语音服务的智能语音聊天机器人，专门为树莓派设计。

## 系统要求

- Raspberry Pi (推荐使用Raspberry Pi 4或更新版本)
- Raspberry Pi OS (基于Debian Bullseye或更新版本)
- Python 3.7+
- 麦克风
- 音箱或耳机
- 网络连接

## 硬件设置

1. 将麦克风连接到树莓派的USB端口或3.5mm音频接口
2. 将音箱或耳机连接到树莓派的音频输出接口

## 安装步骤

1. 首先更新系统包：
```bash
sudo apt update
sudo apt upgrade
```

2. 安装必要的系统依赖：
```bash
sudo apt install -y python3-pip python3-venv portaudio19-dev python3-pyaudio
```

3. 克隆项目仓库：
```bash
git clone [你的仓库地址]
cd ezchatbot
```

4. 创建并激活虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate
```

5. 安装Python依赖：
```bash
pip install -r requirements.txt
```

6. 创建配置文件：
```bash
cp .env.example .env
```

7. 编辑.env文件，填入你的API密钥：
```
OPENAI_API_KEY=你的OpenAI API密钥
OPENAI_API_BASE=https://api.openai.com/v1
SPEECH_KEY=你的Azure语音服务密钥
SPEECH_REGION=你的Azure语音服务区域
```

## 音频设置

1. 检查音频设备：
```bash
arecord -l  # 列出录音设备
aplay -l    # 列出播放设备
```

2. 测试麦克风：
```bash
arecord -d 5 test.wav  # 录制5秒音频
aplay test.wav         # 播放录制的音频
```

## 运行程序

1. 确保在虚拟环境中：
```bash
source venv/bin/activate
```

2. 运行聊天机器人：
```bash
python chat_bot.py
```

## 使用说明

- 启动程序后，默认使用文本输入模式
- 输入 'voice' 切换到语音输入模式
- 输入 'text' 切换回文本输入模式
- 输入 'quit' 或 'exit' 退出程序
- 在语音模式下，说话后会自动识别并回复
- 机器人的回复在语音模式下会自动播放

## 故障排除

1. 如果遇到麦克风问题：
```bash
# 检查麦克风权限
sudo usermod -a -G audio $USER
# 重启树莓派
sudo reboot
```

2. 如果遇到声音输出问题：
```bash
# 运行音频配置工具
sudo raspi-config
# 选择 System Options -> Audio -> 选择合适的音频输出
```

3. 如果遇到依赖安装问题：
```bash
# 确保pip是最新版本
pip install --upgrade pip
# 手动安装特定依赖
pip install azure-cognitiveservices-speech
```

## 注意事项

- 确保树莓派有稳定的网络连接
- 使用优质的麦克风可以提高语音识别准确率
- 定期检查API密钥的有效性和使用配额
- 建议在安静的环境中使用语音功能

