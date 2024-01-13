<template>
  <v-container>
    <h1 class="my-6">All Notifications</h1>
    <v-data-table :headers="headers" :loading="loading" :items="notifications">
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
      </template>
      <template v-slot:[`item.type`]="{ value }">
        <v-chip :color="getColor(value)">
          {{ value.split('_').join(' ') }}
        </v-chip>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon class="me-2" @click.stop="openDialog(item.event_id, item.type)"> mdi-eye </v-icon>
        <CustomVDialog :routeQuery="item.event_id" :modelValue="showDialog[item.event_id]">
          <NotificationDetails
            v-if="item.type === 'vacations'"
            :title="capitalize(vDetails.reason.split('_').join(' '))"
            :eventId="item.event_id"
            :sections="vSections"
            :status="vDetails.status"
            @close="closeDialog(item.event_id)"
          />
          <NotificationDetails
            v-if="item.type === 'hr_letters'"
            title="Applying for an HR Letter"
            :eventId="item.event_id"
            :sections="hrSections"
            :status="hrDetails.status"
            @close="closeDialog(item.event_id)"
          />
        </CustomVDialog>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { computed, onMounted, ref } from 'vue'
import CustomVDialog from '@/components/vuetify/CustomVDialog.vue'
import NotificationDetails from '@/components/NotificationDetails.vue'
import { capitalize } from 'vue'

export default {
  name: 'NotificationsView',
  components: {
    CustomVDialog,
    NotificationDetails
  },
  setup() {
    const headers = [
      { title: 'User', align: 'start', sortable: false, key: 'user.full_name' },
      { title: 'Type', align: 'start', key: 'type' },
      { title: 'Content', align: 'start', key: 'title' },
      { title: 'Created At', align: 'start', key: 'created_at' },
      { title: 'Actions', key: 'actions', align: 'end', sortable: false }
    ] as any[]
    const loading = ref(true)
    const notifications = ref<any[]>()
    const showDialog = ref<{ [key: string]: boolean }>({})
    const hrDetails = ref({
      id: 0,
      addresses: '',
      status: '',
      applying_user: {
        id: 0,
        full_name: '',
        email: '',
        image: '',
        team: '',
        gender: '',
        skills: [],
        job_title: '',
        user_certificates: []
      },
      approval_user: null || '',
      with_date: true,
      created_at: '',
      from_date: '',
      end_date: '',
      with_salary_mentioned: true
    })
    const vDetails = ref({
      reason: '',
      status: '',
      from_date: '',
      end_date: '',
      applying_user: {
        full_name: '',
        email: ''
      },
      approval_user: {
        full_name: '',
        email: ''
      },
      change_log: []
    })

    const vSections = computed(() => [
      {
        title: 'Request Details',
        details: [
          { label: 'From Date', value: vDetails.value.from_date },
          { label: 'End Date', value: vDetails.value.end_date }
        ]
      },
      {
        title: 'Applying User',
        details: [
          { label: 'Name', value: vDetails.value.applying_user.full_name },
          { label: 'Email', value: vDetails.value.applying_user.email }
        ]
      },
      {
        title: 'Approval User',
        details: [
          { label: 'Name', value: vDetails.value.approval_user.full_name },
          { label: 'Email', value: vDetails.value.approval_user.email }
        ]
      }
    ])

    const hrSections = computed(() => [
      {
        title: 'User Details',
        details: [
          { label: 'Name', value: hrDetails.value.applying_user.full_name },
          { label: 'Email', value: hrDetails.value.applying_user.email },
          { label: 'Job Title', value: hrDetails.value.applying_user.job_title || 'Not specified' }
        ]
      },
      {
        title: 'Event Details',
        details: [
          { label: 'Status', value: hrDetails.value.status },
          { label: 'Approval User', value: hrDetails.value.approval_user || '-' },
          { label: 'With Date', value: hrDetails.value.with_date },
          { label: 'From Date', value: hrDetails.value.from_date },
          { label: 'End Date', value: hrDetails.value.end_date },
          { label: 'Salary Mentioned', value: hrDetails.value.with_salary_mentioned },
          { label: 'Addresses', value: hrDetails.value.addresses }
        ]
      }
    ])
    onMounted(async () => {
      notifications.value = await $api.notifications.list()
      loading.value = false
    })

    function getColor(type: string) {
      switch (type) {
        case 'vacations':
          return 'green'
        case 'hr_letters':
          return 'orange'
        default:
          return 'grey'
      }
    }

    async function readNotification(type: string, id: number) {
      return await $api.notifications.read(type, id)
    }

    async function openDialog(id: string, type: string) {
      showDialog.value[id] = true
      switch (type) {
        case 'vacations':
          vDetails.value = await readNotification(type, +id)
          break
        case 'hr_letters':
          hrDetails.value = await readNotification(type, +id)
          break
        default:
          break
      }
    }

    function closeDialog(id: string) {
      showDialog.value[id] = false
    }

    return {
      headers,
      loading,
      notifications,
      showDialog,
      vDetails,
      hrDetails,
      vSections,
      hrSections,
      getColor,
      readNotification,
      openDialog,
      closeDialog,
      capitalize
    }
  }
}
</script>

<style>
.v-list-item-subtitle {
  margin-bottom: 0.5rem;
}
</style>
