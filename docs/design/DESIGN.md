---
name: Nexus Immigration AI
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#43474f'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#747781'
  outline-variant: '#c4c6d1'
  surface-tint: '#3e5e95'
  primary: '#00193c'
  on-primary: '#ffffff'
  primary-container: '#002d62'
  on-primary-container: '#7796d1'
  inverse-primary: '#abc7ff'
  secondary: '#115cb9'
  on-secondary: '#ffffff'
  secondary-container: '#659dfe'
  on-secondary-container: '#003370'
  tertiary: '#001b31'
  on-tertiary: '#ffffff'
  tertiary-container: '#003151'
  on-tertiary-container: '#009cf5'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d7e2ff'
  primary-fixed-dim: '#abc7ff'
  on-primary-fixed: '#001b3f'
  on-primary-fixed-variant: '#24467c'
  secondary-fixed: '#d7e2ff'
  secondary-fixed-dim: '#acc7ff'
  on-secondary-fixed: '#001a40'
  on-secondary-fixed-variant: '#004491'
  tertiary-fixed: '#cfe5ff'
  tertiary-fixed-dim: '#98cbff'
  on-tertiary-fixed: '#001d33'
  on-tertiary-fixed-variant: '#004a77'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
  success-green: '#10B981'
  warning-amber: '#F59E0B'
  error-red: '#EF4444'
  surface-bg: '#F8FAFC'
  ai-accent: '#EEF2FF'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

The design system is engineered to evoke **trust, precision, and global mobility**. As a platform handling life-changing immigration decisions through advanced AI (ML, DL, LLM), the visual language must balance high-tech capability with human-centric accessibility. 

The chosen style is **Cloud-Native Modern**. This approach leverages the cleanliness of SaaS minimalism but introduces "technical depth" through subtle glassmorphism and data-rich interfaces. It reflects a sophisticated architecture (MSA) by using modular UI components that feel independent yet interconnected. The atmosphere is professional and authoritative, utilizing a "command center" aesthetic—organized, data-driven, and highly legible—to reassure users navigating complex legal and bureaucratic processes.

Key visual pillars include:
- **Clarity over Ornament:** Every element serves a functional purpose in the user's immigration journey.
- **Technical Sophistication:** Subtle gradients and micro-interactions that hint at the underlying AI processing.
- **Safety and Reliability:** Stable layouts and a traditional professional color palette to mitigate the stress of immigration.

## Colors

The color palette is anchored in **Deep Navy (#002D62)** to establish immediate institutional trust and authority. This is complemented by **Professional Blue (#0056B3)** for primary actions and interactive elements, symbolizing technology and progress.

**Tertiary Blue** is used sparingly for AI-driven insights and data visualizations to draw the eye to machine-generated recommendations. The **Neutral** palette shifts toward cool slates to maintain the "Cloud-Native" feel without appearing sterile. 

**Color Usage Guidelines:**
- **Primary:** Navigation bars, primary buttons, and heavy headings.
- **Secondary:** Secondary actions, progress indicators, and active states.
- **AI Accent:** Used as a background tint for chatbot messages and OCR-extracted data fields to distinguish AI-generated content from user input.
- **Status Colors:** Standardized green, amber, and red are reserved strictly for visa probability indicators and validation feedback.

## Typography

This design system utilizes **Inter** for all primary interface elements to ensure maximum readability and a clean, neutral tone. Inter’s tall x-height and excellent legibility at small sizes make it ideal for data-heavy dashboards and complex legal text.

To emphasize the "High-Tech AI" aspect of the platform, **JetBrains Mono** is introduced for labels, metadata, and status tags. This monospaced font provides a subtle technical "developer-lite" aesthetic, signaling to the user when they are looking at raw data, calculated probabilities, or system-generated IDs.

**Key Rules:**
- Use `display-lg` only for major onboarding headers.
- `label-md` and `label-sm` (JetBrains Mono) should be used for data points in charts, file sizes in upload zones, and "Calculated by AI" disclaimers.
- Maintain a minimum contrast ratio of 4.5:1 for all body text against backgrounds.

## Layout & Spacing

The layout follows a **Fluid Grid System** with a maximum container width of 1280px to ensure data visualizations remain readable on ultra-wide monitors. 

**Grid Architecture:**
- **Desktop (1024px+):** 12-column grid with 24px gutters. Main content typically spans 8 columns, while the AI Chatbot or secondary insights reside in a 4-column sidebar.
- **Tablet (768px - 1023px):** 8-column grid with 20px gutters. Content reflows to a single column for focus, with the chatbot becoming a floating action button or expandable bottom sheet.
- **Mobile (<767px):** 4-column grid with 16px margins. Information is stacked vertically.

The spacing rhythm is based on an **8px base unit**. All padding, margins, and gaps must be multiples of 8 to maintain a strict, professional alignment that reflects the precision of the underlying ML models.

## Elevation & Depth

To reflect a "Cloud-Native" and "Sophisticated" aesthetic, the design system uses **Tonal Layering** combined with **Ambient Shadows**.

- **Surface Levels:** 
    - **L0 (Background):** `surface-bg` (#F8FAFC) - The base canvas.
    - **L1 (Cards/Sections):** White (#FFFFFF) - Used for primary content blocks.
    - **L2 (Popovers/Modals):** White with a soft, diffused shadow (15% opacity Navy).
- **Glassmorphism:** Reserved for the **AI Chatbot Overlay** and **Fixed Navigation Bars**. Use a `backdrop-filter: blur(12px)` with a semi-transparent white stroke (1px) to create a sense of lightness and technical superiority.
- **Interaction Depth:** Buttons should use a subtle inner-shadow when pressed rather than a heavy drop-shadow, maintaining a flat but tactile feel.

## Shapes

The shape language is **Soft (0.25rem)**. This "near-sharp" approach communicates professional rigor and precision. 

- **Input Fields & Buttons:** 4px (0.25rem) radius.
- **Data Cards:** 8px (0.5rem) radius to soften the presentation of complex information.
- **Chat Bubbles:** 12px (0.75rem) on three corners, with a sharp corner on the anchor side to distinguish the speaker.
- **Progress Bars:** Fully rounded (pill) to represent fluid movement and "loading" states.
- **File Upload Zones:** Dashed borders with a 4px radius, using a light blue tint to invite interaction.

## Components

### 1. Data Charts & Probability Visuals
- **Visa Probability Gauge:** A semi-circular gauge using a gradient from `secondary` to `success-green`. Use `label-md` for the percentage text.
- **Life Cost Bar Charts:** Grouped bar charts using `primary`, `secondary`, and `tertiary` blues.

### 2. AI Chatbot Interface
- **Message Bubbles:** User messages in `primary` blue (white text). AI responses in `ai-accent` with a `primary` blue 2px left-border to denote "system output."
- **Streaming Indicator:** A small, animated three-dot pulse in `secondary` blue when the LLM is generating text.

### 3. File Upload & OCR Zone
- **State 1 (Empty):** Dashed `neutral` border, "Cloud-Native" upload icon.
- **State 2 (Processing):** Progress bar with an indeterminate animation.
- **State 3 (Success):** The zone turns `ai-accent`, and extracted fields are highlighted with a small "OCR" badge in `label-sm` JetBrains Mono.

### 4. Progress Bars
- **Checklist Progress:** A linear bar at the top of the screen. As users check off immigration tasks, the bar fills with a `secondary` blue gradient.

### 5. Form Fields
- **Validation:** Real-time validation using `error-red` for borders and helper text. Labels should always be visible above the input field, never hidden as placeholders.

### 6. Cards
- **Country Recommendation Cards:** Top-weighted with a high-quality flag icon or minimalist country silhouette. Content includes "Match Score" as a prominent `label-md` tag.