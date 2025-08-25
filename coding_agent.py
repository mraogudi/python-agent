import openai
import re
from typing import Dict, Tuple, Optional
from config import Config

class CodingAgent:
    """AI-powered coding agent that generates Python code from natural language descriptions."""
    
    def __init__(self):
        """Initialize the coding agent with OpenAI API."""
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_code(self, task_description: str) -> Dict[str, any]:
        """
        Generate Python code based on natural language task description.
        
        Args:
            task_description (str): Natural language description of the programming task
            
        Returns:
            Dict containing generated code, explanation, and metadata
        """
        try:
            # Create a comprehensive prompt for code generation
            prompt = self._create_code_generation_prompt(task_description)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            # Parse the response
            content = response.choices[0].message.content
            code, explanation = self._parse_response(content)
            
            return {
                "success": True,
                "code": code,
                "explanation": explanation,
                "task": task_description,
                "model_used": "gpt-3.5-turbo"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": "",
                "explanation": f"Failed to generate code: {str(e)}",
                "task": task_description
            }
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI model."""
        return """You are an expert Python programmer. Your job is to generate clean, efficient, and well-commented Python code based on natural language descriptions.

Guidelines:
1. Write clean, readable Python code that follows best practices
2. Include helpful comments explaining the logic
3. Use appropriate variable names and function structures
4. Handle common edge cases and errors when appropriate
5. Keep the code focused and avoid unnecessary complexity
6. Use only standard Python libraries or commonly available packages (math, random, datetime, json, etc.)
7. Format your response with the code in triple backticks followed by an explanation

Response format:
```python
# Your generated Python code here
```

Explanation: Brief explanation of what the code does and how it works."""
    
    def _create_code_generation_prompt(self, task_description: str) -> str:
        """Create a detailed prompt for code generation."""
        return f"""Generate Python code for the following task:

Task: {task_description}

Please provide:
1. Clean, working Python code that accomplishes the task
2. Appropriate comments explaining the code
3. A brief explanation after the code block

Make sure the code is ready to run and includes any necessary imports."""
    
    def _parse_response(self, content: str) -> Tuple[str, str]:
        """
        Parse the AI response to extract code and explanation.
        
        Args:
            content (str): Raw response from the AI model
            
        Returns:
            Tuple of (code, explanation)
        """
        # Extract code block
        code_pattern = r'```python\n(.*?)```'
        code_match = re.search(code_pattern, content, re.DOTALL)
        
        if code_match:
            code = code_match.group(1).strip()
        else:
            # Fallback: look for any code block
            code_pattern_generic = r'```\n(.*?)```'
            code_match_generic = re.search(code_pattern_generic, content, re.DOTALL)
            if code_match_generic:
                code = code_match_generic.group(1).strip()
            else:
                code = content.strip()
        
        # Extract explanation (everything after the code block)
        if code_match:
            explanation_start = code_match.end()
            explanation = content[explanation_start:].strip()
            # Remove "Explanation:" prefix if present
            explanation = re.sub(r'^Explanation:\s*', '', explanation, flags=re.IGNORECASE)
        else:
            explanation = "Generated code based on the given task description."
        
        return code, explanation
    
    def validate_task_description(self, task_description: str) -> Dict[str, any]:
        """
        Validate and provide suggestions for the task description.
        
        Args:
            task_description (str): The task description to validate
            
        Returns:
            Dict with validation results and suggestions
        """
        if not task_description or len(task_description.strip()) < 5:
            return {
                "valid": False,
                "message": "Task description is too short. Please provide more details.",
                "suggestions": [
                    "Describe what you want the code to do",
                    "Include input/output requirements",
                    "Specify any constraints or requirements"
                ]
            }
        
        # Check for vague descriptions
        vague_keywords = ['something', 'anything', 'stuff', 'thing']
        if any(keyword in task_description.lower() for keyword in vague_keywords):
            return {
                "valid": True,
                "message": "Your description seems vague. Consider being more specific.",
                "suggestions": [
                    "Be more specific about the desired functionality",
                    "Include examples of expected input/output",
                    "Mention any specific algorithms or approaches"
                ]
            }
        
        return {
            "valid": True,
            "message": "Task description looks good!",
            "suggestions": []
        } 