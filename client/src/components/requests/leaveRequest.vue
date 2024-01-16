
<template>

      
    <div class="mt-3">
      <v-text-field color="primar'" item-color="primary" base-color="primary" variant="outlined" hide-details="auto"
        label="From" v-model="startDate" :readonly="true">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>

    <div class="mt-3">

      <v-text-field color="primary" item-color="primary" base-color="primary" :readonly="true" variant="outlined"
        v-model="endDate" hide-details="auto" label="To">
        <template v-slot:append>
          <v-icon color="primary">mdi-calendar</v-icon>
        </template>
      </v-text-field>
    </div>

    <!-- <div class="mt-3">
      <select-boat
        :readonly="undefined"
        :request="request"
        @update:select-boat="(selectedItem: string) => emit('update:select-boat', selectedItem)"
      />
    </div> -->

    <!-- <div class="mt-3">
      <v-text-field
        :item-color="request.boat.color || 'primary'"
        :base-color="request.boat.color || 'primary'"
        :color="request.boat.color || 'primary'"
        variant="outlined"
        label="Company Name"
        v-model="$props.request.companyName"
        hide-details="auto"
        :hint="`In case there is no company and it's a personal reservation, please type the person's name.`"
      >
        <template v-slot:append>
          <v-icon :color="request.boat.color || 'primary'">mdi-domain</v-icon>
        </template>
      </v-text-field>
    </div>

    <div class="mt-3">
      <v-text-field
        :item-color="request.boat.color || 'primary'"
        :base-color="request.boat.color || 'primary'"
        :color="request.boat.color || 'primary'"
        variant="outlined"
        hide-details="auto"
        label="Contact Person"
        v-model="$props.request.contactPerson"
        :hint="`The contact person should be a phone number or email, to be used when need to contact the reservation person.`"
      >
        <template v-slot:append>
          <v-icon :color="request.boat.color || 'primary'">mdi-account-box-outline</v-icon>
        </template>
      </v-text-field>
    </div> -->

</template>
<script lang="ts">
import { ref } from 'vue';


export default {
  name: "leaveRequest",
  props: ["dates"],
  // components: {
  //   cshrDialogue,
  // },
  // emits: {
  //   'close-dialogue': (item: Object) => item
  // },

  setup(props) {
    // const emit = defineEmits(['close-dialogue', 'update:request']);
    const startDate = ref<any>(props.dates.startStr)
    const endDate = ref<any>(props.dates.endStr)



    return {
      startDate,
      endDate,
      // cshrDialogue,
      // emit,
    };
  },
};
</script>
