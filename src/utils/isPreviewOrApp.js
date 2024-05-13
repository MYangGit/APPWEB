const isPreviewOrApp = () => {
  return window.location.hash.indexOf('preview') > -1 || import.meta.env.VITE_NODE_ENV === 'SyslabApp'
}
export default isPreviewOrApp