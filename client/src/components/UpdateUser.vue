<template>
  <v-container>
    <v-form ref="form" @submit.prevent="updateUser">
      <v-row class="justify-center align-center">
        <v-col cols='12'>
          <v-select
            v-model="selectedUser"
            :items="officeUsers"
            label="User"
            item-title="full_name"
            item-value="id"
            return-object
            density="comfortable"
            :rules="requiredRules"
          ></v-select>
        </v-col>
        <v-col cols="6" v-if="selectedUser">
          <v-text-field
            v-model="selectedUser.first_name"
            label="First Name"
            density="comfortable"
            :rules="nameRules"
          ></v-text-field>
          <v-text-field
            v-model="selectedUser.last_name"
            label="Last Name"
            density="comfortable"
            :rules="nameRules"
          ></v-text-field>
          <v-text-field
            v-model="selectedUser.email"
            label="Email"
            type="email"
            density="comfortable"
            :rules="emailRules"
          ></v-text-field>
          <v-text-field
            v-model="selectedUser.password"
            label="Password"
            density="comfortable"
            :rules="passwordRules"
          ></v-text-field>
          <v-text-field
            v-model="selectedUser.mobile_number"
            label="Mobile Number"
            type="number"
            density="comfortable"
            :rules="mobileRules"
          ></v-text-field>
          <v-text-field
            v-model="selectedUser.job_title"
            label="Role"
            density="comfortable"
            :rules="jobRules"
          ></v-text-field>

          <v-text-field
            v-model="selectedUser.address"
            label="Address"
            density="comfortable"
            :rules="addressRules"
          ></v-text-field>
          <v-text-field
            v-model="selectedUser.social_insurance_number"
            label="Social Insurance Number"
            type="number"
            density="comfortable"
            :rules="socialInsuranceRules"
          ></v-text-field>
        </v-col>
        <v-col cols='6' v-if="selectedUser">
          <v-text-field
            v-model="selectedUser.telegram_link"
            label="Telegram"
            density="comfortable"
            :rules="telegramRules"
          ></v-text-field>

          <v-text-field
            v-model="selectedUser.birthday"
            label="Birthday"
            density="comfortable"
            :rules="requiredStringRules"
            @click="toggleDatePicker('birthdayPicker')"
            readonly
          >
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>
          <v-date-picker
            v-model="birthdayDate"
            v-if="birthdayPicker"
            density="comfortable"
            :rules="requiredStringRules"
          >
          </v-date-picker>

          <v-text-field
            v-model="selectedUser.joining_at"
            label="Joining Date"
            density="comfortable"
            :rules="requiredStringRules"
            @click="toggleDatePicker('joiningDatePicker')"
            readonly
          >
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>
          <v-date-picker v-model="joiningDate" v-if="joiningDatePicker"> </v-date-picker>

          <v-select
            v-model="selectedUser.team"
            :items="teams"
            label="Team"
            density="comfortable"
            :rules="requiredStringRules"
          ></v-select>
          <v-select
            v-model="selectedUser.gender"
            :items="genders"
            label="Gender"
            density="comfortable"
            :rules="requiredStringRules"
          ></v-select>
          <v-select
            v-model="selectedUser.user_type"
            :items="types"
            label="User Type"
            density="comfortable"
            :rules="requiredStringRules"
          ></v-select>
          <v-select
            v-model="selectedUser.location"
            :items="offices"
            label="Office"
            item-title="name"
            item-value="id"
            return-object
            density="comfortable"
            :rules="requiredRules"
          ></v-select>

          <v-select
            v-model="selectedUser.reporting_to"
            :items="supervisors"
            item-title="name"
            item-value="id"
            label="Supervisors"
            return-object
            density="comfortable"
            multiple
          ></v-select>

        </v-col>
        <v-col cols='12'>
          <v-file-input
            :v-model="image"
            label="Image"
            variant="filled"
            accept="image/*"
            :show-size="1024"
            prepend-icon="mdi-camera"
            @input="chooseImage"
            density="comfortable"
          ></v-file-input>
          <v-img
            v-if="image && image.length > 0 && imageUrl"
            :src="imageUrl"
            width="200"
            height="200"
            class="justify-center mb-5"
          ></v-img>
          <v-btn color="primary" type="submit" :disabled="!form?.isValid">Update User</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { onMounted, ref, watch } from 'vue'
import { $api } from '@/clients'
import {
  nameRules,
  emailRules,
  passwordRules,
  mobileRules,
  jobRules,
  addressRules,
  socialInsuranceRules,
  telegramRules,
  requiredStringRules,
  requiredRules
} from '@/utils'
import moment from 'moment'

export default {
  name: 'UpdateUser',
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
    const types = ['Admin', 'User', 'Supervisor']
    const genders = ['Male', 'Female']
    const birthdayDate = ref(new Date())
    const joiningDate = ref(new Date())
    const birthday = ref(new Date().toISOString().split('T')[0])
    const joining_at = ref(new Date().toISOString().split('T')[0])
    const offices = ref([])
    const supervisors = ref([])
    const image = ref()
    const imageUrl = ref()
    const officeUsers = ref([])
    const selectedUser = ref()

    onMounted(async () => {
      offices.value = (await $api.office.list()).map((office: any) => ({
        id: office.id,
        name: office.name
      }))
      supervisors.value = ((await $api.users.team.supervisors.list()) as any).map(
        (supervisor: any) => ({ id: supervisor.id, name: supervisor.name }) ?? []
      )

      officeUsers.value = await $api.users.admin.office_users.list()
      selectedUser.value = officeUsers.value[0]
    })

    watch([birthdayDate, joiningDate], ([newBirthdayDate, newJoiningDate]) => {
      if (newBirthdayDate) birthday.value = formatDate(newBirthdayDate)
      if (newJoiningDate) joining_at.value = formatDate(newJoiningDate)
    })

    const birthdayPicker = ref(false)
    const joiningDatePicker = ref(false)
    const toggleDatePicker = (picker: string) => {
      if (picker === 'birthdayPicker') birthdayPicker.value = !birthdayPicker.value
      else if (picker === 'joiningDatePicker') joiningDatePicker.value = !joiningDatePicker.value
    }

    const formatDate = (date: any) => moment(date).format('YYYY-MM-DD')

    async function updateUser() {
      await $api.myprofile.update(selectedUser.value.id, selectedUser.value)
    }

    function chooseImage(event: any) {
      let input = event.target
      if (input && input.files) {
        let reader = new FileReader()
        reader.onload = (e: any) => {
          imageUrl.value = e.target.result
        }
        reader.readAsDataURL(input.files[0])
      }
    }

    return {
      form,
      teams,
      genders,
      types,
      offices,
      birthdayPicker,
      joiningDatePicker,
      birthdayDate,
      joiningDate,
      image,
      imageUrl,
      supervisors,
      officeUsers,
      selectedUser,
      nameRules,
      emailRules,
      passwordRules,
      mobileRules,
      jobRules,
      addressRules,
      socialInsuranceRules,
      telegramRules,
      requiredStringRules,
      requiredRules,
      toggleDatePicker,
      updateUser,
      chooseImage
    }
  }
}
</script>

<style scoped>
.v-picker.v-sheet{
  position: absolute !important;
  z-index: 1000 !important;
}
</style>
