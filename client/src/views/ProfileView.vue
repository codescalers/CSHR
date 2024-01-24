<template>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="3" class="pa-2 border rounded ma-2 align-self-start">
        <div class="pa-5">
          <profileImage :image="user.state.value?.image" :fullName="user.state.value?.full_name"/>
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
          <vacationBalance :balance="balance.state.value" />
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
import { onMounted } from 'vue'
import type { Api } from '@/types'
import { useRoute } from 'vue-router';
import { useAsyncState } from '@vueuse/core';
import profileImage from "@/components/profileImage.vue";
export default defineComponent({
  components: {
    vacationBalance,
    personalInformation,
    profileImage,
  },

  setup() {
    const $route = useRoute();
    const user = useAsyncState($route.query.id ? $api.users.getuser(Number($route.query.id)) : $api.myprofile.getUser(), [], {
      onSuccess(data) {
        console.log(data.id);
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


    return {
      user,
      balance,
      vacationBalance,
      personalInformation,
      profileImage,
    }
  }
})
</script>
