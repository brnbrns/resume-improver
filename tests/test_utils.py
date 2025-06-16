"""
Tests for the object-oriented utilities module.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from PIL import Image
import shutil

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    PromptManager, PDFProcessor, ImageProcessor, FileManager, ResumeProcessor
)


class TestPromptManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.prompt_manager = PromptManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_prompt_success(self):
        """Test successful prompt loading."""
        test_prompt = "This is a test prompt."
        prompt_file = os.path.join(self.temp_dir, "test_prompt.txt")
        
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(test_prompt)
        
        result = self.prompt_manager.load_prompt("test_prompt")
        self.assertEqual(result, test_prompt)
    
    def test_load_prompt_file_not_found(self):
        """Test prompt loading when file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            self.prompt_manager.load_prompt("nonexistent_prompt")
    
    def test_prompt_caching(self):
        """Test that prompts are cached correctly."""
        test_prompt = "Cached prompt."
        prompt_file = os.path.join(self.temp_dir, "cached_prompt.txt")
        
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(test_prompt)
        
        # Load prompt twice
        result1 = self.prompt_manager.load_prompt("cached_prompt")
        result2 = self.prompt_manager.load_prompt("cached_prompt")
        
        self.assertEqual(result1, result2)
        self.assertEqual(result1, test_prompt)


class TestPDFProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.pdf_processor = PDFProcessor()
    
    @patch('utils.PyPDF2.PdfReader')
    @patch('builtins.open', create=True)
    @patch('utils.Path.exists')
    def test_extract_text_success(self, mock_exists, mock_open, mock_pdf_reader):
        """Test successful PDF text extraction."""
        mock_exists.return_value = True
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Test page content"
        mock_pdf_reader.return_value.pages = [mock_page, mock_page]
        
        result = self.pdf_processor.extract_text("test.pdf")
        self.assertIn("Test page content", result)
    
    @patch('utils.Path.exists')
    def test_extract_text_file_not_found(self, mock_exists):
        """Test PDF text extraction when file doesn't exist."""
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            self.pdf_processor.extract_text("nonexistent.pdf")
    
    @patch('utils.pdf2image.convert_from_path')
    @patch('utils.Path.exists')
    def test_convert_to_images_success(self, mock_exists, mock_convert):
        """Test successful PDF to images conversion."""
        mock_exists.return_value = True
        mock_image = Image.new('RGB', (100, 100), color='red')
        mock_convert.return_value = [mock_image]
        
        result = self.pdf_processor.convert_to_images("test.pdf")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Image.Image)
    
    @patch('utils.Path.exists')
    def test_convert_to_images_file_not_found(self, mock_exists):
        """Test PDF to images conversion when file doesn't exist."""
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            self.pdf_processor.convert_to_images("nonexistent.pdf")


class TestImageProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_image = Image.new('RGB', (100, 100), color='red')
    
    def test_save_images(self):
        """Test saving images to directory."""
        temp_dir = tempfile.mkdtemp()
        try:
            images = [self.test_image, self.test_image]
            result = ImageProcessor.save_images(images, temp_dir, "test")
            
            self.assertEqual(len(result), 2)
            for path in result:
                self.assertTrue(os.path.exists(path))
                self.assertTrue(path.endswith('.png'))
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestFileManager(unittest.TestCase):
    
    def test_generate_output_filename(self):
        """Test output filename generation."""
        input_path = "resume.pdf"
        result = FileManager.generate_output_filename(input_path)
        
        self.assertEqual(result, "resume_improved.pdf")
        self.assertTrue(result.endswith(".pdf"))
    
    def test_generate_output_filename_with_path(self):
        """Test output filename generation with full path."""
        input_path = os.path.join("path", "to", "resume.pdf")
        result = FileManager.generate_output_filename(input_path)
        
        # Check that it contains the expected parts regardless of path separator
        self.assertIn("resume_improved", result)
        self.assertTrue(result.endswith(".pdf"))
        # Check that the directory structure is preserved
        expected_dir = os.path.join("path", "to")
        self.assertIn(expected_dir, result)
    
    def test_validate_pdf_path_success(self):
        """Test successful PDF path validation."""
        # Create a temporary PDF file
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_file.close()
        
        try:
            result = FileManager.validate_pdf_path(temp_file.name)
            self.assertEqual(str(result), temp_file.name)
        finally:
            os.unlink(temp_file.name)
    
    def test_validate_pdf_path_not_found(self):
        """Test PDF path validation when file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            FileManager.validate_pdf_path("nonexistent.pdf")
    
    def test_validate_pdf_path_not_pdf(self):
        """Test PDF path validation when file is not a PDF."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        temp_file.close()
        
        try:
            with self.assertRaises(ValueError):
                FileManager.validate_pdf_path(temp_file.name)
        finally:
            os.unlink(temp_file.name)


class TestResumeProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.resume_processor = ResumeProcessor(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('utils.PDFProcessor.convert_to_images')
    @patch('utils.PDFProcessor.extract_text')
    @patch('utils.FileManager.validate_pdf_path')
    def test_process_pdf_success(self, mock_validate, mock_extract, mock_convert):
        """Test successful PDF processing."""
        mock_validate.return_value = "test.pdf"
        mock_extract.return_value = "Test content"
        mock_convert.return_value = [Image.new('RGB', (100, 100), color='red')]
        
        text, images, paths = self.resume_processor.process_pdf("test.pdf")
        
        self.assertEqual(text, "Test content")
        self.assertEqual(len(images), 1)
        self.assertEqual(len(paths), 0)  # No output dir specified
    
    @patch('utils.PDFProcessor.convert_to_images')
    @patch('utils.PDFProcessor.extract_text')
    @patch('utils.FileManager.validate_pdf_path')
    @patch('utils.ImageProcessor.save_images')
    def test_process_pdf_with_output_dir(self, mock_save, mock_validate, mock_extract, mock_convert):
        """Test PDF processing with output directory."""
        mock_validate.return_value = "test.pdf"
        mock_extract.return_value = "Test content"
        mock_convert.return_value = [Image.new('RGB', (100, 100), color='red')]
        mock_save.return_value = ["saved_image.png"]
        
        text, images, paths = self.resume_processor.process_pdf("test.pdf", self.temp_dir)
        
        self.assertEqual(text, "Test content")
        self.assertEqual(len(images), 1)
        self.assertEqual(len(paths), 1)
        mock_save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
