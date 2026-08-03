# Design QA

Date: 2026-07-29

## Evidence

All captures use the same browser, page state, color scheme, and viewport within each pair.

| Surface | Viewport | Source capture | EEDIY capture | Combined review |
| --- | --- | --- | --- | --- |
| Home, desktop, light | 1280 × 720 CSS px | `.artifacts/source/source-desktop-light-top.png` | `.artifacts/source/local-home-desktop-final.png` | `.artifacts/source/qa-desktop-home.png` |
| Home, mobile, light | 390 × 844 CSS px | `.artifacts/source/source-mobile-top.png` | `.artifacts/source/local-mobile-home-final2.png` | `.artifacts/source/qa-mobile-home.png` |
| Course, mobile, light | 390 × 844 CSS px | `.artifacts/source/source-course-mobile.png` | `.artifacts/source/local-course-mobile-final.png` | `.artifacts/source/qa-mobile-course.png` |

The browser emitted 1265 × 712 desktop images and 375 × 811 mobile images after accounting for its scrollbar.

## Review history

### Pass 1

- P1 layout: the course tree was hidden behind two extra navigation levels.
- P1 typography and density: course metadata used a large bordered table.
- P1 responsive layout: the long site title truncated in the mobile header.
- P2 icons: palette and repository icons differed from the established icon family.
- P2 branding: the home mark used one fixed size, creating different vertical rhythm across breakpoints.

All findings were corrected before the final captures.

### Final pass

- Header height, three-column grid, sidebar widths, article width, gutters, and scroll behavior align at desktop size.
- Roboto Slab and Roboto Mono, heading weights, line height, palette, and native Material surfaces align in light and dark schemes.
- The mobile header, 16 px article gutter, navigation drawer, overlay, and touch controls remain stable at 390 × 844.
- The 35 course directions are direct navigation groups; the active direction and course expand and highlight correctly.
- Course pages use three top-level sections and an unboxed document flow.
- Theme, language, navigation, search, and back-to-top controls were exercised in the browser.
- The language menu preserves the deep course path and activates the correct language tree.
- A `6.003` search returned the expected course result.
- Focus labels, semantic controls, image alternatives, reduced motion, and wide-table keyboard access are present.
- No P0, P1, or P2 finding remains.

## Final result

passed
