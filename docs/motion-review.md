# Motion refinement review

The portfolio retains its charcoal/teal identity, existing layout and content.
Motion serves navigation continuity and direct feedback, with one focal colour
trace across the hero's solution line. There is no new animation dependency.

| Before | After | Why |
| --- | --- | --- |
| Hero trace used `cubic-bezier(.4, 0, .2, 1)`. | `assets/site.css:19` defines `cubic-bezier(.77, 0, .175, 1)` for the 620ms trace. | A deliberate acceleration/deceleration distinguishes the occasional focal sequence from quick UI arrivals. Text stays readable throughout. |
| Photograph hover zoomed 3.5% over 240ms; underlines took 220ms. | `assets/site.css:478` and `:485` use 180ms; photographs zoom 2.5%. | Smaller, faster feedback suits frequent hovering. Technical diagrams stay completely framed. |
| Keyboard mode could leave a hovered photograph enlarged and persist after mouse movement. | `assets/site.css:494` suppresses hover transforms with sufficient specificity; `assets/motion.js:29` restores pointer feedback after real mouse movement or wheel input. | Keyboard actions are immediate; returning to a pointer restores normal feedback. Input tracking avoids redundant style writes. |
| Collapsing the mobile menu could leave its entrance running. | `assets/site.js:233` uses the shared close routine, which cancels motion before collapsing. | Repeated opening/closing cannot leave stale effects behind. |
| A viewport change could retain transforms calculated for the old carousel width. | `assets/site.js:137` cancels card motion before measuring the changed layout. | Breakpoint changes immediately produce the correct positions and stable row height. |
| Rapid carousel clicks preserved position but restarted opacity at 1. | `assets/site.js:160` captures position and opacity before cancellation, and retargets from both. | An arriving card no longer flashes fully opaque when interrupted. |
| New cards entered just 24px away while neighbouring cards moved a full column, causing overlap. | `assets/site.js:172` uses one card-width plus the grid gap on desktop/tablet; mobile retains a 12px arrival. | The moving row preserves its spacing instead of painting images and text over adjacent cards. |
| Closing an image preview during entrance restarted it at full opacity and scale. | `assets/site.js:205` captures current opacity and transform before its 100ms exit. | Dismissal begins from the visible state without a jump. Escape and focus restoration remain native and immediate. |
| Gallery arrival and filtering faded otherwise readable content. | Gallery images and filtered results remain still. | These fades conveyed no useful state or relationship; media motion belongs to the deliberate 240ms image-preview entrance. |

**Approve.** No unresolved motion defects were found in the bounded source,
browser and visual review. Routine UI effects stay below 300ms. CSS and the Web
Animations API handle hover, feedback and interruption; supported desktop browsers
retain the existing 100/180ms cross-document transition with a stationary header.
There are no section entrance sequences, loops, layout-property animations or
permanent `will-change` hints.

Verification on 29 September 2026:

- Production Jekyll build passed.
- All 42 content and browser tests passed, including six new regressions for mixed
  input, menu cancellation, resize cancellation, modal interruption, interrupted
  carousel opacity and spacing throughout its trajectory.
- Twelve preview combinations covered English/Polish, dark/light, and desktop,
  tablet and mobile. No page script errors or horizontal overflow were observed.
- Paused hero and carousel frames were inspected at multiple points. The corrected
  carousel was confirmed at desktop, tablet and mobile widths.
- The accessibility audit found zero automated violations across 20 combinations.
- Reduced motion, keyboard navigation, unavailable theme storage, no JavaScript,
  category browsing, original diagrams and mocked form delivery remain covered.

Mobile checks used Chromium emulation, not a physical phone. These checks are not
a field-performance assessment or a complete manual accessibility certification.
The preview reported no mobile long tasks; one 51ms task occurred during the initial
desktop load. Observed layout-shift totals stayed below 0.0014 in this preview run.

Publication remains a separate step. Preview: <http://127.0.0.1:4173/> and
<http://127.0.0.1:4173/pl/>. Implementation details and timing tokens are documented
in [motion-system.md](motion-system.md).
