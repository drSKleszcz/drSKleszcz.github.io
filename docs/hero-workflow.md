# Homepage hero workflow

The hero presents the identity line and two-sentence headline, then a centered five-stage illustration above the project/contact links. English reads “Understanding systems. Engineering solutions.” The engineering sentence keeps the cyan accent. Polish uses the paired translation and can wrap without splitting a sentence's reveal. The hero leaves supporting modeling and business-analysis detail to the About, Expertise, project pages, and page metadata.

The illustration explains a way of working; it does not imply that the five linked projects form one integrated system. Its caption identifies it as illustrative. No measurements or performance claims are invented. Model and analysis drawings carry more visual weight than the other stages.

| Stage | Linked project |
| --- | --- |
| System | Hydrogen Hub |
| Modeling | Gas turbine and digital twin |
| Analysis | Techno-economic energy assessment |
| Automation | Orifice calculation software |
| Decision | FedEx pricing calculator |

Stage labels, accessible descriptions, links, and project titles use the active language's collection. The SVGs are decorative for assistive technology; the HTML links and figure caption carry their meaning. Desktop shows a centered row of five, while narrow screens use two rows. Mobile stage links open on the first tap.

## Opening and idle signal

On every eligible homepage document load, CSS fades each complete headline sentence as one block. The two 720ms fades begin at 0 and 780ms, using the focal-duration and tracing-ease tokens. After they finish, the five complete drawings and labels fade in portfolio order over 320ms each, beginning at 1650, 2010, 2370, 2730, and 3090ms. The desktop connector fades across the stage sequence. Geometry, text, and spacing are reserved from first paint; chart lines do not move.

The pre-paint attribute enables the CSS sequence for visible, non-keyboard, non-anchor arrivals, including visitors whose systems request reduced motion. These visitors see the same one-time fade, but no recurring ring pulse or other spatial UI effects. Without JavaScript, everything remains visible. Keyboard input, interaction with the hero, resizing, scrolling away, hiding the tab, or a motion-preference change settles the sequence immediately. Reloading or returning from a project page runs it again on eligible visits. Accessibility scans sample the settled state so the deliberately translucent entrance frames are not mistaken for resting text contrast.

Once the final stage appears, a decorative ring pulses across all five stages in order after a 600ms pause. Each ring scales from .85 to 1.35 and fades from .6 opacity to zero over 650ms; starts are staggered by 220ms and the cycle repeats every 7s. The ring is 36px on desktop and 30px on mobile. It pauses during hover/focus, offscreen or hidden states, and reduced motion. Stage hover/focus retains only ordinary link feedback; hovering the headline never starts motion.

The design uses SVG, CSS animations, and the existing small motion controller. No animation dependency, page router, autoplaying chart, or replay control is required. Browser tests cover timing, replay, interruption, reduced motion, no-JavaScript fallback, first-tap navigation, and theme/language layouts.
