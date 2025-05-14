// Main JavaScript file for Anton AI Assistant

// Markdown parser for better message formatting
function parseMarkdown(text) {
    // Code blocks with language
    text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="code-block language-$1">$2</pre>');
    
    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Italic
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Headers
    text = text.replace(/^### (.*$)/gm, '<h3 class="text-lg font-semibold mt-3 mb-2">$1</h3>');
    text = text.replace(/^## (.*$)/gm, '<h2 class="text-xl font-semibold mt-4 mb-2">$1</h2>');
    text = text.replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mt-4 mb-3">$1</h1>');
    
    // Links
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-500 hover:underline" target="_blank">$1</a>');
    
    // Lists
    text = text.replace(/^\s*(\d+\.)\s+(.*)/gm, '<li class="list-decimal ml-5">$2</li>');
    text = text.replace(/^\s*(\*|\-)\s+(.*)/gm, '<li class="list-disc ml-5">$2</li>');
    
    // Line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Initialize syntax highlighting for code blocks
function initializeSyntaxHighlighting() {
    document.querySelectorAll('pre.code-block').forEach((block) => {
        const language = block.className.split('language-')[1];
        if (language && window.hljs) {
            hljs.highlightElement(block);
        }
    });
}

// Copy to clipboard function
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    // Show tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'bg-gray-800 text-white py-1 px-2 rounded text-sm fixed transition-opacity';
    tooltip.style.top = '20px';
    tooltip.style.left = '50%';
    tooltip.style.transform = 'translateX(-50%)';
    tooltip.style.zIndex = '1000';
    tooltip.textContent = 'Copied to clipboard!';
    document.body.appendChild(tooltip);
    
    setTimeout(() => {
        tooltip.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(tooltip);
        }, 300);
    }, 1500);
}

// Add copy button to code blocks
function addCopyButtonsToCodeBlocks() {
    document.querySelectorAll('pre.code-block').forEach((block) => {
        const copyButton = document.createElement('button');
        copyButton.className = 'absolute top-2 right-2 bg-gray-700 text-white rounded p-1 text-xs opacity-50 hover:opacity-100 transition';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.addEventListener('click', () => {
            copyToClipboard(block.textContent);
        });
        
        // Make the code block relative position for absolute positioning of the button
        block.style.position = 'relative';
        block.appendChild(copyButton);
    });
}

// Toggle dark mode
function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');
    
    // Save preference to localStorage
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}

// Load dark mode preference
function loadDarkModePreference() {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
}

// Initialize file upload
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');
    
    if (fileInput && uploadButton) {
        uploadButton.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                fetch('/api/upload_file', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Add system message about file upload
                        const chatMessages = document.getElementById('chatMessages');
                        const messageEl = document.createElement('div');
                        messageEl.className = 'message-system p-2 mb-4 text-center';
                        messageEl.innerHTML = `<div class="text-sm text-gray-500">File uploaded: ${data.filename}</div>`;
                        chatMessages.appendChild(messageEl);
                        
                        // Scroll to bottom
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                        
                        // Refresh file list
                        loadFiles();
                    } else {
                        alert('Upload failed: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error uploading file:', error);
                    alert('Upload failed due to network error.');
                });
            }
        });
    }
}

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    loadDarkModePreference();
    initializeFileUpload();
    
    // Add dark mode toggle button
    const header = document.querySelector('header');
    const darkModeButton = document.createElement('button');
    darkModeButton.className = 'bg-gray-200 dark:bg-gray-700 p-2 rounded-full ml-2';
    darkModeButton.innerHTML = '<i class="fas fa-moon"></i>';
    darkModeButton.addEventListener('click', toggleDarkMode);
    
    const headerButtons = document.createElement('div');
    headerButtons.className = 'flex items-center';
    headerButtons.appendChild(darkModeButton);
    
    const existingButton = header.querySelector('div:last-child');
    existingButton.parentNode.replaceChild(headerButtons, existingButton);
    headerButtons.appendChild(existingButton);
    
    // Add message post-processing
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                // Process any new messages
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('message-anton')) {
                        const messageDiv = node.querySelector('.text-gray-700');
                        if (messageDiv) {
                            // Apply markdown parsing
                            messageDiv.innerHTML = parseMarkdown(messageDiv.innerHTML);
                            
                            // Add copy buttons to code blocks
                            addCopyButtonsToCodeBlocks();
                            
                            // Apply syntax highlighting
                            initializeSyntaxHighlighting();
                        }
                    }
                });
            }
        });
    });
    
    observer.observe(document.getElementById('chatMessages'), { childList: true });
});