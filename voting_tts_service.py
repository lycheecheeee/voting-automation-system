"""
TTS Module for Voting Automation System
Supports Edge TTS and browser Web Speech API fallback
"""
import os
import asyncio
from typing import Optional

class TTSService:
    """Text-to-Speech service with multiple backends"""
    
    def __init__(self):
        self.default_voice = os.getenv('TTS_VOICE', 'zh-HK-HiuMaanNeural')
        self.tts_mode = os.getenv('TTS_MODE', 'web_speech')  # web_speech or edge_tts
        
    async def generate_audio(self, text: str, voice: Optional[str] = None) -> Optional[bytes]:
        """
        Generate audio from text
        
        Args:
            text: Text to convert to speech
            voice: Voice ID (optional)
            
        Returns:
            Audio bytes or None if failed
        """
        voice = voice or self.default_voice
        
        if self.tts_mode == 'edge_tts':
            return await self._generate_edge_tts(text, voice)
        else:
            # Return JavaScript code for Web Speech API
            return self._get_web_speech_code(text, voice)
    
    async def _generate_edge_tts(self, text: str, voice: str) -> Optional[bytes]:
        """Generate audio using Edge TTS"""
        try:
            import edge_tts
            
            communicate = edge_tts.Communicate(text, voice)
            audio_data = b''
            
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    audio_data += chunk['data']
            
            return audio_data
            
        except ImportError:
            print("⚠️  edge-tts not installed. Run: pip install edge-tts")
            return None
        except Exception as e:
            print(f"❌ Edge TTS error: {e}")
            return None
    
    def _get_web_speech_code(self, text: str, voice: str) -> str:
        """Generate JavaScript code for Web Speech API"""
        lang_map = {
            'zh-HK': 'zh-HK',
            'zh-TW': 'zh-TW',
            'zh-CN': 'zh-CN',
            'en-US': 'en-US'
        }
        
        # Extract language from voice ID
        lang = 'zh-HK'
        for key in lang_map:
            if key in voice:
                lang = lang_map[key]
                break
        
        return f"""
        <script>
            const utterance = new SpeechSynthesisUtterance("{text}");
            utterance.lang = '{lang}';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            speechSynthesis.speak(utterance);
        </script>
        """


# Global instance
tts_service = TTSService()


if __name__ == '__main__':
    # Test the service
    import sys
    
    test_text = "你好，這是粵語測試"
    
    if len(sys.argv) > 1 and sys.argv[1] == '--edge':
        # Test Edge TTS
        audio = asyncio.run(tts_service.generate_audio(test_text))
        if audio:
            with open('test_tts.mp3', 'wb') as f:
                f.write(audio)
            print(f"✅ Audio saved: test_tts.mp3 ({len(audio)} bytes)")
        else:
            print("❌ TTS generation failed")
    else:
        # Test Web Speech API
        js_code = tts_service.generate_audio(test_text)
        print("Web Speech API Code:")
        print(js_code)
