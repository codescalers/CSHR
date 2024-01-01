export const GLOBAL_COMPONENT = {
  // Add global components here
  // -->
  // -->
  /* Not as const is important to infer type  */
} as const

export type GlobalComps = typeof GLOBAL_COMPONENT

export interface GlobalProps {
  $globals: import('@/hooks').$Globals
  $metaEnv: ImportMetaEnv
}
