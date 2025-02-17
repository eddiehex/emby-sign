import os
from openai import OpenAI
import base64
from utils.logger import setup_logger
from dotenv import load_dotenv
import os

load_dotenv()
class ImageAnalyzer:
    def __init__(self):
        self.logger = setup_logger('ImageAnalyzer')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL')
        self.client = OpenAI(api_key=self.api_key)
        self.logger.info("ImageAnalyzer 初始化完成")

    def encode_image(self, image_path):
        """将图片转换为base64编码"""
        try:
            with open(image_path, "rb") as image_file:
                self.logger.debug(f"正在编码图片: {image_path}")
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"图片编码失败: {str(e)}")
            raise

    def analyze_image(self, image_path, custom_prompt=None):
        """分析图片并返回描述"""
        try:
            self.logger.info("开始分析图片")
            base64_image = self.encode_image(image_path)
            
            prompt = custom_prompt or "请描述这张图片中的内容，并尽可能识别出图片中的文字。"
            self.logger.debug(f"使用提示: {prompt}")
            
            response = self.client.chat.completions.create(
                model="grok-2-vision-1212",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            result = response.choices[0].message.content
            self.logger.info("图片分析完成")
            self.logger.debug(f"分析结果: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"图片分析出错: {str(e)}")
            return f"图片分析出错: {str(e)}" 