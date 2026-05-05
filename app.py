from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from datetime import datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
def root():
    return {"GloireMedia": "API TikTok Live", "status": "Amen"}

@app.get("/feed")
def get_feed():
    posts = supabase.table("posts").select("*, users(username, avatar_url)").order("created_at", desc=True).limit(20).execute()
    return posts.data

@app.post("/upload")
async def upload_video(file: UploadFile = File(...), caption: str = Form(""), verse: str = Form("")):
    content = await file.read()
    file_path = f"videos/{datetime.now().timestamp()}_{file.filename}"
    supabase.storage.from_("gloiremedia-videos").upload(file_path, content, {"content-type": file.content_type})
    video_url = supabase.storage.from_("gloiremedia-videos").get_public_url(file_path)
    
    supabase.table("users").upsert({"id": "00000000-0000-0000-0000-000000000001", "username": "pastor_chris_official"}).execute()
    supabase.table("posts").insert({
        "video_url": video_url, "caption": caption, "verse_ref": verse,
        "user_id": "00000000-0000-0000-0000-000000000001"
    }).execute()
    return {"status": "Alléluia", "url": video_url}
