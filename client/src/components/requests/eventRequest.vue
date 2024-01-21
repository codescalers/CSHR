
<template>
  <v-form ref="form" @submit.prevent="createEvent()">


    <div class="mt-3">
      <v-text-field color="primar'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
        label="Start Date" v-model="startDate" :readonly="true">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>

    <div class="mt-3">

      <v-text-field color="primary" item-color="primary" base-color="primary" :readonly="true" variant="outlined"
        v-model="endDate" hide-details="auto" label="End Date">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>


    <div class="mt-3">

      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Event Name"
        v-model="name" hide-details="auto" :rules="fieldRequired">
      </v-text-field>

    </div>
    <div class="mt-3">

      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Description"
        v-model="description" hide-details="auto" :rules="fieldRequired">
      </v-text-field>
    </div>


    <div class="mt-3">



      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Event Start Time"
        v-model="eventStart" hide-details="auto" :rules="fieldRequired" type="time">
      </v-text-field>
    </div>

    <div class="mt-3">



      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Event End Time"
        v-model="eventEnd" hide-details="auto" :rules="fieldRequired" type="time">
      </v-text-field>
    </div>




    <v-row class="mt-3 d-flex flex-row-reverse">

      <v-col cols="3">
        <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%">
          Submit
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { computed, ref } from 'vue';
import { fieldRequired } from '@/utils';
import { useApi } from '@/hooks'


export default {
  name: "leaveRequest",
  props: ["dates"],

  setup(props) {
    const $api = useApi()
    const startDate = ref<string>(props.dates.startStr)
    const endDate = ref<string>(props.dates.endStr)
    const name = ref<string>("")
    const description = ref<string>("")
    const form = ref()
    const eventStart = ref()
    const eventEnd = ref()

    const from_date = computed(() => {
      let val = new Date(startDate.value);
      if (eventStart.value) {
        const [hours, minutes] = eventStart.value.split(':').map(Number);
        val.setHours(hours, minutes, 0, 0);
      }

      return val.toISOString();
    });
    const end_date = computed(() => {
      let val = new Date(endDate.value);
      if (eventEnd.value) {
        const [hours, minutes] = eventEnd.value.split(':').map(Number);
        val.setHours(hours, minutes, 0, 0);
      }

      return val.toISOString();
    });



    async function createEvent() {
      await $api.event.create(
        {
          name: name.value,
          description: description.value,
          from_date: from_date.value,
          end_date: end_date.value,
        },
      )
    }

    return {
      startDate,
      endDate,
      name,
      description,
      form,
      fieldRequired,
      eventStart,
      eventEnd,

      createEvent,
    };
  },
};
</script>
