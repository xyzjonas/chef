// import axios from 'axios';
import { defineStore, acceptHMRUpdate } from 'pinia'
import { computed, ref } from 'vue';

import { API_URL } from '@/constants';

import type { Tag } from '@/types';
import { mande } from 'mande';
import { useLocalStorage } from '@vueuse/core';
import { useQuasar } from 'quasar';
import { catchError } from '@/utils';


const tagsApi = mande(API_URL + "/tags")

const all = useLocalStorage<Tag[]>("tags", [])

export const useTagStore = defineStore('tag', () => {

  const $q = useQuasar();
  const loading = ref<boolean>(false);

  const getById = computed(() => {
    return (tagId: number) => all.value.find(tag => tag.id === tagId);
  })

  function sortAll() {
    all.value = all.value.sort((a: Tag, b: Tag) => a.name > b.name ? 1 : -1);
  }

  async function fetch() {
    loading.value = true
    try {
      all.value = (await tagsApi.get<Tag[]>()).sort((a: Tag, b: Tag) => a.name > b.name ? 1 : -1);
    } catch (err: unknown) {
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function fetchSingle(tagId: number) {
    loading.value = true
    try {
      const newTag = await tagsApi.get<Tag>(tagId);
      all.value = all.value.map(tag => tag.id === newTag.id ? newTag : tag);
      return newTag;
    } catch (err: unknown) {
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function create(data: Omit<Tag, "id">): Promise<Tag> {
    loading.value = true
    let tag: Tag;
    try {
      tag = await tagsApi.post<Tag>(data);
    } catch (e: unknown) {
      catchError(e, $q);
      throw e;
    } finally {
      loading.value = false
    }

    all.value.push(tag);
    sortAll();
    return tag;
  }

  async function update(data: Tag): Promise<Tag> {
    loading.value = true
    let tag: Tag;
    try {
      tag = await tagsApi.put<Tag>(data.id, data);
    } catch (e: unknown) {
      catchError(e, $q);
      throw e;
    } finally {
      loading.value = false
    }

    all.value = all.value.map(t => t.id === tag.id ? tag : t);
    sortAll();
    return tag;
  }

  async function deleteById(tagId: number) {
    loading.value = true
    try {
      await tagsApi.delete(tagId);
      all.value = all.value.filter(t => t.id !== tagId);
    } catch (e: unknown) {
      catchError(e, $q);
      throw e;
    } finally {
      loading.value = false
    }
  }

  return { all, loading, getById, fetch, fetchSingle, create, update, deleteById }

})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useTagStore, import.meta.hot))
}
