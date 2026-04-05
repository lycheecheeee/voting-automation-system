"""
AI Client for Voting Automation System
Supports NVIDIA NIM, OpenRouter, and local Ollama
"""
import requests
import os
import json
from typing import Optional

class AIClient:
    """Unified AI API client with fallback support"""
    
    def __init__(self):
        self.nvidia_key = os.getenv('NVIDIA_API_KEY')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.nvidia_base_url = os.getenv('NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1')
        self.openrouter_base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.default_model = os.getenv('AI_MODEL', 'moonshotai/kimi-k2.5')
        
    def generate_text(self, prompt: str, model: Optional[str] = None, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate text using available AI API
        
        Args:
            prompt: Input prompt
            model: Model name (optional)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or None if failed
        """
        model = model or self.default_model
        
        # Try NVIDIA first
        if self.nvidia_key:
            try:
                return self._call_nvidia(prompt, model, max_tokens)
            except Exception as e:
                print(f"⚠️  NVIDIA API failed: {e}, trying OpenRouter...")
        
        # Fallback to OpenRouter
        if self.openrouter_key:
            try:
                return self._call_openrouter(prompt, max_tokens)
            except Exception as e:
                print(f"⚠️  OpenRouter API failed: {e}")
        
        print("❌ All AI APIs failed")
        return None
    
    def _call_nvidia(self, prompt: str, model: str, max_tokens: int) -> str:
        """Call NVIDIA NIM API"""
        url = f"{self.nvidia_base_url}/chat/completions"
        
        headers = {
            'Authorization': f'Bearer {self.nvidia_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': 0.7,
            'top_p': 1.0
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    def _call_openrouter(self, prompt: str, max_tokens: int) -> str:
        """Call OpenRouter API"""
        url = f"{self.openrouter_base_url}/chat/completions"
        
        headers = {
            'Authorization': f'Bearer {self.openrouter_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://voting-automation.local',
            'X-Title': 'Voting Automation System'
        }
        
        payload = {
            'model': 'nvidia/nemotron-3-super-120b-a12b:free',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']


# Global instance
ai_client = AIClient()


if __name__ == '__main__':
    # Test the client
    test_prompt = "Generate a voting question about international politics in Traditional Chinese"
    result = ai_client.generate_text(test_prompt)
    
    if result:
        print("✅ AI Generation successful!")
        print(result[:200])
    else:
        print("❌ AI Generation failed")
