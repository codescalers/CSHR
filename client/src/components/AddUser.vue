<template>
  <v-container>
    <v-form ref="form" @submit.prevent="addUser">
      <v-row class="justify-center align-center">
        <v-col cols="11">
          <v-text-field v-model="first_name" label="First Name" type="text" density="comfortable"
            :rules=[required]></v-text-field>
          <v-text-field v-model="last_name" label="Last Name" type="text" density="comfortable"
            :rules=[required]></v-text-field>
          <v-text-field v-model="email" label="Email" type="email" density="comfortable"
            :rules='emailRules'></v-text-field>
          <v-text-field v-model="password" label="Password" type="text" density="comfortable"
            :rules=[required]></v-text-field>
          <v-text-field v-model="mobile_number" label="Mobile Number" type="number" density="comfortable"
            :rules=[required]></v-text-field>
          <v-text-field v-model="job_title" label="Role" type="text" density="comfortable"
            :rules=[required]></v-text-field>

          <v-text-field v-model="address" label="Address" type="text" density="comfortable"
            :rules=[required]></v-text-field>
          <v-text-field v-model="social_insurance_number" label="Social Insurance Number" type="number"
            density="comfortable" :rules=[required]></v-text-field>
          <v-text-field v-model="telegram_link" label="Telegram" type="text" density="comfortable"
            :rules=[required]></v-text-field>

          <v-text-field v-model="birthday" label="Birthday" density="comfortable" :rules=[required]
            @click="toggleDatePicker('birthdayPicker')">
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>
          <v-date-picker v-model="birthdayDate" v-if="birthdayPicker" density="comfortable" :rules=[required]>
          </v-date-picker>

          <v-text-field v-model="joining_at" label="Joining Date" density="comfortable" :rules=[required]
            @click="toggleDatePicker('joiningDatePicker')">
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>
          <v-date-picker v-model="joiningDate" v-if="joiningDatePicker">
          </v-date-picker>

          <v-select v-model="selectedTeam" :items="teams" label="Team" density="comfortable" :rules=[required]></v-select>
          <v-select v-model="selectedGender" :items="genders" label="Gender" density="comfortable"
            :rules=[required]></v-select>
          <v-select v-model="user_type" :items="types" label="User Type" density="comfortable"
            :rules=[required]></v-select>
          <v-select v-model="location" :items="offices" item-title="name" item-value="id" label="Office" return-object
            single-line density="comfortable" :rules=[required]></v-select>

          <v-btn color="primary" type="submit" :disabled="!form?.isValid">Add User</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { $api } from '@/clients'
import type { Api } from '@/types'
import { emailRules, required } from '@/utils'
import moment from 'moment'


export default {
  name: 'AddUser',
  setup() {
    const form = ref()
    const teams = [
      'Business Development',
      'Development',
      'HR & Finance',
      'QA',
      'Marketing',
      'Operations',
      'Support'
    ]
    const types = [
      'Admin', 'User', 'Supervisor'
    ]
    const selectedTeam = ref<Api.Teams>(teams[0] as Api.Teams)
    const genders = ['Male', 'Female']
    const selectedGender = ref(genders[0] as Api.Gender)
    const first_name = ref('')
    const last_name = ref('')
    const telegram_link = ref('')
    const email = ref('')
    const birthdayDate = ref(new Date());
    const joiningDate = ref(new Date());
    const birthday = ref(new Date().toISOString().split('T')[0])
    const joining_at = ref(new Date().toISOString().split('T')[0])
    const mobile_number = ref('')
    const password = ref('')
    const offices = ref([]);
    const location = ref()
    const user_type = ref('User')
    const reporting_to = ref([])
    const job_title = ref('')
    const address = ref('')
    const social_insurance_number = ref('')

    const user = computed(() => ({
      first_name: first_name.value,
      last_name: last_name.value,
      telegram_link: telegram_link.value,
      email: email.value,
      birthday: birthday.value,
      joining_at: joining_at.value,
      mobile_number: mobile_number.value,
      password: password.value,
      location: location.value ? (location.value as any).id : 0,
      team: selectedTeam.value,
      user_type: user_type.value,
      reporting_to: [],
      gender: selectedGender.value,
      job_title: job_title.value,
      address: address.value,
      social_insurance_number: social_insurance_number.value
    }))

    onMounted(async () => {
      offices.value = (await $api.office.list()).map((office: any) => ({ id: office.id, name: office.name }));
      location.value = offices.value[0]
    })

    watch([birthdayDate, joiningDate], ([newBirthdayDate, newJoiningDate]) => {
      if (newBirthdayDate) birthday.value = formatDate(newBirthdayDate);
      if (newJoiningDate) joining_at.value = formatDate(newJoiningDate);
    });

    const birthdayPicker = ref(false);
    const joiningDatePicker = ref(false);
    const toggleDatePicker = (picker: string) => {
      if (picker === 'birthdayPicker') birthdayPicker.value = !birthdayPicker.value;
      else if (picker === 'joiningDatePicker') joiningDatePicker.value = !joiningDatePicker.value;
    };

    const formatDate = (date: any) => moment(date).format('YYYY-MM-DD');

    async function addUser() {
      await $api.auth.register(user.value as Api.Inputs.Register)
    }

    return {
      form,
      user,
      teams,
      selectedTeam,
      genders,
      selectedGender,
      types,
      first_name,
      last_name,
      telegram_link,
      email,
      birthday,
      joining_at,
      mobile_number,
      password,
      location,
      user_type,
      reporting_to,
      job_title,
      address,
      social_insurance_number,
      offices,
      birthdayPicker,
      joiningDatePicker,
      birthdayDate,
      joiningDate,
      toggleDatePicker,
      addUser,
      required,
      emailRules
    }
  }
}
</script>
