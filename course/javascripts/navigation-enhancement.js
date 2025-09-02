// Enhanced Navigation and Topic Discovery
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all navigation enhancements
    initializeNavigationEnhancements();
    
    function initializeNavigationEnhancements() {
        addNavigationProgress();
        enhanceSearch();
        addTopicFiltering();
        addKeyboardShortcuts();
        trackUserProgress();
    }
    
    // Add progress indicators to navigation items
    function addNavigationProgress() {
        const navItems = document.querySelectorAll('.md-nav__item');
        const progress = JSON.parse(localStorage.getItem('agentic-ai-progress') || '{}');
        
        navItems.forEach(item => {
            const link = item.querySelector('.md-nav__link');
            if (!link) return;
            
            const href = link.getAttribute('href');
            if (!href) return;
            
            // Check if this item is completed
            if (progress[href]) {
                item.classList.add('completed');
            }
            
            // Check if this is the current page
            if (window.location.pathname.includes(href.replace('.html', ''))) {
                item.classList.add('in-progress');
            }
        });
    }
    
    // Enhanced search functionality
    function enhanceSearch() {
        const searchInput = document.querySelector('.md-search__input');
        if (!searchInput) return;
        
        // Add search suggestions
        const suggestions = [
            'LangChain', 'LangGraph', 'Pydantic AI', 'OpenAI Swarm',
            'multi-agent systems', 'reflection', 'tool use', 'planning',
            'autonomous agents', 'MCP', 'enterprise platforms',
            'fine-tuning', 'RAG', 'optimization', 'debugging'
        ];
        
        // Add placeholder rotation
        let suggestionIndex = 0;
        setInterval(() => {
            if (searchInput.value === '') {
                searchInput.placeholder = `Search for ${suggestions[suggestionIndex]}...`;
                suggestionIndex = (suggestionIndex + 1) % suggestions.length;
            }
        }, 3000);
        
        // Enhanced search results tracking
        searchInput.addEventListener('input', function() {
            if (this.value.length > 2) {
                // Track search queries for analytics
                console.log('Search query:', this.value);
            }
        });
    }
    
    // Topic filtering functionality
    function addTopicFiltering() {
        // Add topic filter buttons if on tags page
        if (window.location.pathname.includes('tags')) {
            addTopicFilterButtons();
        }
        
        // Add course filter functionality
        addCourseFiltering();
    }
    
    function addTopicFilterButtons() {
        const topicCategories = [
            { name: 'All', filter: '' },
            { name: 'Foundation', filter: 'foundation' },
            { name: 'Implementation', filter: 'implementation' },
            { name: 'Advanced', filter: 'advanced' },
            { name: 'Strategy', filter: 'strategy' },
            { name: 'Labs', filter: 'labs' },
            { name: 'Research', filter: 'research' }
        ];
        
        const filterContainer = document.createElement('div');
        filterContainer.className = 'topic-filters';
        filterContainer.innerHTML = '<h3>Filter by Category:</h3>';
        
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'filter-buttons';
        
        topicCategories.forEach(category => {
            const button = document.createElement('button');
            button.className = 'filter-button';
            button.textContent = category.name;
            button.dataset.filter = category.filter;
            
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                document.querySelectorAll('.filter-button').forEach(btn => 
                    btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Filter content
                filterTopicContent(category.filter);
            });
            
            buttonContainer.appendChild(button);
        });
        
        filterContainer.appendChild(buttonContainer);
        
        // Insert filter container after the first heading
        const firstHeading = document.querySelector('.md-content h1');
        if (firstHeading && firstHeading.nextElementSibling) {
            firstHeading.parentNode.insertBefore(filterContainer, firstHeading.nextElementSibling);
        }
    }
    
    function filterTopicContent(filter) {
        const contentSections = document.querySelectorAll('.md-content h2, .md-content h3, .md-content ul, .md-content p');
        
        contentSections.forEach(section => {
            if (filter === '') {
                section.style.display = '';
            } else {
                const text = section.textContent.toLowerCase();
                const shouldShow = text.includes(filter.toLowerCase());
                section.style.display = shouldShow ? '' : 'none';
            }
        });
    }
    
    // Course filtering functionality
    function addCourseFiltering() {
        const courseCards = document.querySelectorAll('.learning-card, .path-card');
        
        courseCards.forEach(card => {
            card.addEventListener('click', function() {
                // Add click analytics
                const courseTitle = this.querySelector('h3')?.textContent || 'Unknown Course';
                console.log('Course clicked:', courseTitle);
                
                // Add visual feedback
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }
    
    // Keyboard shortcuts for navigation
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Don't interfere if user is typing in an input
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            
            switch(e.key) {
                case 's':
                case 'S':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        const searchInput = document.querySelector('.md-search__input');
                        if (searchInput) {
                            searchInput.focus();
                        }
                    }
                    break;
                case 'h':
                case 'H':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        window.location.href = '/';
                    }
                    break;
                case '?':
                    e.preventDefault();
                    showKeyboardShortcuts();
                    break;
            }
        });
    }
    
    function showKeyboardShortcuts() {
        const shortcuts = [
            'Ctrl/Cmd + S: Focus search',
            'Ctrl/Cmd + H: Go to home',
            '?: Show this help',
            '← →: Navigate between chapters',
            'Esc: Close this dialog'
        ];
        
        const modal = document.createElement('div');
        modal.className = 'keyboard-shortcuts-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Keyboard Shortcuts</h3>
                <ul>
                    ${shortcuts.map(shortcut => `<li>${shortcut}</li>`).join('')}
                </ul>
                <button onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                modal.remove();
            }
        });
        
        document.body.appendChild(modal);
    }
    
    // Track user progress and preferences
    function trackUserProgress() {
        // Track page visits
        const currentPath = window.location.pathname;
        let visitHistory = JSON.parse(localStorage.getItem('visit-history') || '[]');
        
        if (!visitHistory.includes(currentPath)) {
            visitHistory.push(currentPath);
            localStorage.setItem('visit-history', JSON.stringify(visitHistory));
        }
        
        // Track time spent on page
        const startTime = Date.now();
        
        window.addEventListener('beforeunload', function() {
            const timeSpent = Date.now() - startTime;
            const timeData = JSON.parse(localStorage.getItem('time-tracking') || '{}');
            timeData[currentPath] = (timeData[currentPath] || 0) + timeSpent;
            localStorage.setItem('time-tracking', JSON.stringify(timeData));
        });
        
        // Track scroll progress
        let maxScroll = 0;
        window.addEventListener('scroll', function() {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            maxScroll = Math.max(maxScroll, scrollPercent);
            
            // Save progress every 25% milestone
            if (maxScroll % 25 === 0 && maxScroll > 0) {
                const progressData = JSON.parse(localStorage.getItem('scroll-progress') || '{}');
                progressData[currentPath] = maxScroll;
                localStorage.setItem('scroll-progress', JSON.stringify(progressData));
            }
        });
    }
    
    // Add visual indicators for learning path progress
    function addLearningPathIndicators() {
        const pathItems = document.querySelectorAll('.tabbed-content ol li');
        const progress = JSON.parse(localStorage.getItem('agentic-ai-progress') || '{}');
        
        pathItems.forEach((item, index) => {
            const link = item.querySelector('a');
            if (!link) return;
            
            const href = link.getAttribute('href');
            if (progress[href]) {
                item.classList.add('completed-step');
                item.insertAdjacentHTML('beforeend', ' <span class="step-complete">✓</span>');
            } else if (index === 0 || document.querySelector(`.tabbed-content ol li:nth-child(${index}) .step-complete`)) {
                item.classList.add('current-step');
                item.insertAdjacentHTML('beforeend', ' <span class="step-current">▶</span>');
            }
        });
    }
    
    // Initialize learning path indicators
    addLearningPathIndicators();
});

// CSS for keyboard shortcuts modal and other enhancements
const additionalStyles = `
<style>
.keyboard-shortcuts-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 500px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.modal-content h3 {
    margin-top: 0;
    color: var(--uvu-green);
}

.modal-content ul {
    list-style: none;
    padding: 0;
}

.modal-content li {
    padding: 0.5rem 0;
    font-family: monospace;
    border-bottom: 1px solid #eee;
}

.modal-content button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: var(--uvu-green);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

.topic-filters {
    margin: 2rem 0;
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(39, 93, 56, 0.05), rgba(58, 125, 80, 0.1));
    border-radius: 12px;
    border: 1px solid rgba(39, 93, 56, 0.1);
}

.filter-buttons {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.filter-button {
    padding: 0.5rem 1rem;
    border: 2px solid var(--uvu-green);
    background: transparent;
    color: var(--uvu-green);
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.filter-button:hover {
    background: var(--uvu-green);
    color: white;
    transform: translateY(-1px);
}

.filter-button.active {
    background: var(--uvu-green);
    color: white;
    box-shadow: 0 2px 8px rgba(39, 93, 56, 0.3);
}

.completed-step {
    color: #28a745;
    font-weight: 600;
}

.current-step {
    color: var(--md-accent-fg-color);
    font-weight: 600;
}

.step-complete, .step-current {
    font-weight: bold;
    margin-left: 0.5rem;
}

.step-complete {
    color: #28a745;
}

.step-current {
    color: var(--md-accent-fg-color);
    animation: pulse 2s infinite;
}
</style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', additionalStyles);
