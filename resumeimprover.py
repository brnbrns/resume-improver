"""
Object-oriented resume improvement system using AI agents.
"""

import asyncio
import os
import sys
from typing import List, Optional

import pdfkit
from PIL import Image as PilImage

from autogen_core import Image
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat

from model import ModelManager, ModelConfig
from utils import ResumeProcessor, PromptManager, FileManager


class AgentFactory:
    """Factory class for creating different types of resume improvement agents."""
    
    def __init__(self, model_manager: ModelManager, prompt_manager: PromptManager):
        """
        Initialize the agent factory.
        
        Args:
            model_manager: Model manager for creating AI clients
            prompt_manager: Prompt manager for loading agent prompts
        """
        self.model_manager = model_manager
        self.prompt_manager = prompt_manager
    
    def create_draft_agent(self) -> AssistantAgent:
        """Create a resume draft agent."""
        return AssistantAgent(
            name="ResumeDraftAgent",
            model_client=self.model_manager.client,
            system_message=self.prompt_manager.load_prompt("resume_draft_agent_prompt"),
        )
    
    def create_enhancement_agent(self) -> AssistantAgent:
        """Create a resume enhancement agent."""
        return AssistantAgent(
            name="ResumeEnhancementAgent",
            model_client=self.model_manager.client,
            system_message=self.prompt_manager.load_prompt("resume_enhancement_agent_prompt"),
        )
    
    def create_conciseness_agent(self) -> AssistantAgent:
        """Create a resume conciseness agent."""
        return AssistantAgent(
            name="ResumeConcisenessAgent",
            model_client=self.model_manager.client,
            system_message=self.prompt_manager.load_prompt("resume_conciseness_agent_prompt"),
        )
    
    def create_image_agent(self) -> AssistantAgent:
        """Create a resume image generation agent."""
        return AssistantAgent(
            name="ResumeImageAgent",
            model_client=self.model_manager.client,
            system_message=self.prompt_manager.load_prompt("resume_image_agent_prompt"),
        )


class ResumeTeam:
    """Manages a team of agents for resume improvement."""
    
    def __init__(self, agent_factory: AgentFactory):
        """
        Initialize the resume team.
        
        Args:
            agent_factory: Factory for creating agents
        """
        self.agent_factory = agent_factory
        self._team = None
        self._image_agent = None
    
    def create_team(self) -> RoundRobinGroupChat:
        """
        Create a team of agents for text improvement.
        
        Returns:
            RoundRobinGroupChat: Team of text improvement agents
        """
        if self._team is None:
            draft_agent = self.agent_factory.create_draft_agent()
            enhancement_agent = self.agent_factory.create_enhancement_agent()
            conciseness_agent = self.agent_factory.create_conciseness_agent()
            
            # All agents except ResumeImageAgent can output FINAL
            termination_condition = TextMentionTermination(
                "FINAL",
                sources=["ResumeConcisenessAgent"]
            )
            
            self._team = RoundRobinGroupChat(
                [draft_agent, enhancement_agent, conciseness_agent],
                termination_condition=termination_condition,
            )
        
        return self._team
    
    def get_image_agent(self) -> AssistantAgent:
        """
        Get the image generation agent.
        
        Returns:
            AssistantAgent: Image generation agent
        """
        if self._image_agent is None:
            self._image_agent = self.agent_factory.create_image_agent()
        return self._image_agent


class ResumeImprover:
    """Main class for orchestrating the resume improvement process."""
    
    def __init__(self, 
                 model_config: Optional[ModelConfig] = None,
                 prompts_directory: Optional[str] = None,
                 default_dpi: int = 300):
        """
        Initialize the resume improver.
        
        Args:
            model_config: Optional model configuration. If None, loads from environment.
            prompts_directory: Path to prompts directory
            default_dpi: Default DPI for PDF processing
        """
        self.model_manager = ModelManager(model_config)
        self.prompt_manager = PromptManager(prompts_directory)
        self.resume_processor = ResumeProcessor(prompts_directory, default_dpi)
        self.file_manager = FileManager()
        
        self.agent_factory = AgentFactory(self.model_manager, self.prompt_manager)
        self.team = ResumeTeam(self.agent_factory)
    
    async def improve_resume_text(self, resume_text: str) -> Optional[str]:
        """
        Improve resume text using the team of text improvement agents.
        
        Args:
            resume_text: Original resume text content
            
        Returns:
            Optional[str]: Improved resume text, or None if improvement failed
        """
        task_prompt = self.prompt_manager.load_prompt("resume_team_task_prompt")
        task = f"{task_prompt}\n\nOriginal Resume Text:\n{resume_text}"
        
        team = self.team.create_team()
        improve_result = None
        
        async for message in team.run_stream(task=task):
            improve_result = message
        
        if improve_result and improve_result.messages:
            return improve_result.messages[-1].content
        return None
    
    async def generate_resume_image(self, improved_text: str, 
                                  original_image: PilImage.Image) -> Optional[str]:
        """
        Generate an improved resume image using the image agent.
        
        Args:
            improved_text: Improved resume text content
            original_image: Original resume image for format reference
            
        Returns:
            Optional[str]: Generated resume image content, or None if generation failed
        """
        image_agent = self.team.get_image_agent()
        
        image_task = MultiModalMessage(
            content=[
                f"New Resume Content:\n{improved_text}\n\nOriginal image with desired format attached",
                Image.from_pil(original_image)
            ],
            source="user"
        )
        
        result = None
        async for message in image_agent.run_stream(task=image_task):
            result = message
        
        if result and result.messages:
            return result.messages[-1].content
        return None
    
    async def improve_resume(self, resume_text: str, 
                           resume_image: PilImage.Image) -> Optional[str]:
        """
        Complete resume improvement workflow.
        
        Args:
            resume_text: Original resume text content
            resume_image: Original resume image for format reference
            
        Returns:
            Optional[str]: Final improved resume content, or None if improvement failed
        """
        print("Step 1: Improving resume text content...")
        improved_text = await self.improve_resume_text(resume_text)
        
        if not improved_text:
            print("❌ Failed to improve resume text content")
            return None
        
        print("✓ Resume text improved successfully")
        print("Step 2: Generating improved resume file...")
        
        final_content = await self.generate_resume_image(improved_text, resume_image)
        
        if final_content:
            print("✓ Resume image generated successfully")
        else:
            print("❌ Failed to generate resume image")
        
        return final_content
    
    def process_pdf_file(self, pdf_path: str) -> tuple[str, List[PilImage.Image]]:
        """
        Process a PDF file to extract text and images.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            tuple: (extracted_text, list_of_images)
        """
        print(f"Processing resume: {pdf_path}")
        print("Extracting text content...")
        
        text_content, images, _ = self.resume_processor.process_pdf(pdf_path)
        
        if not text_content.strip():
            raise ValueError("No text could be extracted from the PDF")
        
        if not images:
            raise ValueError("No images could be extracted from the PDF")
        
        print(f"✓ Extracted {len(text_content)} characters of text")
        print(f"✓ Converted {len(images)} pages to images")
        
        return text_content, images
    
    def save_improved_resume(self, html_content: str, original_pdf_path: str) -> str:
        """
        Save the improved resume as a PDF file.
        
        Args:
            html_content: HTML content of the improved resume
            original_pdf_path: Path to the original PDF file
            
        Returns:
            str: Path to the saved improved resume PDF
        """
        output_path = self.file_manager.generate_output_filename(original_pdf_path)
        
        try:
            pdfkit.from_string(html_content, output_path)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Failed to save improved resume: {e}")


class ResumeImproverCLI:
    """Command-line interface for the resume improver."""
    
    def __init__(self, resumeimprover: Optional[ResumeImprover] = None):
        """
        Initialize the CLI.
        
        Args:
            resumeimprover: Optional ResumeImprover instance. Creates default if None.
        """
        self.improver = resumeimprover or ResumeImprover()
    
    def get_pdf_path(self) -> str:
        """
        Get PDF path from command line arguments or user input.
        
        Returns:
            str: Path to the PDF file
            
        Raises:
            ValueError: If no valid PDF path is provided
        """
        if len(sys.argv) >= 2:
            pdf_path = sys.argv[1]
        else:
            pdf_path = input("Enter the path to your resume PDF: ").strip()
        
        if not pdf_path:
            raise ValueError("No file path provided")
        
        return pdf_path
    
    def validate_pdf_file(self, pdf_path: str) -> str:
        """
        Validate the PDF file path.
        
        Args:
            pdf_path: Path to validate
            
        Returns:
            str: Validated path
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a PDF
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File '{pdf_path}' not found")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("Please provide a PDF file")
        
        return pdf_path
    
    async def run(self) -> None:
        """Run the complete resume improvement process."""
        try:
            # Get and validate PDF path
            pdf_path = self.get_pdf_path()
            pdf_path = self.validate_pdf_file(pdf_path)
            
            # Process the PDF file
            resume_text, resume_images = self.improver.process_pdf_file(pdf_path)
            
            print("\nStarting resume improvement process...")
            print("The AI agents will now work together to improve your resume.")
            print("-" * 60)
            
            # Improve the resume
            final_resume_content = await self.improver.improve_resume(
                resume_text, resume_images[0]
            )
            
            if final_resume_content:
                print("\n" + "=" * 60)
                print("RESUME IMPROVEMENT COMPLETED")
                print("=" * 60)
                
                # Save the improved resume
                try:
                    output_path = self.improver.save_improved_resume(
                        final_resume_content, pdf_path
                    )
                    
                    print(f"\n✅ SUCCESS! Your improved resume has been saved as:")
                    print(f"   {output_path}")
                    print("\nThe improved resume maintains the original format while enhancing:")
                    print("• Content quality and impact")
                    print("• Keyword optimization")  
                    print("• Professional language")
                    print("• ATS compatibility")
                    
                except Exception as e:
                    print(f"\n⚠️  Resume improved but could not save to PDF: {e}")
                    print("HTML content was generated successfully.")
            else:
                print("\n❌ Error: No improved resume was generated by the agents.")
                print("Please check your model configuration and try again.")
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error processing resume: {e}")
            print("Please ensure you have all required dependencies installed.")
            print("Run: uv pip install -r requirements.txt")


async def main():
    """Main entry point for backward compatibility."""
    cli = ResumeImproverCLI()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
