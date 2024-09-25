import type { PaginatedResponse, PaginationOptions, Request } from '@/types/api'
import { ofetch, type FetchContext } from 'ofetch'
import { useQuasar } from 'quasar'

export const useSmeltApi = () => {
  const $q = useQuasar()

  // Shared ofetch instance with a simple PoC error handling (with a notification pop-up)
  const smeltFetch = ofetch.create({
    baseURL: '/api',
    async onRequestError(context: FetchContext) {
      $q.notify({
        color: 'negative',
        icon: 'cloud_off',
        message: 'Network error'
      })
    },
    async onResponseError(context: FetchContext) {
      $q.notify({
        type: 'negative',
        message: context.error?.message ?? 'Something wrong happened, try again later...'
      })
    }
  })

  // Define generic types of request (common methods and return types)
  function paginatedGet<T>(path: string) {
    return async (options: PaginationOptions) => {
      const { page } = options
      return await smeltFetch<T>(`${path}?page=${page ?? 1}`)
    }
  }

  // ...

  // Define the api object, so that it can be easily stepped through
  const v1 = {
    overview: {
      released: {
        get: paginatedGet<PaginatedResponse<Request>>('/api/v1/overview/released')
      }
    }
  }

  return {
    v1
  }
}
