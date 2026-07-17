# design.md

# Design System

> This document defines the visual language for the AI-Powered Fashion
> Discovery Browser Extension. It ensures a consistent, modern, and
> accessible experience across all UI surfaces.

------------------------------------------------------------------------

# Design Principles

-   Minimal and distraction-free.
-   Fashion-first, allowing product imagery to take center stage.
-   Fast to scan with clear visual hierarchy.
-   Accessible with sufficient color contrast.
-   Consistent spacing, typography, and component styling.

------------------------------------------------------------------------

# Theme

## Primary Theme

A clean, premium light theme should be the default.

### Light Theme

-   Background: #FAFAFA
-   Surface: #FFFFFF
-   Surface Secondary: #F5F5F5
-   Border: #E5E7EB
-   Primary Text: #111827
-   Secondary Text: #6B7280

### Dark Theme

-   Background: #111827
-   Surface: #1F2937
-   Surface Secondary: #374151
-   Border: #4B5563
-   Primary Text: #F9FAFB
-   Secondary Text: #D1D5DB

Users should be able to switch between Light, Dark, and System themes.

------------------------------------------------------------------------

# Color Palette

## Primary

-   Indigo: #4F46E5

## Secondary

-   Slate: #64748B

## Success

-   Green: #22C55E

## Warning

-   Amber: #F59E0B

## Error

-   Red: #EF4444

## Info

-   Sky Blue: #0EA5E9

Accent colors should be used sparingly for actions and highlights.
Product images should remain the primary visual focus.

------------------------------------------------------------------------

# Typography

## Font Family

Use **Inter** as the primary font.

Reasons: - Excellent readability. - Modern appearance. - Optimized for
UI. - Widely supported. - Performs well at small sizes.

Fallback stack:

Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
sans-serif

------------------------------------------------------------------------

# Font Scale

  Usage              Size   Weight
  ---------------- ------ --------
  Hero               32px      700
  Page Title         24px      700
  Section Title      20px      600
  Card Title         18px      600
  Body               16px      400
  Secondary Text     14px      400
  Caption            12px      400
  Button             14px      600

Line height: - Headings: 1.2 - Body: 1.5

------------------------------------------------------------------------

# Spacing

Use an 8px spacing system.

-   XS: 4px
-   SM: 8px
-   MD: 16px
-   LG: 24px
-   XL: 32px
-   XXL: 48px

------------------------------------------------------------------------

# Border Radius

-   Buttons: 10px
-   Cards: 12px
-   Dialogs: 16px
-   Chips: 9999px (pill)

------------------------------------------------------------------------

# Elevation

Keep shadows subtle.

-   Cards: Small shadow
-   Dialogs: Medium shadow
-   Popup: Medium shadow

Avoid heavy shadows.

------------------------------------------------------------------------

# Buttons

Primary: - Filled with primary color. - White text.

Secondary: - Neutral background. - Primary text.

Tertiary: - Text only.

Danger: - Red background for destructive actions.

------------------------------------------------------------------------

# Icons

-   Use Lucide icons.
-   20--24px default size.
-   Consistent stroke width.

------------------------------------------------------------------------

# Components

Cards: - Product image first. - Product title. - Brand. - Price. -
Call-to-action button.

Inputs: - Rounded corners. - Clear focus state. - Visible labels.

Badges: - Small, subtle. - Used for tags like "New", "Sale", "Trending".

------------------------------------------------------------------------

# Motion

Animations should be quick and unobtrusive.

-   Duration: 150--250ms
-   Use fade, scale, and slide transitions.
-   Avoid excessive animation.

------------------------------------------------------------------------

# Accessibility

-   Meet WCAG AA contrast where practical.
-   Keyboard accessible.
-   Visible focus indicators.
-   Don't rely on color alone to convey meaning.

------------------------------------------------------------------------

# Responsive Design

The extension popup should remain usable at common extension popup
sizes.

Prioritize: - Compact layouts. - Readable typography. - Minimal
scrolling.

------------------------------------------------------------------------

# Design Consistency Rules

-   Use the defined color palette only.
-   Do not introduce arbitrary colors.
-   Use Inter everywhere.
-   Follow the typography scale.
-   Keep component spacing consistent.
-   Prefer simplicity over visual complexity.
-   Let product imagery be the hero of the interface.
