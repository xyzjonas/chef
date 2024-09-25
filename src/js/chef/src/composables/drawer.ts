import { useLocalStorage } from '@vueuse/core'

const isOpened = useLocalStorage('drawer-state', true)

export const useLayoutDrawer = () => {
  const toggle = () => (isOpened.value = !isOpened.value)

  return {
    toggle,
    isOpened
  }
}
