from yt_dlp import YoutubeDL

class Video:
    def __init__(self, url):
        self.url = url
        self.video_info = None
        self.stream = None
        
        # video information extraction
        self._get_video_info()

    def _get_video_info(self):
        try:
            options = {
                "format": "best",  # selects the best available format
                "noplaylist": True,  # without playlists
            }
            with YoutubeDL(options) as ydl:
                # extracts video information (not download)
                self.video_info = ydl.extract_info(self.url, download=False)
                
                # video download stream
                self.stream = ydl.extract_info(self.url, download=True)["formats"][0]
                
        except Exception as e:
            print("Error retrieving video information:", e)
            self.video_info = None

    def stahnout(self):
        try:
            # is there information about the video?
            if not self.video_info:
                raise ValueError("Video není dostupné")
            
            # get video title
            title = self.video_info.get("title", "video").replace("/", "-").replace("\\", "-")  # replaces characters
            safe_title = "".join(c for c in title if c.isalnum() or c in " _-")  # allowed characters for file name
            
            # YoutubeDL for downloading a file named
            with YoutubeDL({"outtmpl": f"static/videa/{safe_title}.mp4"}) as ydl:
                ydl.download([self.url])  # download video
            return True
        except Exception as e:
            print("Error downloading video:", e)
            return False

    def getInfo(self):
        if self.video_info:
            return [
                self.video_info.get("uploader", "Unknown author"),
                self.video_info.get("duration", 0),
                self.video_info.get("view_count", 0),
                f"{round(self.video_info.get('filesize', 0) / (1024 * 1024), 2)} MB",
                self.video_info.get("title", "Unknown title")
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
