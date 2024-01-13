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
          <v-card v-if="item.type === 'vacations' && vDetails" class="pa-4">
            <v-card-title class="font-weight-bold mb-3"> Emergency Leave </v-card-title>

            <v-card-subtitle>
              <v-chip :color="getStatusColor(vDetails.status)">
                {{ vDetails.status }}
              </v-chip>
            </v-card-subtitle>

            <v-row class="mt-4">
              <v-col v-for="section in sections" :key="section.title" cols="12" md="6">
                <v-list dense>
                  <v-list-item-group>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title class="mb-3 font-weight-bold">
                          {{ section.title }}
                        </v-list-item-title>
                        <v-list-item-subtitle
                          v-for="subtitle in section.subtitles"
                          :key="subtitle.label"
                        >
                          {{ subtitle.label }}: {{ subtitle.value }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-col>
            </v-row>

            <v-card-actions class="mt-6">
              <v-btn color="blue darken-1" @click="closeDialog(item.event_id)"> Close </v-btn>
            </v-card-actions>
          </v-card>

          <v-card v-if="item.type === 'hr_letters' && hrDetails" class="pa-4">
            <v-card-title class="font-weight-bold mb-3"> Applying for HR Letter </v-card-title>

            <v-card-subtitle>
              <v-chip :color="getStatusColor(vDetails.status)">
                {{ hrDetails.status }}
              </v-chip>
            </v-card-subtitle>

            <v-row class="mt-4">
              <v-col v-for="section in hrSections" :key="section.title" cols="12" md="6">
                <v-list dense>
                  <v-list-item-group>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title class="mb-3 font-weight-bold">
                          {{ section.title }}
                        </v-list-item-title>
                        <v-list-item-subtitle v-for="detail in section.details" :key="detail.label">
                          {{ detail.label }}: {{ detail.value }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-col>
            </v-row>

            <v-card-actions class="mt-6">
              <v-btn color="blue darken-1" @click="closeDialog(item.event_id)"> Close </v-btn>
            </v-card-actions>
          </v-card>
        </CustomVDialog>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { computed, onMounted, ref } from 'vue'
import CustomVDialog from '@/components/vuetify/CustomVDialog.vue'
import { capitalize } from 'vue'

export default {
  name: 'NotificationsView',
  components: {
    CustomVDialog
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
      id: Number,
      addresses: String,
      status: String,
      applying_user: {
        id: Number,
        full_name: String,
        email: String,
        image: String,
        team: String,
        gender: String,
        skills: [],
        job_title: String,
        user_certificates: []
      },
      approval_user: null || String,
      with_date: true,
      created_at: String,
      from_date: String,
      end_date: String,
      with_salary_mentioned: Boolean
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

    const sections = computed(() => [
      {
        title: 'Request Details',
        subtitles: [
          { label: 'From Date', value: vDetails.value.from_date },
          { label: 'End Date', value: vDetails.value.end_date }
        ]
      },
      {
        title: 'Applying User',
        subtitles: [
          { label: 'Name', value: vDetails.value.applying_user.full_name },
          { label: 'Email', value: vDetails.value.applying_user.email }
        ]
      },
      {
        title: 'Approval User',
        subtitles: [
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
          { label: 'Approval User', value: hrDetails.value.approval_user || 'Not yet approved' },
          { label: 'With Date', value: hrDetails.value.with_date },
          { label: 'From Date', value: hrDetails.value.from_date },
          { label: 'End Date', value: hrDetails.value.end_date },
          { label: 'Salary Mentioned', value: hrDetails.value.with_salary_mentioned },
          { label: 'Addresses', value: hrDetails.value.addresses }
        ]
      }
    ])
    onMounted(async () => {
      await $api.auth.login({
        email: 'admin@gmail.com',
        password: '0000'
      })
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

    function getStatusColor(status: string) {
      switch (status) {
        case 'approved':
          return 'green'
        case 'pending':
          return 'orange'
        case 'rejected':
          return 'red'
      }
    }

    async function getNotificationDetails(type: string, id: number) {
      return await $api.notifications.read(type, id)
    }

    async function openDialog(id: string, type: string) {
      showDialog.value[id] = true
      switch (type) {
        case 'vacations':
          vDetails.value = await getNotificationDetails(type, +id)
          break
        case 'hr_letters':
          hrDetails.value = await getNotificationDetails(type, +id)
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
      sections,
      hrSections,
      getColor,
      getStatusColor,
      getNotificationDetails,
      openDialog,
      closeDialog,
      capitalize
    }
  }
}
</script>

<style scoped>
.v-list-item-subtitle {
  margin-bottom: 0.5rem;
}
</style>
