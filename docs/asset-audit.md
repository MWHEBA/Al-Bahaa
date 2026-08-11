# Asset Audit

This audit uses visual matching against the supplied PDFs, not filenames alone. Status values:
Exact/strong match, Likely match, Partial/crop match, Missing.

## Summary

- Total image assets found before temporary inspection files: 38
- Raster assets: 36 PNG files, 1 recovered JPEG file
- Vector assets: 1 SVG file
- JPG, JPEG, and WEBP assets found: 0

## Definitive Mapping

| PDF page | PDF visual element | Actual supplied asset path | Dimensions | Status |
|---|---|---:|---:|---|
| Global | Main B-Group / Al Bahaa logo | `static/img/branding/AlBahaa logo.svg` | SVG | Exact/strong match |
| Global | Footer/quote logo | `static/img/branding/AlBahaa logo.svg` | SVG | Exact/strong match |
| Global | Social media icon glyphs | Unresolved | - | Missing |
| Home | Hero seated figure in window, native PDF extraction | `static/img/home/hero-seated-window.jpeg` | 1920x1046 | Exact/strong match |
| Home | Hero seated figure in window, supplied PNG export | `static/img/home/Rectangle 3.png` | 1800x980 | Exact/strong match |
| Home | Specialization pipe/tube image | `static/img/home/Rectangle 8.png` | 400x634 | Exact/strong match |
| Home | Project mosaic architectural drawing | `static/img/home/Rectangle 9.png` | 584x760 | Exact/strong match |
| Home | Project mosaic white skyscraper crop | `static/img/home/Rectangle 9 copy.png` | 370x370 | Exact/strong match |
| Home | Project mosaic structural column crop | `static/img/home/Rectangle 9 copy 2.png` | 370x370 | Exact/strong match |
| Home | Project mosaic glass building crop | `static/img/home/Rectangle 9 copy 3.png` | 370x370 | Exact/strong match |
| Home | Project mosaic curved water/building crop | `static/img/home/Rectangle 9 copy 4.png` | 370x370 | Exact/strong match |
| Home | Project mosaic pressure/gauge crop | `static/img/home/Rectangle 9 copy 11.png` | 370x370 | Exact/strong match |
| Home | Latest news bridge/underpass image | `static/img/home/Rectangle 15.png` | 700x691 | Exact/strong match |
| Home | Client logo: Miller | `static/img/clients/Layer 1.png` | 104x63 | Exact/strong match |
| Home | Client logo: The Don | `static/img/clients/Layer 2.png` | 96x70 | Exact/strong match |
| Home | Client logo: The Spades | `static/img/clients/Layer 3.png` | 107x69 | Exact/strong match |
| Home | Client logo: Creative | `static/img/clients/Layer 4.png` | 111x67 | Exact/strong match |
| Home | Client logo: Jackerson | `static/img/clients/Layer 5.png` | 137x47 | Exact/strong match |
| Home | Client logo: The White | `static/img/clients/Layer 6.png` | 116x60 | Exact/strong match |
| Home | Client logo: Bicycle Company | `static/img/clients/l3.png` | 63x66 | Exact/strong match |
| Home | Client logo: Handmade | `static/img/clients/logo_partner-3.png` | 119x75 | Exact/strong match |
| Home | Client logo: round bird mark | `static/img/clients/11.png` | 75x75 | Exact/strong match |
| Home | Client logo: Steve Harold shield | `static/img/clients/logo_partner-8.png` | 82x66 | Exact/strong match |
| Home | Client logo: Tasty Treats | `static/img/clients/l4.png` | 97x56 | Exact/strong match |
| Home | Client logo: second Miller instance | `static/img/clients/Layer 1 copy.png` | 104x63 | Exact/strong match |
| About | Wide blue facade image | `static/img/about/Rectangle 21.png` | 1800x755 | Exact/strong match |
| About | Team collage curved water/building, top-left/bottom-right source | `static/img/team/Rectangle 24.png` | 390x369 | Exact/strong match |
| About | Team collage curved water/building alternate crop | `static/img/team/Rectangle 24 copy 3 .png` | 390x369 | Exact/strong match |
| About | Team collage bridge/structure crop | `static/img/team/Rectangle 24 copy.png` | 390x369 | Exact/strong match |
| About | Team collage central office tower | `static/img/team/Rectangle 24 copy 2 .png` | 390x369 | Exact/strong match |
| About | Team collage dark blue building | `static/img/team/Rectangle 24 copy 3  .png` | 390x369 | Exact/strong match |
| Projects | First construction band with workers and pipe foreground | `static/img/projects/Rectangle 24 copy 2     .png` | 611x889 | Partial/crop match |
| Projects | Second crane skyline band | Unresolved | - | Missing |
| Projects | Third light-trails/city band | Unresolved | - | Missing |
| Projects | Fourth tower construction band | `static/img/projects/Rectangle 9 copy.png` | 2167x1461 | Exact/strong match |
| Project Details | Main tower construction hero | `static/img/projects/Rectangle 9 copy.png` | 2167x1461 | Exact/strong match |
| News | First article image, beams with suspended worker | Unresolved | - | Missing |
| News | Second article image, building with crane/moon | `static/img/news/Rectangle 24 copy 5.png` | 611x434 | Likely match |
| News | Third article image, scaffold/facade pattern | Unresolved | - | Missing |
| News | Fourth article image, upward crane/building crop | `static/img/news/Rectangle 24 copy 2  .png` | 611x889 | Likely match |
| Contact | Hero crane/building image | `static/img/contact/Clip.png` | 2494x979 | Exact/strong match |

## Supplied But Not Yet Mapped To A PDF Element With Confidence

| Asset path | Dimensions | Notes |
|---|---:|---|
| `static/img/news/Rectangle 24 copy 2.png` | 611x889 | Industrial/tunnel machinery; no clear direct PDF placement found. |
| `static/img/projects/Rectangle 24 copy 3   .png` | 611x578 | Crane/city construction scene; related to Projects/News visual family but not a clear exact visible match. |
| `static/img/news/Rectangle 24 copy 3.png` | 611x578 | Industrial/tunnel machinery; no clear direct PDF placement found. |
| `static/img/projects/Rectangle 24 copy 6.png` | 611x434 | Construction skyline; related to Projects/News visual family but not a clear exact visible match. |

## Remaining Missing Assets

- Projects second crane skyline band.
- Projects third light-trails/city band.
- News first beams/suspended-worker image.
- News third scaffold/facade image.
- Social media icon glyphs.
