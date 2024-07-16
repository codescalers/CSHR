<template>
  <v-container>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="6">
          <v-text-field
            v-model="first_name"
            label="First Name"
            density="comfortable"
            :rules="nameRules"
          ></v-text-field>
          <v-text-field
            v-model="last_name"
            label="Last Name"
            density="comfortable"
            :rules="nameRules"
          ></v-text-field>
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            density="comfortable"
            :rules="emailRules"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            density="comfortable"
            :rules="passwordRules"
          ></v-text-field>
          <v-text-field
            v-model="mobile_number"
            label="Mobile Number"
            type="number"
            density="comfortable"
            :rules="mobileRules"
          ></v-text-field>
          <v-text-field
            v-model="job_title"
            label="Role"
            density="comfortable"
            :rules="jobRules"
          ></v-text-field>

          <v-text-field
            v-model="address"
            label="Address"
            density="comfortable"
            :rules="addressRules"
          ></v-text-field>
          <v-text-field
            v-model="social_insurance_number"
            label="Social Insurance Number"
            type="number"
            density="comfortable"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="telegram_link"
            label="Telegram"
            density="comfortable"
            :rules="requiredRules"
          ></v-text-field>

          <v-text-field
            v-model="birthday"
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
            v-model="joining_at"
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
            v-model="selectedTeam"
            :items="teams"
            label="Team"
            density="comfortable"
            :rules="requiredStringRules"
            clearable
          ></v-select>
          <v-select
            v-model="selectedGender"
            :items="genders"
            label="Gender"
            density="comfortable"
            :rules="requiredStringRules"
            clearable
          ></v-select>
          <v-select
            v-model="user_type"
            :items="types"
            label="User Type"
            density="comfortable"
            :rules="requiredStringRules"
          ></v-select>
          <v-select
            v-model="location"
            :items="offices"
            label="Office"
            item-title="name"
            item-value="id"
            return-object
            density="comfortable"
            :rules="requiredRules"
          ></v-select>

          <v-select
            v-model="selectedSupervisor"
            :items="supervisors"
            item-title="full_name"
            item-value="id"
            label="Team Lead"
            return-object
            density="comfortable"
            clearable
          >
            <template #append-item v-if="reloadMoreSupervisor">
              <VContainer>
                <VBtn
                  @click="
                    () => {
                      return supervisorPage++, supervisorCount--, listSupervisors()
                    }
                  "
                  block
                  color="secondary"
                  variant="tonal"
                  prepend-icon="mdi-reload"
                >
                  Load More Team Leads
                </VBtn>
              </VContainer>
            </template>
          </v-select>
        </v-col>
        <v-col cols="12">
          <v-alert>
            <v-switch
              v-model="isSetBalance"
              label="Would you like to set the user's vacation balance?"
              hide-details
              color="primary"
              inset
            ></v-switch>
            <v-divider class="mb-4" />
            <v-expansion-panels v-model="setBalance" class="pa-4">
              <v-expansion-panel class="pa-4">
                <v-expansion-panel-title>
                  <v-row no-gutters>
                    <v-col class="d-flex justify-start align-center" cols="4">
                      <h4>User Balance</h4>
                    </v-col>
                    <v-col
                      class="text--secondary"
                      cols="8"
                    >
                      <v-fade-transition leave-absolute>
                        <v-row
                          style="width: 100%"
                          no-gutters
                        >
                          <v-col class="d-flex justify-start align-center" cols="4">
                            Annual:
                            <v-chip class="ml-2" variant="tonal" color="primary">
                              {{ annualBalance ? annualBalance > 1 ? `${annualBalance} Days` : `${annualBalance} Day` : '0 Day'}}
                            </v-chip>
                          </v-col>
                          <v-col class="d-flex justify-start align-center" cols="4">
                            Emergency:
                            <v-chip class="ml-2" variant="tonal" color="primary">
                              {{ emergencyBalance ? emergencyBalance > 1 ? `${emergencyBalance} Days` : `${emergencyBalance} Day` : '0 Day'}}
                            </v-chip>
                          </v-col>
                          <v-col class="d-flex justify-start align-center" cols="4">
                            Excuses:
                            <v-chip class="ml-2" variant="tonal" color="primary">
                              {{ excusesBalance ? excusesBalance > 1 ? `${excusesBalance} Days` : `${excusesBalance} Day` : '0 Day'}}
                            </v-chip>
                          </v-col>
                        </v-row>
                      </v-fade-transition>
                    </v-col>
                  </v-row>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-card variant="outlined" class="pa-2 mt-2">
                    <v-alert v-if="notTheCurrentMonth" type="info" class="mb-2" color="warning">
                      Since the user's joining month is not the current month, it is assumed that the user
                      is an existing employee and not newly joined. Therefore, you can set the vacation
                      balance for the user. If you prefer not to set the vacation balance at this time, you
                      can update it later by submitting the
                      <a href="/dashboard?tab=2">Set User Vacation Balance</a>
                      form after the user creation process.
                    </v-alert>
                    <v-row class="justify-center align-center mt-2 pa-2">
                      <v-col cols="6">
                        <v-text-field
                          v-model="annualBalance"
                          label="Annual Balance"
                          density="comfortable"
                          hide-details="auto"
                          :rules="[
                            (value: number) => (isSetBalance && value > 25) ? `The annual balance souldn't be more than 25 days.` : undefined,
                            (value: number) => (isSetBalance && value < 0) ? `The annual balance cannot be less than 0.` : undefined
                          ]"
                          type="number"
                          />
                        </v-col>
                        <v-col cols="6">
                        <v-text-field
                          v-model="emergencyBalance"
                          label="Emergency Balance"
                          density="comfortable"
                          hide-details="auto"
                          :rules="[
                            (value: number) => (isSetBalance && value > 6) ? `The emergency balance souldn't be more than 6 days.` : undefined,
                            (value: number) => (isSetBalance && value < 0) ? `The emergency balance cannot be less than 0.` : undefined,
                          ]"
                          type="number"
                        />
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          v-model="excusesBalance"
                          label="Excuses Balance"
                          density="comfortable"
                          hide-details="auto"
                          :rules="[
                            (value: number) => (isSetBalance && value > 6) ? `The excuses balance souldn't be more than 6 days.` : undefined,
                            (value: number) => (isSetBalance && value < 0) ? `The excuses balance cannot be less than 0.` : undefined,
                          ]"
                          type="number"
                        />
                      </v-col>
                    </v-row>
                  </v-card>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-alert>
        </v-col>
        <v-col cols="12">
          <v-file-input
            v-model="imageInput"
            label="Image"
            variant="filled"
            accept="image/*"
            :show-size="1024"
            prepend-icon="mdi-camera"
            @input="chooseImage"
            density="comfortable"
          ></v-file-input>
          <v-img
            v-if="imageInput && imageInput.length > 0 && imageUrl"
            :src="imageUrl"
            width="200"
            height="200"
            class="justify-center mb-5"
          ></v-img>
          <v-btn
            color="primary"
            type="submit"
            :disabled="!form?.isValid"
            :loading="isLoading"
            @click="execute"
            >Add User</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { $api } from '@/clients'
import type { Api } from '@/types'
import {
  nameRules,
  emailRules,
  passwordRules,
  mobileRules,
  jobRules,
  addressRules,
  requiredStringRules,
  requiredRules
} from '@/utils'
import { formatDate } from '@/utils'
import { useAsyncState } from '@vueuse/core'

export default {
  name: 'AddUser',
  setup() {
    const form = ref()
    const teams = [
      'Business Development',
      'Development',
      'HR & Finance',
      'QA',
      'Marketing and Communications',
      'Operations',
      'Support'
    ]
    const types = ['Admin', 'User', 'Team Lead']
    const selectedTeam = ref<Api.Teams>(teams[0] as Api.Teams)
    const genders = ['Male', 'Female']
    const selectedGender = ref(genders[0] as Api.Gender)
    const first_name = ref('')
    const last_name = ref('')
    const telegram_link = ref('')
    const email = ref('')
    const birthdayDate = ref(new Date())
    const joiningDate = ref(new Date())
    const birthday = ref(new Date().toISOString().split('T')[0])
    const joining_at = ref(new Date().toISOString().split('T')[0])
    const mobile_number = ref('')
    const password = ref('')
    const offices = ref([])
    const location = ref()
    const user_type = ref('User')
    const reporting_to = ref([])
    const job_title = ref('')
    const address = ref('')
    const social_insurance_number = ref('')
    const supervisors = ref<any[]>([])
    const selectedSupervisor = ref()
    const imageInput = ref()
    const imageUrl = ref()
    const supervisorPage = ref(1)
    const supervisorCount = ref(0)
    const annualBalance = ref(0)
    const emergencyBalance = ref(0)
    const excusesBalance = ref(0)
    const setBalance = ref<number[] | number | undefined>()
    const isSetBalance = ref<boolean>(false)
    const notTheCurrentMonth = ref<boolean>(false)
    const thisMonth = new Date().getMonth() + 1;

    const userBalance = computed(() => ({
      annual_leaves: +annualBalance.value || 0,
      emergency_leaves: +emergencyBalance.value || 0,
      leave_excuses: +excusesBalance.value || 0,
    }))

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
      user_type: user_type.value === 'Team Lead' ? 'Supervisor' : user_type.value,
      reporting_to: reporting_to.value,
      gender: selectedGender.value,
      job_title: job_title.value,
      address: address.value,
      social_insurance_number: social_insurance_number.value,
      image: imageUrl.value,
      user_balance: userBalance.value,
      calculate_balance: isSetBalance.value
    }))

    async function listSupervisors() {
      const res = await $api.users.supervisors.list({ page: supervisorPage.value })
      if (res.count) {
        supervisorCount.value = Math.ceil(res.count / 10)
        res.results.forEach((user: any) => {
          supervisors.value.push(user)
        })
      } else {
        supervisorCount.value = 0
      }

      return supervisors.value
    }

    const reloadMoreSupervisor = computed(() => {
      if (supervisorPage.value === supervisorCount.value) {
        return false
      }
      if (supervisorCount.value > 1) {
        return true
      }
      return false
    })

    onMounted(async () => {
      try {
        offices.value = (await $api.office.list()).map((office: any) => ({
          id: office.id,
          name: office.name
        }))

        location.value = offices.value[0]
        await listSupervisors()
      } catch (error) {
        console.error(error)
      }
    })

    watch([birthdayDate, joiningDate], ([newBirthdayDate, newJoiningDate]) => {
      if (newBirthdayDate) birthday.value = formatDate(newBirthdayDate)
      if (newJoiningDate) {
        if(newJoiningDate.getMonth() + 1 !== thisMonth){
          notTheCurrentMonth.value = true
          isSetBalance.value = true
          setBalance.value = [0]
        } else {
          setBalance.value = []
        }
        joining_at.value = formatDate(newJoiningDate)
      }
    })


    const birthdayPicker = ref(false)
    const joiningDatePicker = ref(false)
    const toggleDatePicker = (picker: string) => {
      if (picker === 'birthdayPicker') birthdayPicker.value = !birthdayPicker.value
      else if (picker === 'joiningDatePicker') joiningDatePicker.value = !joiningDatePicker.value
    }

    const { execute, isLoading } = useAsyncState(
      async () => {
        await $api.auth.register(user.value as Api.Inputs.Register)
      },
      null,
      { immediate: false }
    )

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
  
    watch(isSetBalance, () => {
      isSetBalance.value ? setBalance.value = 0 : setBalance.value = undefined
    })

    watch(setBalance, () => {
      if(setBalance.value != 0 && !setBalance.value){
        isSetBalance.value = false;
      } else {
        isSetBalance.value = true;
      }
    },)

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
      imageInput,
      imageUrl,
      supervisors,
      selectedSupervisor,
      nameRules,
      emailRules,
      passwordRules,
      mobileRules,
      jobRules,
      addressRules,
      requiredStringRules,
      requiredRules,
      isLoading,
      supervisorCount,
      supervisorPage,
      reloadMoreSupervisor,
      listSupervisors,
      toggleDatePicker,
      chooseImage,
      execute,
      annualBalance,
      emergencyBalance,
      excusesBalance,
      setBalance,
      isSetBalance,
      notTheCurrentMonth,
    }
  }
}
</script>

<style scoped>
.v-picker.v-sheet {
  position: absolute !important;
  z-index: 1000 !important;
}
</style>
