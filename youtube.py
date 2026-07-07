import asyncio
import os
import re
from typing import Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from py_yt import VideosSearch

from config import XBIT_API_KEY, XBIT_API_URL, STORAGE_DIR

os.makedirs(STORAGE_DIR, exist_ok=True)


def _session():
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


def _clean(link: str) -> str:
    if "&" in link:
        link = link.split("&")[0]
    if "?si=" in link:
        link = link.split("?si=")[0]
    elif "&si=" in link:
        link = link.split("&si=")[0]
    return link


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def track(self, query: str, videoid: Union[bool, str] = None):
        """Search a song by name or link. Returns (details_dict, vidid)."""
        link = self.base + query if videoid else _clean(query)
        results = VideosSearch(link, limit=1)
        title = duration_min = duration_sec = vidid = yturl = thumbnail = None
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            duration_sec = 0
            if duration_min:
                try:
                    parts = duration_min.split(":")
                    if len(parts) == 3:
                        duration_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                    elif len(parts) == 2:
                        duration_sec = int(parts[0]) * 60 + int(parts[1])
                except ValueError:
                    duration_sec = 0
        if vidid is None:
            return None, None
        details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "duration_sec": duration_sec,
            "thumb": thumbnail,
        }
        return details, vidid

    # ===================================================================
    # DOWNLOAD — permanent NVMe storage cache first, then xBit API only
    # ===================================================================
    async def download(self, vidid: str, video: bool = False):
        """
        Returns local filesystem path to the audio/video file.
        1. Check STORAGE_DIR cache first (instant, no API call).
        2. If missing, fetch stream URL from xBit API only (no yt-dlp).
        3. Download & permanently save under STORAGE_DIR for next time.
        """
        ext = "mp4" if video else "mp3"
        local_path = os.path.join(STORAGE_DIR, f"{vidid}.{ext}")

        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            return local_path

        stream_url = await self._xbit_fetch(vidid, want_video=video)
        if not stream_url:
            return None

        return await self._save_to_storage(stream_url, local_path)

    async def _xbit_fetch(self, vidid: str, want_video: bool = False):
        loop = asyncio.get_running_loop()

        def _call():
            try:
                session = _session()
                headers = {"x-api-key": XBIT_API_KEY, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                resp = session.get(f"{XBIT_API_URL}/info/{vidid}", headers=headers, timeout=60)
                print(f"[xBit] GET /info/{vidid} -> status={resp.status_code}")
                data = resp.json()
                print(f"[xBit] response: {data}")
                session.close()
                if data.get("status") == "success":
                    url = data.get("video_url") if want_video else data.get("audio_url")
                    if not url:
                        print(f"[xBit] success=True but no {'video_url' if want_video else 'audio_url'} in response")
                    return url
                print(f"[xBit] status != success, full response above")
                return None
            except Exception as e:
                print(f"[xBit] EXCEPTION for {vidid}: {type(e).__name__}: {e}")
                return None

        return await loop.run_in_executor(None, _call)

    async def _save_to_storage(self, url: str, local_path: str):
        loop = asyncio.get_running_loop()

        def _dl():
            tmp_path = local_path + ".part"
            try:
                session = _session()
                resp = session.get(url, stream=True, timeout=120, allow_redirects=True)
                resp.raise_for_status()
                with open(tmp_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                session.close()
                os.rename(tmp_path, local_path)
                return local_path
            except Exception:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                return None

        return await loop.run_in_executor(None, _dl)


YouTube = YouTubeAPI()
