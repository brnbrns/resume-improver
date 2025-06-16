# Resume Improver

An intelligent AI-powered resume improvement system that uses multiple specialized AI agents to enhance resumes while maintaining their original format and visual appeal.

## 🌟 Features

- **Multi-Agent AI System**: Employs specialized AI agents for different aspects of resume improvement
- **Format Preservation**: Maintains original PDF layout and visual design
- **Intelligent Enhancement**: Improves content quality, keyword optimization, and ATS compatibility
- **Comprehensive Testing**: Full test coverage with 52+ unit and integration tests

## 🏗️ Architecture

The system uses the following main components:

### Core Classes

- **`ResumeImprover`**: Main orchestrator class for the improvement workflow
- **`AgentFactory`**: Factory pattern for creating specialized AI agents
- **`ResumeTeam`**: Manages team of agents for collaborative improvement
- **`ModelManager`**: Handles Azure OpenAI model configuration and clients
- **`ResumeProcessor`**: PDF processing, text extraction, and image conversion
- **`PromptManager`**: Template loading and caching system
- **`FileManager`**: File operations and validation utilities

### AI Agents

1. **Resume Draft Agent**: Creates improved resume content structure
2. **Resume Enhancement Agent**: Enhances language, impact, and keywords
3. **Resume Conciseness Agent**: Optimizes length and clarity
4. **Resume Image Agent**: Generates final formatted resume with original layout

## 🚀 Quick Start

### Prerequisites

Before installing the Python dependencies, ensure you have these system dependencies:

#### System Dependencies

1. **Poppler** (for PDF processing):

   ```bash
   # Windows (using Chocolatey)
   choco install poppler
   
   # Windows (using Scoop)
   scoop install poppler
   
   # macOS
   brew install poppler
   
   # Ubuntu/Debian
   sudo apt-get install poppler-utils
   ```

2. **wkhtmltopdf** (for HTML to PDF conversion):

   ```bash
   # Windows (using Chocolatey)
   choco install wkhtmltopdf
   
   # Windows (using Scoop) 
   scoop install wkhtmltopdf
   
   # macOS
   brew install wkhtmltopdf
   
   # Ubuntu/Debian
   sudo apt-get install wkhtmltopdf
   ```

3. **Verify PATH**: Ensure both `pdftoppm` (from Poppler) and `wkhtmltopdf` are in your system PATH:

   ```bash
   pdftoppm -h
   wkhtmltopdf --version
   ```

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd resume-improver
   ```

2. **Install UV** (if not already installed):

   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create virtual environment and install dependencies**:

   ```bash
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   
   # Install all dependencies
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your Azure OpenAI credentials
   ```

   Required environment variables in `.env`:

   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2025-01-01
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   ```

## 📖 Usage

### Command Line Interface

The simplest way to use the Resume Improver:

```bash
# Run with a PDF file
python resumeimprover.py path/to/your/resume.pdf

# Interactive mode (will prompt for file path)
python resumeimprover.py
```

### Programmatic Usage

```python
from resumeimprover import ResumeImprover
from model import ModelConfig
import asyncio

async def improve_resume():
    # Initialize with custom configuration
    config = ModelConfig(
        api_key="your-api-key",
        endpoint="https://your-resource.openai.azure.com/"
    )
    
    improver = ResumeImprover(model_config=config)
    
    # Process PDF and get improved content
    text, images = improver.process_pdf_file("resume.pdf")
    improved_content = await improver.improve_resume_workflow(text, images[0])
    
    # Save improved resume
    output_path = improver.save_improved_resume(improved_content, "resume.pdf")
    print(f"Improved resume saved to: {output_path}")

# Run the async function
asyncio.run(improve_resume())
```

## 🧪 Testing

The project includes comprehensive test coverage with 52+ tests across all major components.

### Running Tests

```bash
# Run all tests with pytest (recommended)
uv run pytest tests/ -v

# Run with coverage reporting
uv run pytest tests/ --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/test_utils.py -v

# Using unittest
python -m unittest discover tests -v
```

### Test Structure

- **`tests/test_utils.py`**: Tests for utility classes (PDF processing, file management)
- **`tests/test_model.py`**: Tests for model configuration and management
- **`tests/test_resume_improver.py`**: Tests for main application classes and CLI

See [`tests/README.md`](tests/README.md) for detailed testing documentation.

## 📁 Project Structure

```plaintext
resume-improver/
├── resumeimprover.py        # Main application entry point
├── model.py                 # Model configuration classes
├── utils.py                 # Utility classes for PDF/image processing
├── requirements.txt         # Python dependencies
├── pytest.ini             # Pytest configuration
├── .env                    # Environment variables (create from .env.example)
├── LICENSE                 # Project license
├── prompts/                # AI agent prompt templates
│   ├── resume_draft_agent_prompt.txt
│   ├── resume_enhancement_agent_prompt.txt
│   ├── resume_conciseness_agent_prompt.txt
│   ├── resume_image_agent_prompt.txt
│   └── resume_team_task_prompt.txt
└── tests/                  # Test suite
    ├── test_utils.py
    ├── test_model.py
    ├── test_resume_improver.py
    ├── conftest.py
    ├── run_tests.py
    └── README.md
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required: Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2025-01-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Optional: Custom settings
DEFAULT_DPI=300
PROMPTS_DIRECTORY=./prompts
```

### Model Configuration

The system supports custom model configurations:

```python
from model import ModelConfig, ModelManager

# Custom configuration
config = ModelConfig(
    api_key="your-key",
    endpoint="https://your-endpoint.openai.azure.com/",
    api_version="2025-01-01",
    deployment_name="gpt-4o"
)

# Model manager handles client creation
model_manager = ModelManager(config)
client = model_manager.client
```

## 🔧 Dependencies

### Python Dependencies

Core dependencies installed via `uv pip install -r requirements.txt`:

- **`autogen`** - Multi-agent AI framework
- **`autogen-agentchat`** - Agent communication
- **`autogen-ext[openai,azure]`** - Azure OpenAI integration
- **`python-dotenv`** - Environment variable management
- **`PyPDF2`** - PDF text extraction
- **`pdf2image`** - PDF to image conversion
- **`pdfkit`** - HTML to PDF conversion
- **`Pillow`** - Image processing

### Testing Dependencies

- **`pytest`** - Testing framework
- **`pytest-asyncio`** - Async test support
- **`pytest-cov`** - Coverage reporting
- **`coverage`** - Coverage measurement
- **`unittest-xml-reporting`** - XML test reports

## 🚨 Troubleshooting

### Common Issues

1. **"Poppler not found" error**:
   - Install Poppler using your system package manager
   - Ensure `pdftoppm` is in your PATH
   - Restart your terminal after installation

2. **"wkhtmltopdf not found" error**:
   - Install wkhtmltopdf
   - Ensure `wkhtmltopdf` is in your PATH
   - On Windows, may need to restart terminal/IDE

3. **Azure OpenAI authentication errors**:
   - Verify your API key and endpoint in `.env`
   - Check that your Azure OpenAI resource is deployed
   - Ensure the deployment name matches your configuration

4. **PDF processing errors**:
   - Verify PDF is not corrupted or password-protected
   - Check file permissions
   - Ensure PDF contains extractable text

### Getting Help

1. Check the [tests/README.md](tests/README.md) for testing information
2. Review error messages for specific dependency issues
3. Verify all system dependencies are installed and in PATH
4. Ensure environment variables are properly configured

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the OO architecture patterns
4. Add tests for new functionality
5. Ensure all tests pass (`uv run pytest tests/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone and setup for development
git clone <repository-url>
cd resume-improver
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt

# Run tests to verify setup
uv run pytest tests/ -v
```

## 🔄 Workflow

The Resume Improver follows this workflow:

1. **PDF Input**: Load and validate the resume PDF
2. **Text Extraction**: Extract text content from PDF
3. **Image Conversion**: Convert PDF pages to images for format reference
4. **AI Processing**: Multi-agent team improves the content
   - Draft Agent: Creates improved structure
   - Enhancement Agent: Improves language and keywords
   - Conciseness Agent: Optimizes for clarity and length
5. **Format Generation**: Image Agent creates final resume maintaining original format
6. **Output**: Save improved resume as HTML/PDF

The entire process maintains the original visual design while significantly improving content quality and ATS compatibility.
