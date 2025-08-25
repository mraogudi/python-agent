# Python Coding Agent

A powerful AI-powered Python coding agent that understands natural language programming tasks, generates clean Python code, and executes it safely in a sandboxed environment. Features a modern web interface with syntax highlighting, real-time code execution, and comprehensive error handling.

## ✨ Features

- **🤖 AI-Powered Code Generation**: Uses OpenAI's GPT models to generate Python code from natural language descriptions
- **⚡ Real-time Code Execution**: Safely executes generated code with output capture and error handling
- **🔒 Security-First Design**: Sandboxed execution environment with restricted imports and timeouts
- **🎨 Modern Web Interface**: Clean, responsive UI with syntax highlighting and intuitive controls
- **📊 System Monitoring**: Built-in statistics and system status monitoring
- **⌨️ Keyboard Shortcuts**: Efficient workflow with keyboard shortcuts (Ctrl+Enter, Shift+Enter)
- **📋 Code Examples**: Pre-built examples to get started quickly
- **💡 Smart Validation**: Real-time task description validation with helpful suggestions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for code generation features)
- Modern web browser

### Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir python-agent
   cd python-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   # Required for AI code generation
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional Flask settings
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your_secret_key_here
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

## 🎯 Usage

### Basic Workflow

1. **Enter a Task Description**: Describe what you want the Python code to do
2. **Generate Code**: Click "Generate Code" or press `Ctrl+Enter`
3. **Review & Execute**: Review the generated code and click "Run Generated Code"
4. **View Results**: See the output, errors, and execution statistics

### Example Tasks

**Basic Examples:**
- "Calculate the factorial of a number using recursion"
- "Create a function to check if a number is prime"
- "Sort a list of dictionaries by a specific key"

**Advanced Examples:**
- "Create a class for a simple bank account with deposit, withdraw, and balance methods"
- "Generate a random password with specified length and character requirements"
- "Parse a CSV file and calculate summary statistics"

### Keyboard Shortcuts

- `Ctrl+Enter` (or `Cmd+Enter` on Mac): Generate code
- `Shift+Enter`: Generate and run code immediately
- Click example buttons to fill the task description

### API Endpoints

The application provides RESTful API endpoints for integration:

- `POST /api/generate`: Generate code from task description
- `POST /api/execute`: Execute provided Python code
- `POST /api/generate-and-execute`: Generate and execute in one request
- `POST /api/validate`: Validate task description
- `GET /api/stats`: Get system statistics

## 🔧 Configuration

### Security Settings

The code executor includes several security measures:

- **Execution Timeout**: Maximum 10 seconds per execution
- **Output Limiting**: Maximum 10,000 characters output
- **Restricted Imports**: Only safe, whitelisted modules allowed
- **Sandboxed Environment**: Limited access to system functions

### Allowed Python Modules

By default, these modules are available for generated code:
- Standard library: `math`, `random`, `datetime`, `json`, `csv`, `re`
- Collections: `collections`, `itertools`, `functools`, `operator`
- Data science: `numpy`, `pandas` (if installed)
- Web requests: `requests` (if installed)
- Plotting: `matplotlib.pyplot` (if installed)

### Customizing Security Settings

Edit `config.py` to modify security settings:

```python
class Config:
    MAX_EXECUTION_TIME = 10  # seconds
    MAX_OUTPUT_LENGTH = 10000  # characters
    
    ALLOWED_IMPORTS = {
        'math', 'random', 'datetime', 'json', 'csv', 're',
        'collections', 'itertools', 'functools', 'operator',
        # Add more modules as needed
    }
```

## 🏗️ Project Structure

```
python-agent/
├── app.py                 # Main Flask application
├── coding_agent.py        # AI-powered code generation
├── code_executor.py       # Safe code execution engine
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Main interface
│   ├── 404.html        # 404 error page
│   └── 500.html        # 500 error page
└── static/             # Static assets
    ├── css/
    │   └── style.css   # Custom styles
    └── js/
        └── app.js      # Frontend JavaScript
```

## 🔒 Security Considerations

### Safe Code Execution

The application implements multiple security layers:

1. **Code Validation**: Checks for dangerous patterns before execution
2. **Restricted Environment**: Limited built-in functions and modules
3. **Timeout Protection**: Prevents infinite loops and long-running code
4. **Output Limiting**: Prevents memory exhaustion from large outputs
5. **Import Filtering**: Only whitelisted modules can be imported

### Dangerous Operations Blocked

The following operations are automatically blocked:
- File system access (`open`, `file`)
- System commands (`os`, `subprocess`, `sys`)
- Dynamic code execution (`eval`, `exec`, `compile`)
- Environment access (`globals`, `locals`, `vars`)
- Attribute manipulation (`getattr`, `setattr`, `delattr`)

### Production Deployment

For production use, consider:
- Using environment variables for all sensitive configuration
- Implementing rate limiting on API endpoints
- Adding user authentication and authorization
- Running in a containerized environment
- Setting up proper logging and monitoring
- Using a production WSGI server (e.g., Gunicorn)

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Key Issues:**
- Ensure your API key is set in the `.env` file
- Check that your OpenAI account has sufficient credits
- Verify the API key has the correct permissions

**Code Generation Fails:**
- Check your internet connection
- Verify the OpenAI API is accessible
- Review the task description for clarity

**Code Execution Errors:**
- Check if the generated code uses allowed modules
- Verify the code syntax is correct
- Ensure the execution doesn't exceed time limits

**Web Interface Issues:**
- Clear browser cache and cookies
- Check browser developer console for JavaScript errors
- Ensure the Flask server is running on port 5000

### Debug Mode

Enable debug mode for detailed error information:

```bash
export FLASK_DEBUG=True
python app.py
```

### Logs and Monitoring

The application outputs helpful information:
- Server startup messages with configuration details
- API request/response information in debug mode
- Error tracebacks for debugging issues

## 🤝 Contributing

Contributions are welcome! Here are some ways to contribute:

1. **Bug Reports**: Report issues with detailed reproduction steps
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests with bug fixes or new features
4. **Documentation**: Improve documentation and examples

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API for code generation
- **Flask** for the lightweight web framework
- **Bootstrap** for the responsive UI components
- **Prism.js** for syntax highlighting
- **Font Awesome** for icons

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the GitHub issues for similar problems
3. Create a new issue with detailed information
4. Include error messages, logs, and reproduction steps

---

**Happy Coding! 🎉**

*Made with ❤️ for the Python community* 