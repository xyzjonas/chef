import type { Category, Ingredient, Recipe, Tag, Unit } from '@/types'
import { ofetch, type FetchContext } from 'ofetch'
import { useQuasar } from 'quasar'

type QueryArgs = {[key: string]: any}

export const useChefApi = () => {
  const $q = useQuasar()

  // Shared ofetch instance with a simple PoC error handling (with a notification pop-up)
  const chefFetch = ofetch.create({
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
  function getOne<T>(path: string) {
    return async (id: number | string) => {
      return await chefFetch<T>(`${path}/${id}`)
    }
  }

  function getList<T>(path: string) {
    return async (query?: QueryArgs) => {
      let p = path
      if (query && Object.keys(query).length > 0) {
        p += "?"
        for(const [k, v] of Object.entries(query)) {
          p += `${k}=${v}`
        }
      }

      return await chefFetch<T[]>(p)
    }
  }

  const api = {
    recipes: {
      get: getList<Recipe>("recipes"),
      getOne: getOne<Recipe>("recipes")
    },
    categories: {
      get: getList<Category>("categories")
    },
    ingredients: {
      get: getList<Ingredient>("ingredients")
    },
    tags: {
      get: getList<Tag>("tags")
    },
    units: {
      get: getList<Unit>("units")
    }
  }

  return {
    api
  }
}
