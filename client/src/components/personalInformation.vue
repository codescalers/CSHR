<template>
  <v-card>
    <v-card-title class="font-weight-bold bg-primary">Public Information</v-card-title>
    <v-list class="custom-list">
      <v-row class="ma-1 bordered" v-for="header in mappedData" :key="header.key">
        <v-col cols="4" class="ma-0 pa-0">
          <v-list-item>
            <h4>{{ header.key }}</h4>
          </v-list-item>
        </v-col>
        <v-col cols="8" class="ma-0 pa-0">
          <v-list-item>
            {{ header.key === 'Location' ? country : getUserInfo(header.value) }}
          </v-list-item>
        </v-col>
      </v-row>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import { computed, ref } from 'vue'
import { onMounted } from 'vue'

export default {
  name: 'personalInformation',
  props: ['user'],

  setup(props) {
    const country = ref<string>()
    const profileInfoHeaders = [
      'Full Name',
      'Email',
      'Telegram',
      'Birthday',
      'Team',
      'Phone Number',
      'Social insurance number',
      'Address',
      'Joining date',
      'Location'
    ]

    const profileInfodata = [
      'full_name',
      'email',
      'telegram_link',
      'birthday',
      'team',
      'mobile_number',
      'social_insurance_number',
      'address',
      'joining_at'
    ]

    const mappedData = computed(() => {
      return profileInfoHeaders.map((header, index) => {
        return { key: header, value: profileInfodata[index] }
      })
    })
    const getUserInfo = (dataKey: any) => {
      if (props.user) {
        country.value = props.user.location.country
      }
      if (props.user && props.user[dataKey]) {
        return props.user[dataKey]
      }
      return '--'
    }

    return {
      country,
      mappedData,
      profileInfoHeaders,
      profileInfodata,
      getUserInfo
    }
  }
}
</script>

<style scoped>
.custom-list {
  overflow: hidden;
  font-size: 0.875rem;
}

.bordered {
  border-bottom: 0.1px solid #8a8a8a !important;
}
</style>
