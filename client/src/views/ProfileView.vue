<template>
  <p>This is Profile</p>
  <div>
    <v-row class="ma-5">
      <v-col cols="12" sm="12" md="3" class="pa-2 border rounded ma-2 align-self-start">
        <div class="pa-5">

          <v-avatar color="primary" size="50" class="d-flex mx-auto mt-5 mb-3">
            <span class="text-h5 text-uppercase">{{ name ? avatar : "?" }}</span>
          </v-avatar>
          <div class=" text-center">
            <h5 clas=" text-h5 font-weight-bold ">
              {{ name }}
            </h5>
            <span>Working for {{ office }} office</span>
          </div>

        </div>
      </v-col>
      <v-col cols="12" sm="12" md="8" class="pa-2 border rounded position-relative ma-2">
        <div>
          <v-card>
            <v-card-title class="font-weight-bold bg-primary">Public Information</v-card-title>
            <v-list class="custom-list">
              <v-row>
                <v-col cols="2 " class="column-style pa-0 ma-0">
                  <v-list-item v-for="header in profileInfoHeaders" :key="header">
                    {{ header }}
                  </v-list-item>
                </v-col>
                <v-col cols="10" class="column-style pa-0 ma-0">
                  <v-list-item> {{ name }}</v-list-item>
                  <v-list-item> </v-list-item>
                  <v-list-item>

                  </v-list-item>
                </v-col>
              </v-row>
            </v-list>
          </v-card>
          



<!-- 
          <v-card>
            <v-card-title class="font-weight-bold bg-primary">Vacation Balance</v-card-title>
            <v-row class=" text-center mt-2 mb-0">
              <v-col v-for="header in vacationInfoHeaders" :key="header">
               <h4> {{ header }}</h4> 
              </v-col>
            </v-row>
            <v-row class=" text-center mt-0 mb-2">
              <v-col>
                {{ name }} / {{ name }}
              </v-col>
              <v-col>
                {{ name }} / {{ name }}
              </v-col>
              <v-col>
                {{ name }} / {{ name }}
              </v-col>
            </v-row>
          </v-card> -->
          <!-- <v-card>
            <v-card-title class="font-weight-bold bg-primary">Vacation Balance</v-card-title>
            <v-list class="custom-list">
              <v-row>
                <v-col cols="2 " class="column-style pa-0 ma-0">
                  <v-list-item v-for="header in vacationInfoHeaders" :key="header">
                    {{ header }}
                  </v-list-item>
                </v-col>
                <v-col cols="10" class="column-style pa-0 ma-0">
                  <v-list-item> {{ name }}</v-list-item>
                  <v-list-item> </v-list-item>
                  <v-list-item>

                  </v-list-item>
                </v-col>
              </v-row>
            </v-list>
          </v-card> -->

        </div>

      </v-col>
    </v-row>
  </div>

  <div>
  <vacationBalance />
</div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import vacationBalance from "@/components/vacationBalance.vue"

export default defineComponent({
  setup() {

    const name = ref<string>('mayar osama')
    const office = ref<string>('Egypt')
    const profileInfoHeaders = ["Full Name", "Email", "Telegram", "Birthday", "Team", "Phone Number", "Social insurance numebr",
      "Address", "Joining date", "Location"];
      const vacationInfoHeaders = ["Annuals", "Emergencies", "Excuses"];
    const avatar = computed(() => {
      let val = String(name.value);
      return val.charAt(0);
    });
    return {
      name,
      avatar,
      office,
      profileInfoHeaders,
      vacationInfoHeaders,
      vacationBalance,
        }
  }
})


// export default {
//   name: "ProfileView",
//   setup() {
//   }
// }
</script>

<style scoped>
.custom-list {
  overflow: hidden;
  font-size: 0.875rem;
}

.v-list-item {
  border-bottom: 0.1px solid #8a8a8a;
}

/* .column-style {
  border-right: 0.1px solid #8a8a8a;
} */
/* .v-list-item:last-child {
  border-bottom: none;
} */
</style>