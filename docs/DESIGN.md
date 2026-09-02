---
name: Epicurean Minimalist
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#574141'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f1'
  outline: '#8b7170'
  outline-variant: '#debfbe'
  surface-tint: '#a9353c'
  primary: '#a5323a'
  on-primary: '#ffffff'
  primary-container: '#c64b50'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b2'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e4e2e1'
  on-secondary-container: '#656464'
  tertiary: '#006948'
  on-tertiary: '#ffffff'
  tertiary-container: '#00855c'
  on-tertiary-container: '#f5fff7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad9'
  primary-fixed-dim: '#ffb3b2'
  on-primary-fixed: '#410008'
  on-primary-fixed-variant: '#881c27'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474747'
  tertiary-fixed: '#88f8c4'
  tertiary-fixed-dim: '#6bdba9'
  on-tertiary-fixed: '#002114'
  on-tertiary-fixed-variant: '#005237'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
  canvas-white: '#FFFFFF'
  text-primary: '#333333'
  accent-coral: '#D35459'
  surface-muted: '#F8F8F8'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1200px
  gutter: 16px
  margin-mobile: 20px
---

## Brand & Style
The brand personality is refined, intentional, and high-end, catering to home cooks who value clarity and elegance over clutter. The target audience is modern, health-conscious, and tech-savvy. 

The design system adopts a **Minimalist** style with elements of **High-Contrast Modernism**. It prioritizes extreme legibility, generous whitespace to let food photography shine, and a sophisticated use of color. UI elements should feel airy but grounded by strong typographic hierarchies. The emotional response should be one of calm focus, ensuring that the interface never competes with the culinary content.

## Colors
The palette is anchored by a high-contrast foundation of `canvas-white` and `text-primary`. The vibrant `accent-coral` is used sparingly for interactive elements, primary actions, and brand highlights. 

- **Primary:** `accent-coral` (#D35459) for call-to-actions and active states.
- **Secondary:** `text-primary` (#333333) for headers and heavy body text.
- **Neutral:** `surface-muted` (#F8F8F8) for subtle background differentiation and card containers.
- **Background:** Pure `canvas-white` (#FFFFFF) is the default background to maximize whitespace and contrast.

## Typography
This design system utilizes **Hanken Grotesk** for all roles to maintain a clean, contemporary, and systematic feel. The typeface offers a sharp, professional geometry that aligns with the minimalist aesthetic.

- **Headlines:** Use Bold and Semi-Bold weights with tight letter-spacing for a modern, editorial look.
- **Body:** Use a 1.5x to 1.6x line height for recipe instructions to ensure maximum legibility during cooking.
- **Labels:** Use uppercase and slight tracking for metadata like "Prep Time" or "Difficulty" to distinguish from body copy.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a focus on mobile optimization. 

- **Mobile:** A single-column layout with 20px side margins. Spacing between recipe steps should be generous (`lg` / 40px) to prevent accidental taps and visual crowding.
- **Desktop:** A 12-column grid with a 1200px max-width. Content is often centered with significant lateral whitespace to maintain the minimalist feel.
- **Rhythm:** Use an 8px base unit. Component internal padding should favor the `md` (24px) unit to create an "airy" signature.

## Elevation & Depth
In alignment with the minimalist style, depth is conveyed through **Tonal Layers** and **Low-contrast outlines** rather than heavy shadows.

- **Level 0:** `canvas-white` (#FFFFFF) for the primary background.
- **Level 1:** `surface-muted` (#F8F8F8) for secondary sections like ingredient lists or sidebar filters.
- **Borders:** Use 1px solid borders in a very light gray (e.g., #EEEEEE) for cards and input fields. 
- **Shadows:** Use a single "Ambient" shadow for floating elements (like a "Save Recipe" FAB). It should be extremely diffused: `0px 10px 30px rgba(0, 0, 0, 0.04)`.

## Shapes
The shape language is **Soft**, utilizing small radii to maintain a crisp, professional look without feeling "bubbly."

- **Standard Buttons & Inputs:** 4px (0.25rem) corner radius.
- **Recipe Cards:** 8px (0.5rem) corner radius for a subtle distinction.
- **Media (Food Photography):** Should maintain sharp 0px or very slight 4px edges to preserve the editorial quality of the imagery.

## Components
- **Buttons:** Primary buttons use `accent-coral` with white text. Secondary buttons use a `text-primary` outline with no fill. All buttons feature high-density padding (12px vertical, 24px horizontal).
- **Input Fields:** Minimalist design—bottom border only or a very light full-border. Focused state uses an `accent-coral` bottom border.
- **Chips:** Used for dietary tags (e.g., "Vegan"). Use `surface-muted` background with `label-sm` typography. No borders.
- **Cards:** White background with a 1px #EEEEEE border. Avoid shadows unless the card is interactive or draggable.
- **Lists:** Recipe steps should be numbered with `accent-coral` large numerals to guide the user's eye.
- **Progress Bar:** A thin 4px bar at the top of the screen for "Active Cooking Mode" using the `accent-coral` color.