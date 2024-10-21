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
          :disabled="!couldApproveAll"
          @click="approveAll"
        >
          Approve all
        </v-btn>
        <v-btn 
          variant="outlined"
          color="error"
          class="btn"
          :disabled="!couldApproveAll"
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
          <v-col xl="4" :lg="pendingRequests.length > 1 ? 6 : 12" md="12" sm="12" cols="12" v-for="request in pendingRequests" :key="request.id">
            <v-card class="border bg-graytitle">
              <template #prepend>
                <profileImage width="55px" :with-link="false" :user="request.applying_user" />
              </template>
              <template #title>
                <span style="font-size: 16px;">{{ request.applying_user.full_name }}</span>
                <v-chip class="ml-2" :color="getStatusColor(request.status)">{{
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
                <ActionButtons :vacation="request" @update:vacation="($event) => request.status = $event.status"/>
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
    const requestStatus = ref<RequestStatusSelection[]>([
      { title: 'All', value: 'all' },
      { title: formatRequestStatus('pending'), value: 'pending' },
      { title: formatRequestStatus('requested_to_cancel'), value: 'requested_to_cancel' }
    ])

    const pendingRequests = ref<Api.Vacation[]>([]);
    const selectedStatus = ref(requestStatus.value[0].value)

    const pendingRequestsTask = useAsyncState(
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
        immediate: false
      }
    )

    watch([tab, selectedStatus], () => (page.value = 1))
    watch([tab, page, selectedStatus], async () => {
      await pendingRequestsTask.execute()
      pendingRequests.value = pendingRequestsTask.state.value?.results as Api.Vacation[]
    }, {immediate: true})
    
    const changeStateTask = useAsyncState((action: "approve" | "reject") => {
      return $api.vacations.approveOrRejectAllTeamPendingRequets({
        action,
      })
    }, undefined,
      {
        immediate: false
      }
    )
    
    const couldApproveAll = computed(() => pendingRequests.value!.filter((req) => req.status === "pending" || req.status === "requested_to_cancel").length)
    const loading = computed( () => changeStateTask.isLoading.value || pendingRequestsTask.isLoading.value)
    const count = computed(() => (pendingRequestsTask.state.value ? Math.ceil(pendingRequestsTask.state.value!.count / 10) : 0))
    const approveAll = async () => {
      const STATUS = 'approve'
      await changeStateTask.execute(undefined, STATUS)

      const result = pendingRequests.value.map(r => ({
        [r.applying_user.id.toFixed()]: r.id.toFixed()
      }))

      pendingRequests.value = changeStateTask.state.value?.results as Api.Vacation[]
      
      window.connections.ws.value!.send(
        JSON.stringify({
          event: 'approve_or_reject_all_pending_requests',
          data: result,
          status: STATUS,
        })
      )
    }


    const rejectAll = async () => {
      const STATUS = 'reject'
      await changeStateTask.execute(undefined, STATUS)
      const result = pendingRequests.value.map(r => ({
        [r.applying_user.id.toFixed()]: r.id.toFixed()
      }))

      pendingRequests.value = changeStateTask.state.value?.results as Api.Vacation[]

      window.connections.ws.value!.send(
        JSON.stringify({
          event: 'approve_or_reject_all_pending_requests',
          data: result,
          status: STATUS,
        })
      )
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
      couldApproveAll,

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
