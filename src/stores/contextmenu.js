import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useContextMenuStore = defineStore('contextmenu', () => {
    const menuTop = ref(0)
    const menuLeft = ref(0)
    const menuShow = ref(false)
    const showContextMenu = ({ top, left }) => {
        menuShow.value = true
        menuTop.value = top
        menuLeft.value = left
    }

    const hideContextMenu = () => {
        menuShow.value = false
    }

    const setPosition = ({ top, left }) => {
        menuTop.value = top
        menuLeft.value = left
    }
    return {
        menuLeft,
        menuShow,
        menuTop,
        setPosition,
        showContextMenu,
        hideContextMenu,
    }
})
