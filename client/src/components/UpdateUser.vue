<template>
  <v-container>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">

          <v-select v-model="selectedUser" :items="officeUsers" item-title="full_name" item-value="id" label="User"
            return-object density="comfortable" :rules="requiredRules">

            <template #append-item v-if="reloadMore">
              <VContainer>
                <VBtn @click="() => { return page++, count--,  concatUsers()}" block color="secondary" variant="tonal"
                  prepend-icon="mdi-reload">
                  Load More Users
                </VBtn>
              </VContainer>
            </template>
          </v-select>
          <v-select v-model="reporting_to" :items="supervisors" item-title="full_name" item-value="id" label="Team Lead"
            return-object density="comfortable" :rules="requiredRules">

            <template #append-item v-if="reloadMoreSupervisor">
              <VContainer>
                <VBtn @click="() => { return supervisorPage++, supervisorCount--, listSupervisors() }" block
                  color="secondary" variant="tonal" prepend-icon="mdi-reload">
                  Load More Team Leads
                </VBtn>
              </VContainer>
            </template>
          </v-select>

        </v-col>
        <v-col cols="6" v-if="selectedUser">
          <v-text-field v-model="selectedUser.first_name" label="First Name" density="comfortable"
            :rules="nameRules"></v-text-field>
          <v-text-field v-model="selectedUser.last_name" label="Last Name" density="comfortable"
            :rules="nameRules"></v-text-field>
          <v-text-field v-model="selectedUser.email" label="Email" type="email" density="comfortable"
            :rules="emailRules"></v-text-field>
          <v-text-field v-model="selectedUser.mobile_number" label="Mobile Number" type="number" density="comfortable"
            :rules="mobileRules"></v-text-field>
          <v-text-field v-model="selectedUser.job_title" label="Role" density="comfortable"
            :rules="jobRules"></v-text-field>

          <v-text-field v-model="selectedUser.address" label="Address" density="comfortable"
            :rules="addressRules"></v-text-field>
          <v-text-field v-model="selectedUser.social_insurance_number" label="Social Insurance Number" type="number"
            density="comfortable"></v-text-field>
        </v-col>
        <v-col cols="6" v-if="selectedUser">
          <v-text-field v-model="selectedUser.telegram_link" label="Telegram" density="comfortable"
            :rules="requiredRules"></v-text-field>

          <v-text-field v-model="selectedUser.birthday" label="Birthday" density="comfortable"
            :rules="requiredStringRules" @click="toggleDatePicker('birthdayPicker')" readonly>
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>
          <v-date-picker v-model="birthdayDate" v-if="birthdayPicker" density="comfortable" :rules="requiredStringRules">
          </v-date-picker>

          <v-text-field v-model="selectedUser.joining_at" label="Joining Date" density="comfortable"
            :rules="requiredStringRules" @click="toggleDatePicker('joiningDatePicker')" readonly>
            <template v-slot:append-inner>
              <v-icon>mdi-calendar</v-icon>
            </template>
          </v-text-field>
          <v-date-picker v-model="joiningDate" v-if="joiningDatePicker"> </v-date-picker>

          <v-select v-model="selectedUser.team" :items="teams" label="Team" density="comfortable"
            :rules="requiredStringRules"></v-select>
          <v-select v-model="selectedUser.gender" :items="genders" label="Gender" density="comfortable"
            :rules="requiredStringRules"></v-select>
          <v-select v-model="selectedUser.user_type" :items="types" label="User Type" density="comfortable"
            :rules="requiredStringRules"></v-select>
          <v-select v-model="selectedUser.location" :items="offices" label="Office" item-title="name" item-value="id"
            return-object density="comfortable" :rules="requiredRules"></v-select>
        </v-col>
        <v-col cols="12">
          <v-file-input v-model="image" label="Image" variant="filled" accept="image/*" :show-size="1024"
            prepend-icon="mdi-camera" @input="chooseImage" density="comfortable"></v-file-input>
              <v-img v-if="image && image.length > 0 && imageUrl" :src="imageUrl" width="200" height="200"
            class="justify-center mb-5"></v-img>
              <v-img v-else :src="imageSrc+ selectedUser?.image" width="200" height="200"
            ></v-img>
          <v-row>
            <v-col cols="3">
              <v-btn color="primary" type="submit" :disabled="!form?.isValid" :loading="isLoading" @click="execute">Update
                User</v-btn>
            </v-col>

            <v-col cols="9" class="d-flex justify-end">
              <v-btn :disabled="!form?.isValid" @click="activateUser.execute()" :loading="isLoading" v-if="selectedUser"
                :color="`${selectedUser.is_active ? 'error' : 'success'}`">
                {{ selectedUser.is_active ? 'Set as inactive user' : 'Set as active user' }}
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { $api } from '@/clients'
import {
  nameRules,
  emailRules,
  mobileRules,
  jobRules,
  addressRules,
  requiredStringRules,
  requiredRules,
  formatDate,
  listUsers
} from '@/utils'
import { useAsyncState } from '@vueuse/core'

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
    const types = ['Admin', 'User', 'Team Lead']
    const genders = ['Male', 'Female']
    const birthdayDate = ref(new Date())
    const joiningDate = ref(new Date())
    const offices = ref([])
    const supervisors = ref<any[]>([])
    const image = ref()
    const imageUrl = ref()
    const imageSrc = window.env.SERVER_DOMAIN_NAME_API.replace('api', '')
    const selectedUser = ref()
    const reporting_to = ref()
    const userIsActive = ref<boolean>(selectedUser.value?.is_active)
    const officeUsers = ref<any[]>([]);
    const page = ref(1)
    const count = ref(0)
    const supervisorPage = ref(1)
    const supervisorCount = ref(0)
    const reloadMore = computed(() => {
      if (page.value === count.value) {
        return false
      }
      if (count.value > 1) {
        return true
      }
      return false;
    });
    const reloadMoreSupervisor = computed(() => {
      if (supervisorPage.value === supervisorCount.value) {
        return false
      }
      if (supervisorCount.value > 1) {
        return true
      }
      return false;
    });

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

    async function concatUsers() {
      const { page: currentPage, count: currentCount, users: newUsers } = await listUsers($api, page.value, count.value);

      page.value = currentPage;
      count.value = currentCount;
      officeUsers.value = officeUsers.value.concat(newUsers);
    }

    onMounted(async () => {
      try {
        offices.value = (await $api.office.list()).map((office: any) => ({
          id: office.id,
          name: office.name
        }));
        await concatUsers()
        selectedUser.value = officeUsers.value[0]
        await listSupervisors()
        reporting_to.value = selectedUser.value?.reporting_to[0]

      } catch (error) {
        console.error(error)
      }
    })

    watch([ joiningDate], ([ newJoiningDate]) => {
      if (newJoiningDate) selectedUser.value.joining_at = formatDate(newJoiningDate)
    })

    watch([birthdayDate], ([newBirthdayDate,]) => {
      if (newBirthdayDate) selectedUser.value.birthday = formatDate(newBirthdayDate)
    })


    const birthdayPicker = ref(false)
    const joiningDatePicker = ref(false)
    const toggleDatePicker = (picker: string) => {
      if (picker === 'birthdayPicker') birthdayPicker.value = !birthdayPicker.value
      else if (picker === 'joiningDatePicker') joiningDatePicker.value = !joiningDatePicker.value
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
    const activateUser = useAsyncState(
      async () => {
        isLoading.value = true
        if (selectedUser.value.is_active) {
          selectedUser.value.is_active = userIsActive.value = false
          await $api.users.set_inactive.update({ user_id: selectedUser.value.id })
        } else {
          selectedUser.value.is_active = userIsActive.value = true
          await $api.users.set_active.update({ user_id: selectedUser.value.id })
        }
        isLoading.value = false
      },
      null,
      { immediate: false }
    )

    const { execute, isLoading } = useAsyncState(
      async () => {
        selectedUser.value.user_type = selectedUser.value.user_type === "Team Lead" ? "Supervisor" : selectedUser.value.user_type
        await $api.myprofile.update(selectedUser.value.id, {
          ...selectedUser.value,
          image: imageUrl.value ? imageUrl.value : selectedUser.value.image,
          location: selectedUser.value.location.id,
          filename: image.value ? image.value[0].name : null,
          reporting_to: reporting_to.value ? [reporting_to.value.id] : []
        })
      },
      null,
      { immediate: false }
    )

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
      imageSrc,
      supervisors,
      officeUsers,
      selectedUser,
      reporting_to,
      nameRules,
      emailRules,
      mobileRules,
      jobRules,
      addressRules,
      supervisorPage,
      supervisorCount,
      requiredStringRules,
      requiredRules,
      isLoading,
      userIsActive,
      execute,
      toggleDatePicker,
      listSupervisors,
      activateUser,
      count,
      page,
      reloadMore,
      reloadMoreSupervisor,
      concatUsers,
      chooseImage
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
