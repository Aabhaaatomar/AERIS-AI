"""
AERIS AI - LLM Client
Direct REST integration for Google Gemini and OpenAI-compatible APIs without heavy SDKs.
"""
import requests
import json
from typing import List, Dict, Any, Optional

class LLMClient:
    """Lightweight REST client for LLM providers."""
    
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str, provider: str = "gemini", model: Optional[str] = None):
        self.api_key = api_key.strip() if api_key else ""
        self.provider = provider.lower()
        if not model:
            self.model = "gemini-1.5-flash" if self.provider == "gemini" else "gpt-4o-mini"
        else:
            self.model = model

    def generate(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_instruction: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: int = 1200
    ) -> Dict[str, Any]:
        """
        Send a completion request to the configured LLM API.
        
        Returns:
            dict: {
                "success": bool,
                "text": str,
                "model": str,
                "error": Optional[str],
                "error_type": Optional[str]
            }
        """
        if not self.api_key:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": "API Key is missing. Please configure your key in settings or environment.",
                "error_type": "MISSING_KEY"
            }

        if self.provider == "gemini":
            return self._call_gemini(prompt, conversation_history, system_instruction, temperature, max_tokens)
        elif self.provider in ["openai", "groq"]:
            return self._call_openai_compatible(prompt, conversation_history, system_instruction, temperature, max_tokens)
        else:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": f"Unsupported LLM provider: {self.provider}",
                "error_type": "UNSUPPORTED_PROVIDER"
            }

    def _call_gemini(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]],
        system_instruction: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Execute Gemini REST API generateContent call."""
        url = f"{self.GEMINI_BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        
        headers = {"Content-Type": "application/json"}
        
        # Build contents structure
        contents = []
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-8:]:  # keep last 8 turns for context window efficiency
                role = "user" if msg.get("role") == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("content", "")}]
                })
                
        # Add current user prompt
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })
        
        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95
            }
        }
        
        # Add system instruction if provided
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                try:
                    candidate = data["candidates"][0]
                    text = candidate["content"]["parts"][0]["text"]
                    return {
                        "success": True,
                        "text": text,
                        "model": self.model,
                        "error": None,
                        "error_type": None
                    }
                except (KeyError, IndexError) as parse_err:
                    return {
                        "success": False,
                        "text": "",
                        "model": self.model,
                        "error": f"Could not parse Gemini API response: {str(parse_err)}",
                        "error_type": "PARSE_ERROR"
                    }
            elif response.status_code in [400, 403]:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Authentication / Permission Error ({response.status_code}): Invalid or restricted Gemini API key.",
                    "error_type": "AUTH_ERROR"
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": "Rate limit exceeded on Gemini API. Please wait a moment or verify your quota.",
                    "error_type": "RATE_LIMIT"
                }
            else:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Gemini API returned HTTP {response.status_code}: {response.text[:200]}",
                    "error_type": "HTTP_ERROR"
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": "Connection timed out while contacting Gemini API (20s).",
                "error_type": "TIMEOUT"
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": f"Network error contacting Gemini API: {str(req_err)}",
                "error_type": "NETWORK_ERROR"
            }

    def _call_openai_compatible(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]],
        system_instruction: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Execute OpenAI compatible chat completions API call."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
            
        if conversation_history:
            for msg in conversation_history[-8:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
                
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(self.OPENAI_BASE_URL, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                data = response.json()
                text = data["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "text": text,
                    "model": self.model,
                    "error": None,
                    "error_type": None
                }
            else:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"API returned HTTP {response.status_code}: {response.text[:200]}",
                    "error_type": "HTTP_ERROR"
                }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": f"OpenAI API call failed: {str(e)}",
                "error_type": "NETWORK_ERROR"
            }
