<template>
  <v-card elevation="0">
    <v-card-title class="bg-graytitle">
      <div class="d-flex flex-row-reverse">
        <v-icon
          class="me-2"
          size="small"
          @click.stop="$emit('close-dialog', false)"
        >
          mdi-close
        </v-icon>
      </div>
    </v-card-title>
    <v-container class="pa-6">
      <p class="text-subtitle-1 text-center">
        From <b>{{ vacation.from_date }} </b> to
        <b color="primary">{{ vacation.end_date }} </b> vacation

        <v-row class="d-flex justify-center my-2" v-if="couldUpdate">
          <v-btn color="primary" class="mx-1 my-2" @click="readOnly = false"
            >Update</v-btn
          >
          <v-btn color="error" class="mx-1 my-2" @click="handleDelete"
            >Delete</v-btn
          >
        </v-row>
      </p>
      <v-divider class="my-2"></v-divider>
      <v-form ref="form" @submit.prevent="updateVacation()">
        <v-card elevation="0" class="pa-4">
          <v-row class="py-2">
            <v-col cols="6" class="d-flex">
              <v-icon class="mr-2">mdi-account</v-icon>
              <p>
                Applying User :
                <span color="warning" class="mx-2">{{
                  vacation.user.full_name
                }}</span>
              </p>
            </v-col>
            <!-- <v-col cols="3" class="text-right">
              {{ vacation.user.full_name }}
            </v-col> -->

            <v-col cols="6" class="d-flex">
              <v-icon class="mr-2">mdi-account</v-icon>

              <p>
                Approval User :
                <span class="mx-2" v-if="vacation.isUpdated">{{
                  vacation.approval_user
                    ? vacation.approval_user
                    : "Under approving"
                }}</span>
                <span class="mx-2" v-else>{{
                  vacation.approval_user.email
                    ? vacation.approval_user.email
                    : "Under approving"
                }}</span>
              </p>
            </v-col>
            <!-- <v-col cols="3" class="text-right" v-if="vacation.isUpdated">
              {{ vacation.approval_user ? vacation.approval_user : 'Under approving' }}
            </v-col>
            <v-col cols="3" class="text-right" v-else>
              {{ vacation.approval_user.email ? vacation.approval_user.email : 'Under approving' }}
            </v-col> -->
          </v-row>

          <v-row>
            <!-- <v-col cols="2">
              <v-icon>mdi-calendar</v-icon>

              <b> From</b>
            </v-col> -->
            <v-col cols="6">
              <v-text-field
                color="info"
                item-color="info"
                base-color="info"
                variant="outlined"
                hide-details="auto"
                label="From"
                v-model="startDate"
                :readonly="readOnly"
                type="date"
              >
              </v-text-field>
            </v-col>

            <!-- <v-col cols="2">
              <v-icon>mdi-calendar</v-icon>

              <b> To</b>
            </v-col> -->
            <v-col cols="6">
              <v-text-field
                color="info"
                item-color="info"
                base-color="info"
                variant="outlined"
                hide-details="auto"
                label="To"
                v-model="endDate"
                :readonly="readOnly"
                type="date"
                :rules="[validateEndDate]"
              >
              </v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <!-- <v-col cols="2">
              <v-icon>mdi-navigation</v-icon>

              <b> Reason</b>
            </v-col> -->
            <v-col cols="6">
              <v-autocomplete
                color="info"
                item-color="info"
                base-color="info"
                variant="outlined"
                v-model="leaveReason"
                :items="leaveReasons"
                label="Reason"
                return-object
                item-title="name"
                :readonly="readOnly"
              >
              </v-autocomplete>
            </v-col>
            <v-col cols="6" class="d-flex items-center">
              <!-- <v-icon>mdi-calendar</v-icon> -->
              <p>
                Status :
                {{ vacation.status }}
              </p>
            </v-col>
            <!-- <v-col cols="3" class="text-right">
              
            </v-col> -->
          </v-row>
          <v-row class="d-flex justify-center" v-if="!readOnly">
            <v-btn
              color="primary"
              class="my-2 mx-1"
              type="submit"
              :disabled="!form?.isValid"
            >
              Submit
            </v-btn>
            <v-btn color="info" class="my-2 mx-1" @click="readOnly = true"
              >Cancel</v-btn
            >
          </v-row>
        </v-card>
      </v-form>
      <v-divider class="my-2"></v-divider>
      <v-row
        class="d-flex justify-end mt-3"
        v-if="couldApprove && vacation.status == 'pending'"
      >
        <v-btn color="primary" class="ma-1" @click="handleApprove"
          >Approve</v-btn
        >
        <v-btn color="error" class="ma-1" @click="handleReject">Reject</v-btn>
      </v-row>
    </v-container>
  </v-card>
</template>
<script lang="ts">
import type { Api } from "@/types";
import { computed, ref } from "vue";

import { useState } from "@/store";
import { useApi } from "@/hooks";
import { useAsyncState } from "@vueuse/core";

export default {
  name: "vacationCard",
  props: ["vacation"],
  emits: {
    "close-dialog": (item: Boolean) => item,
    "update-vacation": (item: any) => item,
    "delete-vacation": () => true,
    "status-vacation": (item: string) => item,
  },

  setup(props, ctx) {
    const $api = useApi();

    const startDate = ref<Date>(props.vacation.from_date);
    const endDate = ref<Date>(props.vacation.end_date);
    const leaveReason = ref<Api.LeaveReason>({
      name: transformString(props.vacation.reason),
      reason: props.vacation.reason,
    });
    const form = ref();
    const state = useState();
    const readOnly = ref<boolean>(true);
    const leaveReasons = ref<Api.LeaveReason[]>([
      {
        name: "Public Holidays",
        reason: "public_holiday",
      },
      {
        name: "Emergency Leaves",
        reason: "emergency_leaves",
      },
      {
        name: "Sick Leaves",
        reason: "sick_leaves",
      },
      {
        name: "Annual Leaves",
        reason: "annual_leaves",
      },
      {
        name: "Unpaid",
        reason: "unpaid",
      },
      {
        name: "Compensation",
        reason: "compensation",
      },
    ]);
    const couldUpdate = computed(() => {
      if (state.user.value) {
        if (props.vacation.status == "pending") {
          if (
            props.vacation.isUpdated &&
            state.user.value.value.id == props.vacation.applying_user
          ) {
            return true;
          }
          if (
            !props.vacation.isUpdated &&
            state.user.value.value.id == props.vacation.applying_user.id
          ) {
            return true;
          }
          return false;
        }
      }
      return false;
    });

    const couldApprove = computed(() => {
      if (state.user.value) {
        if (
          state.user.value.value.user_type === "Admin" ||
          state.user.value.value.user_type === "Supervisor"
        ) {
          if (props.vacation.user.id == state.user.value.value.id) {
            return true;
          }
          if (
            props.vacation.user.reporting_to.includes(
              state.user.value.value.id
            ) &&
            props.vacation.user.location.name ===
              state.user.value.value.location.name
          ) {
            return true;
          }
          return false;
        }
      }
      return false;
    });

    function validateEndDate(value: any) {
      if (startDate.value && value <= startDate.value) {
        return "To date must be after From date";
      }
      return true;
    }
    async function handleDelete() {
      return useAsyncState($api.vacations.delete(props.vacation.id), [], {
        onSuccess() {
          ctx.emit("delete-vacation");
        },
      });
    }
    async function handleApprove() {
      return useAsyncState(
        $api.vacations.approve.update(props.vacation.id),
        [],
        {
          onSuccess() {
            ctx.emit("status-vacation", "Approve");
          },
        }
      );
    }
    async function handleReject() {
      return useAsyncState(
        $api.vacations.reject.update(props.vacation.id),
        [],
        {
          onSuccess() {
            ctx.emit("status-vacation", "Reject");
          },
        }
      );
    }

    async function calculateActualDays() {
      return useAsyncState(
        $api.vacations.calculate.list({
          start_date: startDate.value,
          end_date: endDate.value,
        }),
        []
      );
    }
    function transformString(inputString: string): string {
      const words = inputString.split("_");
      const capitalizedWords = words.map(
        (word) => word.charAt(0).toUpperCase() + word.slice(1)
      );
      const resultString = capitalizedWords.join(" ");
      return resultString;
    }

    async function updateVacation() {
      const actualDays = await calculateActualDays();

      useAsyncState(
        $api.vacations.edit.update(props.vacation.id, {
          reason: leaveReason.value.reason,
          from_date: startDate.value,
          end_date: endDate.value,
          actual_days: actualDays.state.value,
        }),
        null,
        {
          onSuccess(data) {
            ctx.emit("update-vacation", data);
          },
        }
      );
    }

    return {
      startDate,
      endDate,
      leaveReason,
      leaveReasons,
      readOnly,
      form,
      state,
      couldApprove,
      couldUpdate,
      validateEndDate,
      updateVacation,
      handleApprove,
      handleReject,
      handleDelete,
    };
  },
};
</script>


