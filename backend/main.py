from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import openai
import yt_dlp
import whisper
from pytube import YouTube
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_audio(youtube_url, filename="audio"):
    print(f"[1/5] 🚀 Начинаем скачивание аудио с {youtube_url}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,  # БЕЗ .mp3 здесь!!!
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
    print(f"[2/5] ✅ Аудио скачано: {filename}.mp3")
    return info_dict.get('title', 'Без названия')



def transcribe_audio(audio_path):
    print(f"[3/5] 🎧 Начинаем транскрипцию аудио: {audio_path}")
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    print(f"[4/5] ✅ Транскрипция завершена ({len(result['text'])} символов)")
    return result["text"]

def analyze_text(text):
    print("[5/5] 🧠 Отправляем текст в OpenAI на анализ...")
    max_chars = 3000
    if len(text) > max_chars:
        print(f"⚠️ Текст длиннее {max_chars} символов. Будет обрезан.")
        text = text[:max_chars]

    prompt = f"""
    Вот транскрипция видео:
    {text}

    Нужно:
    - 5-7 коротких буллетпоинтов о содержании
    - Главные важные моменты
    - Общее краткое описание в 2-3 предложениях.
    Ответь кратко и структурированно.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    print("✅ Ответ от OpenAI получен.")
    return response['choices'][0]['message']['content']

def get_video_title(youtube_url):
    print("🎬 Пытаемся получить название видео...")
    yt = YouTube(youtube_url)
    title = yt.title
    print(f"✅ Название видео: {title}")
    return title

@app.post("/analyze")
async def analyze(request: Request):
    body = await request.json()
    youtube_url = body["youtube_url"]

    print("\n========== Новый Запрос ==========")
    print(f"Получена ссылка: {youtube_url}")

    try:
        title = download_audio(youtube_url)  # <-- тут теперь получаем title сразу
        print(f"🎬 Название видео: {title}")

        transcript = transcribe_audio("audio.mp3")

        if not transcript.strip() or len(transcript.strip()) < 20:
            print("❌ Ошибка: Транскрипция пустая или слишком короткая.")
            return {"result": "❌ Ошибка: Не удалось получить нормальную транскрипцию. Видео слишком короткое, пустое или битое."}

        analysis = analyze_text(transcript)
        result_text = f"🎬 Название видео: {title}\n\n{analysis}"

        print("✅ Полный процесс завершен успешно!")
        return {"result": result_text}

    except Exception as e:
        print(f"💥 Ошибка в процессе: {str(e)}")
        return {"result": f"Ошибка: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
