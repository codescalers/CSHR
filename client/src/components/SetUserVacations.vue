<template>
  <v-container>
    <v-alert type="info" class="mb-4">
      The displayed balance pertains to the selected user. In multiple selections, default values
      are set to 0 due to space limitations. Hover over user cards to view individual balances.
    </v-alert>
    <v-form ref="form" @submit.prevent>
      <v-row class="justify-center align-center">
        <v-col cols="12">
          <v-text-field
            v-model="user!.fullUser.location.name"
            label="Office"
            type="text"
            :rules="requiredStringRules"
            disabled
          ></v-text-field>
          <v-select
            multiple
            v-model="selectedUsers"
            :items="officeUsers"
            item-title="full_name"
            item-value="id"
            label="User"
            return-object
            density="comfortable"
            :rules="requiredRules"
          >
            <template v-slot:prepend-item>
              <v-list-item title="Select All Users" @click="toggleSelectedUsers">
                <template v-slot:prepend>
                  <v-checkbox-btn
                    :color="selectedSomeUsers ? 'indigo-darken-2' : undefined"
                    :indeterminate="selectedSomeUsers && !selectedAllUsers"
                    :model-value="selectedAllUsers"
                  ></v-checkbox-btn>
                </template>
              </v-list-item>
            </template>

            <template v-slot:selection="selectedUsers">
              <v-tooltip theme="dark" location="bottom">
                <template #default>
                  <v-card class="pa-2">
                    <h3 class="pa-2">Vacation Balances</h3>
                    <v-card>
                      <div class="reason mb-2">
                        <div class="d-flex">
                          <div class="dot" />
                          <h4 class="mb-2">Annual Leaves</h4>
                        </div>
                        <p class="ml-5">
                          <v-chip class="mr-3" color="green">
                            All: {{ userBalance.annual_leaves.all }}
                          </v-chip>
                          <v-chip class="mr-3" color="yellow">
                            Reserved: {{ userBalance.annual_leaves.reserved }}
                          </v-chip>
                        </p>
                      </div>
                      <div class="reason mb-2">
                        <div class="d-flex">
                          <div class="dot" />
                          <h4 class="mb-2">Emergency Leaves</h4>
                        </div>
                        <p class="ml-5">
                          <v-chip class="mr-3" color="green">
                            All: {{ userBalance.emergency_leaves.all }}
                          </v-chip>
                          <v-chip class="mr-3" color="yellow">
                            Reserved: {{ userBalance.emergency_leaves.reserved }}
                          </v-chip>
                        </p>
                      </div>
                      <div class="reason mb-2">
                        <div class="d-flex">
                          <div class="dot" />
                          <h4 class="mb-2">Excuses Leaves</h4>
                        </div>
                        <p class="ml-5">
                          <v-chip class="mr-3" color="green">
                            All: {{ userBalance.leave_excuses.all }}
                          </v-chip>
                          <v-chip class="mr-3" color="yellow">
                            Reserved: {{ userBalance.leave_excuses.reserved }}
                          </v-chip>
                        </p>
                      </div>
                      <div class="reason mb-2">
                        <div class="d-flex">
                          <div class="dot" />
                          <h4 class="mb-2">Compensations</h4>
                        </div>
                        <p class="ml-5">
                          <v-chip class="mr-3" color="green">
                            All: {{ userBalance.compensation.all }}
                          </v-chip>
                          <v-chip class="mr-3" color="yellow">
                            Reserved: {{ userBalance.compensation.reserved }}
                          </v-chip>
                        </p>
                      </div>
                    </v-card>
                  </v-card>
                </template>

                <template v-slot:activator="{ props }">
                  <div class="ml-4 mr-2 mt-2">
                    <profile-image
                      @mouseenter="setUserBalanceValues(selectedUsers.item.value)"
                      v-bind="props"
                      class="mb-3"
                      :width="'45px'"
                      :user="officeUsers.filter((user) => user.id === selectedUsers.item.value)[0]"
                    />
                  </div>
                  {{ selectedUsers.item.title }}
                </template>
              </v-tooltip>
            </template>

            <template #append-item v-if="reloadMore">
              <VContainer>
                <VBtn
                  @click="
                    () => {
                      return page++, count--, listUsers()
                    }
                  "
                  block
                  color="secondary"
                  variant="tonal"
                  prepend-icon="mdi-reload"
                >
                  Load More Users
                </VBtn>
              </VContainer>
            </template>
          </v-select>
          <v-text-field
            v-model="inputBalance.annual_leaves"
            label="Annual Leaves"
            type="number"
            :rules="[...vacationRules, ...checkAnnualBalanceRule]"
          ></v-text-field>
          <v-text-field
            v-model="inputBalance.leave_excuses"
            label="Leave Excuses"
            type="number"
            :rules="[...vacationRules, ...checkExcusesBalanceRule]"
          ></v-text-field>
          <v-text-field
            v-model="inputBalance.emergency_leaves"
            label="Emergency Leaves"
            type="number"
            :rules="[...vacationRules, ...checkEmergencyBalanceRule]"
            ></v-text-field>
            <v-text-field
            v-model="inputBalance.compensation"
            label="Compensation"
            type="number"
            :rules="checkCompensationsBalanceRule"
          ></v-text-field>
          <v-btn
            color="primary"
            type="submit"
            :disabled="!form?.isValid"
            :loading="isLoading"
            @click="execute"
            >Set Vacations</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { requiredRules, requiredStringRules, vacationRules } from '@/utils'
import { onMounted, ref, watchEffect, computed } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { ApiClientBase } from '@/clients/api/base'
import ProfileImage from '@/components/profileImage.vue'
import { type Api } from '@/types/api'

export default {
  name: 'SetUserVacations',
  computed: {
    selectedSomeUsers() {
      return this.selectedUsers.length > 0
    },
    selectedAllUsers() {
      return this.selectedUsers.length === this.officeUsers.length
    }
  },
  methods: {
    toggleSelectedUsers() {
      if (this.selectedAllUsers) {
        this.selectedUsers = []
      } else {
        this.selectedUsers = this.officeUsers.slice()
      }
    }
  },

  setup() {
    const form = ref()
    const user = ApiClientBase.user
    const officeUsers = ref<any[]>([])
    const selectedUsers = ref<any[]>([])
    const userVacations = ref()
    const page = ref(1)
    const count = ref(0)
    const inputBalance = ref({
      annual_leaves: 0,
      leave_excuses: 0,
      emergency_leaves: 0,
      compensation: 0
    })

    const userBalance = ref({
      annual_leaves: { all: '', reserved: 0 },
      leave_excuses: { all: '', reserved: 0 },
      emergency_leaves: { all: '', reserved: 0 },
      compensation: { all: '', reserved: 0 }
    })

    const reloadMore = computed(() => {
      if (page.value === count.value) {
        return false
      }
      if (count.value > 1) {
        return true
      }
      return false
    })

    const checkAnnualBalanceRule = [
      (v: string) =>
        +v <= +userBalance.value.annual_leaves.all ||
        `The actual annual value cannot be smaller than the reserved annual value, the actual value is ${userBalance.value.annual_leaves.all}.`
    ]

    const checkEmergencyBalanceRule = [
      (v: string) =>
        +v <= +userBalance.value.emergency_leaves.all ||
        `The actual emergency value cannot be smaller than the reserved emergency value, the actual value is ${userBalance.value.emergency_leaves.all}.`
    ]

    const checkExcusesBalanceRule = [
      (v: string) =>
        +v <= +userBalance.value.leave_excuses.all ||
        `The actual excuses value cannot be smaller than the reserved excuses value, the actual value is ${userBalance.value.leave_excuses.all}.`
    ]

    const checkCompensationsBalanceRule = [
      (v: string) =>
        +v <= +userBalance.value.compensation.all ||
        `The actual compensation value cannot be smaller than the reserved compensation value, the actual value is ${userBalance.value.compensation.all}.`
    ]

    function getSelectedUsersIds(): number[] {
      let userIds: any[] = []
      if (selectedUsers.value) {
        selectedUsers.value.forEach((user) => {
          userIds.push(user.id)
        })
      }
      return userIds
    }

    function setUserBalanceValues(userID: number) {
      const _userBalance: Api.BalanceVacation = userVacations.value.find(
        (balance: Api.BalanceVacation) => balance.user!.id === userID
      )

      if (userVacations.value) {
        userBalance.value.annual_leaves = _userBalance.annual_leaves
        userBalance.value.leave_excuses = _userBalance.leave_excuses
        userBalance.value.emergency_leaves = _userBalance.emergency_leaves
        userBalance.value.compensation = _userBalance.compensation
      }
    }

    async function getUserBalance() {
      if (selectedUsers.value.length) {
        const result = await $api.vacations.balance.list({
          user_ids: getSelectedUsersIds().join(',')
        })
        userVacations.value = result
        if (userVacations.value.length === 1) {
          const { annual_leaves, leave_excuses, emergency_leaves, compensation } =
            userVacations.value[0]
          inputBalance.value.annual_leaves = annual_leaves.reserved
          inputBalance.value.leave_excuses = leave_excuses.reserved
          inputBalance.value.emergency_leaves = emergency_leaves.reserved
          inputBalance.value.compensation = compensation.reserved
        } else {
          inputBalance.value.annual_leaves = 0
          inputBalance.value.leave_excuses = 0
          inputBalance.value.emergency_leaves = 0
        }
        setUserBalanceValues(selectedUsers.value[0].id)
      }
    }

    watchEffect(async () => {
      try {
        await getUserBalance()
      } catch (error) {
        console.error(error)
      }
    })

    async function listUsers() {
      const res = await $api.users.admin.office_users.list({ page: page.value })
      if (res.count) {
        count.value = Math.ceil(res.count / 10)
      } else {
        count.value = 0
      }
      res.results.forEach((user: any) => {
        officeUsers.value.push(user)
      })
      return officeUsers.value
    }
    onMounted(async () => {
      try {
        await listUsers()
        selectedUsers.value.push(officeUsers.value[0])
        await getUserBalance()
      } catch (error) {
        console.error(error)
      }
    })
    const { execute, isLoading } = useAsyncState(
      async () => {
        await $api.vacations.balance.update(
          { user_ids: getSelectedUsersIds().join(',') },
          inputBalance.value
        )
        await getUserBalance()
      },
      null,
      { immediate: false }
    )
    return {
      form,
      user,
      page,
      count,
      selectedUsers,
      officeUsers,
      userVacations,
      inputBalance,
      requiredStringRules,
      requiredRules,
      vacationRules,
      isLoading,
      reloadMore,
      listUsers,
      execute,
      setUserBalanceValues,
      userBalance,
      checkAnnualBalanceRule,
      checkEmergencyBalanceRule,
      checkExcusesBalanceRule,
      checkCompensationsBalanceRule,
    }
  },
  components: { ProfileImage }
}
</script>

<style scoped>
.dot {
  width: 7px;
  height: 7px;
  padding: 7px;
  border-radius: 50px;
  /* margin: 0 auto; */
  opacity: 0.8;
  background: rgba(42, 218, 231, 0.473);
  margin-left: 5px;
  margin-right: 5px;
  margin-bottom: 7px;
  margin-top: 3px;
}
</style>
