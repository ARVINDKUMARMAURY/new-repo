import asyncio
import os
import re
from typing import Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from py_yt import VideosSearch

from config import BASE_URL, API_KEY, STORAGE_DIR

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

    def _build_url(self, vidid: str, video: bool) -> str:
        kind = "video" if video else "audio"
        return f"{BASE_URL}/download?url={vidid}&type={kind}&api_key={API_KEY}"

    def _ext(self, video: bool) -> str:
        # Artistbots returns webm for audio, mp4 for video
        return "mp4" if video else "webm"

    async def _check_reachable(self, url: str) -> bool:
        """Quick HEAD-style check (falls back to ranged GET) that the link is good."""
        loop = asyncio.get_running_loop()

        def _call():
            try:
                session = _session()
                # Some Workers endpoints don't support HEAD, so do a tiny ranged GET.
                headers = {"Range": "bytes=0-0"}
                resp = session.get(url, timeout=20, headers=headers, stream=True)
                ok = resp.status_code in (200, 206)
                ct = resp.headers.get("content-type", "")
                print(f"[Artistbots] check -> status={resp.status_code} content-type={ct}")
                resp.close()
                session.close()
                if not ok:
                    return False
                if ct and "json" in ct.lower():
                    # An error JSON came back instead of a media file
                    return False
                return True
            except Exception as e:
                print(f"[Artistbots] check EXCEPTION: {type(e).__name__}: {e}")
                return False

        return await loop.run_in_executor(None, _call)

    async def download(self, vidid: str, video: bool = False):
        local_path = os.path.join(STORAGE_DIR, f"{vidid}.{self._ext(video)}")

        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            return local_path

        url = self._build_url(vidid, video)
        saved_path = await self._save_to_storage(url, local_path)
        return saved_path

    async def get_playable(self, vidid: str, video: bool = False):
        """
        Returns a LOCAL file path that is guaranteed to be fully downloaded
        before it's handed to pytgcalls. This avoids ffprobe being pointed
        at a remote URL that isn't fully readable, or a partially-downloaded
        file, both of which cause 'ffprobe not installed' / JSON decode
        crashes in pytgcalls.

        - If the file is already cached locally, returns it instantly.
        - Otherwise, downloads it fully (via curl) and only then returns
          the local path. This is a bit slower on cache-miss than the old
          "stream from URL immediately" approach, but it's reliable.
        """
        local_path = os.path.join(STORAGE_DIR, f"{vidid}.{self._ext(video)}")

        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            return local_path

        url = self._build_url(vidid, video)
        ok = await self._check_reachable(url)
        if not ok:
            print(f"[Artistbots] link not reachable/usable for {vidid}")
            return None

        # Wait for the FULL download to finish before returning anything.
        # This is the key fix: no more asyncio.create_task() fire-and-forget
        # background caching while returning a possibly-unprobable URL.
        saved_path = await self._save_to_storage(url, local_path)
        if not saved_path:
            print(f"[Artistbots] download failed for {vidid}")
            return None

        return saved_path

    async def _save_to_storage(self, url: str, local_path: str):
        tmp_path = local_path + ".part"
        try:
            print(f"[save] Starting download to {local_path}")
            proc = await asyncio.create_subprocess_exec(
                "curl", "-L", url, "-o", tmp_path, "-s", "--max-time", "180"
            )
            await proc.communicate()

            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) < 50_000:
                print(f"[save] Download too small or missing for {local_path}")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                return None

            os.rename(tmp_path, local_path)
            print(f"[save] Done: {local_path}")
            return local_path

        except Exception as e:
            print(f"[save] EXCEPTION saving {local_path}: {type(e).__name__}: {e}")
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return None


YouTube = YouTubeAPI()
