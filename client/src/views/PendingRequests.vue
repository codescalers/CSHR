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
      <v-container fluid>
        <template v-if="isLoading">
          <div class="d-flex justify-center">
            <VProgressCircular indeterminate color="primary"/>
          </div>
        </template>
        <v-list lines="one" color="primary" v-else>
          <v-list-item class="mb-3" v-for="request in state?.results" :key="request.id">
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
        <card v-if="!isLoading && !state?.results?.length">
          <p class="text-center">No requests were found</p>
        </card>
        <v-pagination v-if="state?.results?.length" v-model="page" :length="count" rounded="circle"></v-pagination>
      </v-container>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { ApiClientBase } from '@/clients/api/base'
import { useAsyncState } from '@vueuse/core'
import { computed, defineComponent, ref, watch } from 'vue'
import { formatDateTime, formatVacationReason } from '@/utils'
import profileImage from '@/components/profileImage.vue'
import ActionButtons from '@/components/requests/ActionButtons.vue'

export default defineComponent({
  components: { profileImage, ActionButtons },
  setup() {
    const tab = ref(1)
    const user = ApiClientBase.user
    const isTeamlead = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'supervisor')
    const isAdmin = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'admin')
    const page = ref(1)
    const count = computed(() => state.value ? Math.ceil(state.value!.count / 3) : 0)

    const { execute, state, isLoading } = useAsyncState(() => {
      if (tab.value === 1) {
        return $api.vacations.myPendingRequests({page: page.value})
      }
      return $api.vacations.myTeamPendingRequests({page: page.value})
    }, undefined, {
      immediate: true,
    })

    watch([tab, page], () => execute())

    return {
      tab,
      user,
      isTeamlead,
      isAdmin,
      page,
      state,
      isLoading,
      count,

      formatDateTime,
      formatVacationReason
    }
  }
})
</script>
