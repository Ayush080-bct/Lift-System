import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App.tsx'

const root = createRoot(document.getElementById('root')!); 
// The ! is the non-null assertion operator.
// TypeScript normally thinks document.getElementById('root') might be null.
// Using ! tells TypeScript: "I am 100% sure this element exists, it’s not null."
// This way, TypeScript stops complaining and allows createRoot to use it safely.
//TypeScript = JavaScript + static typing + better tooling for large projects.
//TypeScript is a strongly-typed, 
// compiled superset of JavaScript that adds optional static types to the language.
root.render(
  <StrictMode>
    <App />
  </StrictMode>,
)
