from ai_vision import ImageAnalyzer
import os

def test_image_recognition():
    # 初始化图像分析器
    analyzer = ImageAnalyzer()
    
    # 图片路径
    image_path = "1.jpg"
    
    # 确保图片存在
    if not os.path.exists(image_path):
        print(f"错误：找不到图片 {image_path}")
        return
    
    # 定义选项
    options = ["电脑", "书", "桌子", "菜"]
    options_str = ", ".join(options)
    
    # 构建提示语
    custom_prompt = f"请分析这张图片，并判断图片中是否包含以下物品：{options_str}。" \
                   f"只需返回最匹配的一个选项，不需要其他解释。"
    
    try:
        # 调用图像分析
        result = analyzer.analyze_image(image_path, custom_prompt)
        
        print("\n=== 图像分析结果 ===")
        print(result)
        print("==================\n")
        
    except Exception as e:
        print(f"测试过程中发生错误：{str(e)}")

if __name__ == "__main__":
    test_image_recognition() 