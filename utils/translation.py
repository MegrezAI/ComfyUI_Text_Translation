
def translators(text: str, translator: str = "bing", source_language="auto", target_language="en", timeout: float = 10.0):
    if not text:
        return ""
    
    # Use Azure Text Translation SDK for "bing" translator
    if translator.lower() == "bing":
        try:
            # Import our new Bing translator implementation
            from .bing_translator import create_bing_translator
            
            bing_translator = create_bing_translator()
            
            print("使用 Azure Bing Translator API 进行翻译")
            # 只需要传 source_language 和 target_language
            return bing_translator.translate(
                text=text,
                target_language=target_language,
                source_language=source_language
            )
                
        except ImportError:
            # Fallback to original translators library if our module or Azure SDK not available
            try:
                import translators
                print("Azure SDK 不可用，回退到 translators 库 (bing)")
                result = translators.translate_text(
                    query_text=text, 
                    translator=translator,
                    from_language=source_language, 
                    to_language=target_language, 
                    timeout=timeout
                )
                return result
            except Exception as e:
                raise Exception(f"Error: Translation failed, Message: {e}")
        except Exception as e:
            print(f"Azure Bing Translator API 调用失败，错误信息: {e}")
            print("回退到 translators 库 (bing)")
            try:
                import translators
                result = translators.translate_text(
                    query_text=text, 
                    translator=translator,
                    from_language=source_language, 
                    to_language=target_language, 
                    timeout=timeout
                )
                return result
            except Exception as e2:
                raise Exception(f"Error: Translation failed, Message: {e2}")
    else:
        # Use original translators library for other providers
        try:
            import translators
            print(f"[LOG] 使用 translators 库 ({translator}) 进行翻译")
            result = translators.translate_text(
                query_text=text, 
                translator=translator,
                from_language=source_language, 
                to_language=target_language, 
                timeout=timeout
            )
            return result
        except Exception as e:
            raise Exception(f"Error: Translation failed, Message: {e}")

def get_translator():
    try:
        # Return supported translators
        return "Bing (Azure SDK)\nGoogle\nAlibaba\nApertium\nArgos\nBaidu\nCaiyun\nCloudTranslation\nDeepL\nElia\nHujiang\nIciba\nIflytek\nIflyrec\nItranslate\nJudic\nLanguageWire\nLingvanex\nNiutrans\nMglip\nMirai\nModernMt\nMyMemory\nPapago\nQqFanyi\nQqTranSmart\nReverso\nSogou\nSysTran\nTilde\nTranslateCom\nTranslateMe\nUtibet\nVolcEngine\nYandex\nYeekit\nYoudao"
    except Exception as e:
        raise Exception(f"Error: Translation failed, Message: {e}")


    
