<template>
    <div id="notification-drawer">
        <Transition>
            <section v-if="notificatonError" class="container error">
                <ui-button type="primary" size="large" disabled icon="fa-solid fa-circle-exclamation"/>
                {{ notificatonError.message }}
                <ui-button
                    v-if="notificatonError && notificatonError.action"
                    id="confirm"
                    @click="actionError"
                    type="secondary"
                    :text="notificatonError.action.label"
                />
                <ui-button id="close" @click="notificatonError = undefined" type="primary" icon="fa-solid fa-xmark"/>
            </section>
        </Transition>
        <Transition>
            <section v-if="notificatonInfo" class="container info">
                <ui-button type="secondary" disabled icon="fa-solid fa-warning"/>
                {{ notificatonInfo.message }}
                <ui-button id="close" @click="notificatonInfo = undefined" type="secondary" icon="fa-solid fa-xmark"/>
            </section>
        </Transition>
    </div>
</template>
<script lang="ts" setup>
import type { Notification } from '@/types';
import UiButton from './UiButton.vue';

import { useEventBus } from '@vueuse/core'
import { ref, type Ref } from 'vue';
// import { useNotifications } from "@/composables/notifications"

// const { notificaton } = useNotifications();
const notifications = ref([])

const notificatonInfo = ref<Notification>()
const notificatonError = ref<Notification>()
const notificatonSuccess = ref<Notification>()

const bus = useEventBus<Notification>("notifications")
bus.on((not: Notification) => {
    console.info(not)
    if (not.level === 'ERROR') {
        notificatonError.value = not
    } else if (not.level === "INFO") {
        notificatonInfo.value = not
    }
})

const actionError = (reference: Ref<Notification | undefined>) => {
    const busId = notificatonError.value?.action?.id
    console.info(`Trigger: ${busId}`)
    if (busId) {
        const responseBus = useEventBus<string>(busId)
        responseBus.emit(busId)
        notificatonError.value = undefined
    }
}


</script>
<style lang="css" scoped>
#notification-drawer {
    --w: min(96%, 1270px);

    position: fixed;
    width: 100%;
    bottom: 2rem;

}

section {
    padding: 1rem;

    border-radius: .2rem;
    box-shadow: 1px 1px 7px var(--text), 3px 3px 20px var(--text);

    width: var(--w);
    margin-inline: auto;

    -moz-box-sizing: border-box; 
    -webkit-box-sizing: border-box; 
     box-sizing: border-box;

     display: flex;
     flex-direction: row;
     align-items: center;
     gap: .5rem;
}

.info {
    background-color: var(--text-inv);
}

.error {
    background-color: var(--primary);
    color: var(--text-inv);
}

#close {
    margin-left: auto;
}
</style>