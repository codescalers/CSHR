<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3 ml-2">Pending Requests</h2>
      <v-divider></v-divider>
    </div>
    <v-card class="mb-4">
      <v-tabs v-model="tab" align-tabs="center" color="primary">
        <v-tab :value="1">My Pending Requests</v-tab>
        <v-tab :value="2" v-if="isTeamlead || isAdmin">Team Pending Requests</v-tab>
      </v-tabs>
    </v-card>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item >
        <v-container fluid>
          <v-list lines="one" color="primary" v-if="requests?.length">
            <v-list-item class="mb-3" v-for="request in requests" :key="request">
              <v-card variant="tonal" class="elevation-4 border bg-graytitle">
                <template #prepend>
                  <profileImage width="55px" :with-link="false" :user="request.applying_user" />
                </template>
                <template #title>
                  {{ request.applying_user.full_name }}
                </template>
                <template #subtitle>
                  Applied for a vacation request from
                  <strong>( {{ formatDateTime(request.from_date) }} )</strong>
                  to
                  <strong>( {{ formatDateTime(request.end_date) }} )</strong>
                  <p>
                    Reason: <strong>{{ formatVacationReason(request.reason) }}</strong>
                  </p>
                </template>
                <div class="ma-5">
                  <ActionButtons :vacation="request" />
                </div>
              </v-card>
            </v-list-item>
          </v-list>
          <card v-else>
            <p class="text-center">No requests were found</p>
          </card>
        </v-container>
        <v-pagination v-if="requests?.length" v-model="page" :length="requestCount" rounded="circle"></v-pagination>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { ApiClientBase } from '@/clients/api/base'
import type { Api } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { computed, defineComponent, ref, watch } from 'vue'
import { formatDateTime, formatVacationReason } from '@/utils'
import profileImage from '@/components/profileImage.vue'
import ActionButtons from '@/components/requests/ActionButtons.vue'

export default defineComponent({
  components: { profileImage, ActionButtons },
  setup() {
    const tab = ref()
    const user = ApiClientBase.user
    const isTeamlead = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'supervisor')
    const isAdmin = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'admin')
    const requests = ref<Api.Vacation[]>()
    const requestMethod = ref()
    const requestCount = ref<number>()
    const page = ref(1)

    watch(
      [tab, page],
      () => {
        if (tab.value === 1) {
          requestMethod.value = $api.vacations.myPendingRequests({page: page.value})
        }

        if (tab.value === 2 && (isTeamlead.value === true || isAdmin.value === true)) {
          requestMethod.value = $api.vacations.myTeamPendingRequests({page: page.value})
        }

        useAsyncState(requestMethod.value, undefined, {
          onSuccess(data: {results: Api.Vacation[], count: number, next: string |  null, previous: string |  null} | undefined) {
            requests.value = data!.results
            requestCount.value = Math.ceil(data!.count / 3)
          }
        })
      },
      { deep: true }
    )

    return {
      tab,
      user,
      isTeamlead,
      requests,
      isAdmin,
      requestCount,
      page,

      formatDateTime,
      formatVacationReason
    }
  }
})
</script>
