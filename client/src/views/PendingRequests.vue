<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3 ml-2">Pending Requests</h2>
      <v-divider></v-divider>
      <v-select
        class="mt-4"
        label="Request Status"
        v-model="selectedStatus"
        :items="requestStatus"
      ></v-select>
      <v-divider></v-divider>
    </div>
    <v-card class="pb-4">
      <v-tabs v-model="tab" align-tabs="center" color="primary">
        <v-tab :value="1">My Pending Requests</v-tab>
        <v-tab :value="2" v-if="isTeamlead || isAdmin">Team Pending Requests</v-tab>
      </v-tabs>
    </v-card>
    <v-container fluid>
      <div class="d-flex justify-end" v-if="tab === 2">
        <v-btn 
          variant="outlined"
          color="primary"
          class="mr-3 btn"
          :disabled="!pendingRequests.length"
          @click="approveAll"
        >
          Approve all
        </v-btn>
        <v-btn 
          variant="outlined"
          color="error"
          class="btn"
          :disabled="!pendingRequests.length"
          @click="rejectAll"
        >
          Reject all
        </v-btn>
      </div>

      <template v-if="loading">
        <div class="d-flex justify-center align-center" style="height: 150px;">
          <VProgressCircular indeterminate color="primary" />
        </div>
      </template>

      <div v-if="!loading" class="mb-5 mt-5">
        <v-row>
          <v-col xl="4" lg="6" md="12" sm="12" cols="12" v-for="request in pendingRequests" :key="request.id">
            <v-card variant="tonal" class="elevation-4 border bg-graytitle">
              <template #prepend>
                <profileImage width="55px" :with-link="false" :user="request.applying_user" />
              </template>
              <template #title>
                {{ request.applying_user.full_name }}
                <v-chip :color="getStatusColor(request.status)">{{
                  formatRequestStatus(request.status)
                }}</v-chip>
              </template>
              <template #subtitle>
                <div class="mt-2">
                  Vacation request from
                  <strong>{{ formatDateString(request.from_date) }}</strong>
                  -
                  <strong>{{ formatDateString(request.end_date) }}</strong>
                  <p>
                    Reason: <strong>{{ formatVacationReason(request.reason) }}</strong>
                  </p>
                </div>
              </template>
              <div class="ma-5">
                <ActionButtons :vacation="request" />
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>
      <card v-if="!loading && !pendingRequests.length">
        <p class="text-center">No requests were found</p>
      </card>
      <v-pagination
        v-if="pendingRequests.length"
        v-model="page"
        :length="count"
        rounded="circle"
        class="mt-5"
      ></v-pagination>
    </v-container>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import type { Api } from '@/types'
import { ApiClientBase } from '@/clients/api/base'
import { useAsyncState } from '@vueuse/core'
import { computed, defineComponent, ref, watch } from 'vue'
import { formatDateString, formatRequestStatus, formatVacationReason, getStatusColor } from '@/utils'
import profileImage from '@/components/profileImage.vue'
import ActionButtons from '@/components/requests/ActionButtons.vue'

type RequestStatusSelection = {
  title: string
  value: Api.RequestStatus | 'all'
}

export default defineComponent({
  components: { profileImage, ActionButtons },
  setup() {
    const tab = ref(1)
    const user = ApiClientBase.user
    const isTeamlead = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'supervisor')
    const isAdmin = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'admin')
    const page = ref(1)
    const count = computed(() => (state.value ? Math.ceil(state.value!.count / 10) : 0))
    const requestStatus = ref<RequestStatusSelection[]>([
      { title: 'All', value: 'all' },
      { title: formatRequestStatus('pending'), value: 'pending' },
      { title: formatRequestStatus('requested_to_cancel'), value: 'requested_to_cancel' }
    ])
    const pendingRequests = ref<Api.Vacation[]>([]);

    const selectedStatus = ref(requestStatus.value[0].value)

    const { execute, state, isLoading } = useAsyncState(
      () => {
        if (tab.value === 1) {
          return $api.vacations.myPendingRequests({
            page: page.value,
            status: selectedStatus.value
          })
        }
        return $api.vacations.myTeamPendingRequests({
          page: page.value,
          status: selectedStatus.value
        })
      },
      undefined,
      {
        immediate: true
      }
    )

    watch([tab, selectedStatus], () => (page.value = 1))
    watch([tab, page, selectedStatus], async () => {
      await execute()
      pendingRequests.value = state.value?.results as Api.Vacation[]
    })

    const changeStateTask = useAsyncState((action: "approve" | "reject") => {
      const requests = state.value?.results.map((req) => req.id) || []
      return $api.vacations.approveOrRejectAllTeamPendingRequets({
        action,
        ids: requests
      })
      }, undefined,
      {
        immediate: false
      }
    )

    const loading = computed( () => changeStateTask.isLoading.value || isLoading.value)

    const approveAll = async () => {
      await changeStateTask.execute(undefined, 'approve')
      pendingRequests.value = changeStateTask.state.value?.results as Api.Vacation[]
    }

    const rejectAll = async () => {
      await changeStateTask.execute(undefined, 'reject')
      pendingRequests.value = changeStateTask.state.value?.results as Api.Vacation[]
    }

    return {
      tab,
      user,
      isTeamlead,
      isAdmin,
      page,
      pendingRequests,
      loading,
      count,
      selectedStatus,
      requestStatus,

      formatDateString,
      formatVacationReason,
      formatRequestStatus,
      getStatusColor,
      approveAll,
      rejectAll,
    }
  }
})
</script>

<style>
.btn{
  text-transform: capitalize !important;
  border-radius: 6px;
}
</style>
