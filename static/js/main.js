document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".glass-navbar");

    if (navbar) {
        function handleNavbarShadow() {
            navbar.classList.toggle("navbar-scrolled", window.scrollY > 20);
        }

        handleNavbarShadow();
        window.addEventListener("scroll", handleNavbarShadow, { passive: true });
    }

    document.querySelectorAll("#mainNavbar .nav-link:not(.dropdown-toggle), #mainNavbar .dropdown-item").forEach(function (link) {
        link.addEventListener("click", function () {
            const menu = document.getElementById("mainNavbar");
            if (menu && window.innerWidth < 992 && menu.classList.contains("show") && window.bootstrap) {
                bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }
        });
    });

    const hero = document.querySelector("[data-hero]");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const timers = [];

    if (hero && !reducedMotion) {
        const slides = hero.querySelectorAll(".hero-slide");
        let activeSlide = 0;

        if (slides.length > 1) {
            const sliderTimer = window.setInterval(function () {
                slides[activeSlide].classList.remove("active");
                activeSlide = (activeSlide + 1) % slides.length;
                slides[activeSlide].classList.add("active");
            }, 7000);
            timers.push({ id: sliderTimer, type: "interval" });
        }
    }

    const typewriter = document.querySelector("[data-typewriter]");
    if (typewriter && !reducedMotion) {
        const phrases = typewriter.dataset.typewriterPhrases.split("|");
        let phraseIndex = 0;
        let characterIndex = 0;
        let deleting = false;
        let typewriterTimer;

        typewriter.textContent = "";

        function runTypewriter() {
            const phrase = phrases[phraseIndex];
            characterIndex += deleting ? -1 : 1;
            typewriter.textContent = phrase.slice(0, characterIndex);

            let delay = deleting ? 30 : 62;
            if (!deleting && characterIndex === phrase.length) {
                deleting = true;
                delay = 2200;
            } else if (deleting && characterIndex === 0) {
                deleting = false;
                phraseIndex = (phraseIndex + 1) % phrases.length;
                delay = 350;
            }

            typewriterTimer = window.setTimeout(runTypewriter, delay);
        }

        typewriterTimer = window.setTimeout(runTypewriter, 350);
        timers.push({ get id() { return typewriterTimer; }, type: "timeout" });
    }

    const trainingCarousel = document.querySelector("[data-training-carousel]");
    if (trainingCarousel && !reducedMotion) {
        const viewport = trainingCarousel.querySelector(".training-carousel__viewport");
        const track = trainingCarousel.querySelector(".training-carousel__track");
        const originalCards = Array.from(track.children);
        const cloneCount = 4;
        let currentIndex = 0;
        let autoplayTimer;
        let resumeTimer;
        let pointerStartX = 0;
        let pointerDelta = 0;
        let dragging = false;
        let paused = false;

        originalCards.slice(0, cloneCount).forEach(function (card) {
            const clone = card.cloneNode(true);
            clone.setAttribute("aria-hidden", "true");
            clone.setAttribute("tabindex", "-1");
            track.appendChild(clone);
        });

        function getStep() {
            const cards = track.children;
            return cards.length > 1 ? cards[1].offsetLeft - cards[0].offsetLeft : 0;
        }

        function setPosition(animate, dragOffset) {
            track.classList.toggle("is-animating", animate);
            track.style.transform = "translate3d(" + ((-currentIndex * getStep()) + (dragOffset || 0)) + "px, 0, 0)";
        }

        function scheduleAutoplay(delay) {
            window.clearTimeout(autoplayTimer);
            if (!paused && !dragging) {
                autoplayTimer = window.setTimeout(advance, delay || 4000);
            }
        }

        function advance() {
            currentIndex += 1;
            setPosition(true, 0);
        }

        function pause() {
            paused = true;
            window.clearTimeout(autoplayTimer);
            window.clearTimeout(resumeTimer);
        }

        function resume(delay) {
            window.clearTimeout(resumeTimer);
            resumeTimer = window.setTimeout(function () {
                paused = false;
                scheduleAutoplay();
            }, delay || 500);
        }

        track.addEventListener("transitionend", function (event) {
            if (event.propertyName !== "transform") return;
            if (currentIndex === originalCards.length) {
                currentIndex = 0;
                setPosition(false, 0);
            }
            scheduleAutoplay();
        });

        trainingCarousel.addEventListener("mouseenter", pause);
        trainingCarousel.addEventListener("mouseleave", function () { resume(700); });
        trainingCarousel.addEventListener("focusin", pause);
        trainingCarousel.addEventListener("focusout", function (event) {
            if (!trainingCarousel.contains(event.relatedTarget)) resume(700);
        });

        viewport.addEventListener("pointerdown", function (event) {
            if (event.pointerType === "mouse" && event.button !== 0) return;
            dragging = true;
            pointerStartX = event.clientX;
            pointerDelta = 0;
            pause();
            viewport.classList.add("is-dragging");
            viewport.setPointerCapture(event.pointerId);
            track.classList.remove("is-animating");
        });

        viewport.addEventListener("pointermove", function (event) {
            if (!dragging) return;
            pointerDelta = event.clientX - pointerStartX;
            setPosition(false, pointerDelta);
        });

        function finishDrag(event) {
            if (!dragging) return;
            dragging = false;
            viewport.classList.remove("is-dragging");
            if (viewport.hasPointerCapture(event.pointerId)) viewport.releasePointerCapture(event.pointerId);

            const threshold = Math.min(80, getStep() * .18);
            if (pointerDelta < -threshold) {
                currentIndex += 1;
            } else if (pointerDelta > threshold && currentIndex > 0) {
                currentIndex -= 1;
            }
            pointerDelta = 0;
            setPosition(true, 0);
            resume(1500);
        }

        viewport.addEventListener("pointerup", finishDrag);
        viewport.addEventListener("pointercancel", finishDrag);
        window.addEventListener("resize", function () { setPosition(false, 0); }, { passive: true });

        setPosition(false, 0);
        scheduleAutoplay();
        timers.push({ get id() { return autoplayTimer; }, type: "timeout" });
        timers.push({ get id() { return resumeTimer; }, type: "timeout" });
    }

    window.addEventListener("pagehide", function () {
        timers.forEach(function (timer) {
            if (timer.type === "interval") {
                window.clearInterval(timer.id);
            } else {
                window.clearTimeout(timer.id);
            }
        });
    }, { once: true });
});
