<template>
  <v-form ref="form" @submit.prevent="createLeave()">
    <v-alert v-if="form?.isValid && isValid" density="compact" class="pa-5 my-5" type="warning">
      {{
        actualDays.state.value === 0
        ? 'Actual vacation days requested is zero, Selected days might include weekends or public holidays'
        : actualDays.state.value === 1 && days < 1 && days > 0 ? 'Actual vacation days requested are ' + days + ' days'
          : 'Actual vacation days requested are ' + actualDays.state.value + ' days'
      }}
    </v-alert>
    <div class="mt-3" v-if="user?.fullUser.user_type === 'Admin'">
      <v-radio-group inline v-model="selectedOption">
        <v-radio label="For yourself" value="me"></v-radio>
        <v-radio label="For Another User" value="anotheruser"></v-radio>
      </v-radio-group>
    </div>
    <div class="mt-3" v-if="selectedOption === 'anotheruser'">
      <v-autocomplete color="info" item-color="info" base-color="info" variant="outlined" v-model="selectedUser"
        :items="officeUsers" item-title="full_name" item-value="id" label="User" return-object :rules="requiredRules">
        <template #append-item v-if="reloadMore">
          <VContainer>
            <VBtn @click="() => {
              return page++, count--, concatUsers()
            }
              " block color="secondary" variant="tonal" prepend-icon="mdi-reload">
              Load More Users
            </VBtn>
          </VContainer>
        </template>
      </v-autocomplete>
    </div>

    <div class="mt-3">
      <v-autocomplete color="info" item-color="info" base-color="info" variant="outlined" v-model="leaveReason"
        :items="leaveReasons" label="Reason" return-object item-title="name">
      </v-autocomplete>
    </div>

    <div class="mt-3">
      <v-text-field ref="startDateField" color="info" item-color="info" base-color="info" variant="outlined"
        hide-details="auto" label="From" v-model="startDate" type="date" :rules="[validateDates]"></v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field ref="endDateField" color="info" item-color="info" base-color="info" variant="outlined"
        hide-details="auto" label="To" v-model="endDate" type="date" :rules="[validateDates]"></v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field ref="excuseStartField" item-color="info" base-color="info" color="info" variant="outlined"
        label="Vacation Start Time" v-model="excuseStart" hide-details="auto" type="time" :rules="[validateTimes]"
        :readonly="startDate !== endDate">
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field ref="excuseEndField" item-color="info" base-color="info" color="info" variant="outlined"
        label="Vacation End Time" v-model="excuseEnd" hide-details="auto" type="time" :rules="[validateTimes]"
        :readonly="startDate !== endDate">
      </v-text-field>
    </div>
    <v-row class="mt-3 pa-4 d-flex justify-end">
      <v-btn color="primary" type="Submit"
        :disabled="!form?.isValid || !isValid || actualDays.state.value === 0 || requesting" :loading="requesting">
        Submit
      </v-btn>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { useApi } from '@/hooks'
import { Selection, type Api } from '@/types'
import { requiredRules, listUsers, calculateTimes } from '@/utils'
import { useAsyncState } from '@vueuse/core'
import { computed, onMounted, ref, watch } from 'vue'
import { ApiClientBase } from '@/clients/api/base'
import { fieldRequired } from '@/utils'

export default {
  name: 'leaveRequest',
  props: ['dates'],
  emits: {
    'create-event': (item: any) => item
  },
  setup(props, ctx) {
    const $api = useApi()
    const form = ref()
    const officeUsers = ref<any[]>([])
    const selectedUser = ref()
    const selectedOption = ref<Selection>(Selection.ME)
    const page = ref(1)
    const count = ref(0)
    const startDateField = ref()
    const endDateField = ref()
    const excuseStartField = ref()
    const excuseEndField = ref()
    const startDate = ref<Date>(props.dates.startStr)
    const endDate = ref<any>(new Date(props.dates.endStr))
    endDate.value.setDate(endDate.value.getDate() - 1)
    endDate.value = endDate.value.toISOString().split('T')[0]
    const user = ApiClientBase.user
    const userId = ref<number | undefined>()
    const leaveReason = ref<Api.LeaveReason>()
    const leaveReasons = ref<Api.LeaveReason[]>([])
    const requesting = ref<boolean>(false)
    const excuseStart = ref('08:00')
    const excuseEnd = ref('16:00')
    const days = ref()

    const actualDays = useAsyncState(async () => {
      return $api.vacations.calculate.list({
        start_date: startDate.value,
        end_date: endDate.value
      })
    }, undefined)

    const isValid = computed(() => {
      let val = leaveReason.value ? true : false
      return val
    })

    const balance = useAsyncState(
      () => $api.vacations.getVacationBalance({ user_ids: userId.value }),
      null,
      {
        immediate: false,
        onSuccess(data: any) {
          leaveReasons.value = [
            {
              name: `Emergency Leaves  ${data[0].emergency_leaves.reserved} / ${data[0].emergency_leaves.all}`,
              reason: 'emergency_leaves'
            },
            {
              name: `Sick Leaves  ${data[0].sick_leaves.reserved} / ∞`,
              reason: 'sick_leaves'
            },
            {
              name: `Annual Leaves  ${data[0].annual_leaves.reserved} / ${data[0].annual_leaves.all}`,
              reason: 'annual_leaves'
            },
            {
              name: `Unpaid ${data[0].unpaid.reserved} / ∞`,
              reason: 'unpaid'
            },
            {
              name: `Compensation  ${data[0].compensation.reserved} / ∞`,
              reason: 'compensation'
            },
            {
              name: `Leave Excuse  ${data[0].leave_excuses.reserved} / ${data[0].leave_excuses.all}`,
              reason: 'leave_excuses'
            }
          ]
        }
      }
    )

    watch(
      () => [selectedOption.value],
      () => {
        leaveReason.value = undefined
        if (selectedOption.value === Selection.ANOTHERUSER) {
          selectedUser.value = officeUsers.value[0]
        } else {
          selectedUser.value = undefined
          userId.value = user.value?.fullUser.id
          balance.execute()
        }
      }
    )

    watch(
      () => [selectedUser.value],
      async () => {
        if (selectedUser.value) {
          userId.value = selectedUser.value.id
          balance.execute()
        }
      }
    )

    watch(
      () => [startDate.value, endDate.value],
      async () => {
        setTimeout(async () => {
          startDateField.value.validate()
          endDateField.value.validate()
          if (startDate.value !== endDate.value) {
            days.value = 0;
            excuseStart.value = '08:00'
            excuseEnd.value = '16:00'
          }

          if(form.value.isValid){
            actualDays.execute()
          }

        }, 200)
      }
    )

    watch(
      () => [excuseStart.value, excuseEnd.value],
      async () => {
        setTimeout(async () => {
          excuseStartField.value.validate()
          excuseEndField.value.validate()
          if (startDate.value == endDate.value) {
            days.value = calculateTimes(excuseStart.value, excuseEnd.value)
          }
        }, 200)
      }
    )
    const validateDates = (): string | boolean => {
      if (!startDate.value) return 'Please select start date.'
      if (!endDate.value) return 'Please select end date.'
      if (endDate.value < startDate.value) return 'End date must be after start date.'
      return true
    }

    const validateTimes = (): string | boolean => {
      if (!excuseEnd.value) return 'Please select end time.'
      if (excuseEnd.value < excuseStart.value) return 'End time must be after start time.'
      return true
    }
    async function concatUsers() {
      const {
        page: currentPage,
        count: currentCount,
        users: newUsers
      } = await listUsers($api, page.value, count.value)

      page.value = currentPage
      count.value = currentCount
      officeUsers.value = officeUsers.value.concat(newUsers)
    }
    onMounted(async () => {
      startDateField.value.validate()
      endDateField.value.validate()
      userId.value = user.value?.fullUser.id
      balance.execute()
      if(user.value?.fullUser.user_type === 'Admin'){
        concatUsers()
      }
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

    async function createLeave() {
      requesting.value = true
      if (leaveReason.value) {
        if (selectedOption.value === Selection.ANOTHERUSER) {
          await useAsyncState(
            $api.vacations.admin.create(selectedUser.value.id, {
              reason: leaveReason.value.reason,
              from_date: `${startDate.value}T${excuseStart.value}`,
              end_date: `${endDate.value}T${excuseEnd.value}`,
            }),
            null,
            {
              onSuccess(data) {
                ctx.emit('create-event', data)
              }
            }
          )
        } else {
          await useAsyncState(
            $api.vacations.create({
              reason: leaveReason.value.reason,
              from_date: `${startDate.value}T${excuseStart.value}`,
              end_date: `${endDate.value}T${excuseEnd.value}`,
            }),
            undefined,
            {
              onSuccess(data) {
                ctx.emit('create-event', data)
              }
            }
          )
        }
      }
      requesting.value = false
    }

    return {
      startDate,
      endDate,
      leaveReasons,
      leaveReason,
      form,
      isValid,
      actualDays,
      user,
      startDateField,
      endDateField,
      requiredRules,
      reloadMore,
      selectedUser,
      officeUsers,
      page,
      requesting,
      count,
      selectedOption,
      fieldRequired,
      excuseStart,
      excuseEnd,
      days,
      excuseStartField,
      excuseEndField,
      concatUsers,
      createLeave,
      validateDates,
      validateTimes,
    }
  }
}
</script>
