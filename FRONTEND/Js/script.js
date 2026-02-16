// Common Functions
// Use dynamic API URL to support local network testing (e.g. from a phone)
const API_BASE_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000/api'
    : `http://${window.location.hostname}:8000/api`;

document.addEventListener('DOMContentLoaded', function () {
    // Initialize mobile navigation
    initMobileNavigation();

    // Initialize active navigation link
    setActiveNavLink();

    // Initialize modals
    initModals();

    // Initialize form validation if forms exist on page
    if (document.getElementById('donationForm')) {
        initDonationForm();
    }

    if (document.getElementById('volunteerForm')) {
        initVolunteerForm();
    }

    if (document.getElementById('contactForm')) {
        initContactForm();
    }

    if (document.getElementById('newsletterForm')) {
        initNewsletterForm();
    }

    // Initialize carousel if it exists on page
    if (document.getElementById('carousel')) {
        initCarousel();
    }

    // Initialize gallery if it exists on page
    if (document.getElementById('gallery')) {
        initGallery();
    }

    // Initialize animated counters if they exist on page
    if (document.querySelector('.stat-number')) {
        initCounters();
    }

    // Initialize support buttons if they exist on page
    if (document.querySelector('.support-btn')) {
        initSupportButtons();
    }
});

// Mobile Navigation
function initMobileNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');
    const closeSidebar = document.getElementById('closeSidebar');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            if (navOverlay) navOverlay.classList.toggle('active');
        });

        // Close mobile menu when clicking on close button
        if (closeSidebar) {
            closeSidebar.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                if (navOverlay) navOverlay.classList.remove('active');
            });
        }

        // Close mobile menu when clicking on overlay
        if (navOverlay) {
            navOverlay.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                navOverlay.classList.remove('active');
            });
        }

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                if (navOverlay) navOverlay.classList.remove('active');
            });
        });
    }
}

// Set Active Navigation Link
function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage ||
            (currentPage === '' && href === 'index.html') ||
            (currentPage === 'index.html' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Modals
function initModals() {
    // Close modals when clicking X
    document.querySelectorAll('.close-modal, .close-confirmation').forEach(btn => {
        btn.addEventListener('click', function () {
            this.closest('.modal').style.display = 'none';
        });
    });

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
}

// Support Buttons
function initSupportButtons() {
    const supportBtns = document.querySelectorAll('.support-btn');
    const supportModal = document.getElementById('supportModal');

    if (supportBtns.length && supportModal) {
        supportBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const program = btn.getAttribute('data-program');
                document.getElementById('programName').textContent =
                    program.charAt(0).toUpperCase() + program.slice(1);
                supportModal.style.display = 'flex';
            });
        });
    }
}

// Carousel
function initCarousel() {
    const carouselTrack = document.querySelector('.carousel-track');
    const carouselSlides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const indicators = document.querySelectorAll('.indicator');

    if (!carouselTrack || !carouselSlides.length) return;

    let currentSlide = 0;
    let slideInterval;

    function moveToSlide(index) {
        if (index < 0) index = carouselSlides.length - 1;
        if (index >= carouselSlides.length) index = 0;

        currentSlide = index;
        carouselTrack.style.transform = `translateX(-${currentSlide * 100}%)`;

        // Update indicators
        indicators.forEach(indicator => indicator.classList.remove('active'));
        if (indicators[currentSlide]) {
            indicators[currentSlide].classList.add('active');
        }
    }

    function moveToPrevSlide() {
        moveToSlide(currentSlide - 1);
        startCarousel();
    }

    function moveToNextSlide() {
        moveToSlide(currentSlide + 1);
        startCarousel();
    }

    function startCarousel() {
        if (slideInterval) {
            clearInterval(slideInterval);
        }

        slideInterval = setInterval(() => {
            moveToNextSlide();
        }, 5000);
    }

    // Event listeners
    if (prevBtn) prevBtn.addEventListener('click', moveToPrevSlide);
    if (nextBtn) nextBtn.addEventListener('click', moveToNextSlide);

    indicators.forEach(indicator => {
        indicator.addEventListener('click', () => {
            const slideIndex = parseInt(indicator.getAttribute('data-slide'));
            moveToSlide(slideIndex);
            startCarousel();
        });
    });

    // Start carousel
    startCarousel();
}

// Gallery
function initGallery() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const viewBtns = document.querySelectorAll('.view-btn');
    const lightbox = document.getElementById('lightbox');

    if (!filterBtns.length || !galleryItems.length) return;

    // Filter functionality
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active filter button
            filterBtns.forEach(button => button.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            // Filter gallery items
            galleryItems.forEach(item => {
                const category = item.getAttribute('data-category');

                if (filter === 'all' || filter === category) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 10);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
        });
    });

    // Lightbox functionality
    const galleryImages = Array.from(galleryItems).map((item, index) => {
        const img = item.querySelector('img');
        const title = item.querySelector('h3')?.textContent || '';
        const description = item.querySelector('p')?.textContent || '';

        return {
            src: img.src,
            title: title,
            description: description,
            index: index
        };
    });

    let currentImageIndex = 0;

    function openLightbox(index) {
        currentImageIndex = index;
        const image = galleryImages[currentImageIndex];

        if (lightbox && image) {
            document.getElementById('lightbox-img').src = image.src;
            document.getElementById('lightbox-caption').textContent = `${image.title} - ${image.description}`;
            lightbox.style.display = 'flex';
        }
    }

    function closeLightbox() {
        if (lightbox) {
            lightbox.style.display = 'none';
        }
    }

    function prevImage() {
        currentImageIndex--;
        if (currentImageIndex < 0) {
            currentImageIndex = galleryImages.length - 1;
        }
        openLightbox(currentImageIndex);
    }

    function nextImage() {
        currentImageIndex++;
        if (currentImageIndex >= galleryImages.length) {
            currentImageIndex = 0;
        }
        openLightbox(currentImageIndex);
    }

    // Event listeners for view buttons
    viewBtns.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            openLightbox(index);
        });
    });

    // Lightbox controls
    document.querySelector('.close-lightbox')?.addEventListener('click', closeLightbox);
    document.querySelector('.prev-lightbox')?.addEventListener('click', prevImage);
    document.querySelector('.next-lightbox')?.addEventListener('click', nextImage);

    // Keyboard navigation for lightbox
    document.addEventListener('keydown', (e) => {
        if (lightbox && lightbox.style.display === 'flex') {
            if (e.key === 'Escape') {
                closeLightbox();
            } else if (e.key === 'ArrowLeft') {
                prevImage();
            } else if (e.key === 'ArrowRight') {
                nextImage();
            }
        }
    });
}

// Animated Counters
function initCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const suffix = element.textContent.includes('%') ? '%' : '';
        const duration = 2000;
        const increment = target / (duration / 16);

        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + suffix;
        }, 16);
    }

    // Start animation when element comes into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                statNumbers.forEach(number => {
                    animateCounter(number);
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        observer.observe(statsSection);
    }
}

// Donation Form
function initDonationForm() {
    const donationForm = document.getElementById('donationForm');
    const amountOptions = document.querySelectorAll('.amount-option');
    const customAmountInput = document.getElementById('customAmount');
    const donationAmountInput = document.getElementById('donationAmount');

    if (!donationForm) return;

    // Handle amount selection
    amountOptions.forEach(option => {
        option.addEventListener('click', () => {
            // Remove active class from all options
            amountOptions.forEach(opt => opt.classList.remove('active'));
            // Add active class to clicked option
            option.classList.add('active');

            // Update hidden input
            const amount = option.getAttribute('data-amount');
            donationAmountInput.value = amount;
            customAmountInput.value = '';
        });
    });

    // Handle custom amount
    if (customAmountInput) {
        customAmountInput.addEventListener('input', () => {
            amountOptions.forEach(opt => opt.classList.remove('active'));
            donationAmountInput.value = customAmountInput.value;
        });
    }

    donationForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Basic Validation
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const amount = donationAmountInput.value;

        let isValid = true;

        if (!fullName.trim()) {
            showError('nameError', 'Please enter your full name');
            isValid = false;
        } else {
            hideError('nameError');
        }

        if (!email.trim() || !validateEmail(email)) {
            showError('emailError', 'Please enter a valid email address');
            isValid = false;
        } else {
            hideError('emailError');
        }

        if (isValid) {
            showLoading();

            const formData = {
                donor_name: fullName,
                donor_email: email,
                donor_phone: document.getElementById('phone')?.value || '',
                amount: parseFloat(amount),
                payment_method: document.querySelector('input[name="paymentMethod"]:checked')?.value || 'credit_card',
                donation_type: document.getElementById('donationType')?.value || 'one_time',
                is_anonymous: false
            };


            fetch(`${API_BASE_URL}/donations/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
                .then(async response => {
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(JSON.stringify(errorData));
                    }
                    return response.json();
                })
                .then(data => {
                    hideLoading();
                    document.getElementById('confirmationMessage').textContent =
                        'Thank you for your donation! Your support makes a difference.';
                    const modal = document.getElementById('confirmationModal');
                    modal.style.display = 'flex';

                    // Redirect after 3 seconds
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 3000);

                    // Also handle OK button click
                    const closeBtn = modal.querySelector('.close-confirmation');
                    if (closeBtn) {
                        closeBtn.onclick = function () {
                            window.location.href = 'index.html';
                        }
                    }

                    donationForm.reset();
                })
                .catch(error => {
                    hideLoading();
                    console.error('Error:', error);

                    // Try to parse and display specific error messages
                    try {
                        const errorObj = JSON.parse(error.message);
                        let errorMessage = 'Failed to process donation:\n';
                        for (const [field, messages] of Object.entries(errorObj)) {
                            if (Array.isArray(messages)) {
                                errorMessage += `${field}: ${messages.join(', ')}\n`;
                            } else {
                                errorMessage += `${field}: ${messages}\n`;
                            }
                        }
                        alert(errorMessage);
                    } catch (e) {
                        alert('Failed to process donation. Please try again.');
                    }
                });
        }
    });
}
// Volunteer Form
function initVolunteerForm() {
    const volunteerForm = document.getElementById('volunteerForm');

    if (!volunteerForm) return;

    // Set minimum date for start date
    const startDateInput = document.getElementById('volunteerStartDate');
    if (startDateInput) {
        const today = new Date().toISOString().split('T')[0];
        startDateInput.setAttribute('min', today);
    }

    volunteerForm.addEventListener('submit', function (e) {
        e.preventDefault();

        let isValid = true;

        // Simple validation
        const name = document.getElementById('volunteerName').value;
        const email = document.getElementById('volunteerEmail').value;
        const age = document.getElementById('volunteerAge').value;

        if (!name.trim()) {
            showError('volunteerNameError', 'Please enter your full name');
            isValid = false;
        } else {
            hideError('volunteerNameError');
        }

        if (!email.trim() || !validateEmail(email)) {
            showError('volunteerEmailError', 'Please enter a valid email address');
            isValid = false;
        } else {
            hideError('volunteerEmailError');
        }

        if (!age || age < 18) {
            showError('volunteerAgeError', 'You must be at least 18 years old');
            isValid = false;
        } else {
            hideError('volunteerAgeError');
        }

        if (isValid) {
            showLoading();

            // Collect interests (checkboxes)
            const interests = [];
            document.querySelectorAll('input[name="volunteerInterests"]:checked').forEach(checkbox => {
                interests.push(checkbox.value);
            });

            // Collect availability (checkboxes)
            const availability = [];
            document.querySelectorAll('input[name="volunteerAvailability"]:checked').forEach(checkbox => {
                availability.push(checkbox.value);
            });

            const formData = {
                name: name,
                email: email,
                age: parseInt(age),
                phone: document.getElementById('volunteerPhone')?.value || '',
                occupation: document.getElementById('volunteerOccupation')?.value || '',
                skills: document.getElementById('volunteerSkills')?.value || '',
                interests: interests,
                availability: availability,
                commitment_level: document.getElementById('volunteerCommitment')?.value || '',
                motivation: document.getElementById('volunteerMotivation')?.value || '',
                start_date: document.getElementById('volunteerStartDate')?.value || null,
            };

            fetch(`${API_BASE_URL}/volunteers/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
                .then(async response => {
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(JSON.stringify(errorData));
                    }
                    return response.json();
                })
                .then(data => {
                    hideLoading();
                    document.getElementById('confirmationMessage').textContent =
                        'Thank you for your volunteer application! We will contact you soon.';
                    document.getElementById('confirmationModal').style.display = 'flex';

                    // Redirect after 3 seconds
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 3000);

                    // Also handle OK button click
                    const modal = document.getElementById('confirmationModal');
                    const closeBtn = modal.querySelector('.close-confirmation');
                    if (closeBtn) {
                        closeBtn.onclick = function () {
                            window.location.href = 'index.html';
                        }
                    }

                    volunteerForm.reset();
                })
                .catch(error => {
                    hideLoading();
                    console.error('Error:', error);

                    // Try to parse and display specific error messages
                    try {
                        const errorMsg = error.message;
                        if (errorMsg.includes('Failed to fetch') || errorMsg.includes('NetworkError')) {
                            alert('Network error: Cannot reach the backend server. If you are on a mobile device, ensure it can access ' + API_BASE_URL);
                        } else {
                            const errorObj = JSON.parse(errorMsg);
                            let errorMessage = 'Failed to submit application:\n';
                            for (const [field, messages] of Object.entries(errorObj)) {
                                if (Array.isArray(messages)) {
                                    errorMessage += `${field}: ${messages.join(', ')}\n`;
                                } else {
                                    errorMessage += `${field}: ${messages}\n`;
                                }
                            }
                            alert(errorMessage);
                        }
                    } catch (e) {
                        alert('Failed to submit application. Please check your network connection and try again.');
                    }
                });
        }
    });
}

// Contact Form
function initContactForm() {
    const contactForm = document.getElementById('contactForm');

    if (!contactForm) return;

    contactForm.addEventListener('submit', function (e) {
        e.preventDefault();

        let isValid = true;

        // Simple validation
        const name = document.getElementById('contactName').value;
        const email = document.getElementById('contactEmail').value;
        const message = document.getElementById('contactMessage').value;

        if (!name.trim()) {
            showError('contactNameError', 'Please enter your name');
            isValid = false;
        } else {
            hideError('contactNameError');
        }

        if (!email.trim() || !validateEmail(email)) {
            showError('contactEmailError', 'Please enter a valid email address');
            isValid = false;
        } else {
            hideError('contactEmailError');
        }

        if (!message.trim()) {
            showError('contactMessageError', 'Please enter your message');
            isValid = false;
        } else {
            hideError('contactMessageError');
        }

        if (isValid) {
            showLoading();

            const formData = {
                name: name,
                email: email,
                subject: document.getElementById('contactSubject')?.value || 'General Inquiry',
                message: message,
                phone: document.getElementById('contactPhone')?.value || ''
            };

            fetch(`${API_BASE_URL}/contact/messages/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
                .then(async response => {
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(JSON.stringify(errorData));
                    }
                    return response.json();
                })
                .then(data => {
                    hideLoading();
                    document.getElementById('confirmationMessage').textContent =
                        'Thank you for your message! We will respond soon.';
                    document.getElementById('confirmationModal').style.display = 'flex';

                    // Redirect after 3 seconds
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 3000);

                    // Also handle OK button click
                    const modal = document.getElementById('confirmationModal');
                    const closeBtn = modal.querySelector('.close-confirmation');
                    if (closeBtn) {
                        closeBtn.onclick = function () {
                            window.location.href = 'index.html';
                        }
                    }

                    contactForm.reset();
                })
                .catch(error => {
                    hideLoading();
                    console.error('Error:', error);
                    alert('Failed to send message. Please try again later.');
                });
        }
    });
}

// Newsletter Form
function initNewsletterForm() {
    const newsletterForm = document.getElementById('newsletterForm');

    if (!newsletterForm) return;

    newsletterForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const emailInput = newsletterForm.querySelector('input[type="email"]');
        const email = emailInput.value;

        if (email && validateEmail(email)) {
            showLoading();

            fetch(`${API_BASE_URL}/contact/newsletter/subscribe/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email })
            })
                .then(async response => {
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(JSON.stringify(errorData));
                    }
                    return response.json();
                })
                .then(data => {
                    hideLoading();
                    document.getElementById('confirmationMessage').textContent =
                        'Thank you for subscribing to our newsletter!';
                    document.getElementById('confirmationModal').style.display = 'flex';

                    newsletterForm.reset();
                })
                .catch(error => {
                    hideLoading();
                    console.error('Error:', error);
                    alert('Failed to subscribe. Please try again.');
                });
        }
    });
}

// Utility Functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function hideError(elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

function showLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
}

function hideLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

