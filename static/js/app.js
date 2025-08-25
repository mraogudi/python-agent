// Python Coding Agent - Frontend JavaScript

class CodingAgentApp {
    constructor() {
        this.currentCode = '';
        this.isLoading = false;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Form submission
        document.getElementById('taskForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateCode();
        });

        // Generate and run button
        document.getElementById('generateAndRunBtn').addEventListener('click', () => {
            this.generateAndRunCode();
        });

        // Run code button
        document.getElementById('runCodeBtn').addEventListener('click', () => {
            this.runCode();
        });

        // Task description input validation
        document.getElementById('taskDescription').addEventListener('input', (e) => {
            this.validateTaskDescription(e.target.value);
        });

        // Task description blur event for validation
        document.getElementById('taskDescription').addEventListener('blur', (e) => {
            if (e.target.value.trim()) {
                this.validateTaskDescription(e.target.value);
            }
        });
    }

    async validateTaskDescription(description) {
        if (!description || description.length < 5) {
            this.hideValidationAlert();
            return;
        }

        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ task_description: description })
            });

            const data = await response.json();
            this.showValidationAlert(data);
        } catch (error) {
            console.error('Validation error:', error);
        }
    }

    showValidationAlert(validation) {
        const alertDiv = document.getElementById('validationAlert');
        const messageEl = document.getElementById('validationMessage');
        const suggestionsEl = document.getElementById('validationSuggestions');

        messageEl.textContent = validation.message;

        // Clear previous suggestions
        suggestionsEl.innerHTML = '';

        if (validation.suggestions && validation.suggestions.length > 0) {
            const suggestionsList = document.createElement('ul');
            suggestionsList.className = 'mb-0';
            
            validation.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                suggestionsList.appendChild(li);
            });
            
            suggestionsEl.appendChild(suggestionsList);
        }

        // Set alert class based on validation result
        alertDiv.className = validation.valid ? 
            'alert alert-info mt-3' : 
            'alert alert-warning mt-3';

        alertDiv.style.display = 'block';
        alertDiv.classList.add('fade-in');
    }

    hideValidationAlert() {
        const alertDiv = document.getElementById('validationAlert');
        alertDiv.style.display = 'none';
    }

    async generateCode() {
        const taskDescription = document.getElementById('taskDescription').value.trim();
        
        if (!taskDescription) {
            this.showError('Please enter a task description.');
            return;
        }

        this.setLoadingState(true, 'Generating code...');

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ task_description: taskDescription })
            });

            const data = await response.json();

            if (data.success) {
                this.displayGeneratedCode(data);
                this.currentCode = data.code;
                document.getElementById('runCodeBtn').disabled = false;
                this.hideValidationAlert();
            } else {
                this.showError(data.error, data.suggestions);
            }
        } catch (error) {
            this.showError('Failed to generate code. Please try again.');
            console.error('Generate code error:', error);
        } finally {
            this.setLoadingState(false);
        }
    }

    async generateAndRunCode() {
        const taskDescription = document.getElementById('taskDescription').value.trim();
        
        if (!taskDescription) {
            this.showError('Please enter a task description.');
            return;
        }

        this.setLoadingState(true, 'Generating and running code...');

        try {
            const response = await fetch('/api/generate-and-execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ task_description: taskDescription })
            });

            const data = await response.json();

            if (data.success) {
                this.displayGeneratedCode(data.generation);
                this.displayExecutionResults(data.execution);
                this.currentCode = data.generation.code;
                document.getElementById('runCodeBtn').disabled = false;
                this.hideValidationAlert();
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Failed to generate and run code. Please try again.');
            console.error('Generate and run error:', error);
        } finally {
            this.setLoadingState(false);
        }
    }

    async runCode() {
        if (!this.currentCode) {
            this.showError('No code to run. Generate code first.');
            return;
        }

        this.setLoadingState(true, 'Running code...');

        try {
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: this.currentCode })
            });

            const data = await response.json();
            this.displayExecutionResults(data);
        } catch (error) {
            this.showError('Failed to run code. Please try again.');
            console.error('Run code error:', error);
        } finally {
            this.setLoadingState(false);
        }
    }

    displayGeneratedCode(data) {
        const codeSection = document.getElementById('codeSection');
        const codeElement = document.getElementById('generatedCode');
        const explanationElement = document.getElementById('explanationText');

        // Update code
        codeElement.textContent = data.code;
        
        // Update explanation
        explanationElement.textContent = data.explanation;

        // Show code section
        this.hideAllSections();
        codeSection.style.display = 'block';
        codeSection.classList.add('fade-in');

        // Trigger syntax highlighting
        if (window.Prism) {
            Prism.highlightElement(codeElement);
        }
    }

    displayExecutionResults(data) {
        const executionSection = document.getElementById('executionSection');
        const outputElement = document.getElementById('executionOutput');
        const errorElement = document.getElementById('executionError');
        const timeElement = document.getElementById('executionTime');

        // Clear previous results
        outputElement.textContent = '';
        errorElement.textContent = '';
        errorElement.style.display = 'none';

        if (data.success) {
            outputElement.textContent = data.output || 'Code executed successfully (no output)';
            outputElement.className = 'output-container';
        } else {
            errorElement.textContent = data.error;
            errorElement.style.display = 'block';
        }

        // Show execution time
        timeElement.textContent = `Execution time: ${(data.execution_time * 1000).toFixed(2)}ms`;

        // Show execution section
        executionSection.style.display = 'block';
        executionSection.classList.add('slide-up');
    }

    setLoadingState(isLoading, text = 'Processing...') {
        this.isLoading = isLoading;
        const loadingState = document.getElementById('loadingState');
        const loadingText = document.getElementById('loadingText');
        const buttons = ['generateBtn', 'generateAndRunBtn', 'runCodeBtn'];

        if (isLoading) {
            this.hideAllSections();
            loadingText.textContent = text;
            loadingState.style.display = 'block';
            
            // Disable buttons
            buttons.forEach(btnId => {
                document.getElementById(btnId).disabled = true;
            });
        } else {
            loadingState.style.display = 'none';
            
            // Enable buttons
            buttons.forEach(btnId => {
                const btn = document.getElementById(btnId);
                if (btnId === 'runCodeBtn') {
                    btn.disabled = !this.currentCode;
                } else {
                    btn.disabled = false;
                }
            });
        }
    }

    hideAllSections() {
        const sections = ['initialState', 'codeSection', 'executionSection', 'loadingState'];
        sections.forEach(sectionId => {
            document.getElementById(sectionId).style.display = 'none';
        });
    }

    showError(message, suggestions = []) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
        alertDiv.innerHTML = `
            <h6 class="alert-heading">Error</h6>
            <p class="mb-2">${message}</p>
            ${suggestions.length > 0 ? `
                <hr>
                <h6>Suggestions:</h6>
                <ul class="mb-0">
                    ${suggestions.map(s => `<li>${s}</li>`).join('')}
                </ul>
            ` : ''}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert error after the form
        const form = document.getElementById('taskForm');
        form.parentNode.insertBefore(alertDiv, form.nextSibling);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 10000);
    }
}

// Utility functions
function fillExample(text) {
    document.getElementById('taskDescription').value = text;
    document.getElementById('taskDescription').focus();
    
    // Trigger validation
    app.validateTaskDescription(text);
}

function copyCode() {
    const codeElement = document.getElementById('generatedCode');
    const code = codeElement.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        // Show success feedback
        const copyBtn = event.target.closest('button');
        const originalHtml = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        copyBtn.classList.add('btn-success');
        copyBtn.classList.remove('btn-outline-secondary');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalHtml;
            copyBtn.classList.remove('btn-success');
            copyBtn.classList.add('btn-outline-secondary');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy code:', err);
        alert('Failed to copy code to clipboard');
    });
}

async function showStats() {
    try {
        const modal = new bootstrap.Modal(document.getElementById('statsModal'));
        modal.show();
        
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        const statsContent = document.getElementById('statsContent');
        
        if (data.error) {
            statsContent.innerHTML = `
                <div class="alert alert-danger">
                    <h6>Error loading stats</h6>
                    <p>${data.error}</p>
                </div>
            `;
            return;
        }
        
        const stats = data.executor_stats;
        statsContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Code Execution Environment</h6>
                    <table class="table table-sm stats-table">
                        <tr>
                            <th>Max Execution Time</th>
                            <td>${stats.max_execution_time}s</td>
                        </tr>
                        <tr>
                            <th>Max Output Length</th>
                            <td>${stats.max_output_length.toLocaleString()} chars</td>
                        </tr>
                        <tr>
                            <th>Security Level</th>
                            <td><span class="badge bg-success">${stats.security_level}</span></td>
                        </tr>
                        <tr>
                            <th>Python Version</th>
                            <td>${stats.python_version.split(' ')[0]}</td>
                        </tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <h6>System Status</h6>
                    <table class="table table-sm stats-table">
                        <tr>
                            <th>AI Agent Status</th>
                            <td>
                                <span class="badge ${data.agent_available ? 'bg-success' : 'bg-warning'}">
                                    ${data.agent_available ? 'Available' : 'Not Available'}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <th>Allowed Imports</th>
                            <td>${stats.allowed_imports.length} modules</td>
                        </tr>
                        <tr>
                            <th>Last Updated</th>
                            <td>${new Date(data.timestamp).toLocaleString()}</td>
                        </tr>
                    </table>
                    
                    <h6 class="mt-3">Allowed Python Modules</h6>
                    <div class="text-muted small">
                        ${stats.allowed_imports.sort().map(module => 
                            `<span class="badge bg-light text-dark me-1 mb-1">${module}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading stats:', error);
        document.getElementById('statsContent').innerHTML = `
            <div class="alert alert-danger">
                <h6>Error</h6>
                <p>Failed to load system statistics.</p>
            </div>
        `;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CodingAgentApp();
    
    // Focus on task description input
    document.getElementById('taskDescription').focus();
});

// Handle keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate code
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!app.isLoading) {
            app.generateCode();
        }
    }
    
    // Shift + Enter to generate and run
    if (e.shiftKey && e.key === 'Enter') {
        e.preventDefault();
        if (!app.isLoading) {
            app.generateAndRunCode();
        }
    }
}); 