import { useStorage } from '@vueuse/core'
import { useQuasar } from 'quasar'

const isDark = useStorage('theme-dark', false)

export const useDarkmode = () => {
  // Toggle Quasar dark theme
  const $q = useQuasar()
  $q.dark.set(isDark.value)

  const toggle = () => {
    isDark.value = !isDark.value
    document.documentElement.setAttribute("data-theme", isDark.value ? 'dark' : 'light')
    $q.dark.set(isDark.value)
  }

  return {
    isDark,
    toggle
  }
}
