<template>
  <v-container>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-alert
            class="mb-3"
            type="info"
            :text="`Please note that this value will be applied to the ${selectedReason.text} balance for all users. If you accidentally submit this form, you'll need to reset the value for users using the appropriate form.`"
          ></v-alert>
          <v-text-field
            v-model="user!.fullUser.location.name"
            label="Office"
            type="text"
            disabled
          ></v-text-field>
          <v-select
            v-model="selectedReason"
            :items="reasons"
            item-title="text"
            item-value="id"
            label="Day/s"
            return-object
            single-line
          ></v-select>
          <v-text-field
            v-model="vacation.value"
            label="Vacation Type"
            type="text"
            :rules="requiredStringRules"
          ></v-text-field>
          <v-btn
            color="primary"
            type="submit"
            :disabled="!form?.isValid"
            :loading="isLoading"
            @click="execute"
            >Update Vacations</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { ref } from 'vue'
import { requiredStringRules } from '@/utils'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'

export default {
  name: 'UpdateOfficeVacations',
  setup() {
    const form = ref()
    const user = ApiClientBase.user
    const reasons = ref([
      {
        id: 1,
        value: 'annual_leaves',
        text: 'Annual Leaves'
      },
      {
        id: 2,
        value: 'leave_excuses',
        text: 'Leave Excuses'
      },
      {
        id: 3,
        value: 'emergency_leaves',
        text: 'Emergency Leaves'
      }
    ])
    const selectedReason = ref(reasons.value[0])

    const vacation = ref({
      officeId: user.value?.fullUser.location.id as any,
      value: 1,
      reason: selectedReason.value.value
    })

    const { execute, isLoading } = useAsyncState(
      async () => {
        await $api.vacations.balance.adjustment.update(vacation.value)
      },
      null,
      { immediate: false }
    )

    return {
      form,
      vacation,
      reasons,
      selectedReason,
      user,
      requiredStringRules,
      isLoading,
      execute
    }
  }
}
</script>
