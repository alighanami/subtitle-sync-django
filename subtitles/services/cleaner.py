import re
from bs4 import BeautifulSoup

class Cleaner:


    def clean(self, raw_text: str):
        if not raw_text or not isinstance(raw_text, str):
            return raw_text

        cleaned_lines = []

        for line in raw_text.splitlines():
            stripped = line.strip()

            if stripped == "":
                cleaned_lines.append("")
                continue

            if stripped.upper().startswith("WEBVTT"):
                cleaned_lines.append("WEBVTT")
                continue

            if re.fullmatch(r"\d+", stripped):
                cleaned_lines.append(stripped)
                continue

            if "-->" in stripped:
                cleaned_lines.append(stripped)
                continue

            cleaned_line = self._clean_caption_text(stripped)
            cleaned_lines.append(cleaned_line)

        return "\n".join(cleaned_lines)

    def _clean_caption_text(self, text_line: str) -> str:


        soup = BeautifulSoup(text_line, "html.parser")
        clean_text = soup.get_text(separator=" ")

        clean_text = clean_text.rstrip("+").strip()

        clean_text = re.sub(r"\s+", " ", clean_text)

        return clean_text.strip()
