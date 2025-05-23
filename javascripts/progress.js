// Reading Progress and Section Tracking
document.addEventListener('DOMContentLoaded', function() {
    // Create progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    document.body.appendChild(progressBar);

    // Update progress on scroll
    function updateProgress() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    }

    // Highlight sections in view
    function highlightSections() {
        const sections = document.querySelectorAll('h2, h3');
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight + 200) {
                section.classList.add('in-view');
            } else {
                section.classList.remove('in-view');
            }
        });
    }

    // Track reading time and chapter completion
    function trackReadingProgress() {
        const readingTimeElement = document.querySelector('[data-reading-time]');
        if (!readingTimeElement) return;

        const estimatedTime = parseInt(readingTimeElement.dataset.readingTime) || 10;
        const startTime = Date.now();
        
        // Store reading session
        const chapterPath = window.location.pathname;
        const sessions = JSON.parse(localStorage.getItem('reading-sessions') || '{}');
        
        window.addEventListener('beforeunload', () => {
            const timeSpent = (Date.now() - startTime) / 1000 / 60; // minutes
            sessions[chapterPath] = (sessions[chapterPath] || 0) + timeSpent;
            localStorage.setItem('reading-sessions', JSON.stringify(sessions));
            
            // Mark as completed if read for estimated time
            if (timeSpent >= estimatedTime * 0.8) {
                const completed = JSON.parse(localStorage.getItem('completed-chapters') || '[]');
                if (!completed.includes(chapterPath)) {
                    completed.push(chapterPath);
                    localStorage.setItem('completed-chapters', JSON.stringify(completed));
                }
            }
        });
    }

    // Add completion indicators to navigation
    function updateNavigationProgress() {
        const completed = JSON.parse(localStorage.getItem('completed-chapters') || '[]');
        const navLinks = document.querySelectorAll('.md-nav__link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && completed.includes(href)) {
                link.parentElement.classList.add('md-nav__item--completed');
            }
        });
    }

    // Smooth scroll for anchor links
    function setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Enhance reading time display
    function enhanceReadingTime() {
        const readingTimeText = document.querySelector('strong:contains("Estimated reading time")');
        if (readingTimeText) {
            const timeMatch = readingTimeText.textContent.match(/(\d+)\s*minutes?/);
            if (timeMatch) {
                const minutes = parseInt(timeMatch[1]);
                readingTimeText.className = 'reading-time';
                readingTimeText.dataset.readingTime = minutes;
                
                // Add progress indicator
                const progressContainer = document.createElement('div');
                progressContainer.className = 'chapter-meta';
                progressContainer.innerHTML = `
                    <span>Progress:</span>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                    <span class="progress-text">0%</span>
                `;
                readingTimeText.parentNode.insertBefore(progressContainer, readingTimeText.nextSibling);
            }
        }
    }

    // Update chapter progress based on scroll
    function updateChapterProgress() {
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        if (progressFill && progressText) {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = Math.round((winScroll / height) * 100);
            
            progressFill.style.width = scrolled + '%';
            progressText.textContent = scrolled + '%';
        }
    }

    // Initialize all features
    window.addEventListener('scroll', function() {
        updateProgress();
        highlightSections();
        updateChapterProgress();
    });

    // Initialize on load
    updateNavigationProgress();
    setupSmoothScroll();
    enhanceReadingTime();
    trackReadingProgress();
    setupChapterNavigation();
    setupQuickNavigation();
    setupBreadcrumb();
    setupKeyboardNavigation();
    
    // Initial calls
    updateProgress();
    highlightSections();

    // Chapter Navigation System
    function setupChapterNavigation() {
        const chapterOrder = [
            // AI Systems
            'AI_Systems/1.md', 'AI_Systems/2.md', 'AI_Systems/3.md', 'AI_Systems/4.md', 'AI_Systems/5.md',
            'AI_Systems/6.md', 'AI_Systems/7.md', 'AI_Systems/8.md', 'AI_Systems/9.md', 'AI_Systems/10.md', 'AI_Systems/11.md',
            // Agent Development
            'Agentic_AI_in_Action/1.md', 'Agentic_AI_in_Action/2.md', 'Agentic_AI_in_Action/3.md', 'Agentic_AI_in_Action/4.md',
            'Agentic_AI_in_Action/5.md', 'Agentic_AI_in_Action/6.md', 'Agentic_AI_in_Action/7.md', 'Agentic_AI_in_Action/8.md', 'Agentic_AI_in_Action/9.md',
            // AI Strategies  
            'AI_Strategies/1.md', 'AI_Strategies/2.md', 'AI_Strategies/3.md', 'AI_Strategies/4.md', 'AI_Strategies/5.md', 'AI_Strategies/6.md',
            'AI_Strategies/7.md', 'AI_Strategies/8.md', 'AI_Strategies/9.md', 'AI_Strategies/10.md', 'AI_Strategies/11.md', 'AI_Strategies/12.md',
            'AI_Strategies/13.md', 'AI_Strategies/14.md', 'AI_Strategies/15.md', 'AI_Strategies/16.md', 'AI_Strategies/17.md'
        ];

        const currentPath = window.location.pathname.replace(/^\//, '').replace(/\/$/, '');
        const currentIndex = chapterOrder.findIndex(chapter => currentPath.includes(chapter.replace('.md', '')));
        
        if (currentIndex === -1) return;

        // Create navigation container
        const navContainer = document.createElement('div');
        navContainer.className = 'chapter-navigation';
        
        // Previous button
        const prevButton = document.createElement('a');
        prevButton.className = 'nav-button nav-button--prev';
        if (currentIndex > 0) {
            prevButton.href = chapterOrder[currentIndex - 1].replace('.md', '/');
            prevButton.innerHTML = 'Previous Chapter';
        } else {
            prevButton.className += ' disabled';
            prevButton.innerHTML = 'Previous Chapter';
        }
        
        // Chapter overview
        const overview = document.createElement('div');
        overview.className = 'chapter-overview';
        overview.innerHTML = `
            <div class="chapter-title">Chapter ${currentIndex + 1} of ${chapterOrder.length}</div>
            <div class="chapter-progress-mini">
                ${chapterOrder.map((_, idx) => 
                    `<div class="progress-dot ${idx < currentIndex ? 'completed' : ''} ${idx === currentIndex ? 'current' : ''}"></div>`
                ).join('')}
            </div>
        `;
        
        // Next button
        const nextButton = document.createElement('a');
        nextButton.className = 'nav-button nav-button--next';
        if (currentIndex < chapterOrder.length - 1) {
            nextButton.href = chapterOrder[currentIndex + 1].replace('.md', '/');
            nextButton.innerHTML = 'Next Chapter';
        } else {
            nextButton.className += ' disabled';
            nextButton.innerHTML = 'Next Chapter';
        }
        
        navContainer.appendChild(prevButton);
        navContainer.appendChild(overview);
        navContainer.appendChild(nextButton);
        
        // Insert at the end of content
        const content = document.querySelector('.md-content__inner');
        if (content) {
            content.appendChild(navContainer);
        }
    }

    // Quick navigation dots
    function setupQuickNavigation() {
        const headings = document.querySelectorAll('h2, h3');
        if (headings.length < 2) return;

        const quickNav = document.createElement('div');
        quickNav.className = 'quick-nav';
        
        headings.forEach((heading, index) => {
            const button = document.createElement('button');
            button.className = 'quick-nav-button';
            button.title = heading.textContent;
            button.addEventListener('click', () => {
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
            quickNav.appendChild(button);
        });
        
        document.body.appendChild(quickNav);
        
        // Update active state based on scroll
        function updateQuickNav() {
            const scrollPos = window.scrollY + 100;
            let activeIndex = 0;
            
            headings.forEach((heading, index) => {
                if (scrollPos >= heading.offsetTop) {
                    activeIndex = index;
                }
            });
            
            quickNav.querySelectorAll('.quick-nav-button').forEach((button, index) => {
                button.classList.toggle('active', index === activeIndex);
            });
        }
        
        window.addEventListener('scroll', updateQuickNav);
        updateQuickNav();
    }

    // Breadcrumb navigation
    function setupBreadcrumb() {
        const pathParts = window.location.pathname.split('/').filter(part => part);
        if (pathParts.length < 2) return;
        
        const breadcrumb = document.createElement('div');
        breadcrumb.className = 'chapter-breadcrumb';
        
        const sectionMap = {
            'AI_Systems': 'AI Systems',
            'Agentic_AI_in_Action': 'Agent Development', 
            'AI_Strategies': 'AI Strategies'
        };
        
        let breadcrumbHTML = '<a href="/" class="breadcrumb-link">Home</a>';
        
        if (pathParts[0] && sectionMap[pathParts[0]]) {
            breadcrumbHTML += ' <span class="breadcrumb-separator">▶</span> ';
            breadcrumbHTML += `<span class="breadcrumb-current">${sectionMap[pathParts[0]]}</span>`;
        }
        
        breadcrumb.innerHTML = breadcrumbHTML;
        
        const content = document.querySelector('.md-content__inner');
        if (content && content.firstChild) {
            content.insertBefore(breadcrumb, content.firstChild);
        }
    }

    // Keyboard navigation
    function setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Don't interfere if user is typing
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            
            const prevButton = document.querySelector('.nav-button--prev:not(.disabled)');
            const nextButton = document.querySelector('.nav-button--next:not(.disabled)');
            
            if (e.key === 'ArrowLeft' && prevButton) {
                window.location.href = prevButton.href;
            } else if (e.key === 'ArrowRight' && nextButton) {
                window.location.href = nextButton.href;
            }
        });
    }
});

// Helper function for contains selector (since it's not standard)
document.querySelectorAll = (function(querySelectorAll) {
    return function(selector) {
        if (selector.includes(':contains(')) {
            const match = selector.match(/:contains\("([^"]+)"\)/);
            if (match) {
                const text = match[1];
                const elements = document.getElementsByTagName('*');
                const results = [];
                for (let el of elements) {
                    if (el.textContent && el.textContent.includes(text)) {
                        results.push(el);
                    }
                }
                return results;
            }
        }
        return querySelectorAll.call(this, selector);
    };
})(document.querySelectorAll); 