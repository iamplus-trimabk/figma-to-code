/*
 * Design System Component Types
 * Generated from Stage 2: Design System Converter
 */

import React from 'react';

// ===========================================
// Base Component Interfaces
// ===========================================

// Base component props
export interface BaseComponentProps {
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
}

// Interactive component props
export interface InteractiveProps extends BaseComponentProps {
  interactive?: boolean;
  disabled?: boolean;
  onClick?: (event: React.MouseEvent) => void;
  onFocus?: (event: React.FocusEvent) => void;
  onBlur?: (event: React.FocusEvent) => void;
}

// Button component props
export interface ButtonProps extends InteractiveProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

// Text component props
export interface TextProps extends BaseComponentProps {
  as?: keyof React.ReactHTML;
  variant?: string;
  weight?: string;
  size?: string;
  color?: string;
  align?: 'left' | 'center' | 'right' | 'justify';
}

// Layout component props
export interface LayoutProps extends BaseComponentProps {
  display?: React.CSSProperties['display'];
  position?: React.CSSProperties['position'];
  overflow?: React.CSSProperties['overflow'];
  width?: string | number;
  height?: string | number;
  minWidth?: string | number;
  minHeight?: string | number;
  maxWidth?: string | number;
  maxHeight?: string | number;
}

// ===========================================
// Style Type Definitions
// ===========================================

// Colors Types

// Typography Types

// Spacing Types

// Effects Types

// ===========================================
// Utility Types
// ===========================================

export type ComponentSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type ComponentVariant = 'default' | 'primary' | 'secondary' | 'outline';
export type AnimationState = 'idle' | 'loading' | 'success' | 'error';
export type InteractionState = 'none' | 'hover' | 'focus' | 'active' | 'disabled';
export type ResponsiveValue = T | T[] | { sm?: T; md?: T; lg?: T; xl?: T };
export type Breakpoint = 'sm' | 'md' | 'lg' | 'xl' | '2xl';

// ===========================================
// Component Interfaces
// ===========================================

export interface Bg extends React.HTMLAttributes<HTMLElement> {
  /** bg - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Bg Variant Types
export type BgWidth = width: 788.0;
export type BgName = name: 'bg';
export type BgHeight = height: 940.0;
export type BgX = x: -8850.0;
export type BgCornerradius = cornerRadius: 8.0;
export type BgType = type: 'rectangle';
export type BgY = y: -6976.0;

export interface Angle extends React.HTMLAttributes<HTMLElement> {
  /** angle - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Angle Variant Types
export type AngleWidth = width: 681.0;
export type AngleName = name: 'Rectangle 2';
export type AngleHeight = height: 78.0;
export type AngleX = x: -8786.0;
export type AngleCornerradius = cornerRadius: 8.0;
export type AngleType = type: 'rectangle';
export type AngleY = y: -6781.0;

export interface Search extends React.HTMLAttributes<HTMLElement>, InteractiveProps {
  /** search - Interactive UI component with user interactions */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  interactive?: boolean;
  hover?: boolean;
  focus?: boolean;
  active?: boolean;
  onPress?: () => void;
  onHover?: (hovering: boolean) => void;
}

// Search Variant Types
export type SearchWidth = width: 32.0;
export type SearchName = name: 'search 1';
export type SearchHeight = height: 32.0;
export type SearchX = x: -8541.0;
export type SearchType = type: 'frame';
export type SearchY = y: -6756.0;

export interface ForgotPassword extends React.HTMLAttributes<HTMLElement>, InteractiveProps {
  /** forgot-password? - Interactive UI component with user interactions */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  fontFamily?: string;
  fontSize?: string | number;
  fontWeight?: string | number;
  text?: string;
  textAlign?: left | center | right | justify;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  interactive?: boolean;
  hover?: boolean;
  focus?: boolean;
  active?: boolean;
  onPress?: () => void;
  onHover?: (hovering: boolean) => void;
}

// ForgotPassword Variant Types
export type ForgotPasswordWidth = width: 141.0;
export type ForgotPasswordName = name: 'Forgot Password?';
export type ForgotPasswordHeight = height: 22.0;
export type ForgotPasswordText = text: 'Forgot Password?';
export type ForgotPasswordX = x: -8251.0;
export type ForgotPasswordFont_Family = font_family: 'Poppins';
export type ForgotPasswordFont_Size = font_size: 16.0;
export type ForgotPasswordFont_Weight = font_weight: 400;
export type ForgotPasswordText_Align = text_align: 'left';
export type ForgotPasswordType = type: 'text';
export type ForgotPasswordY = y: -6306.0;
export type ForgotPasswordLetter_Spacing = letter_spacing: 0;

export interface Email extends React.HTMLAttributes<HTMLElement>, InteractiveProps {
  /** email - Interactive UI component with user interactions */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  fontFamily?: string;
  fontSize?: string | number;
  fontWeight?: string | number;
  text?: string;
  textAlign?: left | center | right | justify;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  interactive?: boolean;
  hover?: boolean;
  focus?: boolean;
  active?: boolean;
  onPress?: () => void;
  onHover?: (hovering: boolean) => void;
}

// Email Variant Types
export type EmailWidth = width: 33.0;
export type EmailName = name: 'Email';
export type EmailHeight = height: 16.0;
export type EmailText = text: 'Email';
export type EmailX = x: -8694.0;
export type EmailFont_Family = font_family: 'Poppins';
export type EmailFont_Size = font_size: 12.0;
export type EmailFont_Weight = font_weight: 400;
export type EmailText_Align = text_align: 'left';
export type EmailType = type: 'text';
export type EmailY = y: -6489.0;
export type EmailLetter_Spacing = letter_spacing: 0;

export interface Angle4 extends React.HTMLAttributes<HTMLElement> {
  /** angle-4 - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Angle4 Variant Types
export type Angle4Width = width: 671.0;
export type Angle4Name = name: 'Rectangle 4';
export type Angle4Height = height: 77.0;
export type Angle4X = x: -8776.0;
export type Angle4Cornerradius = cornerRadius: 8.0;
export type Angle4Type = type: 'rectangle';
export type Angle4Y = y: -6504.0;

export interface Password extends React.HTMLAttributes<HTMLElement>, InteractiveProps {
  /** password - Interactive UI component with user interactions */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  fontFamily?: string;
  fontSize?: string | number;
  fontWeight?: string | number;
  text?: string;
  textAlign?: left | center | right | justify;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  interactive?: boolean;
  hover?: boolean;
  focus?: boolean;
  active?: boolean;
  onPress?: () => void;
  onHover?: (hovering: boolean) => void;
}

// Password Variant Types
export type PasswordWidth = width: 58.0;
export type PasswordName = name: 'Password';
export type PasswordHeight = height: 16.0;
export type PasswordText = text: 'Password';
export type PasswordX = x: -8694.0;
export type PasswordFont_Family = font_family: 'Poppins';
export type PasswordFont_Size = font_size: 12.0;
export type PasswordFont_Weight = font_weight: 400;
export type PasswordText_Align = text_align: 'left';
export type PasswordType = type: 'text';
export type PasswordY = y: -6392.0;
export type PasswordLetter_Spacing = letter_spacing: 0;

export interface Angle5 extends React.HTMLAttributes<HTMLElement> {
  /** angle-5 - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Angle5 Variant Types
export type Angle5Width = width: 671.0;
export type Angle5Name = name: 'Rectangle 5';
export type Angle5Height = height: 77.0;
export type Angle5X = x: -8776.0;
export type Angle5Cornerradius = cornerRadius: 8.0;
export type Angle5Type = type: 'rectangle';
export type Angle5Y = y: -6407.0;

export interface Button extends React.HTMLAttributes<HTMLElement>, ButtonProps {
  /** button - Interactive UI component with user interactions */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  variant?: primary | secondary | outline | ghost;
  size?: sm | md | lg;
  disabled?: boolean;
  loading?: boolean;
  onClick?: (event: React.MouseEvent) => void;
  type?: 'button' | 'submit' | 'reset';
}

// Button Variant Types
export type ButtonWidth = width: 671.0;
export type ButtonName = name: 'button';
export type ButtonHeight = height: 77.0;
export type ButtonX = x: -8776.0;
export type ButtonCornerradius = cornerRadius: 8.0;
export type ButtonType = type: 'group';
export type ButtonY = y: -6260.0;

export interface Angle6 extends React.HTMLAttributes<HTMLElement> {
  /** angle-6 - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Angle6 Variant Types
export type Angle6Width = width: 671.0;
export type Angle6Name = name: 'Rectangle 6';
export type Angle6Height = height: 77.0;
export type Angle6X = x: -8776.0;
export type Angle6Cornerradius = cornerRadius: 8.0;
export type Angle6Type = type: 'rectangle';
export type Angle6Y = y: -6260.0;

export interface RememberMe extends React.HTMLAttributes<HTMLElement> {
  /** remember-me - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// RememberMe Variant Types
export type RememberMeWidth = width: 153.0;
export type RememberMeName = name: 'Remember me';
export type RememberMeHeight = height: 22.0;
export type RememberMeX = x: -8774.0;
export type RememberMeCornerradius = cornerRadius: 4.0;
export type RememberMeType = type: 'group';
export type RememberMeY = y: -6306.0;

export interface Check extends React.HTMLAttributes<HTMLElement> {
  /** check - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderColor?: string;
  borderWidth?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Check Variant Types
export type CheckWidth = width: 18.0;
export type CheckName = name: 'check';
export type CheckHeight = height: 18.0;
export type CheckX = x: -8774.0;
export type CheckCornerradius = cornerRadius: 4.0;
export type CheckType = type: 'rectangle';
export type CheckY = y: -6304.0;

export interface Angle7 extends React.HTMLAttributes<HTMLElement> {
  /** angle-7 - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  borderColor?: string;
  borderWidth?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Angle7 Variant Types
export type Angle7Width = width: 958.0;
export type Angle7Name = name: 'Rectangle 7';
export type Angle7Height = height: 524.0;
export type Angle7X = x: -9600.0;
export type Angle7Cornerradius = cornerRadius: 25.0;
export type Angle7Type = type: 'rectangle';
export type Angle7Y = y: -8088.0;

export interface Login extends React.HTMLAttributes<HTMLElement> {
  /** login - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  borderRadius?: string | number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Login Variant Types
export type LoginWidth = width: 934.0;
export type LoginName = name: 'Login 1';
export type LoginHeight = height: 498.0;
export type LoginX = x: -9587.0;
export type LoginCornerradius = cornerRadius: 22.0;
export type LoginType = type: 'rectangle';
export type LoginY = y: -8075.0;

export interface Image extends React.HTMLAttributes<HTMLElement> {
  /** image - Visual component for displaying content */
  width?: string | number;
  height?: string | number;
  position?: { x?: number; y?: number };
  backgroundColor?: string;
  backgroundOpacity?: number;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  id?: string;
  testId?: string;
  display?: block | inline | inline-block | flex | grid | none;
  overflow?: visible | hidden | scroll | auto;
  opacity?: number;
}

// Image Variant Types
export type ImageWidth = width: 50.0;
export type ImageName = name: 'image 1';
export type ImageHeight = height: 75.0;
export type ImageX = x: -9864.0;
export type ImageType = type: 'rectangle';
export type ImageY = y: -7633.0;
