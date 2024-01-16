
<template>
  <v-form ref="form" @submit.prevent="createEvent(name, description, startDate, endDate)">



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
        <!-- <template v-slot:append>
          <v-icon color="primary">mdi-domain</v-icon>
        </template> -->
      </v-text-field>
      <!-- 
        <v-text-field color="primary" item-color="primary" base-color="primary" :readonly="true" variant="outlined"
          v-model="name" label="Name" :rules="fieldRequired">

        </v-text-field> -->
    </div>
    <div class="mt-3">

      <v-text-field item-color="primary" base-color="primary" color="primary" variant="outlined" label="Description"
        v-model="description" hide-details="auto" :rules="fieldRequired">
        <!-- <template v-slot:append>
          <v-icon color="primary">mdi-domain</v-icon>
        </template> -->
      </v-text-field>
    </div>

    <v-row class="mt-3">

      <v-col cols="3">
        <v-btn color="primary" type="submit" :disabled="!form?.isValid" width="100%">
          Submit
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { ref } from 'vue';
import { fieldRequired } from '@/utils';
import { $api } from '@/clients';
import { useRouter } from 'vue-router';


export default {
  name: "leaveRequest",
  props: ["dates"],

  setup(props) {
    // (new Date(props.dates.startStr)
    const startDate = ref<any>(props.dates.startStr)
    const endDate = ref<any>(props.dates.endStr)
    const name = ref<string>("")
    const description = ref<string>("")
    const form = ref()
    const $router = useRouter()

    // const startDate = ref<Date>(new Date(props.dates.startStr));
    //   const endDate = ref<Date>(new Date(props.dates.endStr));


    async function createEvent(name: string, description: string, startDate: string, endDate: string) {
      await $api.event.create(
        {
          name: name,
          description: description,
          from_date: startDate,
          end_date: endDate,
        },
      )
      $router.push('/calender')
    }

    return {
      startDate,
      endDate,
      name,
      description,
      form,
      fieldRequired,
      createEvent,
    };
  },
};
</script>
