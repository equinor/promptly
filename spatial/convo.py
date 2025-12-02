import base64
import io
import os

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import fsspec


__ = load_dotenv("../.env")

MODELS = {
    'openai': ['gpt-4o-mini', 'gpt-4.1', 'o4-mini-2025-04-16', 'gpt-5.1-2025-11-13'],
    'anthropic': ['claude-sonnet-4-20250514', 'claude-sonnet-4-5-20250929'],
    'mistral': ['mistral-small-latest', 'mistral-medium-latest', 'mistral-large-latest'],
    'perplexity': ['sonar'],
    'gemini': ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-3-pro-preview'],
    'deepSeek': ['deepseek-chat'],
    'xai': ['grok-3', 'grok-4', 'grok-4-1-fast-non-reasoning', 'grok-4-1-fast-reasoning'],
    'qwen': ['qwen-plus'],
}

PROVIDERS = {v: k for k, l in MODELS.items() for v in l}


def get_image_data(image_uri, provider=None):
    """Make an image content dict."""
    image_format = image_uri.split('.')[-1].lower().replace('jpg', 'jpeg')
    image_media_type = f"image/{image_format}"
    with fsspec.open(image_uri, mode='rb') as file:
        image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{image_media_type};base64,{image_b64}", image.size


class Convo:
    provider = None
    model = None
    notebook = False

    def __init__(self, system=None):
        """Start a new conversation."""
        urls = {
            'xai': 'https://api.x.ai/v1',
            'perplexity': "https://api.perplexity.ai",
            'anthropic': "https://api.anthropic.com/v1",
            'openai': "https://api.openai.com/v1",
            'mistral': "https://api.mistral.ai/v1",
            'gemini': "https://generativelanguage.googleapis.com/v1beta/openai",
            'deepseek': 'https://api.deepseek.com',  # Currently DeepSeek-V3-0324
            'qwen': 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
        }
        self.log = []
        self.base_url = urls[Convo.provider]
        self.api_key = os.environ[f'{Convo.provider.upper()}_API_KEY']
        self.messages = []
        if system is None:
            self.system = "You are a helpful assistant."
        else:
            self.system = system
        self.messages.append({"role": "system", "content": self.system})

    def ask(self, prompt, image_uri=None):
        """Send a prompt in the current Convo."""
        if Convo.model is None:
            raise ValueError("Set the Convo.model attribute before asking.")

        # Build content for this prompt.
        content = []
        if image_uri:
            image_data, (width, height) = get_image_data(image_uri)
            w, h = 256, 20 + 256 * height / width  # Add div padding to h.
            image_content = {"type": "image_url",
                             "image_url": {"url": image_data},
                            }
            content.append(image_content)
        elif Convo.notebook:
            # Create an empty pixel for the notebook repr.
            image_data = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
            w, h = 0, 0
        content.append({"type": "text", "text": prompt})
        self.messages.append({"role": "user", "content": content})

        # Send this content.
        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        completion = client.chat.completions.create(
            model=Convo.model,
            messages=self.messages,
        )

        # Deal with the response.
        self.log.append(completion)
        response = completion.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': response})
        if Convo.notebook:
            return f"""<div style="border: 3px solid #aaaaee; border-radius: 5px; background-color: #eeeeff; padding: 5px 10px 5px 10px; min-height: {h}px;">
                  <img src="{image_data}" style="float:right; width: {w}px; margin: 10px;" />
                  <h4>{prompt}</h4>
                  <hr height="10px" color="#aaaaee" />
                  <h4 style="color: #aaaaee;">{self.provider}/{self.model}</h4>
                  \n{response}\n</div>"""
        else:
            return response.strip()

    def history(self):
        """See previous messages (text prompt and response only)."""
        return self.messages

    def log(self):
        """See previous response objects."""
        return self.log