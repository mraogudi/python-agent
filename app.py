from flask import Flask, render_template, request, jsonify
import json
import traceback
from datetime import datetime
from config import Config
from coding_agent import CodingAgent
from code_executor import CodeExecutor

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
try:
    coding_agent = CodingAgent()
    code_executor = CodeExecutor()
except Exception as e:
    print(f"Warning: Failed to initialize coding agent: {e}")
    print("Please make sure your OpenAI API key is set in the environment variables.")
    coding_agent = None
    code_executor = CodeExecutor()

@app.route('/')
def index():
    """Main page route."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_code():
    """API endpoint to generate code from natural language description."""
    try:
        # Get task description from request
        data = request.get_json()
        print(data)
        task_description = data.get('task_description', '').strip()
        print(task_description)
        print(coding_agent)
        
        if not task_description:
            return jsonify({
                'success': False,
                'error': 'Please provide a task description'
            }), 400
        
        if not coding_agent:
            return jsonify({
                'success': False,
                'error': 'Coding agent not available. Please check your OpenAI API key configuration.'
            }), 500
        
        # Validate task description
        validation = coding_agent.validate_task_description(task_description)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'error': validation['message'],
                'suggestions': validation.get('suggestions', [])
            }), 400
        
        # Generate code
        result = coding_agent.generate_code(task_description)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """API endpoint to execute generated code."""
    try:
        # Get code from request
        data = request.get_json()
        code = data.get('code', '').strip()
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Please provide code to execute'
            }), 400
        
        # Execute code
        result = code_executor.execute_code(code)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/api/generate-and-execute', methods=['POST'])
def generate_and_execute():
    """API endpoint to generate and execute code in one request."""
    try:
        # Get task description from request
        data = request.get_json()
        task_description = data.get('task_description', '').strip()
        
        if not task_description:
            return jsonify({
                'success': False,
                'error': 'Please provide a task description'
            }), 400
        
        if not coding_agent:
            return jsonify({
                'success': False,
                'error': 'Coding agent not available. Please check your OpenAI API key configuration.'
            }), 500
        
        # Validate task description
        validation = coding_agent.validate_task_description(task_description)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'error': validation['message'],
                'suggestions': validation.get('suggestions', [])
            }), 400
        
        # Generate code
        generation_result = coding_agent.generate_code(task_description)
        
        if not generation_result['success']:
            return jsonify({
                'success': False,
                'error': f"Code generation failed: {generation_result.get('error', 'Unknown error')}",
                'generation_result': generation_result
            }), 500
        
        # Execute the generated code
        execution_result = code_executor.execute_code(generation_result['code'])
        
        # Combine results
        combined_result = {
            'success': True,
            'task_description': task_description,
            'generation': generation_result,
            'execution': execution_result,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(combined_result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/api/validate', methods=['POST'])
def validate_task():
    """API endpoint to validate task description."""
    try:
        data = request.get_json()
        task_description = data.get('task_description', '').strip()
        
        if not coding_agent:
            return jsonify({
                'valid': True,
                'message': 'Task validation not available (coding agent not initialized)',
                'suggestions': []
            })
        
        validation = coding_agent.validate_task_description(task_description)
        return jsonify(validation)
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': f'Validation error: {str(e)}',
            'suggestions': []
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint to get system statistics."""
    try:
        stats = {
            'executor_stats': code_executor.get_execution_stats(),
            'agent_available': coding_agent is not None,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get stats: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Check if OpenAI API key is configured
    if not Config.OPENAI_API_KEY:
        print("⚠️  WARNING: OpenAI API key not found!")
        print("Please set the OPENAI_API_KEY environment variable to use the code generation features.")
        print("You can still use the code execution features without an API key.")
        print()
    
    print("🚀 Starting Python Coding Agent...")
    print(f"📝 Debug mode: {Config.DEBUG}")
    print(f"🔧 Flask environment: {Config.FLASK_ENV}")
    print()
    print("🌐 Access the application at: http://localhost:5000")
    print()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    ) 
