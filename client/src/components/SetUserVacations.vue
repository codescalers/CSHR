<template>
  <v-container>
    <v-form ref="form" @submit.prevent="updateVacations">
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-text-field
            v-model="state.user.value.location.name"
            label="Office"
            type="text"
            :rules="requiredStringRules"
            disabled
          ></v-text-field>
          <v-select
            v-model="selectedUser"
            :items="users"
            item-title="name"
            item-value="id"
            label="User"
            return-object
            :rules="requiredRules"
          ></v-select>
          <v-text-field
            v-model="vacation.annual_leaves"
            label="Annual Leaves"
            type="number"
            :rules="requiredRules"
          ></v-text-field>
          <v-text-field
            v-model="vacation.leave_excuses"
            label="Leave Excuses"
            type="number"
            :rules="requiredRules"
          ></v-text-field>
          <v-text-field
            v-model="vacation.emergency_leaves"
            label="Emergency Leaves"
            type="number"
            :rules="requiredRules"
          ></v-text-field>
          <v-btn color="primary" type="submit" :disabled="!form?.isValid">Set Vacations</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { useState } from '@/store'
import { requiredRules, requiredStringRules } from '@/utils'
import { onMounted, ref, watchEffect } from 'vue'

export default {
  name: 'SetUserVacations',
  setup() {
    const form = ref()
    const state = useState()
    const officeUsers = ref()
    const users = ref([])
    const selectedUser = ref()
    const userVacations = ref()
    const vacation = ref({
      annual_leaves: 0,
      leave_excuses: 0,
      emergency_leaves: 0
    })

    watchEffect(async () => {
      if (selectedUser.value) {
        const result = await $api.vacations.balance.list({
          user_ids: selectedUser.value.id
        })
        userVacations.value = result ? result[0] : null
        if (userVacations.value) {
          const { annual_leaves, leave_excuses, emergency_leaves } = userVacations.value
          vacation.value.annual_leaves = annual_leaves.all
          vacation.value.leave_excuses = leave_excuses.all
          vacation.value.emergency_leaves = emergency_leaves.all
        }
      }
    })

    onMounted(async () => {
      officeUsers.value = await $api.users.admin.office_users.list()
      users.value = officeUsers.value?.map((user: any) => ({ id: user.id, name: user.full_name }))
      selectedUser.value = users.value[0]
    })

    async function updateVacations() {
      await $api.vacations.balance.update({ user_ids: selectedUser.value.id }, vacation.value)
    }

    return {
      form,
      state,
      users,
      selectedUser,
      officeUsers,
      userVacations,
      vacation,
      requiredStringRules,
      requiredRules,
      updateVacations
    }
  }
}
</script>
