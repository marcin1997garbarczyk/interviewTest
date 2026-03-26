<template>
  <div :class="containerClasses">
    <div :class="bubbleClasses">
      {{ message.content }}
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
});

const isUserMessage = computed(() => props.message.role === "user");
const isSystemLikeMessage = computed(() => ["system", "tool"].includes(props.message.role));

const containerClasses = computed(() =>
  isUserMessage.value ? "flex justify-end" : "flex justify-start"
);

const bubbleClasses = computed(() =>
  isUserMessage.value
    ? "max-w-[80%] rounded-2xl rounded-br-md bg-blue-600 px-4 py-2 text-sm text-white"
    : isSystemLikeMessage.value
      ? "max-w-[80%] rounded-2xl rounded-bl-md border border-amber-300 bg-amber-50 px-4 py-2 text-sm text-amber-900"
      : "max-w-[80%] rounded-2xl rounded-bl-md bg-white px-4 py-2 text-sm text-slate-800 shadow"
);
</script>
