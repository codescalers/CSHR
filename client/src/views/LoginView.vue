<template>
  <v-container fluid class="pa-0">
    <v-row align="center" justify="center">
      <v-col cols="12" md="7">
        <v-card height="100vh" style="background-color: black">
          <v-img :src="background" height="65%" cover />
          <div class="pa-2 pa-md-10 mx-auto">
            <v-card-title class="text-h6 text-md-h5 font-weight-bold">
              CSHR (Codescalers HR Management System)
            </v-card-title>

            <v-card-text>
              A versatile management system with vacation request submissions and seamless
              integration with a global calendar. Users across offices can collectively view
              approved Vacations, Birthdates, Events, Meetings, and Holidays, providing a
              centralized overview for the entire organization.
            </v-card-text>
            <v-card-subtitle class="text-white"> Powered by CodeScalers Egypt. </v-card-subtitle>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="5">
        <v-form v-model="valid" @submit.prevent>
          <v-img :src="logo" max-width="140" class="mx-auto justify-center"></v-img>
          <h2 class="text-center my-5">Sign In</h2>
          <v-row class="justify-center align-center">
            <v-col cols="7">
              <v-text-field v-model="email" label="Email" :rules="emailRules"></v-text-field>
            </v-col>

            <v-col cols="7">
              <v-text-field
                v-model="password"
                :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="passwordRules"
                :type="show ? 'text' : 'password'"
                label="Password"
                @click:append-inner="show = !show"
              ></v-text-field>
            </v-col>

            <v-col cols="7" class="d-flex justify-content-between align-center pa-0">
              <v-checkbox v-model="rememberMe" label="Remember me"></v-checkbox>
            </v-col>

            <v-col cols="7">
              <v-btn
                color="primary"
                type="submit"
                :disabled="!valid"
                width="100%"
                :loading="isLoading"
                @click="execute"
              >
                Login
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import background from '@/assets/login.png'
import logo from '@/assets/cshr_logo.png'
import { $api } from '@/clients'
import { emailRules, passwordRules } from '@/utils'
import { useRouter } from 'vue-router'
import { useAsyncState } from '@vueuse/core'

export default defineComponent({
  setup() {
    const valid = ref(false)
    const email = ref<string>('')
    const password = ref<string>('')
    const show = ref<boolean>(false)
    const rememberMe = ref<boolean>(false)
    const router = useRouter()

    const { isLoading, execute } = useAsyncState(
      () => {
        console.log('here??')

        return $api.auth.login({ email: email.value, password: password.value })
      },
      null,
      {
        immediate: false,
        onSuccess: () => router.push('/')
      }
    )

    return {
      valid,
      email,
      password,
      rememberMe,
      show,
      emailRules,
      passwordRules,
      background,
      logo,
      isLoading,
      execute
    }
  }
})
</script>
<style scoped>
:deep(.v-card-title) {
  white-space: unset;
}
:deep(.v-card-text) {
  font-size: 1.125rem;
  line-height: 1.75rem;
}
</style>
