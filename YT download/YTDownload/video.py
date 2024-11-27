from yt_dlp import YoutubeDL

class Video:
    def __init__(self, url):
        self.url = url
        self.video_info = None
        self.stream = None
        
        # extrakce informací o videu
        self._get_video_info()

    def _get_video_info(self):
        try:
            options = {
                "format": "best",  # vybere nejlepší dostupný formát
                "noplaylist": True,  # bez playlistů
            }
            with YoutubeDL(options) as ydl:
                # extrahuje informace o videu (ne stažení)
                self.video_info = ydl.extract_info(self.url, download=False)
                
                # stream pro stáhnutí videa
                self.stream = ydl.extract_info(self.url, download=True)["formats"][0]
                
        except Exception as e:
            print("Chyba při získávání informací o videu:", e)
            self.video_info = None

    def stahnout(self):
        try:
            # máme informace o videu?
            if not self.video_info:
                raise ValueError("Video není dostupné")
            
            # získání názvu videa
            title = self.video_info.get("title", "video").replace("/", "-").replace("\\", "-")  # nahradí znaky
            safe_title = "".join(c for c in title if c.isalnum() or c in " _-")  # povolené znaky pro název souboru
            
            # YoutubeDL pro stahování souboru s názvem
            with YoutubeDL({"outtmpl": f"static/videa/{safe_title}.mp4"}) as ydl:
                ydl.download([self.url])  # stáhnout video
            return True
        except Exception as e:
            print("Chyba při stahování videa:", e)
            return False

    def getInfo(self):
        if self.video_info:
            return [
                self.video_info.get("uploader", "Neznámý autor"),
                self.video_info.get("duration", 0),
                self.video_info.get("view_count", 0),
                f"{round(self.video_info.get('filesize', 0) / (1024 * 1024), 2)} MB",
                self.video_info.get("title", "Neznámý název")
            ]
        return []

    def odkaz(self):
        if self.video_info:
            return f"static/videa/{self.video_info.get('id')}.mp4"
        return ""

    def getObrazek(self):
        if self.video_info:
            return self.video_info.get("thumbnail", "")
        return ""