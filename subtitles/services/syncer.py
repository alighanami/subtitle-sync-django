from io import StringIO
from typing import  Optional
from webvtt import WebVTT


class SubtitleSyncer:
    def _read_vtt_from_memory(self, text: str):
        memory_buffer: StringIO = StringIO(text)
        vtt_object: WebVTT = WebVTT().read_buffer(memory_buffer)
        return vtt_object

    def sync(self, primary_text: str, secondary_text: Optional[str] = None):
        primary_vtt: WebVTT = self._read_vtt_from_memory(primary_text)

        if secondary_text:
            secondary_vtt: WebVTT = self._read_vtt_from_memory(secondary_text)
            secondary_count = len(secondary_vtt)
        else:
            secondary_count = 0

        return {
            "status": "success",
            "message": "زیرنویس‌ها پردازش شدند.",
            "primary_caption_count": len(primary_vtt),
            "secondary_caption_count": secondary_count,
        }
