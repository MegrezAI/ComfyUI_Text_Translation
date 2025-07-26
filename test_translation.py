
import sys
from dotenv import load_dotenv

load_dotenv()


def test_bing_translation():
    """测试Bing翻译功能"""
    print("🧪 开始测试Bing翻译功能...")
    
    try:
        from utils.translation import translators
        
        # 测试1：中文到英文
        print("\n📋 测试1：中文 → 英文")
        text1 = "你好，世界"
        result1 = translators(text1, translator="bing", source_language="zh", target_language="en")
        print(f"原文：{text1}")
        print(f"翻译：{result1}")
        
        # 测试2：英文到中文
        print("\n📋 测试2：英文 → 中文")
        text2 = "Hello, World!"
        result2 = translators(text2, translator="bing", source_language="en", target_language="zh")
        print(f"原文：{text2}")
        print(f"翻译：{result2}")
        
        # 测试3：日文到中文
        print("\n📋 测试3：日文 → 中文")
        text3 = "こんにちは"
        result3 = translators(text3, translator="bing", source_language="ja", target_language="zh")
        print(f"原文：{text3}")
        print(f"翻译：{result3}")
        
        # 测试4：自动检测语言
        print("\n📋 测试4：自动检测语言 → 英文")
        text4 = "这是一个测试"
        result4 = translators(text4, translator="bing", target_language="en")
        print(f"原文：{text4}")
        print(f"翻译：{result4}")
        
        # 测试5：空文本
        print("\n📋 测试5：空文本处理")
        result5 = translators("", translator="bing", target_language="en")
        print(f"空文本结果：'{result5}'")
        
        print("\n✅ 所有测试通过！Bing翻译功能正常")
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误：{e}")
        print("请确保已安装：pip install azure-ai-translation-text")
        return False
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def main():
    """主测试函数"""
    print("🚀 翻译功能测试开始")
    print("=" * 50)
    
    success = test_bing_translation()
    
    if success:
        print("\n🎉 测试完成！")
    else:
        print("\n💥 测试未通过，请检查配置")
        sys.exit(1)

if __name__ == "__main__":
    main()