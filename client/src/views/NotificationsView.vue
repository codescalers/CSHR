<template>
  <v-container>
    <h1 class="my-6">All Notifications</h1>
    <v-data-table :headers="headers" :loading="loading" :items="notifications">
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
      </template>
      <template v-slot:item.type="{ value }">
        <v-chip :color="getColor(value)">
          {{ value.split('_').join(' ') }}
        </v-chip>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon class="me-2" @click.stop="openDialog(item.event_id, item.type)"> mdi-eye </v-icon>
        <CustomVDialog :routeQuery="item.event_id" :modelValue="showDialog[item.event_id]">
          <v-card v-if="item.type === 'vacations'" class="pa-4">
            <v-card-title class="font-weight-bold  mb-3">
              {{ capitalize(details.reason.split('_').join(' ')) }}
            </v-card-title>

            <v-card-subtitle>
              <v-chip :color="getStatusColor(details.status)" label>
                {{ details.status }}
              </v-chip>
            </v-card-subtitle>
            <v-row class="mt-4">
              <v-col cols="12" md="6">
                <v-list dense>
                  <v-list-item-group>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title class="mb-3 font-weight-bold">
                          Request Details
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          From Date: {{ details.from_date }}
                        </v-list-item-subtitle>
                        <v-list-item-subtitle>
                          End Date: {{ details.end_date }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-col>

              <v-col cols="12" md="6">
                <v-list dense>
                  <v-list-item-group>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title class="mb-3 font-weight-bold">
                          Applying User
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          Name: {{ details.applying_user.full_name }}
                        </v-list-item-subtitle>
                        <v-list-item-subtitle>
                          Email: {{ details.applying_user.email }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-col>

              <v-col cols="12" md="6">
                <v-list dense>
                  <v-list-item-group>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title class="mb-3 font-weight-bold">
                          Approval User
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          Name: {{ details.approval_user.full_name }}
                        </v-list-item-subtitle>
                        <v-list-item-subtitle>
                          Email: {{ details.approval_user.email }}
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

          <v-card v-if="item.type === 'hr_letters'">
            <p>itemmmm: {{ item }}</p>
            <v-btn @click="closeDialog(item.event_id)">close</v-btn>
          </v-card>
        </CustomVDialog>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { onMounted, ref } from 'vue'
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
    ]
    const loading = ref(true)
    const notifications = ref()
    const showDialog = ref<{ [key: string]: boolean }>({})
    const details = ref({
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
        case 'rejected':
          return 'red'
      }
    }

    async function getNotificationDetails(type: string, id: number) {
      return await $api.notifications.read(type, id)
    }

    async function openDialog(id: string, type: string) {
      showDialog.value[id] = true
      details.value = await getNotificationDetails(type, +id)
    }

    function closeDialog(id: string) {
      showDialog.value[id] = false
    }

    return {
      headers,
      loading,
      notifications,
      getColor,
      getStatusColor,
      getNotificationDetails,
      showDialog,
      details,
      openDialog,
      closeDialog,
      capitalize
    }
  }
}
</script>
