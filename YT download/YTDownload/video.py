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
                "format": "best",  # choose the best available format
                "noplaylist": True,  # disable playlists
            }
            with YoutubeDL(options) as ydl:
                # load video information
                self.video_info = ydl.extract_info(self.url, download=False)
        except Exception as e:
            print("Error retrieving video information:", e)
            self.video_info = None

    def stahnout(self):
        try:
            if not self.video_info:
                raise ValueError("Video is not available.")
            
            title = self.video_info.get("title", "video").replace("/", "-").replace("\\", "-")
            safe_title = "".join(c for c in title if c.isalnum() or c in " _-")
            
            output_path = "static/videa"
            output_file = f"{output_path}/{safe_title}.mp4"
            
            options = {
                "outtmpl": output_file,
                "noplaylist": True,  # disable playlists
            }
            with YoutubeDL(options) as ydl:
                ydl.download([self.url])  # downloanding video
            
            self.downloaded_path = output_file
            return True
        except Exception as e:
            print("Error downloading video:", e)
            return False


    def getInfo(self):
        if self.video_info:
            filesize = self.video_info.get("filesize")
            size_str = (
                f"{round(filesize / (1024 * 1024), 2)} MB" if filesize else "Unknown size"
            )
            return [
                self.video_info.get("uploader", "Unknown author"),
                self.video_info.get("duration", 0),
                self.video_info.get("view_count", 0),
                size_str,  # file size
                self.video_info.get("title", "Unknown title"),
            ]
        return []


    def odkaz(self):
        # is there a path to the downloaded video
        if hasattr(self, "downloaded_path"):
            return self.downloaded_path
        return ""

    def getObrazek(self):
        if self.video_info:
            return self.video_info.get("thumbnail", "")
        return ""
