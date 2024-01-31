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
            <section v-if="notificatonSuccess" class="container success">
                <ui-button type="link" size="large" disabled icon="fa-solid fa-regular fa-circle-check"/>
                {{ notificatonSuccess.message }}
                <ui-button
                    v-if="notificatonSuccess && notificatonSuccess.action"
                    id="confirm"
                    @click="actionError"
                    type="secondary"
                    :text="notificatonSuccess.action.label"
                />
                <ui-button id="close" @click="notificatonSuccess = undefined" type="link" icon="fa-solid fa-xmark"/>
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
import type { ChefNotification } from '@/types';
import UiButton from './UiButton.vue';

import { useEventBus } from '@vueuse/core'
import { ref, type Ref } from 'vue';
// import { useNotifications } from "@/composables/notifications"

// const { notificaton } = useNotifications();
const notifications = ref([])

const notificatonInfo = ref<ChefNotification>()
const notificatonError = ref<ChefNotification>()
const notificatonSuccess = ref<ChefNotification>()

const bus = useEventBus<ChefNotification>("notifications")
bus.on((not: ChefNotification) => {
    console.info(not)
    if (not.level === 'ERROR') {
        notificatonError.value = not
    } else if (not.level === "INFO") {
        notificatonInfo.value = not
    } else if (not.level === "SUCCESS") {
        notificatonSuccess.value = not
    }
})

const actionError = (reference: Ref<ChefNotification | undefined>) => {
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

.success {
    background-color: var(--success);
    color: var(--text-inv);
}

#close {
    margin-left: auto;
}
</style>