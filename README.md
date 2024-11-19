# Terminus Bot 自动签到工具

这是一个用于自动完成 Terminus Bot 签到的 Python 工具。它能够自动处理验证码识别并完成签到流程。

## 功能特点

- 自动连接 Telegram 客户端
- AI 验证码识别
- 自动签到
- 详细的日志记录
- 异常处理机制

## 安装要求

- Python 3.8+
- Telegram 账号
- OpenAI API 密钥
- Telegram API 凭据

## 安装步骤

1. 克隆仓库： 
```shell
git clone https://github.com/eddiehex/emby-sign.git
cd [项目目录]
```

2. 安装依赖：
```shell
pip install -r requirements.txt
```

3. 配置环境变量：
```shell
cp .env_demo .env
vim .env
``` 

```plaintext
OPENAI_BASE_URL=你的OpenAI基础URL
OPENAI_API_KEY=你的OpenAI API密钥
TELEGRAM_API_ID=你的Telegram API ID
TELEGRAM_API_HASH=你的Telegram API Hash
```

## 使用方法

1. 获取 Telegram API 凭据：
   - 访问 https://my.telegram.org/apps
   - 创建一个新的应用
   - 获取 API ID 和 API Hash

2. 运行程序：
```shell
python src/terminal.py
```

## 文件结构
```
.
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   ├── log
│   ├── my_account.session
│   ├── terminal.py
│   └── test_vision.py
```
