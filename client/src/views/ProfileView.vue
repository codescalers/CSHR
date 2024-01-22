<template>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="3" class="pa-2 border rounded ma-2 align-self-start">
        <div class="pa-5">
          <v-avatar color="primary" size="50" class="d-flex mx-auto mt-5 mb-3">
            <span class="text-h5 text-uppercase">{{ user?.full_name ? avatar : "?" }}</span>
          </v-avatar>
          <div class=" text-center">
            <h5 clas=" text-h5 font-weight-bold ">
              {{ user?.full_name }}
            </h5>
            <span>Working for {{ user?.location.country }} office</span>
          </div>

        </div>
      </v-col>
      <v-col cols="12" sm="12" md="8" class="pa-2 border rounded position-relative ma-2">
        <div>
          <personalInformation :user="user" />
          <vacationBalance :balance="balance"/>
        </div>

      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import vacationBalance from "@/components/vacationBalance.vue";
import personalInformation from "@/components/personalInformation.vue";
import { $api } from '@/clients';
import { onMounted } from 'vue';
import type { Api } from '@/types'
import { useRoute } from 'vue-router';
export default defineComponent({
  components: {
    vacationBalance,
    personalInformation,
  },

  setup() {
    const user = ref<Api.User>();
    const balance = ref<Api.BalanceVacation>();
    const $route = useRoute();

    const avatar = computed(() => {
      if (user.value) {
        let val = String(user.value.full_name);
        return val.charAt(0);
      }
      return "??";
    });

    async function getProfile() {
      if ($route.query.id) {
        user.value = await $api.users.getuser(Number($route.query.id));
      } else {
        user.value = await $api.myprofile.getUser();

      }
    }

    async function getUserBalance() {
      balance.value = await $api.vacations.getVacationBalance({ "user_ids": user.value?.id });

    }

    onMounted(async () => {
      await getProfile();
      await getUserBalance();

    })

    return {
      avatar,
      user,
      balance,
      vacationBalance,
      personalInformation,
    }
  }
})

</script>