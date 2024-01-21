<template>
  <v-row no-gutters class="fill-height" align="center" justify="center">
    <v-col cols="7">
      <v-card
        class="fill-hight pa-16"
        :image="background"
        height="100vh"
        title="CSHR (Codescalers HR Management System)"
        subtitle="A versatile management system with vacation request submissions and seamless integration with a global calendar. Users across offices can collectively view approved vacations, Birthdates, Events, Meetings, and Holidays, providing a centralized overview for the entire organization."
      ></v-card>
    </v-col>
    <v-col cols="5">
      <v-form ref="form" @submit.prevent="login(email, password)">
        <v-img :src="logo" max-width="200" class="mx-auto justify-center"></v-img>
        <h1 class="text-center my-5">Sign In</h1>
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
            <!-- <v-btn color="primary" class="mb-6" variant='plain' style="text-transform: none !important;">Forgot password?</v-btn> -->
          </v-col>

          <v-col cols="7">
            <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%">
              Login
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import background from '@/assets/login.png'
import logo from '@/assets/cshr_logo.png'
import { $api } from '@/clients'
import { emailRules, passwordRules } from '@/utils'
import { useRouter } from 'vue-router'
import { useState } from '../store'

export default defineComponent({
  setup() {
    const form = ref()
    const email = ref<string>('')
    const password = ref<string>('')
    const show = ref<boolean>(false)
    const rememberMe = ref<boolean>(false)
    const $router = useRouter()
    const state = useState();

    async function login(email: string, password: string) {
      await $api.auth.login(
        {
          email,
          password
        },
        rememberMe.value
      )
      const user = await $api.myprofile.getUser();
      state.user.value = user;
      state.rememberMe.value = rememberMe.value;
      $router.push('/')
    }

    return {
      form,
      email,
      password,
      rememberMe,
      show,
      login,
      emailRules,
      passwordRules,
      background,
      logo
    }
  }
})
</script>
<style scoped>
:deep(.v-card-title) {
  margin-top: 20% !important;
  font-weight: bold !important;
  font-size: 1.5rem !important;
}

:deep(.v-card-subtitle) {
  margin-top: 1rem !important;
  font-size: 1rem !important;
  white-space: inherit !important;
  opacity: 1 !important;
}
</style>
