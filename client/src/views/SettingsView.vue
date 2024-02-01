<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-6">Change Password</h2>
      <v-divider></v-divider>
    </div>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-text-field
            v-model="old_password"
            :append-inner-icon="show_old ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="passwordRules"
            :type="show_old ? 'text' : 'password'"
            label="Old Password"
            @click:append-inner="show_old = !show_old"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-text-field
            v-model="new_password"
            :append-inner-icon="show_new ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[...passwordRules, confirmPassword]"
            :type="show_new ? 'text' : 'password'"
            label="New Password"
            @click:append-inner="show_new = !show_new"
            @input="validateForm"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-text-field
            v-model="confirm_password"
            :append-inner-icon="show_confirm ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[...passwordRules, confirmPassword]"
            :type="show_confirm ? 'text' : 'password'"
            label="Confirm Password"
            @click:append-inner="show_confirm = !show_confirm"
            @input="validateForm"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-btn
            color="primary"
            type="submit"
            :disabled="!form?.isValid"
            width="100%"
            :loading="isLoading"
            @click="execute"
            >submit</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { $api } from '@/clients'
import { passwordRules } from '@/utils'
import { useAsyncState } from '@vueuse/core'

export default defineComponent({
  setup() {
    const form = ref()
    const show_old = ref<boolean>(false)
    const show_new = ref<boolean>(false)
    const show_confirm = ref<boolean>(false)
    const old_password = ref<string>('')
    const new_password = ref<string>('')
    const confirm_password = ref<string>('')

    const { execute, isLoading } = useAsyncState(
      async () => {
        await $api.auth.changePassword({
          old_password: old_password.value,
          new_password: new_password.value
        })
      },
      null,
      { immediate: false }
    )

    const confirmPassword = () => new_password.value == confirm_password.value || "Passwords should match."

    const validateForm = () => {
      form.value?.validate()
    }

    return {
      form,
      show_old,
      show_new,
      old_password,
      new_password,
      show_confirm,
      confirm_password,
      passwordRules,
      isLoading,
      execute,
      confirmPassword,
      validateForm
    }
  }
})
</script>
