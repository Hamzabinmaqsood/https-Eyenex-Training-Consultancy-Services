# EYENEX Project Changes

## Implemented

- Added a **Book Appointment** action to database-driven course cards, course details, related courses, featured courses, and the home training-area cards.
- Added course delivery mode support: Physical, Online, or Physical & Online.
- Added admin-controlled **appointment fee** per course.
- Appointment submissions store a snapshot of the fee that was shown when the student submitted the request.
- Added appointment form fields for student contact details, city, preferred date/time, payment screenshot, optional message, and financial aid.
- Payment screenshot is required when an appointment fee is greater than zero, unless financial aid is selected.
- Financial aid requests require a reason.
- Added Course Appointments to Django Admin with status management.
- Added EasyPaisa appointment-payment instructions: `03408186889` — Raja Khizar Hayat.
- EasyPaisa details are configurable with `EYENEX_EASYPAISA_NUMBER` and `EYENEX_EASYPAISA_ACCOUNT_NAME` environment variables for production.
- Updated site email to `eyenextrainingsandconsultancy@gmail.com`.
- Updated course catalogue data:
  - NEBOSH IGC — 15 Days — Physical & Online — PKR 180,000
  - IOSH Course Preparation — Physical & Online — PKR 35,000
  - OSHA Training — Physical & Online — PKR 22,000
  - Spoken English — Physical & Online — PKR 20,000
  - IELTS Preparation — Physical & Online — PKR 90,000
- The configured fees above are marked as including the applicable official test/exam fee.
- Added Spoken English and IELTS Preparation to the database-backed course catalogue.
- Normalized `requirements.txt` to UTF-8 for deployment tooling.

## Admin Workflow

1. Sign in to `/admin/`.
2. Open **Courses > Courses**.
3. Edit a course to change its course fee, delivery mode, duration/classes, or appointment fee.
4. Open **Admissions > Course Appointments** to review student requests, payment screenshots, financial-aid reasons, appointment date/time, and status.

## Before Production Deployment

- Configure production environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS`).
- Configure the Namecheap hosting plan for Django/Python, static files, media uploads, and the production database strategy.
- Payment receipt uploads should be treated as private/sensitive files when configuring production media access.

## Verification

- `python manage.py check` passes.
- Django migration state has no pending model changes.
- Full automated test suite: **53 tests passed**.
- Smoke-tested all active course detail and appointment pages with successful HTTP 200 responses.

## UI/UX Redesign — September 2026

- Rebuilt the site-wide visual hierarchy with calmer surfaces, clearer typography, consistent spacing, accessible focus states, and a restrained navy/gold EYENEX design system.
- Simplified the primary navigation by grouping secondary pages under **Programs** and **Resources**, while keeping Courses, Admissions, Contact, and Apply easy to reach.
- Added a desktop contact strip and a more useful footer with direct course, support, phone, email, and WhatsApp paths.
- Reworked the homepage hero to a static high-impact layout instead of distracting typewriter/carousel motion.
- Replaced the auto-moving training carousel with a scannable responsive course grid.
- Added a clear three-step **Explore → Discuss → Apply** journey so users understand the difference between appointments and applications.
- Redesigned course catalogue cards to make price, mode, level, duration, and next actions easier to compare.
- Redesigned course detail pages with breadcrumbs, key facts, a sticky enrollment summary, and separate guidance for **Book Appointment** vs **Apply for Course**.
- Redesigned appointment booking into numbered sections for contact details, schedule, payment/financial aid, and optional notes.
- Added a one-click EasyPaisa number copy control and clearer paid/free appointment states.
- Redesigned the application form into logical sections and added a visible explanation of what happens after submission.
- Corrected the Contact page's previous misleading "Apply Now" heading and created distinct inquiry/contact information areas.
- Reworked Admissions into a visual enrollment timeline.
- Updated About, IELTS, Study Abroad, Leadership, Gallery, FAQ, Privacy, Terms, 404, and 500 pages to use the same design language.
- Updated Privacy and Terms copy so appointment payment screenshots and financial-aid reasons are covered by the public-facing information.
- Added a minimum selectable appointment date in the browser while keeping server-side validation intact.
- Added skip-navigation, visible keyboard focus, labeled form controls, reduced-motion support, and improved mobile layouts.
- Re-encoded the homepage hero image as WebP (about 1.9 MB → about 84 KB) to improve initial page loading without changing the visual content.

## Final Production Fixes — September 2026

- Updated public address to Burj-e-Noor Plaza, First Floor, Shamsabad, Rawalpindi, Pakistan.
- Updated canonical/site domain to `eyenextrainingconsultancy.services`.
- Fixed the protected staff payment-receipt view by importing `CourseAppointment` correctly.
- Added final instructor-based artwork for Spoken English and IELTS Preparation.
- Hardened GitHub hygiene so the public repository excludes SQLite data, student uploads, payment screenshots, environment files, and production secrets.
