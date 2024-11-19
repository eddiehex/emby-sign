import emoji
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError
from ai_vision import ImageAnalyzer
from utils.logger import setup_logger

# 添加调试信息
print("当前工作目录:", os.getcwd())
env_path = find_dotenv()
print("找到的.env文件路径:", env_path)

# 明确指定 .env 文件路径来加载
load_dotenv(env_path)

# 调试环境变量
print("环境变量值：")
print(f"TELEGRAM_API_ID: {os.getenv('TELEGRAM_API_ID')}")
print(f"TELEGRAM_API_HASH: {os.getenv('TELEGRAM_API_HASH')}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")  # 用作对照

class TerminusCheckin:
    def __init__(self):
        # 设置日志记录器
        self.logger = setup_logger('TerminusCheckin')
        
        # 直接设置 API 配置
        self.api_id = 27298067  # 整数类型
        self.api_hash = "2abb9ab6deab9f69a1fc68ec76efcc07"
        
        self.bot_username = "EmbyPublicBot"
        self.image_analyzer = ImageAnalyzer()
        self.client = None
        
        self.logger.info("TerminusCheckin 初始化完成")

    async def start(self):
        """启动 Telegram 客户端"""
        try:
            self.client = Client(
                "my_account",
                api_id=self.api_id,
                api_hash=self.api_hash
            )
            await self.client.start()
            self.logger.info("Telegram 客户端启动成功")
        except Exception as e:
            self.logger.error(f"Telegram 客户端启动失败: {str(e)}")
            raise

    async def stop(self):
        """停止 Telegram 客户端"""
        if self.client:
            try:
                await self.client.stop()
                self.logger.info("Telegram 客户端已停止")
            except Exception as e:
                self.logger.error(f"Telegram 客户端停止失败: {str(e)}")

    async def analyze_captcha(self, photo_path, options):
        """使用AI分析验证码图片并匹配选项"""
        try:
            self.logger.info(f"开始分析验证码图片，可选项: {options}")
            
            prompt = f"这是一个图片。请从以下选项中选择最匹配图片内容的答案：{', '.join(options)}。只需返回最匹配的一个选项，不需要其他解释。"
            
            result = self.image_analyzer.analyze_image(photo_path, prompt)
            self.logger.debug(f"AI分析结果: {result}")
            
            result = result.strip()
            
            for option in options:
                if option.lower() in result.lower():
                    self.logger.info(f"找到匹配选项: {option}")
                    return option
            
            self.logger.warning("未找到匹配选项")
            return None
        except Exception as e:
            self.logger.error(f"验证码分析失败: {str(e)}")
            return None

    async def handle_checkin_response(self, message: Message):
        """处理签到响应消息"""
        try:
            if message.photo and message.reply_markup:
                self.logger.info("收到带有图片的签到响应")
                
                keys = [k for r in message.reply_markup.inline_keyboard for k in r]
                options = [k.text for k in keys]
                options_cleaned = [emoji.replace_emoji(o, "").replace(" ", "") for o in options]
                
                self.logger.debug(f"可选项: {options_cleaned}")
                
                if len(options) < 2:
                    self.logger.warning("选项数量不足")
                    return False

                photo_path = await message.download()
                self.logger.debug(f"验证码图片已下载: {photo_path}")
                
                try:
                    result = await self.analyze_captcha(photo_path, options_cleaned)
                    
                    if result:
                        self.logger.info(f"AI识别结果: {result}")
                        original_option = options[options_cleaned.index(result)]
                        try:
                            await message.click(original_option)
                            self.logger.info("成功点击选项")
                            return True
                        except RPCError as e:
                            self.logger.error(f"按钮点击失败: {e}")
                    else:
                        self.logger.warning("AI未能识别出正确答案")
                finally:
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                        self.logger.debug("临时文件已清理")
            
            return False
        except Exception as e:
            self.logger.error(f"处理签到响应时出错: {str(e)}")
            return False

    async def perform_checkin(self):
        """执行签到流程"""
        try:
            self.logger.info("开始执行签到流程")
            
            bot = await self.client.get_users(self.bot_username)
            await self.client.send_message(bot.id, "/checkin")
            self.logger.info("已发送签到命令")
            
            async def wait_for_response():
                async for message in self.client.get_chat_history(bot.id, limit=1):
                    if message.photo:
                        self.logger.debug("收到带图片的响应")
                        return message
                return None

            for attempt in range(5):
                self.logger.debug(f"等待响应，尝试 {attempt + 1}/5")
                await asyncio.sleep(2)
                response = await wait_for_response()
                if response:
                    success = await self.handle_checkin_response(response)
                    if success:
                        self.logger.info("签到成功完成")
                        return True
                    break
            
            self.logger.warning("签到失败")
            return False

        except Exception as e:
            self.logger.error(f"签到过程出错: {str(e)}")
            return False

async def main():
    logger = setup_logger('main')
    checkin = TerminusCheckin()
    try:
        logger.info("开始签到程序")
        await checkin.start()
        await checkin.perform_checkin()
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
    finally:
        await checkin.stop()
        logger.info("程序结束")

if __name__ == "__main__":
    asyncio.run(main())