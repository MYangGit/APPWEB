const isPreview = () => {
  return window.location.hash.indexOf('preview') > -1 
}

const isSyslabApp = () => {
  return import.meta.env.VITE_NODE_ENV === 'SyslabApp'
}
export {
  isPreview,
  isSyslabApp
}