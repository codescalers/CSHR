<template>
  <v-container class="pa-6 mx-auto">
    <v-row class="d-flex justify-center align-center">
      <v-col cols="12">
        <div v-if="pageNotFound" class="header text-center">
          <strong>4</strong>
          <strong class="text-primary">0</strong>
          <strong>4</strong>
        </div>
        <div v-else class="body text-center">
          <v-icon size="300" style="color: lightgray;opacity: 0.5;">mdi-package-variant</v-icon>
        </div>
        <div class="header text-center">
          <p v-if="pageNotFound">{{ message || 'Seems like there are no pages matching this route. Please ensure you are in the right place.' }}</p>
          <p v-else>{{ message || 'Seems like there are no items.' }}</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
export default {
  name: 'UsersView',
  components: {
  },
  props: {
    message: {
      type: String,
      required: false,
    },
    pageNotFound: {
      type: Boolean,
      required: true,
    }
  },
}
</script>

<style>
.header strong{
  font-size: 200px;
}
.body p{
  margin-top: -40px;
  font-size: 25px;
}
</style>