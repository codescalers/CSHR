import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Api } from '@/types';

export const useHomeEventsStore = defineStore('homeEventsStore', () => {
  const events = ref<Api.Home[]>([]);
  const vacations = ref<Api.Vacation[]>([]);
  const holidays = ref<Api.Holiday[]>([]);
  const meetings = ref<Api.Meeting[]>([]);
  const birthdays = ref<Api.User[]>([]);
  const userEvents = ref<Api.Event[]>([]);
  const reload = ref<boolean>(false)

  const addEvent = (newEvent: Api.Home) => {
    events.value.push(newEvent);
  };

  const addNewEvents = (newEvent: Api.Home) => {
    events.value.push(newEvent);
  };

  const setEvents = (newEvent: Api.Home[]) => {
    events.value = newEvent;
  };

  const clearEvents = () => {
    events.value = [];
  };


  return {
    events,
    vacations,
    holidays,
    meetings,
    birthdays,
    userEvents,
    addNewEvents,
    addEvent,
    setEvents,
    clearEvents,
    reload,
  };
});
