import { useDataCenterStore } from './dataCenter'
import { useComposeStore } from './compose'
import { useContextMenuStore } from './contextmenu'
import { useEditorStore } from './editor'
import { usePageStore } from './page'
import { useSnapShotStore } from './snapshot'
import pinia from './index'

const dataCenter = useDataCenterStore(pinia)
const compose = useComposeStore(pinia)
const contextmenu = useContextMenuStore(pinia)
const editor = useEditorStore(pinia)
const page = usePageStore(pinia)
const snapshot = useSnapShotStore(pinia)

export const rootStore = {
  useDataCenterStore,
  useComposeStore,
  useContextMenuStore,
  useEditorStore,
  usePageStore,
  useSnapShotStore,
  dataCenter,
  compose,
  contextmenu,
  editor,
  page,
  snapshot,
}
