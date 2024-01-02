<template>
  <VDialog
    :model-value="routeQueryValue === 'open'"
    @update:model-value="bindModelValue"
    v-bind="/* prettier-ignore */ ($props as any)"
  >
    <!-- @vue-skip -->
    <template v-for="(_, slot) of $slots" v-slot:[slot]="scope">
      <slot :name="slot" v-bind="scope" />
    </template>
  </VDialog>
</template>

<script lang="ts">
import { VDialog } from 'vuetify/components/VDialog'

import { useRouteQuery } from '@vueuse/router'
import { watchImmediate } from '@vueuse/core'
import { panic } from '@/utils'

export default {
  name: 'CustomVDialog',
  props: {
    routeQuery: { type: String, required: true },
    modelValue: Boolean
  },
  emits: {
    'update:model-value': (value: boolean) => true || value
  },
  components: { VDialog },
  setup(props, ctx) {
    // assert routeQuery
    !props.routeQuery && panic('VDialog require route query to bind in url.')

    const routeQueryValue = useRouteQuery<'open' | undefined>(
      props.routeQuery,
      props.modelValue ? 'open' : undefined
    )

    watchImmediate(
      () => props.modelValue,
      (modelValue) => {
        if ((routeQueryValue.value === 'open' && !modelValue) || modelValue) {
          return bindModelValue(true)
        }
      }
    )

    function bindModelValue(value: boolean) {
      const newQueryValue = value ? 'open' : undefined
      if (newQueryValue !== routeQueryValue.value) {
        routeQueryValue.value = newQueryValue
      }

      value !== props.modelValue && ctx.emit('update:model-value', value)
    }

    return { routeQueryValue, bindModelValue }
  }
}
</script>
