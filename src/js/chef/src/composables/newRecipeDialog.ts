import { ref } from 'vue'

const isOpened = ref(false)

export const useNewRecipeDialog = () => {
  const open = () => (isOpened.value = true)
  const close = () => (isOpened.value = false)

  return {
    isOpened,
    open,
    close,
  }
}
