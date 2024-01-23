<template>
  <v-form ref="form" @submit.prevent>
    <v-row class="justify-center align-center">
      <v-col cols="7">
        <h1 class="mt-10">Change Password</h1>
      </v-col>
      <v-col cols="7">
        <v-text-field
          v-model="old_password"
          :rules="passwordRules"
          type="text"
          label="Old Password"
        ></v-text-field>
      </v-col>

      <v-col cols="7">
        <v-text-field
          v-model="new_password"
          :rules="passwordRules"
          type="text"
          label="New Password"
        ></v-text-field>
      </v-col>

      <v-col cols="7">
        <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%" :loading='isLoading' @click="execute">submit</v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { $api } from '@/clients'
import { passwordRules } from '@/utils'
import { useAsyncState } from '@vueuse/core'

export default defineComponent({
  setup() {
    const form = ref()
    const old_password = ref<string>('')
    const new_password = ref<string>('')

    const {execute, isLoading} = useAsyncState(async() => {
      await $api.auth.changePassword({
        old_password: old_password.value,
        new_password: new_password.value
      })
    }, null, {immediate: false})

    return {
      form,
      old_password,
      new_password,
      passwordRules,
      isLoading,
      execute
    }
  }
})
</script>
