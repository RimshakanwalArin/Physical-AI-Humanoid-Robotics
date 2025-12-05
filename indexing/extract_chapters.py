#!/usr/bin/env python3
"""
Extract chapters from markdown files and segment into indexable sections.

This script:
1. Reads all markdown files from docs/
2. Extracts metadata (title, position)
3. Splits content into chapters and sections
4. Returns structured data for embedding
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import frontmatter


@dataclass
class Chapter:
    """Represents a chapter in the textbook."""
    id: str
    title: str
    position: int
    file_path: str
    content: str
    sections: List['Section']


@dataclass
class Section:
    """Represents a section within a chapter."""
    id: str
    title: str
    level: int  # 1 for H1, 2 for H2, etc.
    content: str
    parent_chapter_id: str


class ChapterExtractor:
    """Extract structured chapter and section data from markdown files."""

    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.chapters: List[Chapter] = []

    def extract_all(self) -> List[Chapter]:
        """Extract all chapters from the docs directory."""
        markdown_files = sorted(self.docs_dir.glob("*.md"))

        for md_file in markdown_files:
            chapter = self.extract_chapter(md_file)
            if chapter:
                self.chapters.append(chapter)

        return self.chapters

    def extract_chapter(self, file_path: Path) -> Chapter:
        """Extract a single chapter from a markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Extract metadata
        metadata = post.metadata
        chapter_id = metadata.get("id", file_path.stem)
        title = metadata.get("title", file_path.stem)
        position = metadata.get("sidebar_position", 999)

        # Extract sections
        sections = self._extract_sections(post.content, chapter_id)

        chapter = Chapter(
            id=chapter_id,
            title=title,
            position=position,
            file_path=str(file_path),
            content=post.content,
            sections=sections,
        )

        return chapter

    def _extract_sections(
        self, content: str, chapter_id: str
    ) -> List[Section]:
        """Extract sections from chapter content based on markdown headers."""
        sections = []
        current_section_content = ""
        current_header = None
        current_level = 0

        lines = content.split("\n")

        for line in lines:
            # Check for markdown headers
            match = re.match(r"^(#+)\s+(.+)$", line)

            if match:
                # Save previous section if exists
                if current_header:
                    section = Section(
                        id=self._generate_section_id(chapter_id, current_header),
                        title=current_header,
                        level=current_level,
                        content=current_section_content.strip(),
                        parent_chapter_id=chapter_id,
                    )
                    if section.content:  # Only add non-empty sections
                        sections.append(section)

                # Start new section
                current_level = len(match.group(1))
                current_header = match.group(2)
                current_section_content = ""
            else:
                # Add line to current section
                current_section_content += line + "\n"

        # Save last section
        if current_header:
            section = Section(
                id=self._generate_section_id(chapter_id, current_header),
                title=current_header,
                level=current_level,
                content=current_section_content.strip(),
                parent_chapter_id=chapter_id,
            )
            if section.content:
                sections.append(section)

        return sections

    def _generate_section_id(self, chapter_id: str, section_title: str) -> str:
        """Generate a unique section ID."""
        section_slug = section_title.lower().replace(" ", "-")
        section_slug = re.sub(r"[^\w-]", "", section_slug)
        return f"{chapter_id}-{section_slug}"

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert chapters to dictionary format for JSON serialization."""
        return [
            {
                "id": chapter.id,
                "title": chapter.title,
                "position": chapter.position,
                "file_path": chapter.file_path,
                "sections": [
                    {
                        "id": section.id,
                        "title": section.title,
                        "level": section.level,
                        "content": section.content,
                        "parent_chapter_id": section.parent_chapter_id,
                    }
                    for section in chapter.sections
                ],
            }
            for chapter in self.chapters
        ]


def main():
    """Extract all chapters and save to JSON."""
    extractor = ChapterExtractor(docs_dir="docs")
    chapters = extractor.extract_all()

    # Save to JSON
    output_file = Path("indexing/extracted_chapters.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extractor.to_dict(), f, indent=2)

    # Print summary
    total_sections = sum(len(ch.sections) for ch in chapters)
    print(f"Extracted {len(chapters)} chapters, {total_sections} sections")
    print(f"Saved to {output_file}")

    # Print chapter list
    for chapter in chapters:
        print(f"  - {chapter.title} ({len(chapter.sections)} sections)")


if __name__ == "__main__":
    main()
