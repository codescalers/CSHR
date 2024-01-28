<template>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="3" class="pa-2 border rounded ma-2 align-self-start">
        <div class="pa-5">
          <profileImage :user="user.state.value" />
          <div class=" text-center">
            <h5 clas=" text-h5 font-weight-bold ">
              {{ user.state.value?.full_name }}
            </h5>
            <span>Working for {{ user.state.value?.location?.country }} office</span>
          </div>
        </div>
      </v-col>
      <v-col cols="12" sm="12" md="8" class="pa-2 border rounded position-relative ma-2">
        <div>
          <personalInformation :user="user.state.value" />
          <vacationBalance :balance="balance.state.value" v-if="showBalance" />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import vacationBalance from '@/components/vacationBalance.vue'
import personalInformation from '@/components/personalInformation.vue'
import { $api } from '@/clients'
import { useRoute } from 'vue-router';
import { useAsyncState } from '@vueuse/core';
import profileImage from "@/components/profileImage.vue";
import { useState } from '@/store'

export default defineComponent({
  components: {
    vacationBalance,
    personalInformation,
    profileImage,
  },

  setup() {
    const $route = useRoute();
    const state = useState()
    const user = useAsyncState($route.query.id ? $api.users.getuser(Number($route.query.id)) : $api.myprofile.getUser(), [], {
      onSuccess(data) {
        balance.execute(undefined, data.id)
      }
    })

    const balance = useAsyncState(
      async (id: number) => {
        return $api.vacations.getVacationBalance({ "user_ids": id })
      },
      null,
      { immediate: false }
    )

    const showBalance = computed(() => {
      if (state.user.value) {
        if (user.state.value.id === state.user.value.value.id) {
          return true;
        }
        else if (state.user.value.value.user_type === 'Admin') {
          if (user.state.value.reporting_to) {
            if (user.state.value.reporting_to.includes(state.user.value.value.id)
              && user.state.value.location.name === state.user.value.value.location.name) {
              return true;
            }
          }
          return false
        }
      }
      return false
    });

    return {
      user,
      state,
      balance,
      showBalance,
      vacationBalance,
      personalInformation,
      profileImage,
    }
  }
})
</script>
