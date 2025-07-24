from pyannote.audio.models.embedding.wespeaker.convert import model

from gpt_functions import  get_current_time,tools
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_ai_response(messages, tools = None) :
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = messages,
        tools = tools
    )
    return response