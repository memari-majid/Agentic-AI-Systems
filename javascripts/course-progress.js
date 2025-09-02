// Course Progress Tracking for Agentic AI Systems
document.addEventListener('DOMContentLoaded', function() {
    
    // Course structure definition
    const courseStructure = {
        'AI_Systems': {
            name: 'AI Systems',
            chapters: 11,
            color: '#667eea',
            icon: '🧠'
        },
        'Agentic_AI_in_Action': {
            name: 'Agent Development', 
            chapters: 9,
            color: '#f093fb',
            icon: '⚡'
        },
        'Modern_AI_Frameworks': {
            name: 'Modern AI Frameworks',
            chapters: 8,
            color: '#43e97b',
            icon: '🚀'
        },
        'AI_Strategies': {
            name: 'AI Strategies',
            chapters: 17,
            color: '#4facfe',
            icon: '📈'
        }
    };

    // Initialize progress tracking
    function initProgressTracking() {
        // Load existing progress from localStorage
        let progress = JSON.parse(localStorage.getItem('agentic-ai-progress') || '{}');
        
        // Update progress for current page
        updateCurrentPageProgress();
        
        // Display progress indicators
        displayProgressIndicators(progress);
        
        // Add chapter completion buttons
        addCompletionButtons();
    }

    // Update progress for current page
    function updateCurrentPageProgress() {
        const currentPath = window.location.pathname;
        const pathParts = currentPath.split('/');
        
        // Extract track and chapter from URL
        let track = null;
        let chapter = null;
        
        if (pathParts.includes('AI_Systems')) {
            track = 'AI_Systems';
            const fileName = pathParts[pathParts.length - 1];
            if (fileName.match(/\d+\.html?/)) {
                chapter = parseInt(fileName.match(/\d+/)[0]);
            }
        } else if (pathParts.includes('Agentic_AI_in_Action')) {
            track = 'Agentic_AI_in_Action';
            const fileName = pathParts[pathParts.length - 1];
            if (fileName.match(/\d+\.html?/)) {
                chapter = parseInt(fileName.match(/\d+/)[0]);
            }
        } else if (pathParts.includes('Modern_AI_Frameworks')) {
            track = 'Modern_AI_Frameworks';
            // Modern frameworks don't have numbered chapters
        } else if (pathParts.includes('AI_Strategies')) {
            track = 'AI_Strategies';
            const fileName = pathParts[pathParts.length - 1];
            if (fileName.match(/\d+\.html?/)) {
                chapter = parseInt(fileName.match(/\d+/)[0]);
            }
        }

        if (track && chapter) {
            markChapterAsViewed(track, chapter);
        }
    }

    // Mark chapter as viewed
    function markChapterAsViewed(track, chapter) {
        let progress = JSON.parse(localStorage.getItem('agentic-ai-progress') || '{}');
        if (!progress[track]) progress[track] = {};
        if (!progress[track].viewed) progress[track].viewed = [];
        
        if (!progress[track].viewed.includes(chapter)) {
            progress[track].viewed.push(chapter);
            localStorage.setItem('agentic-ai-progress', JSON.stringify(progress));
        }
    }

    // Mark chapter as completed
    function markChapterAsCompleted(track, chapter) {
        let progress = JSON.parse(localStorage.getItem('agentic-ai-progress') || '{}');
        if (!progress[track]) progress[track] = {};
        if (!progress[track].completed) progress[track].completed = [];
        
        if (!progress[track].completed.includes(chapter)) {
            progress[track].completed.push(chapter);
            localStorage.setItem('agentic-ai-progress', JSON.stringify(progress));
            
            // Update UI immediately
            displayProgressIndicators(progress);
            
            // Show completion message
            showCompletionMessage(track, chapter);
        }
    }

    // Display progress indicators
    function displayProgressIndicators(progress) {
        // Add progress to main page if we're on index
        if (window.location.pathname.includes('index.html') || 
            window.location.pathname.endsWith('/')) {
            addMainPageProgress(progress);
        }
        
        // Add track progress if we're in a track
        addTrackProgress(progress);
    }

    // Add progress indicators to main page
    function addMainPageProgress(progress) {
        const trackCards = document.querySelectorAll('[href*="AI_Systems"], [href*="Agentic_AI_in_Action"], [href*="Modern_AI_Frameworks"], [href*="AI_Strategies"]');
        
        trackCards.forEach(card => {
            const href = card.getAttribute('href');
            let track = null;
            
            if (href.includes('AI_Systems')) track = 'AI_Systems';
            else if (href.includes('Agentic_AI_in_Action')) track = 'Agentic_AI_in_Action';
            else if (href.includes('Modern_AI_Frameworks')) track = 'Modern_AI_Frameworks';
            else if (href.includes('AI_Strategies')) track = 'AI_Strategies';
            
            if (track && courseStructure[track]) {
                const trackData = courseStructure[track];
                const completedCount = progress[track] ? (progress[track].completed || []).length : 0;
                const totalCount = trackData.chapters;
                const percentage = Math.round((completedCount / totalCount) * 100);
                
                // Add progress indicator to card
                const progressHTML = `
                    <div style="margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-size: 0.8rem; opacity: 0.8;">Progress</span>
                            <span style="font-size: 0.8rem; font-weight: bold;">${completedCount}/${totalCount}</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: rgba(255,255,255,0.8); height: 100%; width: ${percentage}%; transition: width 0.3s ease;"></div>
                        </div>
                    </div>
                `;
                
                // Find the parent container and add progress
                const cardParent = card.closest('div[style*="border"]');
                if (cardParent && !cardParent.querySelector('.progress-indicator')) {
                    const progressDiv = document.createElement('div');
                    progressDiv.className = 'progress-indicator';
                    progressDiv.innerHTML = progressHTML;
                    cardParent.appendChild(progressDiv);
                }
            }
        });
    }

    // Add track-specific progress
    function addTrackProgress(progress) {
        const currentPath = window.location.pathname;
        let currentTrack = null;
        
        if (currentPath.includes('AI_Systems')) currentTrack = 'AI_Systems';
        else if (currentPath.includes('Agentic_AI_in_Action')) currentTrack = 'Agentic_AI_in_Action';
        else if (currentPath.includes('Modern_AI_Frameworks')) currentTrack = 'Modern_AI_Frameworks';
        else if (currentPath.includes('AI_Strategies')) currentTrack = 'AI_Strategies';
        
        if (currentTrack && courseStructure[currentTrack]) {
            const trackData = courseStructure[currentTrack];
            const completedCount = progress[currentTrack] ? (progress[currentTrack].completed || []).length : 0;
            const totalCount = trackData.chapters;
            
            // Add floating progress indicator
            addFloatingProgress(trackData, completedCount, totalCount);
        }
    }

    // Add floating progress indicator
    function addFloatingProgress(trackData, completed, total) {
        const existingIndicator = document.getElementById('floating-progress');
        if (existingIndicator) return; // Already exists
        
        const percentage = Math.round((completed / total) * 100);
        
        const progressHTML = `
            <div id="floating-progress" style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                padding: 12px 16px;
                border-radius: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1000;
                font-size: 0.9rem;
                border-left: 4px solid ${trackData.color};
                min-width: 200px;
            ">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span>${trackData.icon}</span>
                    <strong style="color: ${trackData.color};">${trackData.name}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 0.8rem; color: #666;">Progress</span>
                    <span style="font-size: 0.8rem; font-weight: bold; color: ${trackData.color};">${completed}/${total} (${percentage}%)</span>
                </div>
                <div style="background: #f0f0f0; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="background: ${trackData.color}; height: 100%; width: ${percentage}%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', progressHTML);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const indicator = document.getElementById('floating-progress');
            if (indicator) {
                indicator.style.opacity = '0.7';
                indicator.style.transform = 'translateX(10px)';
            }
        }, 5000);
    }

    // Add completion buttons to chapters
    function addCompletionButtons() {
        const currentPath = window.location.pathname;
        let track = null;
        let chapter = null;
        
        // Extract track and chapter
        if (currentPath.includes('AI_Systems')) {
            track = 'AI_Systems';
            const fileName = currentPath.split('/').pop();
            if (fileName.match(/\d+\.html?/)) {
                chapter = parseInt(fileName.match(/\d+/)[0]);
            }
        } else if (currentPath.includes('Agentic_AI_in_Action')) {
            track = 'Agentic_AI_in_Action';
            const fileName = currentPath.split('/').pop();
            if (fileName.match(/\d+\.html?/)) {
                chapter = parseInt(fileName.match(/\d+/)[0]);
            }
        } else if (currentPath.includes('AI_Strategies')) {
            track = 'AI_Strategies';
            const fileName = currentPath.split('/').pop();
            if (fileName.match(/\d+\.html?/)) {
                chapter = parseInt(fileName.match(/\d+/)[0]);
            }
        }
        
        if (track && chapter) {
            addChapterCompletionButton(track, chapter);
        }
    }

    // Add chapter completion button
    function addChapterCompletionButton(track, chapter) {
        let progress = JSON.parse(localStorage.getItem('agentic-ai-progress') || '{}');
        const isCompleted = progress[track] && progress[track].completed && 
                          progress[track].completed.includes(chapter);
        
        const buttonHTML = `
            <div id="chapter-completion" style="
                margin: 2rem 0;
                padding: 1.5rem;
                background: linear-gradient(135deg, ${courseStructure[track].color}20, ${courseStructure[track].color}10);
                border-radius: 12px;
                text-align: center;
                border: 2px solid ${courseStructure[track].color}30;
            ">
                <h3 style="margin: 0 0 1rem 0; color: ${courseStructure[track].color};">
                    ${courseStructure[track].icon} Chapter ${chapter} ${isCompleted ? 'Completed!' : 'Progress'}
                </h3>
                <button id="complete-chapter" onclick="completeChapter('${track}', ${chapter})" style="
                    padding: 12px 24px;
                    background: ${isCompleted ? '#28a745' : courseStructure[track].color};
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 1rem;
                    transition: all 0.3s ease;
                " ${isCompleted ? 'disabled' : ''}>
                    ${isCompleted ? '✅ Completed' : '✅ Mark as Complete'}
                </button>
            </div>
        `;
        
        // Add to end of main content
        const mainContent = document.querySelector('main') || document.querySelector('.md-content');
        if (mainContent && !document.getElementById('chapter-completion')) {
            mainContent.insertAdjacentHTML('beforeend', buttonHTML);
        }
    }

    // Show completion message
    function showCompletionMessage(track, chapter) {
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            z-index: 1001;
            text-align: center;
            border-left: 4px solid ${courseStructure[track].color};
        `;
        
        message.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
            <h3 style="margin: 0 0 1rem 0; color: ${courseStructure[track].color};">Chapter Completed!</h3>
            <p style="margin: 0; color: #666;">Great progress on your AI agent learning journey!</p>
            <button onclick="this.parentElement.remove()" style="
                margin-top: 1rem;
                padding: 8px 16px;
                background: ${courseStructure[track].color};
                color: white;
                border: none;
                border-radius: 16px;
                cursor: pointer;
            ">Continue Learning</button>
        `;
        
        document.body.appendChild(message);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (message.parentElement) {
                message.remove();
            }
        }, 3000);
    }

    // Global function for chapter completion
    window.completeChapter = function(track, chapter) {
        markChapterAsCompleted(track, chapter);
        
        // Update button
        const button = document.getElementById('complete-chapter');
        if (button) {
            button.textContent = '✅ Completed';
            button.style.background = '#28a745';
            button.disabled = true;
        }
    };

    // Initialize everything
    initProgressTracking();
});