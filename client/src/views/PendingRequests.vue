<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3 ml-2">Pending Requests</h2>
      <v-divider></v-divider>
    </div>
    <v-card class="mb-4">
      <v-tabs
        v-model="tab"
        align-tabs="center"
        color="primary"
      >
        <v-tab :value="1">My Pending Requests</v-tab>
        <v-tab :value="2" v-if="isTeamlead">Team Pending Requests</v-tab>
        <!-- <v-tab :value="2">Team Pending Requests</v-tab> -->
      </v-tabs>

    </v-card>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item
        v-if="tab === 1"
      >
        <v-container fluid>
          <v-list lines="one" color="primary">
            <v-list-item
              class="mb-3"
              v-for="request in requests"
              :key="request"
              >
            <v-card variant="tonal" class="elevation-4 border bg-graytitle">
              <template #prepend>
                <profileImage
                  width="55px"
                  :with-link="false"
                  :user="request.applying_user"
                />
              </template>
              <template #title>
                  {{ request.applying_user.full_name }}
              </template>
              <template #subtitle>
                Applied for a vacation request from
                <strong>( {{ formatDateTime(request.from_date) }} )</strong>
                to
                <strong>( {{ formatDateTime(request.end_date) }} )</strong>
                <p>Reason: <strong>{{formatVacationReason(request.reason)}}</strong></p>
              </template>
              <v-row class="mt-4 d-flex justify-end align-center mb-4">
                <v-btn class="ml-1 mr-1" color="primary">Approve</v-btn>
                <v-btn class="ml-2 mr-8" color="error">Reject</v-btn>
              </v-row>
            </v-card>
          </v-list-item>
          </v-list>
        </v-container>
        <v-pagination :length="4"></v-pagination>
      </v-tabs-window-item>

      <v-tabs-window-item
        v-if="tab === 2"
      >
        <v-container fluid>
        </v-container>
        <v-pagination :length="4"></v-pagination>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients';
import { ApiClientBase } from '@/clients/api/base';
import type { Api } from '@/types';
import { useAsyncState } from '@vueuse/core';
import { computed, defineComponent, ref, } from 'vue';
import { formatDateTime, formatVacationReason } from '@/utils'
import profileImage from "@/components/profileImage.vue"


export default defineComponent({
  components: {profileImage,},
  setup() {
    const tab = ref(1);
    const user = ApiClientBase.user;
    const isTeamlead = computed(() => user.value?.fullUser.user_type.toLowerCase() === 'supervisor')
    const requests = ref<Api.Vacation>()
    // my-peneding-requests
    useAsyncState(
      $api.vacations.myPendingRequests(),
      undefined,
      {
        onSuccess(data) {
          requests.value = data;
          console.log({data})
          // requests.value = data?.results
          // setCount(data)
          // users.execute(undefined, data?.results || [])
        }
      }
    )

    return {
      tab,
      user,
      isTeamlead,
      requests,

      formatDateTime,
      formatVacationReason
    }
  },
})
</script>

<!-- <style>
.v-list-item--density-default:not(.v-list-item--nav).v-list-item--one-line {
  border-color: #2c2b2b !important;
  padding-right: 1px !important;
}
</style> -->