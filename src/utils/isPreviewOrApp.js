const isPreview = () => {
  return window.location.hash.indexOf('preview') > -1 
}

const isSyslabApp = () => {
  return import.meta.env.VITE_NODE_ENV === 'SyslabApp'
}

const isWebApp = () => {
  return import.meta.env.VITE_NODE_ENV === 'WebApp'
}

const isQt = () => {
  return import.meta.env.VITE_NODE_ENV === 'qt'
}

const isUseVInteractPlot = () => {
  return false
}
export {
  isWebApp,
  isPreview,
  isSyslabApp,
  isUseVInteractPlot,
  isQt
}