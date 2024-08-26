<template>
  <v-card class="pa-4">
    <div class="my-2">
      <v-row class="mb-0">
        <v-col class="d-flex justify-start mb-0">
          <v-card-title class="font-weight-bold mb-0"> {{ $props.modelValue.title }} </v-card-title>
        </v-col>
        <v-col class="d-flex justify-end mb-0 align-center">
          <v-chip :color="getStatusColor(requestStatus!)">
            {{ formatRequestStatus(requestStatus!) }}
          </v-chip>
        </v-col>
      </v-row>
      <v-card-text class="mt-0 pt-0">
        <p>
          {{ $props.modelValue.body }}
        </p>
      </v-card-text>
    </div>
    
    <v-row no-gutters class="mx-3">
      <v-col v-for="section in sections" :key="section.key" cols="12">
        <v-card class="mb-6 elevation-12">
          <v-card-title class="card-title bg-primary white--text">{{ section.title }}</v-card-title>

          <v-list class="custom-list">
            <v-row
              v-for="detail in section.details"
              :key="detail.label"
              class="ma-1 bordered"
              no-gutters
            >
              <v-col cols="3">
                <v-list-item>
                  <v-list-item-content class="ma-0">
                    {{ detail.label }}
                  </v-list-item-content>
                </v-list-item>
              </v-col>

              <v-col cols="9">
                <v-list-item>
                  <v-list-item-content>
                    {{ detail.value }}
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

      <v-row class="d-flex justify-end mt-3 mb-3 mr-4">
        <ActionButtons 
          :vacation="vacation"
          :display-close-btn="true"
          @update:close-dialog="closeDialog"
          @update:vacation="$emit('update:vacation', $event)"
        />
      </v-row>
  </v-card>
</template>

<script lang="ts">
import { computed, type PropType } from 'vue'
import type { Api, notificationType } from '@/types'
import { ApiClientBase } from '@/clients/api/base'
import ActionButtons from "@/components/requests/ActionButtons.vue"
import { formatRequestStatus, getStatusColor } from '@/utils';

export default {
  components: { ActionButtons },
  name: 'NotificationDetails',
  emits: ["update:vacation"],
  props: {
    modelValue: {
      type: Object as PropType<notificationType>,
      required: true
    },
    sections: {
      type: Array as PropType<any[]>,
      required: true
    },
    requestStatus: {
      type: Object as PropType<Api.RequestStatus>,
      required: false
    },
    vacation: {
      type: Object as PropType<notificationType["request"]>,
      required: false
    },
    onClose: {
      type: Function as PropType<() => void>,
      required: true
    }
  },
  setup(props) {
    const user = ApiClientBase.user

    const closeDialog = () => {
      props.onClose()
    }

    const couldApprove = computed(() => {
      if( user.value?.id && props.modelValue.request.approvals.includes(user.value?.id)){
        return true
      }
      return false
    })

    return {
      couldApprove,
      closeDialog,
      formatRequestStatus,
      getStatusColor,
    }
  }
}
</script>

<style scoped>
.card-title {
  font-size: 1rem !important;
  line-height: 1.5rem !important;
}
</style>
