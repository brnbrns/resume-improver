"""
Object-oriented utilities for resume processing.
"""

import os
import sys
from typing import List, Tuple, Optional
from pathlib import Path

import PyPDF2
import pdf2image
from PIL import Image


class PromptManager:
    """Manages loading and caching of prompt templates."""
    
    def __init__(self, prompts_directory: Optional[str] = None):
        """
        Initialize the prompt manager.
        
        Args:
            prompts_directory: Path to directory containing prompt files. 
                             If None, uses 'prompts' directory relative to this file.
        """
        if prompts_directory is None:
            self.prompts_dir = Path(__file__).parent / "prompts"
        else:
            self.prompts_dir = Path(prompts_directory)
        
        self._prompt_cache = {}
    
    def load_prompt(self, filename: str) -> str:
        """
        Load prompt from a text file with caching.
        
        Args:
            filename: Name of the prompt file (without .txt extension)
            
        Returns:
            str: Content of the prompt file
        """
        if filename in self._prompt_cache:
            return self._prompt_cache[filename]
        
        prompt_path = self.prompts_dir / f"{filename}.txt"
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self._prompt_cache[filename] = content
                return content
        except FileNotFoundError:            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")


class PDFProcessor:
    """Handles PDF text extraction and image conversion."""
    
    def __init__(self, default_dpi: int = 300):
        """
        Initialize the PDF processor.
        
        Args:
            default_dpi: Default DPI for image conversion
        """
        self.default_dpi = default_dpi
        self._poppler_path = None
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            str: Extracted text content from all pages
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text_content = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
        except Exception as e:
            print(f"Warning: Could not extract text from PDF: {e}")
            text_content = ""
        
        return text_content.strip()
    
    def convert_to_images(self, pdf_path: str, dpi: Optional[int] = None) -> List[Image.Image]:
        """
        Convert PDF pages to images.
        
        Args:
            pdf_path: Path to the PDF file
            dpi: Resolution for image conversion (uses default_dpi if None)
            
        Returns:
            List[Image.Image]: List of PIL Images, one for each page
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        dpi = dpi or self.default_dpi
        
        try:
            # Find Poppler path if needed
            if self._poppler_path is None:
                self._poppler_path = self._find_poppler_path()
            
            # Convert PDF to images
            images = pdf2image.convert_from_path(
                str(pdf_path),
                dpi=dpi,
                fmt='PNG',
                poppler_path=self._poppler_path
            )
            return images
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            return []
    
    def _find_poppler_path(self) -> Optional[str]:
        """
        Find Poppler binaries path for pdf2image.
        
        Returns:
            str or None: Path to Poppler binaries if found, None otherwise
        """
        # Common Poppler paths to check
        possible_paths = [
            "/usr/bin",
            "/usr/local/bin", 
            "/opt/homebrew/bin",
            "C:\\Program Files\\poppler\\bin",
            "C:\\Program Files (x86)\\poppler\\bin",
        ]
        
        # Check if running in virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            venv_path = Path(sys.executable).parent
            possible_paths.extend([
                str(venv_path / "poppler" / "bin"),
                str(venv_path.parent / "poppler" / "bin"),
            ])
        
        # Test each path for pdftoppm executable
        for path in possible_paths:
            pdftoppm_name = "pdftoppm.exe" if os.name == 'nt' else "pdftoppm"
            pdftoppm_path = Path(path) / pdftoppm_name
            if pdftoppm_path.exists():
                return str(path)
        
        print("Warning: Poppler not found. PDF to image conversion may not work.")
        return None


class ImageProcessor:
    """Handles image conversion and manipulation tasks."""
    
    @staticmethod
    def save_images(images: List[Image.Image], output_dir: str, 
                   base_filename: str = "page") -> List[str]:
        """
        Save a list of PIL Images to a directory.
        
        Args:
            images: List of PIL Images to save
            output_dir: Directory to save images to
            base_filename: Base filename for the images (default: "page")
            
        Returns:
            List[str]: List of saved file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_paths = []
        for i, img in enumerate(images, 1):
            filename = f"{base_filename}_{i:02d}.png"
            filepath = output_path / filename
            img.save(filepath, 'PNG')
            saved_paths.append(str(filepath))
        
        return saved_paths


class FileManager:
    """Handles file operations and path management."""
    
    @staticmethod
    def generate_output_filename(input_path: str, suffix: str = "improved") -> str:
        """
        Generate an output filename based on the input PDF path.
        
        Args:
            input_path: Path to the original PDF file
            suffix: Suffix to add to the filename (default: "improved")
            
        Returns:
            str: Path for the output PDF file
        """
        input_path = Path(input_path)
        base_name = input_path.stem
        return str(input_path.parent / f"{base_name}_{suffix}.pdf")
    
    @staticmethod
    def validate_pdf_path(pdf_path: str) -> Path:
        """
        Validate that a PDF path exists and has correct extension.
        
        Args:
            pdf_path: Path to validate
            
        Returns:
            Path: Validated Path object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a PDF
        """
        path = Path(pdf_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {path}")
        
        return path


class ResumeProcessor:
    """Main class that orchestrates resume processing workflow."""
    
    def __init__(self, prompts_directory: Optional[str] = None, default_dpi: int = 300):
        """
        Initialize the resume processor.
        
        Args:
            prompts_directory: Path to directory containing prompt files
            default_dpi: Default DPI for image conversion
        """
        self.prompt_manager = PromptManager(prompts_directory)
        self.pdf_processor = PDFProcessor(default_dpi)
        self.image_processor = ImageProcessor()
        self.file_manager = FileManager()
    
    def process_pdf(self, pdf_path: str, output_dir: Optional[str] = None) -> Tuple[str, List[Image.Image], List[str]]:
        """
        Complete workflow to process a resume PDF.
        
        Args:
            pdf_path: Path to the resume PDF file
            output_dir: Directory to save page images. If None, images won't be saved to disk.
            
        Returns:
            Tuple[str, List[Image.Image], List[str]]: A tuple containing:
                - Extracted text content
                - List of PIL Images (one per page)
                - List of saved image file paths (empty if output_dir is None)
        """
        # Validate input
        validated_path = self.file_manager.validate_pdf_path(pdf_path)
        
        print(f"Processing resume PDF: {validated_path}")
          # Extract text and convert to images
        text_content = self.pdf_processor.extract_text(str(validated_path))
        images = self.pdf_processor.convert_to_images(str(validated_path))
        
        print(f"Extracted {len(text_content)} characters of text")
        print(f"Converted {len(images)} pages to images")
        
        saved_paths = []
        if output_dir:
            # Save images to directory
            saved_paths = self.image_processor.save_images(images, output_dir, "resume_page")
            print(f"Saved {len(saved_paths)} images to {output_dir}")
        
        return text_content, images, saved_paths
