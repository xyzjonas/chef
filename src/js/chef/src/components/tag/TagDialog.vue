<template>
  <q-dialog v-model="isOpened" @hide="onHide" position="bottom">
    <q-card class="w-[26rem] px-1 py-3">
      <q-form @submit="doSave">
        <q-card-section>
          <h3 class="my-0 mb-1">{{ isEditing ? "Edit tag" : "Create a new tag" }}</h3>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            outlined
            autofocus
            v-model="name"
            label="Name"
            autocomplete="off"
            :rules="[(val: string) => !!val || 'Name is required']"
          />
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="text-caption text-gray-6 mb-1">Icon</div>
          <IconPicker v-model="icon" />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            v-if="isEditing"
            flat
            label="Delete"
            color="negative"
            class="mr-auto"
            @click="doDelete"
            :loading="deleting"
          />
          <q-btn flat label="Cancel" color="secondary" @click="close" />
          <q-btn
            unelevated
            :label="isEditing ? 'Save' : 'Create'"
            color="primary"
            type="submit"
            :loading="loading"
          />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import IconPicker from "@/components/ui/IconPicker.vue";
import { useTagDialog } from "@/composables/tagDialog";
import { useTagStore } from "@/stores/tags";
import { computed, ref, watch } from "vue";

const { isOpened, editingTag, close } = useTagDialog();
const tagStore = useTagStore();

const name = ref("");
const icon = ref<string | null>();
const loading = ref(false);
const deleting = ref(false);

const isEditing = computed(() => !!editingTag.value?.id);

watch(isOpened, (opened) => {
  if (opened) {
    name.value = editingTag.value?.name ?? "";
    icon.value = editingTag.value?.icon ?? null;
  }
});

const doSave = async () => {
  loading.value = true;
  try {
    if (isEditing.value && editingTag.value?.id) {
      await tagStore.update({
        id: editingTag.value.id,
        name: name.value,
        icon: icon.value,
      });
    } else {
      await tagStore.create({ name: name.value, icon: icon.value });
    }
    close();
  } finally {
    loading.value = false;
  }
};

const doDelete = async () => {
  if (!editingTag.value?.id) {
    return;
  }
  deleting.value = true;
  try {
    await tagStore.deleteById(editingTag.value.id);
    close();
  } finally {
    deleting.value = false;
  }
};

const onHide = () => {
  name.value = "";
  icon.value = null;
};
</script>
