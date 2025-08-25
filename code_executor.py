import subprocess
import sys
import io
import contextlib
import signal
import threading
import time
from typing import Dict, Any, Optional
from config import Config

class CodeExecutor:
    """Safe Python code executor with timeout and output capture."""
    
    def __init__(self):
        """Initialize the code executor with security settings."""
        self.max_execution_time = Config.MAX_EXECUTION_TIME
        self.max_output_length = Config.MAX_OUTPUT_LENGTH
        self.allowed_imports = Config.ALLOWED_IMPORTS
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code safely with timeout and output capture.
        
        Args:
            code (str): Python code to execute
            
        Returns:
            Dict containing execution results, output, errors, and metadata
        """
        # Validate code before execution
        validation_result = self._validate_code(code)
        if not validation_result["valid"]:
            return {
                "success": False,
                "output": "",
                "error": validation_result["error"],
                "execution_time": 0,
                "code": code
            }
        
        # Prepare execution environment
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        result = {
            "success": False,
            "output": "",
            "error": "",
            "execution_time": 0,
            "code": code
        }
        
        try:
            # Create a restricted execution environment
            exec_globals = self._create_safe_globals()
            exec_locals = {}
            
            # Execute code with timeout
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                
                # Use threading for timeout control
                execution_thread = threading.Thread(
                    target=self._execute_with_globals,
                    args=(code, exec_globals, exec_locals)
                )
                
                execution_thread.daemon = True
                execution_thread.start()
                execution_thread.join(timeout=self.max_execution_time)
                
                if execution_thread.is_alive():
                    # Timeout occurred
                    result["error"] = f"Code execution timed out after {self.max_execution_time} seconds"
                    return result
            
            # Capture output
            stdout_content = stdout_capture.getvalue()
            stderr_content = stderr_capture.getvalue()
            
            # Limit output length
            if len(stdout_content) > self.max_output_length:
                stdout_content = stdout_content[:self.max_output_length] + "\n... (output truncated)"
            
            result["success"] = True
            result["output"] = stdout_content
            result["error"] = stderr_content if stderr_content else ""
            
        except SyntaxError as e:
            result["error"] = f"Syntax Error: {str(e)}"
        except ImportError as e:
            result["error"] = f"Import Error: {str(e)} - This import is not allowed for security reasons"
        except Exception as e:
            result["error"] = f"Runtime Error: {str(e)}"
        
        finally:
            result["execution_time"] = time.time() - start_time
        
        return result
    
    def _execute_with_globals(self, code: str, exec_globals: dict, exec_locals: dict):
        """Execute code with the provided globals and locals."""
        exec(code, exec_globals, exec_locals)
    
    def _validate_code(self, code: str) -> Dict[str, Any]:
        """
        Validate code for basic security and syntax issues.
        
        Args:
            code (str): Code to validate
            
        Returns:
            Dict with validation results
        """
        if not code or not code.strip():
            return {"valid": False, "error": "No code provided"}
        
        # Check for dangerous operations
        dangerous_patterns = [
            'import os', 'import subprocess', 'import sys',
            'eval(', 'exec(', '__import__',
            'open(', 'file(', 'input(',
            'raw_input(', 'compile(',
            'globals()', 'locals()', 'vars(',
            'dir(', 'getattr(', 'setattr(',
            'delattr(', 'hasattr(',
            'exit(', 'quit(', 'reload('
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return {
                    "valid": False,
                    "error": f"Potentially dangerous operation detected: {pattern}"
                }
        
        # Check syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error: {str(e)}"
            }
        
        return {"valid": True, "error": ""}
    
    def _create_safe_globals(self) -> dict:
        """
        Create a safe globals dictionary with limited built-ins.
        
        Returns:
            Dict with safe global variables and functions
        """
        # Start with a minimal set of safe built-ins
        safe_builtins = {
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sorted': sorted,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'pow': pow,
                'divmod': divmod,
                'isinstance': isinstance,
                'type': type,
                'ValueError': ValueError,
                'TypeError': TypeError,
                'IndexError': IndexError,
                'KeyError': KeyError,
                'Exception': Exception,
            }
        }
        
        # Add allowed modules
        allowed_modules = {}
        for module_name in self.allowed_imports:
            try:
                if '.' in module_name:
                    # Handle imports like 'matplotlib.pyplot'
                    parts = module_name.split('.')
                    module = __import__(module_name, fromlist=[parts[-1]])
                    allowed_modules[parts[-1]] = module
                else:
                    module = __import__(module_name)
                    allowed_modules[module_name] = module
            except ImportError:
                # Module not available, skip it
                pass
        
        # Combine safe builtins with allowed modules
        safe_globals = {**safe_builtins, **allowed_modules}
        return safe_globals
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        Get current execution environment statistics.
        
        Returns:
            Dict with execution environment info
        """
        return {
            "max_execution_time": self.max_execution_time,
            "max_output_length": self.max_output_length,
            "allowed_imports": list(self.allowed_imports),
            "python_version": sys.version,
            "security_level": "restricted"
        } 