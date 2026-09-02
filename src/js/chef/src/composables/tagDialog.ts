import { ref } from 'vue'
import type { Tag } from '@/types'

const isOpened = ref(false)
const editingTag = ref<Tag | null>(null)

export const useTagDialog = () => {
  const open = (tag?: Tag) => {
    editingTag.value = tag ?? null
    isOpened.value = true
  }
  const close = () => (isOpened.value = false)

  return {
    isOpened,
    editingTag,
    open,
    close,
  }
}
