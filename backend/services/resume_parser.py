"""
Resume Parser Service
Extracts structured text and raw content from PDF and DOCX resume files.
"""

import io
import re
from typing import Optional
from pathlib import Path

import pdfplumber
from docx import Document


class ResumeParser:
    """Handles extraction of raw text from PDF and DOCX resume files."""

    SECTION_HEADERS = [
        "summary", "objective", "profile", "about",
        "experience", "work experience", "employment", "career",
        "education", "academic", "qualification",
        "skills", "technical skills", "core competencies", "technologies",
        "projects", "portfolio",
        "certifications", "certificates", "awards",
        "languages", "hobbies", "interests", "volunteer",
        "publications", "achievements", "accomplishments",
    ]

    def parse(self, file_bytes: bytes, filename: str) -> dict:
        """
        Parse a resume file and return extracted text + metadata.

        Returns:
            {
                "raw_text": str,
                "sections": dict,
                "metadata": dict
            }
        """
        ext = Path(filename).suffix.lower()
        if ext == ".pdf":
            raw_text = self._parse_pdf(file_bytes)
        elif ext in (".doc", ".docx"):
            raw_text = self._parse_docx(file_bytes)
        elif ext == ".txt":
            raw_text = file_bytes.decode("utf-8", errors="ignore")
        else:
            raise ValueError(f"Unsupported file format: {ext}. Use PDF, DOCX, or TXT.")

        sections = self._extract_sections(raw_text)
        metadata = self._extract_metadata(raw_text)

        return {
            "raw_text": raw_text,
            "sections": sections,
            "metadata": metadata,
        }

    # ── PDF Parsing ─────────────────────────────────────────────────────────

    def _parse_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF using pdfplumber."""
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(layout=True)
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    # ── DOCX Parsing ────────────────────────────────────────────────────────

    def _parse_docx(self, file_bytes: bytes) -> str:
        """Extract text from DOCX using python-docx."""
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        # Also extract from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        paragraphs.append(cell.text.strip())
        return "\n".join(paragraphs)

    # ── Section Detection ───────────────────────────────────────────────────

    def _extract_sections(self, text: str) -> dict:
        """Split resume text into logical sections by header detection."""
        lines = text.split("\n")
        sections = {}
        current_section = "header"
        current_content = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                current_content.append("")
                continue

            # Detect section headers: short lines in UPPER CASE or matching keywords
            is_header = (
                len(stripped) < 50
                and any(kw in stripped.lower() for kw in self.SECTION_HEADERS)
                and (stripped.isupper() or stripped.istitle() or stripped.endswith(":"))
            )

            if is_header:
                # Save current section
                if current_content:
                    sections[current_section] = "\n".join(current_content).strip()
                # Start new section
                current_section = stripped.lower().rstrip(":").strip()
                current_content = []
            else:
                current_content.append(stripped)

        # Save last section
        if current_content:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    # ── Metadata Extraction ─────────────────────────────────────────────────

    def _extract_metadata(self, text: str) -> dict:
        """Extract contact information and basic metadata via regex."""
        metadata = {}

        # Email
        email_match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
        metadata["email"] = email_match.group(0) if email_match else None

        # Phone (Indian + international formats)
        phone_match = re.search(
            r"(?:\+91[\s\-]?)?(?:\d{5}[\s\-]?\d{5}|\d{10}|\(\d{3}\)\s?\d{3}[\s\-]\d{4})",
            text
        )
        metadata["phone"] = phone_match.group(0).strip() if phone_match else None

        # LinkedIn
        linkedin_match = re.search(r"linkedin\.com/in/[\w\-]+", text, re.IGNORECASE)
        metadata["linkedin"] = linkedin_match.group(0) if linkedin_match else None

        # GitHub
        github_match = re.search(r"github\.com/[\w\-]+", text, re.IGNORECASE)
        metadata["github"] = github_match.group(0) if github_match else None

        # Experience years (look for patterns like "5 years", "3+ years")
        exp_match = re.search(r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)", text, re.IGNORECASE)
        metadata["years_experience"] = int(exp_match.group(1)) if exp_match else None

        # Name (first non-empty line, usually)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        metadata["name_candidate"] = lines[0] if lines else None

        return metadata


# Singleton instance
resume_parser = ResumeParser()
