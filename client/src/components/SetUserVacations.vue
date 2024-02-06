<template>
  <v-container>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-text-field
            v-model="user!.fullUser.location.name"
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
          >
          <template #append-item v-if="next !== null">
              <VContainer>
                <VBtn
                  @click="() => {return page++, listUsers()}"
                  block
                  color="secondary"
                  variant="tonal"
                  prepend-icon="mdi-reload"
                >
                  Load More Users
                </VBtn>
              </VContainer>
            </template>
          </v-select>
          <v-text-field
            v-model="vacation.annual_leaves"
            label="Annual Leaves"
            type="number"
            :rules="vacationRules"
          ></v-text-field>
          <v-text-field
            v-model="vacation.leave_excuses"
            label="Leave Excuses"
            type="number"
            :rules="vacationRules"
          ></v-text-field>
          <v-text-field
            v-model="vacation.emergency_leaves"
            label="Emergency Leaves"
            type="number"
            :rules="vacationRules"
          ></v-text-field>
          <v-btn
            color="primary"
            type="submit"
            :disabled="!form?.isValid"
            :loading="isLoading"
            @click="execute"
            >Set Vacations</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { requiredRules, requiredStringRules, vacationRules } from '@/utils'
import { onMounted, ref, watchEffect } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'

export default {
  name: 'SetUserVacations',
  setup() {
    const form = ref()
    const user = ApiClientBase.user
    const officeUsers = ref()
    const users = ref([])
    const selectedUser = ref()
    const userVacations = ref()
    const page = ref(1)
    const next = ref(null)
    const vacation = ref({
      annual_leaves: 0,
      leave_excuses: 0,
      emergency_leaves: 0
    })

    watchEffect(async () => {
      try {
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
      } catch (error) {
        console.error(error)
      }
    })

    async function listUsers(){
      const res = await $api.users.admin.office_users.list({page: page.value})
      next.value = res.next
      return res.results
    }

    onMounted(async () => {
      try {   
        officeUsers.value = await listUsers()
        users.value = officeUsers.value?.map((user: any) => ({ id: user.id, name: user.full_name }))
        selectedUser.value = users.value[0]
      } catch (error) {
        console.error(error)
      }
    })

    const { execute, isLoading } = useAsyncState(
      async () => {
        await $api.vacations.balance.update({ user_ids: selectedUser.value.id }, vacation.value)
      },
      null,
      { immediate: false }
    )

    return {
      form,
      user,
      users,
      page,
      next,
      selectedUser,
      officeUsers,
      userVacations,
      vacation,
      requiredStringRules,
      requiredRules,
      vacationRules,
      isLoading,
      listUsers,
      execute
    }
  }
}
</script>
