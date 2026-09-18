# EYENEX UI/UX Redesign Notes

## Main weaknesses identified

1. Navigation exposed too many equal-priority links, making the header harder to scan.
2. Homepage motion (typewriter + automatic training carousel) competed with the primary conversion actions.
3. Repeated glass-card styling gave nearly every section the same visual weight and weakened hierarchy.
4. Course cards did not make fee, duration, mode, and next actions easy enough to compare at a glance.
5. Course details did not clearly explain the difference between booking an appointment and applying directly.
6. Appointment and application forms were long, flat forms without meaningful grouping or a clear sense of progress.
7. Contact page used an "Apply Now" heading even though the page was an inquiry/contact flow.
8. Mobile behavior was functional but not designed as a separate reading and conversion experience.
9. Privacy/terms copy did not reflect the newer payment screenshot and financial-aid workflow.
10. Homepage hero PNG was unnecessarily heavy for the first viewport.

## Design changes implemented

- Introduced a restrained EYENEX design system using navy, white, soft gray, and gold accents.
- Simplified navigation and grouped secondary destinations under Programs and Resources.
- Rebuilt the homepage hero around one clear value proposition and two clear CTAs.
- Removed typewriter and automatic course-carousel behavior.
- Added a scannable training grid and an Explore → Discuss → Apply journey.
- Reworked catalogue cards around decision-making information.
- Added stronger course-detail hierarchy, breadcrumbs, key-fact pills, and a sticky enrollment card.
- Clarified Appointment vs Apply with contextual explanation rather than competing unlabeled actions.
- Structured appointment/application forms into numbered sections with better field rhythm and error presentation.
- Improved EasyPaisa payment UI and added a Copy Number action.
- Made financial-aid selection visually distinct and easier to understand.
- Rebuilt Admissions as a process timeline and Contact as a true inquiry page.
- Updated About, IELTS, planned programs, Gallery, FAQs, legal pages, and error pages to the same design language.
- Added accessibility improvements: skip link, focus-visible states, proper labels, semantic headings, reduced-motion support, and more readable contrast.
- Improved responsive behavior for navigation, grids, forms, course pages, footer, and CTA groups.
- Re-encoded the homepage hero to WebP for a much smaller initial asset.

## Verification

- `python manage.py check`: pass
- `python manage.py makemigrations --check --dry-run`: no changes detected
- Automated tests: 53/53 pass
- Public-route smoke test: 33 routes checked, 0 failures
- CSS parse: balanced braces and no `tinycss2` parse errors
- Rendered HTML spot-check: single H1, no duplicate IDs, no missing image alt attributes, and no unlabeled form controls on the reviewed pages
