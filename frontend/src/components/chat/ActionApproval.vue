<template>
  <div class="mt-2 rounded-lg border border-amber-300 bg-amber-50 p-3">
    <p class="text-sm font-semibold text-amber-800">Action requires human approval</p>
    <p class="mt-1 text-sm text-slate-700">Type: {{ action.action_type }}</p>
    <pre class="mt-2 overflow-x-auto rounded bg-white p-2 text-xs text-slate-700">{{ formattedDetails }}</pre>
    <div class="mt-3 flex gap-2">
      <button
        class="rounded-md bg-emerald-600 px-3 py-1 text-sm text-white hover:bg-emerald-700"
        :disabled="isProcessing"
        @click="emitDecision('approve')"
      >
        Approve
      </button>
      <button
        class="rounded-md bg-rose-600 px-3 py-1 text-sm text-white hover:bg-rose-700"
        :disabled="isProcessing"
        @click="emitDecision('reject')"
      >
        Reject
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  action: {
    type: Object,
    required: true
  },
  isProcessing: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["decision"]);

const formattedDetails = computed(() => JSON.stringify(props.action.details || {}, null, 2));

const emitDecision = (decision) => {
  emit("decision", { actionId: props.action.action_id, decision });
};
</script>
