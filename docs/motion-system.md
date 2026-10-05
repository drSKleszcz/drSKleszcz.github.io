# Portfolio motion

Motion follows the technical visual language: it clarifies navigation, preserves context when content changes, and briefly explains the homepage workflow. Reading sections, original project images, and charts otherwise stay still.

| Role | Duration | Use |
| --- | --- | --- |
| Feedback | 120ms | Control colour/press states and theme icon |
| Hover | 180ms | Navigation underline and photographic preview zoom |
| Change | 220ms | Carousel continuity and mobile menu |
| Overlay | 240ms | Image preview |
| Hero stages | 320ms | Whole-diagram fades |
| Expertise trace | 280ms, 140ms stagger | Numbered rules on first view |
| Exit | 100ms | Pointer-initiated image preview dismissal |
| Focal | 720ms headline / 650ms signal | Explanatory headline and decorative workflow signal |

Values live in `assets/site.css`. Ordinary UI uses `cubic-bezier(.23, 1, .32, 1)`. The desktop hero connector uses `cubic-bezier(.77, 0, .175, 1)`. Photograph hover uses `ease`.

`assets/motion.js` owns the small Web Animations API helper. `assets/site.js` calls it after updating state, so controls never wait for animation. Carousel cards retain their visual position and opacity during rapid arrow clicks, then move to the new layout. Resizing cancels obsolete distances. The reserved row height prevents shifts; the mobile menu entrance cancels on close.

Only photographic previews zoom. Diagrams and screenshots keep their complete framing and original colours. Gallery images, filtered results, and reading text do not receive generic entrances. When Expertise reaches the reading area, its existing dividers trace across three numbered capabilities once, then settle into subtle rules. Desktop rules draw downward; mobile rules draw across. Pointer hover briefly brightens the local rule and heading without suggesting the column is a link. The image dialog preserves focus, Escape, original-image access, and its visual state if dismissed mid-entrance.

The homepage headline and complete workflow stages use the CSS sequence documented in [hero-workflow.md](hero-workflow.md). The two 720ms sentences start at 0 and 780ms; five 320ms stage fades start at 1650ms and 360ms intervals. The connector fades in place. The one-time opening also runs when reduced motion is requested; only the recurring signal and other spatial UI effects stay disabled. A small pre-paint attribute prevents a visible-to-hidden flash. Eligible homepage reloads and returns replay the explanation. The entire composition stays visible without JavaScript and for keyboard or anchor arrivals. Interruptions settle it into its completed state.

After the final stage, a 7s repeating signal runs across the five markers. Only each ring's scale and opacity animate. Hovering or focusing a workflow link pauses this idle signal; link colour and focus affordances remain. The caption does not change on hover. Offscreen, hidden-tab, and reduced-motion states also pause the signal. Direct mobile taps still navigate.

Keyboard actions cancel active effects and update immediately. Real mouse movement, pointer presses, and wheel input restore pointer feedback without writing styles on every movement. Reduced motion removes spatial movement but keeps short colour feedback. Hidden tabs stop active effects. Palette changes are immediate for reliable contrast; only the theme icon moves. A short-lived session hint carries keyboard navigation mode to the next page when storage is available.

Expertise remains fully readable if JavaScript is unavailable, on keyboard arrivals, and under reduced motion. Its decorative sequence is skipped in those cases; reduced motion retains only a short hover colour change.

On supported desktop browsers, CSS cross-document View Transitions provide a 100/180ms exit/arrival crossfade while the header remains stationary. Keyboard, touch, narrow screens, and reduced motion use ordinary navigation. There is no client router, navigation interception, animation library, or fallback delay.

If JavaScript or an animation API is unavailable, all content and links remain visible and usable.
