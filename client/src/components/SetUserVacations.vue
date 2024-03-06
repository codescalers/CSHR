<template>
  <v-container>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-text-field v-model="user!.fullUser.location.name" label="Office" type="text" :rules="requiredStringRules"
            disabled></v-text-field>
          <v-select v-model="selectedUser" :items="officeUsers" item-title="full_name" item-value="id" label="User"
            return-object density="comfortable" :rules="requiredRules">

            <template #append-item v-if="reloadMore">
              <VContainer>
                <VBtn @click="() => { return page++, count--, concatUsers() }" block color="secondary" variant="tonal"
                  prepend-icon="mdi-reload">
                  Load More Users
                </VBtn>
              </VContainer>
            </template>
          </v-select>
          <v-text-field v-model="vacation.annual_leaves" label="Annual Leaves" type="number"
            :rules="vacationRules"></v-text-field>
          <v-text-field v-model="vacation.leave_excuses" label="Leave Excuses" type="number"
            :rules="vacationRules"></v-text-field>
          <v-text-field v-model="vacation.emergency_leaves" label="Emergency Leaves" type="number"
            :rules="vacationRules"></v-text-field>
          <v-btn color="primary" type="submit" :disabled="!form?.isValid" :loading="isLoading" @click="execute">Set
            Vacations</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { listUsers, requiredRules, requiredStringRules, vacationRules } from '@/utils'
import { onMounted, ref, watchEffect, computed } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'

export default {
  name: 'SetUserVacations',
  setup() {
    const form = ref()
    const user = ApiClientBase.user
    const officeUsers = ref<any[]>([]);
    const selectedUser = ref()
    const userVacations = ref()
    const page = ref(1)
    const count = ref(0)
    const vacation = ref({
      annual_leaves: 0,
      leave_excuses: 0,
      emergency_leaves: 0
    })

    const reloadMore = computed(() => {
      if (page.value === count.value) {
        return false
      }
      if (count.value > 1) {
        return true
      }
      return false;
    });

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

    async function concatUsers() {
      const { page: currentPage, count: currentCount, users: newUsers } = await listUsers($api, page.value, count.value);

      page.value = currentPage;
      count.value = currentCount;
      officeUsers.value = officeUsers.value.concat(newUsers);
    }


    onMounted(async () => {
      try {
        await concatUsers()
        selectedUser.value = officeUsers.value[0]
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
      page,
      count,
      selectedUser,
      officeUsers,
      userVacations,
      vacation,
      requiredStringRules,
      requiredRules,
      vacationRules,
      isLoading,
      reloadMore,
      concatUsers,
      execute
    }
  }
}
</script>
