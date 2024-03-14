import { useDataCenterStore } from './dataCenter'
import { useComposeStore } from './compose'
import { useContextMenuStore } from './contextmenu'
import { useEditorStore } from './editor'
import { usePageStore } from './page'
import { useSnapShotStore } from './snapshot'
import { useCopyStore } from './copy'
import { useDataConfigStore } from './dataConfig'
import pinia from './index'

const dataCenter = useDataCenterStore(pinia)
const compose = useComposeStore(pinia)
const contextmenu = useContextMenuStore(pinia)
const editor = useEditorStore(pinia)
const page = usePageStore(pinia)
const snapshot = useSnapShotStore(pinia)
const copy = useCopyStore(pinia)
const dataConfig = useDataConfigStore(pinia)

export const rootStore = {
  useDataCenterStore,
  useComposeStore,
  useContextMenuStore,
  useEditorStore,
  usePageStore,
  useSnapShotStore,
  useCopyStore,
  useDataConfigStore,
  dataCenter,
  compose,
  contextmenu,
  editor,
  page,
  snapshot,
  copy,
  dataConfig
}
