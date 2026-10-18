"""Build the local transcript search page for the UNED course.

Reads the five class transcriptions from private/uned/clase-N.txt, the mind map
(artifacts/curso-uned-mapa-mental.html) and the Spanish half of the Curso UNED tab
of the main page, and writes private/buscar-curso-uned.html with all of it inline.

The output holds the lecturer's full transcripts, so it stays in the gitignored
private/ folder and is never committed or published.

    python scripts/build_uned_search.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
PRIVATE = ROOT / "private"
TEMPLATE = Path(__file__).with_name("uned-search.tpl.html")
OUT = PRIVATE / "buscar-curso-uned.html"

# Longest caption-like segment a hit shows; the transcripts often run on without punctuation
MAX_SEGMENT_WORDS = 40
PARAGRAPH_CHARS = 900

# Recordings of each class on UNED's INTECCA portal
VIDEO_URLS = {
    1: "https://www.intecca.uned.es/portal/grabacion?ID_Sala=3&ID_Grabacion=884774&hashData=b1c7e18cdbcc711e72137ad4062de3d5&paramsToCheck=SURfR3JhYmFjaW9uLElEX1NhbGEs",
    2: "https://www.intecca.uned.es/portal/grabacion?ID_Sala=3&ID_Grabacion=888749&hashData=f810265829f72467c8b9a201a8b21faa&paramsToCheck=SURfR3JhYmFjaW9uLElEX1NhbGEs",
    3: "https://www.intecca.uned.es/portal/grabacion?ID_Sala=3&ID_Grabacion=895813&hashData=5ea08b26b75fc4cb016347b9333213b1&paramsToCheck=SURfR3JhYmFjaW9uLElEX1NhbGEs",
    4: "https://www.intecca.uned.es/portalavip/grabacion.php?ID_Sala=3&ID_Grabacion=899417&hashData=bba0d981a1733675b01315666f4c38b7&paramsToCheck=SURfR3JhYmFjaW9uLElEX1NhbGEs",
    5: "https://www.intecca.uned.es/portalavip/grabacion.php?ID_Sala=3&ID_Grabacion=903269&hashData=ec3895f1a16f6dc1dcd48cbcd75f1b32&paramsToCheck=SURfR3JhYmFjaW9uLElEX1NhbGEs",
}


def strip_tags(fragment):
    text = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def segments_of(text):
    """Split a transcript into sentences, cutting run-on stretches into shorter pieces."""
    text = re.sub(r"\s+", " ", text).strip()
    out = []
    for sentence in re.split(r"(?<=[.?!])\s+", text):
        words = sentence.split(" ")
        for i in range(0, len(words), MAX_SEGMENT_WORDS):
            out.append(" ".join(words[i : i + MAX_SEGMENT_WORDS]))
    return out


def paragraph_starts(segments):
    """Index of the first segment of each ~900-character paragraph."""
    starts, length = [0], 0
    for i, segment in enumerate(segments):
        length += len(segment) + 1
        if length >= PARAGRAPH_CHARS and i + 1 < len(segments):
            starts.append(i + 1)
            length = 0
    return starts


def class_number(label):
    match = re.search(r"Clase (\d)", label)
    return int(match.group(1)) if match else 0  # 0 = "Todo el curso"


def read_mind_map():
    source = (ARTIFACTS / "curso-uned-mapa-mental.html").read_text(encoding="utf8")
    entries = []
    for branch in re.findall(r'<article class="branch.*?</article>', source, re.S):
        label = strip_tags(re.search(r'<span class="branch-num">(.*?)</span>', branch, re.S).group(1))
        n = class_number(label)
        entries.append([n, "Mapa mental", strip_tags(re.search(r"<h3>(.*?)</h3>", branch, re.S).group(1))])
        for leaf in re.findall(r"<li>(.*?)</li>", branch, re.S):
            entries.append([n, "Mapa mental", strip_tags(leaf)])
    return entries


def read_tab():
    """Day cards and note cards of the Spanish block of the Curso UNED tab."""
    source = (ARTIFACTS / "ancient-egypt-history-main-points.html").read_text(encoding="utf8")
    start = source.index('<div data-lang="es"', source.index('id="panel-uned"'))
    block = source[start : source.index("<script", start)]
    entries, details, dates, titles = [], {}, {}, {}
    for card in re.findall(r'<article class="day-card".*?</article>', block, re.S):
        label = strip_tags(re.search(r'<p class="day-num">(.*?)</p>', card, re.S).group(1))
        n = class_number(label)
        dates[n] = label.split("·", 1)[1].strip()
        titles[n] = strip_tags(re.search(r"<h3>(.*?)</h3>", card, re.S).group(1))
        detail = re.search(r'href="(https://claude\.ai/artifact/[^"]+)"', card)
        if detail:
            details[n] = detail.group(1)
        for item in re.findall(r"<li>(.*?)</li>", card, re.S):
            entries.append([n, "Apuntes", strip_tags(item)])
        meta = re.search(r'<p class="day-meta">(.*?)</p>', card, re.S)
        if meta:
            entries.append([n, "Apuntes", strip_tags(meta.group(1))])
    for heading, items in re.findall(r'<div class="note-card"[^>]*>\s*<h3[^>]*>(.*?)</h3>(.*?)</ul>', block, re.S):
        kind = strip_tags(heading)
        for item in re.findall(r"<li>(.*?)</li>", items, re.S):
            entries.append([0, kind, strip_tags(item)])
    return entries, details, dates, titles


def main():
    tab_entries, details, dates, titles = read_tab()
    classes = []
    for n in range(1, 6):
        segments = segments_of((PRIVATE / "uned" / f"clase-{n}.txt").read_text(encoding="utf8"))
        classes.append({
            "n": n,
            "date": dates.get(n, ""),
            "title": titles.get(n, ""),
            "detailUrl": details.get(n),
            "videoUrl": VIDEO_URLS.get(n),
            "segments": segments,
            "paragraphs": paragraph_starts(segments),
        })
    data = {"classes": classes, "notes": read_mind_map() + tab_entries}
    # "</" can't appear inside the inline <script>
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf8").replace("/*DATA*/null", payload)
    OUT.write_text(page, encoding="utf8", newline="\n")
    print(f"{OUT.relative_to(ROOT)}: {sum(len(c['segments']) for c in classes)} segments, {len(data['notes'])} note entries")


if __name__ == "__main__":
    main()
