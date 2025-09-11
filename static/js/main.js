// Main JavaScript for Stock Sentiment Analyzer

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const mobileOverlay = document.getElementById('mobileOverlay');
    
    if (mobileMenuBtn && sidebar && mobileOverlay) {
        console.log('Mobile menu elements found:', { mobileMenuBtn, sidebar, mobileOverlay }); // Debug log
        
        mobileMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Mobile menu button clicked'); // Debug log
            
            sidebar.classList.toggle('open');
            mobileOverlay.classList.toggle('show');
            
            // Change icon
            const icon = this.querySelector('i');
            if (sidebar.classList.contains('open')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });
        
        // Close menu when clicking overlay
        mobileOverlay.addEventListener('click', function() {
            sidebar.classList.remove('open');
            mobileOverlay.classList.remove('show');
            
            // Reset icon
            const icon = mobileMenuBtn.querySelector('i');
            icon.className = 'fas fa-bars';
        });
        
        // Close menu when clicking on sidebar links
        document.querySelectorAll('.sidebar-link').forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                    mobileOverlay.classList.remove('show');
                    
                    // Reset icon
                    const icon = mobileMenuBtn.querySelector('i');
                    icon.className = 'fas fa-bars';
                }
            });
        });
        
        // Close menu on window resize if screen becomes larger
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                sidebar.classList.remove('open');
                mobileOverlay.classList.remove('show');
                
                // Reset icon
                const icon = mobileMenuBtn.querySelector('i');
                icon.className = 'fas fa-bars';
            }
        });
    } else {
        console.error('Mobile menu elements not found:', { 
            mobileMenuBtn: !!mobileMenuBtn, 
            sidebar: !!sidebar, 
            mobileOverlay: !!mobileOverlay 
        });
    }

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href && href.length > 1) { // Check if href is not just '#'
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add fade-in animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all cards for animation
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });

    // Add loading state to buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (this.form.checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...';
                this.disabled = true;
            }
        });
    });

    // Add keyboard navigation for autocomplete
    let currentAutocompleteIndex = -1;
    
    document.addEventListener('keydown', function(e) {
        const autocompleteItems = document.querySelectorAll('.autocomplete-item');
        
        if (autocompleteItems.length === 0) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentAutocompleteIndex = Math.min(currentAutocompleteIndex + 1, autocompleteItems.length - 1);
                updateAutocompleteSelection(autocompleteItems);
                break;
            case 'ArrowUp':
                e.preventDefault();
                currentAutocompleteIndex = Math.max(currentAutocompleteIndex - 1, -1);
                updateAutocompleteSelection(autocompleteItems);
                break;
            case 'Enter':
                e.preventDefault();
                if (currentAutocompleteIndex >= 0 && autocompleteItems[currentAutocompleteIndex]) {
                    autocompleteItems[currentAutocompleteIndex].click();
                }
                break;
            case 'Escape':
                document.getElementById('autocompleteDropdown').style.display = 'none';
                currentAutocompleteIndex = -1;
                break;
        }
    });

    function updateAutocompleteSelection(items) {
        items.forEach((item, index) => {
            if (index === currentAutocompleteIndex) {
                item.style.backgroundColor = '#e9ecef';
                item.style.fontWeight = 'bold';
            } else {
                item.style.backgroundColor = '';
                item.style.fontWeight = '';
            }
        });
    }

    // Add copy to clipboard functionality for results
    function addCopyToClipboard() {
        const copyButtons = document.querySelectorAll('.copy-result');
        copyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const textToCopy = this.dataset.copyText;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    // Show success feedback
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
                    this.classList.add('btn-success');
                    this.classList.remove('btn-outline-primary');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-primary');
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        });
    }

    // Add share functionality
    function addShareFunctionality() {
        if (navigator.share) {
            const shareButtons = document.querySelectorAll('.share-result');
            shareButtons.forEach(button => {
                button.addEventListener('click', async function() {
                    const shareData = {
                        title: 'Stock Sentiment Analysis',
                        text: this.dataset.shareText,
                        url: window.location.href
                    };
                    
                    try {
                        await navigator.share(shareData);
                    } catch (err) {
                        console.error('Error sharing: ', err);
                    }
                });
            });
        }
    }

    // Initialize additional functionality
    addCopyToClipboard();
    addShareFunctionality();

    // Add error handling for failed API calls
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        // You could show a user-friendly error message here
    });

    // Add performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }, 0);
        });
    }

    // Add accessibility improvements
    function improveAccessibility() {
        // Add ARIA labels to interactive elements
        const searchInput = document.getElementById('stockSearch');
        if (searchInput) {
            searchInput.setAttribute('aria-label', 'Search for stock symbol or company name');
            searchInput.setAttribute('aria-describedby', 'search-help');
        }

        // Add role attributes to custom components
        const autocompleteDropdown = document.getElementById('autocompleteDropdown');
        if (autocompleteDropdown) {
            autocompleteDropdown.setAttribute('role', 'listbox');
            autocompleteDropdown.setAttribute('aria-label', 'Stock search suggestions');
        }

        // Add keyboard support for custom buttons
        document.querySelectorAll('.autocomplete-item').forEach(item => {
            item.setAttribute('role', 'option');
            item.setAttribute('tabindex', '0');
        });
    }

    improveAccessibility();

    // Add theme detection and switching
    function detectTheme() {
        const savedTheme = localStorage.getItem('theme');
        
        if (savedTheme) {
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-theme');
                updateThemeIcon('dark');
            } else {
                document.body.classList.remove('dark-theme');
                updateThemeIcon('light');
            }
        } else {
            // Default to light mode
            document.body.classList.remove('dark-theme');
            updateThemeIcon('light');
            localStorage.setItem('theme', 'light');
        }
    }

    function updateThemeIcon(theme) {
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-moon';
            } else {
                themeIcon.className = 'fas fa-sun';
            }
        }
    }

    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const isDark = document.body.classList.contains('dark-theme');
            if (isDark) {
                document.body.classList.remove('dark-theme');
                localStorage.setItem('theme', 'light');
                updateThemeIcon('light');
            } else {
                document.body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark');
                updateThemeIcon('dark');
            }
        });
    }

    detectTheme();

    // Back to top functionality
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Back to top clicked'); // Debug log
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Also add scroll event to show/hide button
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
    }

    // Listen for theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        const savedTheme = localStorage.getItem('theme');
        if (!savedTheme) { // Only auto-switch if user hasn't manually set a preference
            if (e.matches) {
                document.body.classList.add('dark-theme');
                updateThemeIcon('dark');
            } else {
                document.body.classList.remove('dark-theme');
                updateThemeIcon('light');
            }
        }
    });
});

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatPercentage(num) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
    }).format(num);
}

function formatDate(timestamp) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(timestamp * 1000));
}

// Error handling utility
function handleError(error, userMessage = 'An unexpected error occurred') {
    console.error('Error:', error);
    
    // Show user-friendly error message
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        const errorText = document.getElementById('errorText');
        if (errorText) {
            errorText.textContent = userMessage;
        }
        errorDiv.classList.remove('d-none');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.classList.add('d-none');
        }, 5000);
    }
}

// Success message utility
function showSuccess(message) {
    // Create a temporary success alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alertDiv.style.top = '100px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// Debounce utility for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle utility for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
