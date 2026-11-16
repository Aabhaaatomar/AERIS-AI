"""
AERIS AI - LLM Client
Direct integration with official Google GenAI SDK (google-genai)
with REST API fallback for maximum resilience.
"""
import requests
import json
from typing import List, Dict, Any, Optional

try:
    from google import genai
    from google.genai import types, errors as genai_errors
    HAS_GENAI_SDK = True
except ImportError:
    HAS_GENAI_SDK = False

class LLMClient:
    """Client for Google Gemini and OpenAI-compatible LLM providers."""
    
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str, provider: str = "gemini", model: Optional[str] = None):
        self.api_key = api_key.strip() if api_key else ""
        self.provider = provider.lower()
        
        # Clean and normalize model names
        if not model:
            self.model = "gemini-2.0-flash" if self.provider == "gemini" else "gpt-4o-mini"
        else:
            clean_m = model.split(" ")[0].strip()
            self.model = clean_m if clean_m else "gemini-2.0-flash"

        # Initialize Google GenAI client if available and using Gemini
        self.genai_client = None
        if self.provider == "gemini" and self.api_key and HAS_GENAI_SDK:
            try:
                self.genai_client = genai.Client(api_key=self.api_key)
            except Exception:
                self.genai_client = None

    def generate(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_instruction: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: int = 1500
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
        if not self.api_key or len(self.api_key) < 6:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": "Gemini API Key is missing. Please configure your key in sidebar under 'AI Engine Settings' or via .env.",
                "error_type": "MISSING_KEY"
            }

        if self.provider == "gemini":
            # Attempt official GenAI SDK first
            if self.genai_client is not None:
                sdk_result = self._call_gemini_sdk(prompt, conversation_history, system_instruction, temperature, max_tokens)
                if sdk_result["success"] or sdk_result.get("error_type") in ["AUTH_ERROR", "RATE_LIMIT"]:
                    return sdk_result
            
            # Fallback to direct REST API
            return self._call_gemini_rest(prompt, conversation_history, system_instruction, temperature, max_tokens)
            
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

    def _call_gemini_sdk(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]],
        system_instruction: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Execute Gemini API call using official google-genai SDK."""
        try:
            # Build conversation turns as types.Content
            contents = []
            if conversation_history:
                for msg in conversation_history[-10:]:
                    role = "user" if msg.get("role") == "user" else "model"
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg.get("content", ""))]
                        )
                    )
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            )

            # Build config
            config_kwargs: Dict[str, Any] = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95
            }
            if system_instruction:
                config_kwargs["system_instruction"] = system_instruction

            config = types.GenerateContentConfig(**config_kwargs)

            # Generate content
            response = self.genai_client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config
            )

            if response and response.text:
                return {
                    "success": True,
                    "text": response.text.strip(),
                    "model": self.model,
                    "error": None,
                    "error_type": None
                }
            else:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": "Gemini API returned an empty completion response.",
                    "error_type": "EMPTY_RESPONSE"
                }

        except genai_errors.ClientError as ce:
            code = getattr(ce, "code", 400)
            msg = getattr(ce, "message", str(ce))
            if code in [400, 403]:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Authentication Error ({code}): Invalid or restricted Gemini API key. Please check your key in settings.",
                    "error_type": "AUTH_ERROR"
                }
            elif code == 429:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": "Rate Limit Exceeded (HTTP 429): Your Gemini API quota has been exceeded. Please wait a moment or check quota.",
                    "error_type": "RATE_LIMIT"
                }
            elif code == 404:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Model Not Found (HTTP 404): The model '{self.model}' was not found. Try 'gemini-1.5-flash' or 'gemini-2.0-flash'.",
                    "error_type": "MODEL_NOT_FOUND"
                }
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": f"Gemini Client Error ({code}): {msg}",
                "error_type": "CLIENT_ERROR"
            }

        except genai_errors.ServerError as se:
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": f"Google Server Error: {str(se)}. Gemini services are experiencing intermittent issues.",
                "error_type": "SERVER_ERROR"
            }

        except Exception as e:
            err_str = str(e)
            if "getaddrinfo" in err_str or "ConnectError" in err_str or "Timeout" in err_str:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Network Error: Could not connect to Gemini servers ({err_str[:120]}).",
                    "error_type": "NETWORK_ERROR"
                }
            return {
                "success": False,
                "text": "",
                "model": self.model,
                "error": f"Gemini API Execution Exception: {err_str}",
                "error_type": "SDK_EXCEPTION"
            }

    def _call_gemini_rest(
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
        
        contents = []
        if conversation_history:
            for msg in conversation_history[-10:]:
                role = "user" if msg.get("role") == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("content", "")}]
                })
                
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
                        "text": text.strip(),
                        "model": self.model,
                        "error": None,
                        "error_type": None
                    }
                except (KeyError, IndexError) as parse_err:
                    return {
                        "success": False,
                        "text": "",
                        "model": self.model,
                        "error": f"Could not parse Gemini API response payload: {str(parse_err)}",
                        "error_type": "PARSE_ERROR"
                    }
            elif response.status_code in [400, 403]:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Authentication Error ({response.status_code}): Invalid or restricted Gemini API key.",
                    "error_type": "AUTH_ERROR"
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": "Rate Limit Exceeded (HTTP 429): Quota exceeded. Please wait a moment.",
                    "error_type": "RATE_LIMIT"
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Model Not Found (HTTP 404): '{self.model}' is unavailable on the REST API endpoint.",
                    "error_type": "MODEL_NOT_FOUND"
                }
            else:
                return {
                    "success": False,
                    "text": "",
                    "model": self.model,
                    "error": f"Gemini API HTTP Error {response.status_code}: {response.text[:200]}",
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
            for msg in conversation_history[-10:]:
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
                    "text": text.strip(),
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
