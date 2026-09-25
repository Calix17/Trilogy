#!/usr/bin/env python3
"""Render a literary Markdown manuscript as a book PDF, plus page QA metadata.

Requires Python 3.10+, reportlab, Pillow, and pypdf. Uses installed STIXGeneral
TrueType fonts, with DejaVu Serif as a fallback. No network access is used.

Run from any directory:
    python3 08-production/render-book-v6.py
    python3 08-production/render-book-v6.py --source path.md --output path.pdf

Chapter headings must have the form ``## 1. The Good Days``. The first H1 is
the book title; a pre-chapter H2 is the subtitle. Pre-chapter blockquotes form
the epigraph. Other pre-chapter editorial notes are excluded from the reading
edition and listed in the QA JSON. Markdown prose and emphasis are preserved.
Unicode dashes are normalized to ASCII hyphens in the PDF only.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys

from PIL import Image as PILImage
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_RE = re.compile(r"^##\s+(\d+)[.)]\s+(.+?)\s*$", re.MULTILINE)
RULE_RE = re.compile(r"^(?:-{3,}|\*\s*\*\s*\*|_{3,})$")
INK = colors.HexColor("#212323")
QUIET = colors.HexColor("#656563")


def normalize(text: str) -> str:
    text = text.replace("\u2014", " - ").replace("\u2013", " - ")
    text = re.sub(r"[\u2010\u2011\u2012\u2015\u2212]", "-", text)
    return re.sub(r"[ \t]{2,}", " ", text)


def inline(text: str) -> str:
    """Convert the small Markdown inline vocabulary used by the manuscript."""
    text = html.escape(normalize(text), quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def register_fonts() -> dict[str, str]:
    candidates: list[Path] = []
    try:
        import matplotlib

        candidates.append(Path(matplotlib.get_data_path()) / "fonts" / "ttf")
    except ImportError:
        pass
    runtime_root = os.environ.get("CODEX_PRIMARY_RUNTIME_ROOT")
    if runtime_root:
        candidates.extend(
            Path(runtime_root).glob(
                "dependencies/python/lib/python*/site-packages/matplotlib/mpl-data/fonts/ttf"
            )
        )
    candidates.extend(
        Path("/opt/codex/runtimes").glob(
            "*/dependencies/python/lib/python*/site-packages/matplotlib/mpl-data/fonts/ttf"
        )
    )
    candidates.extend(
        [Path("/usr/share/fonts/truetype/dejavu"), Path(sys.prefix) / "share/fonts"]
    )
    variants = [
        ("STIXGeneral.ttf", "STIXGeneralItalic.ttf", "STIXGeneralBol.ttf", "STIXGeneralBolIta.ttf"),
        ("DejaVuSerif.ttf", "DejaVuSerif-Italic.ttf", "DejaVuSerif-Bold.ttf", "DejaVuSerif-BoldItalic.ttf"),
    ]
    for names in variants:
        for directory in candidates:
            if all((directory / name).is_file() for name in names):
                registered = {}
                for suffix, filename in zip(("", "-Italic", "-Bold", "-BoldItalic"), names):
                    face = "BookSerif" + suffix
                    path = directory / filename
                    pdfmetrics.registerFont(TTFont(face, str(path)))
                    registered[face] = str(path)
                pdfmetrics.registerFontFamily(
                    "BookSerif",
                    normal="BookSerif",
                    italic="BookSerif-Italic",
                    bold="BookSerif-Bold",
                    boldItalic="BookSerif-BoldItalic",
                )
                return registered
    raise RuntimeError("No complete STIXGeneral or DejaVu Serif TrueType family found.")


def read_manuscript(source: Path) -> dict:
    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    matches = list(CHAPTER_RE.finditer(text))
    if not matches:
        raise ValueError("No numbered chapter headings found: expected '## 1. Title'.")
    numbers = [int(match.group(1)) for match in matches]
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"Chapter numbers must be consecutive and unique: {numbers}")
    front = text[: matches[0].start()]
    title = next((line[2:].strip() for line in front.splitlines() if line.startswith("# ")), "The Final Decision")
    subtitle = next((line[3:].strip() for line in front.splitlines() if line.startswith("## ")), "Book I - Paradise")
    epigraph = [line.lstrip()[1:].strip() for line in front.splitlines() if line.lstrip().startswith(">")]
    edition = next((line.strip().strip("*") for line in front.splitlines() if re.match(r"^\*?Version\s+\d+\b", line.strip(), re.IGNORECASE)), "")
    omitted = [
        line.strip()
        for line in front.splitlines()
        if line.strip()
        and not line.startswith("#")
        and not line.lstrip().startswith(">")
        and not RULE_RE.match(line.strip())
        and not line.lstrip().startswith("![")
        and line.strip().strip("*") != edition
    ]
    chapters = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        blocks = [block.strip() for block in re.split(r"\n\s*\n", body) if block.strip()]
        while blocks and RULE_RE.match(blocks[-1]):
            blocks.pop()
        while blocks and RULE_RE.match(blocks[0]):
            blocks.pop(0)
        chapters.append({"number": int(match.group(1)), "title": match.group(2), "blocks": blocks, "source_words": len(re.findall(r"\b[\w'’]+\b", body))})
    return {"title": title, "subtitle": subtitle, "edition": edition, "epigraph": epigraph, "omitted_frontmatter": omitted, "chapters": chapters}


class SceneBreak(Flowable):
    """A quiet ornament that cannot create an otherwise empty trailing page."""

    def __init__(self):
        super().__init__()
        self.height = 18
        self.keepWithNext = True

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        return avail_width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(QUIET)
        self.canv.setLineWidth(0.4)
        mid = self.width / 2
        self.canv.line(mid - 14, 9, mid + 14, 9)
        self.canv.restoreState()


class BookDoc(BaseDocTemplate):
    def __init__(self, output: Path, *, title: str, subtitle: str, author: str):
        super().__init__(
            str(output),
            pagesize=(6 * inch, 9 * inch),
            leftMargin=0.72 * inch,
            rightMargin=0.72 * inch,
            topMargin=0.72 * inch,
            bottomMargin=0.68 * inch,
            title=normalize(title),
            author=author,
            subject=normalize(subtitle),
            pageCompression=1,
            allowSplitting=1,
            invariant=1,
        )
        self.book_title = normalize(title)
        self.chapter_starts = []
        self.current_chapter = None
        self.chapter_start_pages = set()
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="reading")
        self.addPageTemplates(PageTemplate(id="book", frames=[frame], onPageEnd=self.page_end))

    def afterFlowable(self, flowable):
        chapter = getattr(flowable, "chapter_metadata", None)
        if chapter is None:
            return
        self.current_chapter = chapter
        self.chapter_start_pages.add(self.page)
        anchor = f"chapter-{chapter['number']}"
        self.canv.bookmarkPage(anchor)
        self.canv.addOutlineEntry(normalize(f"{chapter['number']}. {chapter['title']}"), anchor, level=0)
        self.chapter_starts.append({"number": chapter["number"], "title": chapter["title"], "pdf_start_page": self.page, "printed_start_page": self.page - 1, "source_words": chapter["source_words"]})

    def page_end(self, canvas, doc):
        if self.page == 1:
            return
        canvas.saveState()
        canvas.setFillColor(QUIET)
        canvas.setFont("BookSerif", 8.3)
        if self.page not in self.chapter_start_pages:
            label = self.book_title if self.page % 2 == 0 else normalize(self.current_chapter["title"] if self.current_chapter else self.book_title)
            canvas.drawCentredString(self.pagesize[0] / 2, self.pagesize[1] - 30, label)
        canvas.setFont("BookSerif", 9)
        canvas.drawCentredString(self.pagesize[0] / 2, 27, str(self.page - 1))
        canvas.restoreState()


def styles_for(leading: float, compact: bool = False) -> dict[str, ParagraphStyle]:
    base = dict(fontName="BookSerif", fontSize=11, leading=leading, textColor=INK, alignment=TA_JUSTIFY, firstLineIndent=12, spaceAfter=0.5 if compact else 1.7, allowWidows=0, allowOrphans=0, splitLongWords=0, hyphenationLang=None)
    return {
        "body": ParagraphStyle("Body", **base),
        "first": ParagraphStyle("First", **{**base, "firstLineIndent": 0}),
        "quote": ParagraphStyle("Quotation", **{**base, "alignment": TA_LEFT, "firstLineIndent": 0, "leftIndent": 16, "rightIndent": 12, "spaceBefore": 5, "spaceAfter": 6}),
        "display": ParagraphStyle("Display", **{**base, "alignment": TA_LEFT, "firstLineIndent": 0, "leftIndent": 16, "spaceBefore": 5, "spaceAfter": 6}),
        "chapter": ParagraphStyle("Chapter", fontName="BookSerif", fontSize=20, leading=24, alignment=TA_CENTER, textColor=INK, spaceBefore=4 if compact else 8, spaceAfter=10 if compact else 24, keepWithNext=True),
        "chapter_number": ParagraphStyle("ChapterNumber", fontName="BookSerif", fontSize=9, leading=11, alignment=TA_CENTER, textColor=QUIET, spaceBefore=2 if compact else 8, spaceAfter=3 if compact else 9, keepWithNext=True),
    }


def build_story(manuscript: dict, image_path: Path, leading: float, tight_chapters: set[int], compact_chapters: set[int]) -> list:
    title_style = ParagraphStyle("Title", fontName="BookSerif", fontSize=29, leading=32, alignment=TA_CENTER, textColor=INK, spaceAfter=9)
    subtitle_style = ParagraphStyle("Subtitle", fontName="BookSerif", fontSize=15, leading=19, alignment=TA_CENTER, textColor=INK, spaceAfter=9 if manuscript["edition"] else 20)
    edition_style = ParagraphStyle("Edition", fontName="BookSerif", fontSize=9, leading=12, alignment=TA_CENTER, textColor=QUIET, spaceAfter=20)
    epigraph_style = ParagraphStyle("Epigraph", fontName="BookSerif-Italic", fontSize=10.4, leading=14, alignment=TA_CENTER, textColor=QUIET)
    story = [Spacer(1, 3), Paragraph(inline(manuscript["title"]), title_style), Paragraph(inline(manuscript["subtitle"]), subtitle_style)]
    if manuscript["edition"]:
        story.append(Paragraph(inline(manuscript["edition"]), edition_style))
    if image_path.is_file():
        with PILImage.open(image_path) as picture:
            ratio = picture.height / picture.width
        width = 3.5 * inch
        story.extend([Image(str(image_path), width=width, height=width * ratio), Spacer(1, 16)])
    if manuscript["epigraph"]:
        story.append(Paragraph("<br/>".join(inline(line) for line in manuscript["epigraph"]), epigraph_style))
    for chapter in manuscript["chapters"]:
        story.append(PageBreak())
        compact = chapter["number"] in compact_chapters
        st = styles_for(leading - (0.6 if compact else 0.4 if chapter["number"] in tight_chapters else 0), compact=compact)
        label = Paragraph(f"CHAPTER {chapter['number']}", st["chapter_number"])
        label.chapter_metadata = chapter
        story.append(label)
        story.append(Paragraph(inline(chapter["title"]), st["chapter"]))
        content = []
        first = True
        for block in chapter["blocks"]:
            if RULE_RE.match(block):
                content.append(SceneBreak())
                first = True
                continue
            if block.startswith("#"):
                raise ValueError(f"Unexpected nested heading in chapter {chapter['number']}: {block[:80]}")
            if block.startswith(">"):
                lines = [line.lstrip()[1:].lstrip() if line.lstrip().startswith(">") else line for line in block.splitlines()]
                content.append(Paragraph("<br/>".join(inline(line) for line in lines), st["quote"]))
                first = True
            else:
                para = " ".join(line.strip() for line in block.splitlines())
                is_display = para.startswith("*") and para.endswith("*") and len(para) < 280
                content.append(Paragraph(inline(para), st["display"] if is_display else st["first"] if first else st["body"]))
                first = False
        # Keep a short ending exchange together. This prevents a lone final
        # line from receiving a whole page without shrinking the entire book.
        if len(content) >= 2:
            tail = content[-2:]
            total_height = sum(item.wrap(4.56 * inch, 9 * inch)[1] + item.getSpaceBefore() + item.getSpaceAfter() for item in tail)
            if total_height <= 95:
                content[-2:] = [KeepTogether(tail)]
        story.extend(content)
    return story


def write_qa(output: Path, source: Path, doc: BookDoc, manuscript: dict, fonts: dict, qa_path: Path, leading: float, tight_chapters: set[int], compact_chapters: set[int]) -> dict:
    reader = PdfReader(str(output))
    starts = doc.chapter_starts
    for index, chapter in enumerate(starts):
        chapter["pdf_end_page"] = starts[index + 1]["pdf_start_page"] - 1 if index + 1 < len(starts) else len(reader.pages)
        chapter["printed_end_page"] = chapter["pdf_end_page"] - 1
    pages = []
    sparse = []
    blank = []
    for page_number, page in enumerate(reader.pages, 1):
        extracted = page.extract_text() or ""
        chapter = next((item for item in starts if item["pdf_start_page"] <= page_number <= item["pdf_end_page"]), None)
        lines = extracted.splitlines()
        if page_number > 1:
            lines = [line for line in lines if line.strip() not in {str(page_number - 1), normalize(manuscript["title"]), normalize(chapter["title"]) if chapter else ""}]
        content_words = len(re.findall(r"\b[\w'’]+\b", " ".join(lines)))
        record = {"pdf_page": page_number, "printed_page": page_number - 1 if page_number > 1 else None, "chapter": chapter["number"] if chapter else None, "content_word_count": content_words, "text": extracted}
        pages.append(record)
        if page_number > 1 and content_words == 0:
            blank.append(page_number)
        if chapter and page_number == chapter["pdf_end_page"] and page_number > chapter["pdf_start_page"] and content_words < 80:
            sparse.append({"chapter": chapter["number"], "pdf_page": page_number, "content_words": content_words})
    qa = {
        "source": str(source), "output": str(output),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "page_size_inches": [6, 9], "font_size": 11, "leading": leading,
        "tightened_chapters": sorted(tight_chapters), "fonts": fonts,
        "compact_chapters": sorted(compact_chapters), "edition": manuscript["edition"],
        "page_count": len(reader.pages), "chapter_count": len(starts),
        "source_chapter_word_count": sum(ch["source_words"] for ch in manuscript["chapters"]),
        "omitted_editorial_frontmatter": manuscript["omitted_frontmatter"],
        "blank_body_pages": blank, "sparse_chapter_end_pages": sparse,
        "chapters": starts, "pages": pages,
    }
    qa_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if blank:
        raise RuntimeError(f"Blank body pages detected: {blank}; review QA before delivery.")
    return qa


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, default=ROOT / "02-book-one/book-one-paradise-v6.md")
    parser.add_argument("--output", type=Path, default=ROOT / "02-book-one/book-one-paradise-v6.pdf")
    parser.add_argument("--qa", type=Path, default=None)
    parser.add_argument("--frontispiece", type=Path, default=ROOT / "05-art/laniakea-tree.png")
    parser.add_argument("--author", default="")
    parser.add_argument("--leading", type=float, default=14.8)
    parser.add_argument("--tighten-chapters", default="", help="Comma-separated chapter numbers; reduce their leading by 0.4pt after inspecting sparse endings.")
    parser.add_argument("--compact-chapters", default="", help="Comma-separated chapter numbers; reduce leading by 0.6pt, paragraph gaps to 0.5pt, and heading whitespace. Use only to remove short spillover pages.")
    args = parser.parse_args()
    if not 14 <= args.leading <= 16:
        parser.error("Use leading between 14 and 16 points for the 11pt body.")
    source = args.source.resolve()
    output = args.output.resolve()
    qa_path = args.qa.resolve() if args.qa else output.with_suffix(".qa.json")
    if source == output:
        parser.error("Source and output paths must differ.")
    tight_chapters = {int(value.strip()) for value in args.tighten_chapters.split(",") if value.strip()}
    compact_chapters = {int(value.strip()) for value in args.compact_chapters.split(",") if value.strip()}
    manuscript = read_manuscript(source)
    fonts = register_fonts()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BookDoc(output, title=manuscript["title"], subtitle=manuscript["subtitle"], author=args.author)
    doc.build(build_story(manuscript, args.frontispiece.resolve(), args.leading, tight_chapters, compact_chapters))
    qa = write_qa(output, source, doc, manuscript, fonts, qa_path, args.leading, tight_chapters, compact_chapters)
    print(json.dumps({"pdf": str(output), "qa": str(qa_path), "pages": qa["page_count"], "chapters": qa["chapter_count"], "sparse_chapter_end_pages": qa["sparse_chapter_end_pages"], "blank_body_pages": qa["blank_body_pages"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
