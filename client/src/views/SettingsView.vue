<template>
  <v-row no-gutters class="fill-height" align="center" justify="center">
    <v-col cols="5">
      <v-form ref="form" @submit.prevent="change(old_password, new_password)">
        <h1 class="text-center my-5">Change Password</h1>
        <v-row class="justify-center align-center">
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
            <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%"
              >submit</v-btn
            >
          </v-col>
        </v-row>
      </v-form>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import { $api } from '@/clients'
import { test_auth_api } from '@/tests/api/auth'
import { passwordRules } from '@/utils'
import { useStorage } from '@vueuse/core'

export default defineComponent({
  setup() {
    const form = ref()
    const old_password = ref<string>('')
    const new_password = ref<string>('')

    onMounted(async () => {
      const loggedUser = await test_auth_api();
      console.log({loggedUser})
    })
    async function change(old_password: string, new_password: string) {
      await $api.auth.changePassword({
        old_password,
        new_password
      })
      useStorage('user', {new_password}, localStorage, { mergeDefaults: true })
    }

    return {
      form,
      old_password,
      new_password,
      change,
      passwordRules,
    }
  }
})
</script>