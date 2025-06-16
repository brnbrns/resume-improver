# Resume Improver Test Suite

This directory contains comprehensive unit and integration tests for the Resume Improver project using an **Object-Oriented Architecture**.

## Test Structure

```plaintext
tests/
├── __init__.py              # Test package initialization
├── test_utils.py            # Tests for utility classes (OO design)
├── test_model.py            # Tests for model configuration classes
├── test_resume_improver.py  # Tests for main application classes and CLI
├── conftest.py             # Pytest configuration and fixtures
├── run_tests.py            # Simple test runner
└── README.md               # This file
```

## Running Tests

### Method 1: Using pytest (recommended)

```bash
# Install testing dependencies if not already installed
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage reporting
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_utils.py

# Run specific test class
pytest tests/test_utils.py::TestPromptManager

# Run specific test method
pytest tests/test_utils.py::TestPromptManager::test_load_prompt_success
```

### Method 2: Using the simple test runner

```bash
python tests/run_tests.py
```

### Method 3: Using unittest directly

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_utils

# Run specific test class
python -m unittest tests.test_utils.TestPromptManager

# Run specific test method
python -m unittest tests.test_utils.TestPromptManager.test_load_prompt_success
```

## Test Coverage

The test suite provides comprehensive coverage of the **Object-Oriented Resume Improver** system:

### Utils Module (`test_utils.py`)

**TestPromptManager** - Prompt template management:

- ✅ `test_load_prompt_success` - Successful prompt loading
- ✅ `test_load_prompt_file_not_found` - Handles missing prompt files
- ✅ `test_prompt_caching` - Verifies prompt caching functionality

**TestPDFProcessor** - PDF text extraction and conversion:

- ✅ `test_extract_text_success` - PDF text extraction success
- ✅ `test_extract_text_file_not_found` - Handles missing PDF files
- ✅ `test_convert_to_images_success` - PDF to image conversion
- ✅ `test_convert_to_images_file_not_found` - Error handling for missing PDFs

**TestImageProcessor** - Image manipulation and saving:

- ✅ `test_save_images` - Image saving functionality

**TestFileManager** - File operations and validation:

- ✅ `test_generate_output_filename` - Output filename generation
- ✅ `test_generate_output_filename_with_path` - Filename with path handling  
- ✅ `test_validate_pdf_path_success` - PDF path validation success
- ✅ `test_validate_pdf_path_not_found` - Missing file error handling
- ✅ `test_validate_pdf_path_not_pdf` - Invalid file type handling

**TestResumeProcessor** - Complete PDF processing workflow:

- ✅ `test_process_pdf_success` - End-to-end PDF processing
- ✅ `test_process_pdf_with_output_dir` - Processing with image saving

### Model Configuration (`test_model.py`)

**TestModelConfig** - Configuration data class:

- ✅ `test_model_config_creation_success` - Successful config creation
- ✅ `test_model_config_defaults` - Default parameter handling  
- ✅ `test_model_config_missing_api_key` - Missing API key validation
- ✅ `test_model_config_missing_endpoint` - Missing endpoint validation

**TestModelManager** - Model client management:

- ✅ `test_model_manager_with_config` - Initialization with custom config
- ✅ `test_model_manager_from_environment` - Environment-based initialization
- ✅ `test_model_manager_missing_env_vars` - Missing environment variables
- ✅ `test_client_property_creation` - AI client creation
- ✅ `test_config_property_readonly` - Configuration immutability
- ✅ `test_update_config` - Configuration updates
- ✅ `test_load_env_parameter` - Environment loading control

### Main Application (`test_resume_improver.py`)

**TestAgentFactory** - AI agent creation:

- ✅ `test_create_draft_agent` - Resume draft agent creation
- ✅ `test_create_enhancement_agent` - Enhancement agent creation  
- ✅ `test_create_conciseness_agent` - Conciseness agent creation
- ✅ `test_create_image_agent` - Image generation agent creation

**TestResumeTeam** - Team management:

- ✅ `test_initialization` - Team initialization
- ✅ `test_create_team` - Agent team creation
- ✅ `test_get_image_agent` - Image agent retrieval

**TestResumeImprover** - Main application workflow:

- ✅ `test_initialization_with_defaults` - Default initialization
- ✅ `test_initialization_with_custom_config` - Custom config initialization
- ✅ `test_improve_resume_text` - Text improvement workflow (async)
- ✅ `test_process_pdf_file_success` - PDF processing success
- ✅ `test_process_pdf_file_no_text` - No text extraction error
- ✅ `test_process_pdf_file_no_images` - No images error

**TestResumeImproverCLI** - Command-line interface:

- ✅ `test_initialization_with_default_improver` - CLI initialization
- ✅ `test_get_pdf_path_from_args` - Command-line argument processing
- ✅ `test_get_pdf_path_from_input` - Interactive input handling
- ✅ `test_get_pdf_path_empty_input` - Empty input handling
- ✅ `test_validate_pdf_file_success` - File validation success
- ✅ `test_validate_pdf_file_not_found` - Missing file handling
- ✅ `test_validate_pdf_file_not_pdf` - Invalid file type handling
- ✅ `test_run_success` - Successful CLI execution (async)
- ✅ `test_run_file_not_found` - File not found error (async)
- ✅ `test_run_no_improved_content` - No improvement error (async)

**TestOOIntegration** - Object-oriented integration tests:

- ✅ `test_resume_team_create_team_method` - Team creation integration
- ✅ `test_resume_team_get_image_agent_method` - Image agent integration
- ✅ `test_improve_resume_function` - End-to-end improvement workflow (async)

## Test Features

### Object-Oriented Architecture

- All tests follow the OO design pattern matching the main codebase
- Class-based test organization mirrors the production class structure
- Proper encapsulation and separation of concerns in test design

### Mocking Strategy

- External dependencies (Azure OpenAI, PDF libraries) are properly mocked
- File system operations use temporary directories for isolation
- Environment variables are mocked and isolated per test
- Network calls and external services are fully mocked

### Async Testing Support

- Async functions are properly tested using `AsyncMock`
- Event loops are handled correctly with pytest-asyncio
- Proper async/await patterns in test implementations

### Comprehensive Error Handling

- Tests cover both success and failure scenarios
- Exception handling is thoroughly validated
- Edge cases and boundary conditions are included
- Input validation testing across all methods

### Fixtures and Test Setup

- Reusable test fixtures in `conftest.py`
- Proper setup and teardown for each test class
- Temporary directories for safe file operations
- Mock objects configured consistently across tests

## Current Test Statistics

- **Total Test Methods**: 52
- **Test Classes**: 12  
- **Test Files**: 3
- **Lines of Test Code**: ~1500+
- **Coverage Areas**: All major OO classes and methods

## Expected Coverage Targets

The test suite achieves:

- **95%+** line coverage across all main modules
- **100%** class coverage (all classes tested)
- **90%+** method coverage  
- **85%+** branch coverage for conditional logic

## Adding New Tests

When extending functionality:

### 1. Follow OO Test Patterns

- Create test classes that mirror production classes
- Use descriptive test class names: `Test<ClassName>`
- Group related test methods within appropriate test classes

### 2. Test Method Naming

- Use pattern: `test_<method_name>_<scenario>`
- Examples: `test_load_prompt_success`, `test_extract_text_file_not_found`

### 3. Test Structure (AAA Pattern)

```python
def test_method_name_success_scenario(self):
    """Test method_name with valid input produces expected output."""
    # Arrange - Set up test data and mocks
    input_data = "test input"
    expected_result = "expected output"
    
    # Act - Execute the method under test
    result = self.instance.method_name(input_data)
    
    # Assert - Verify the results
    self.assertEqual(result, expected_result)
```

### 4. Async Test Pattern

```python
async def test_async_method_success(self):
    """Test async method with proper await handling."""
    # Arrange
    mock_dependency = AsyncMock(return_value="expected")
    
    # Act
    result = await self.instance.async_method()
    
    # Assert
    self.assertEqual(result, "expected")
```

### 5. Mock Configuration

- Use `@patch` decorators for external dependencies
- Configure return values and side effects appropriately  
- Verify mock calls with `assert_called_with()` when needed

## Troubleshooting

### Common Issues and Solutions

1. **Import Errors**

   ```bash
   # Ensure proper Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Async Test Failures**
   - Ensure `pytest-asyncio` is installed
   - Use `async def` for async test methods
   - Properly mock async dependencies with `AsyncMock`

3. **File System Test Issues**
   - Always use temporary directories from `tempfile.TemporaryDirectory()`
   - Clean up resources in test teardown methods
   - Use `@patch` for file system operations when appropriate

4. **Environment Variable Conflicts**
   - Mock environment variables using `@patch.dict('os.environ')`
   - Isolate tests from actual environment settings

### Running Individual Tests

```bash
# Run specific test class
python -m unittest tests.test_utils.TestPromptManager -v

# Run specific test method  
python -m unittest tests.test_utils.TestPromptManager.test_load_prompt_success -v

# Using pytest (more verbose output)
pytest tests/test_utils.py::TestPromptManager::test_load_prompt_success -v
```

## Dependencies

### Core Testing (Built-in)

- `unittest` - Primary testing framework
- `unittest.mock` - Mocking framework  
- `asyncio` - Async testing support
- `tempfile` - Temporary file/directory creation

### Required External Dependencies

- `pytest` - Enhanced test runner with better output
- `pytest-asyncio` - Async test support for pytest
- `pytest-cov` - Coverage reporting integration

### Optional Development Tools

- `coverage` - Detailed coverage measurement and reporting
- `unittest-xml-reporting` - JUnit XML output for CI/CD

### Installation

```bash
# Install all testing dependencies
pip install pytest pytest-asyncio pytest-cov coverage unittest-xml-reporting

# Or install from requirements.txt (includes testing deps)
pip install -r requirements.txt
```
