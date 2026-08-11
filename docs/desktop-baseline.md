# Desktop Baseline Manifest

This document freezes the approved desktop visual baseline before responsive work starts. Validation diff values use the established threshold-40 pixel comparison against the supplied PDF render unless noted otherwise.

## Home

- Route: `/`
- PDF reference: `Home.pdf`
- Final validation screenshot: `validation/home_2b_final.png`
- Final rendered dimensions: `1920x6390`
- Header logo asset: `static/img/branding/AlBahaa logo.svg`
- Major image assets:
  - `static/img/home/Rectangle 3.png`
  - `static/img/home/Rectangle 8.png`
  - `static/img/home/Rectangle 9.png`
  - `static/img/home/Rectangle 9 copy*.png`
  - `static/img/home/Rectangle 15.png`
  - `static/img/clients/*.png`
- Final known PDF diff: `3.7467%`
- Intentional visual exceptions: current approved SVG production logo is preserved for Home; historical footer/content text is not normalized in this phase.
- Approval status: `HOME DESKTOP APPROVED BASELINE`

## About

- Route: `/about/`
- PDF reference: `About.pdf`
- Final validation screenshot: `validation/about_3b_final.png`
- Final rendered dimensions: `1920x5541`
- Header logo asset: `static/img/branding/about-pdf-logo.png`
- Major image assets:
  - `static/img/about/Rectangle 21.png`
  - `static/img/team/*.png`
  - `static/img/clients/*.png`
- Final known PDF diff: `2.7130%`
- Intentional visual exceptions: About uses the PDF-recovered logo variant and page-specific footer geometry.
- Approval status: `ABOUT DESKTOP APPROVED BASELINE`

## Projects Listing

- Route: `/projects/`
- PDF reference: `Projects.pdf`
- Final validation screenshot: `validation/projects_final.png`
- Final rendered dimensions: `1920x4479`
- Header logo asset: `static/img/branding/about-pdf-logo.png`
- Major image assets:
  - `static/img/projects/projects-band-1-recovered.png`
  - `static/img/projects/projects-band-2-recovered.png`
  - `static/img/projects/projects-band-3-recovered.png`
  - `static/img/projects/projects-band-4-recovered.png`
- Final known PDF diff: `1.6494%`
- Intentional visual exceptions: project-band photography crops were recovered from PDF-rendered image areas because the PDF exposes no reusable image XObjects; all text/UI remains HTML/CSS.
- Approval status: `PROJECTS DESKTOP APPROVED BASELINE`

## Project Detail

- Route: `/projects/sed-ut-perspiciatis/`
- PDF reference: `Project Details.pdf`
- Final validation screenshot: `validation/project_detail_final.png`
- Final rendered dimensions: `3149x2965`
- Header logo asset: `static/img/branding/project-detail-pdf-logo.png`
- Major image assets:
  - `static/img/projects/project-detail-tower-recovered.png`
- Final known PDF diff: `1.3715%`
- Intentional visual exceptions: the detail page preserves the unusually wide `3149px` PDF canvas for desktop fidelity.
- Approval status: `PROJECT DETAIL DESKTOP APPROVED BASELINE`

## News

- Route: `/news/`
- PDF reference: `News.pdf`
- Final validation screenshot: `validation/news_final.png`
- Final rendered dimensions: `1920x3782`
- Header logo asset: `static/img/branding/about-pdf-logo.png`
- Major image assets:
  - `static/img/news/news-article1-recovered.png`
  - `static/img/news/news-article2-recovered.png`
  - `static/img/news/news-article3-recovered.png`
  - `static/img/news/news-article4-recovered.png`
- Final known PDF diff: `2.0288%`
- Intentional visual exceptions: article images were recovered as clean image-only crops; article text, buttons, and pagination remain HTML/CSS.
- Approval status: `NEWS DESKTOP APPROVED BASELINE`

## Contact

- Route: `/contact/`
- PDF reference: `Contact.pdf`
- Final validation screenshot: `validation/contact_final.png`
- Final rendered dimensions: `2650x2956`
- Header logo asset: `static/img/branding/contact-pdf-logo.png`
- Major image assets:
  - `static/img/contact/contact-hero-recovered.png`
- Final known PDF diff: `1.0530%`
- Intentional visual exceptions: Contact preserves the `2650px` PDF canvas and has a functional Django form while matching the default GET visual state.
- Approval status: `CONTACT DESKTOP APPROVED BASELINE`

## Canonical Fresh Freeze Screenshots

Fresh Phase 8 regression captures are stored as:

- `validation/freeze_home.png`
- `validation/freeze_about.png`
- `validation/freeze_projects.png`
- `validation/freeze_project_detail.png`
- `validation/freeze_news.png`
- `validation/freeze_contact.png`

The `validation/` directory is development/reference material only and is ignored by git.
