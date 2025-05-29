import os
import json
from decouple import config
from google import genai
from google.genai import types
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


GEMINI_API_KEY = config('GEMINI_API_KEY')

def predict_spam_score(description: str) -> float:
    """
    Predicts the spam score for a given description using Google Gemini API.
    Returns a float between 0 and 1.
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set")
        return 0.0

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = (
        "Дайте строгое числовое значение от 0.0 до 1.0 – "
        "вероятность того, что этот текст является спамом, без дополнительных слов.\n"
        f"Текст: {description}\n"
        "Ответ (только число):"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=[prompt]
        )
        # Извлекаем сырое содержимое
        raw_obj = None
        if hasattr(response, 'candidates') and response.candidates:
            raw_obj = response.candidates[0].content
        elif hasattr(response, 'prediction'):
            raw_obj = response.prediction
        else:
            logger.error("No candidates or prediction in response")
            return 0.0

        # Преобразуем в строку
        raw = raw_obj if isinstance(raw_obj, str) else str(raw_obj)
        raw = raw.strip()
        logger.debug(f"Raw Gemini output: '{raw}'")

        # Ищем число вида 0.x или 1.0
        match = re.search(r"\b([01](?:\.\d+)?)\b", raw)
        if match:
            score = float(match.group(1))
            return max(0.0, min(score, 1.0))
        else:
            logger.error(f"Can't parse spam score from: '{raw}'")
            return 0.0
    except Exception as e:
        logger.exception(f"Error predicting spam score: {e}")
        return 0.0
