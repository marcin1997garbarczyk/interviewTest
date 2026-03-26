<template>
  <form class="flex items-center gap-2 p-4" @submit.prevent="submitMessage">
    <FileUploader @select-file="handleFileSelect" />
    <input
      v-model="draftMessage"
      class="w-full rounded-md border border-slate-300 px-4 py-2 text-sm focus:border-blue-500 focus:outline-none"
      type="text"
      placeholder="Type your message..."
      :disabled="isLoading"
    />
    <button
      type="submit"
      class="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:opacity-60"
      :disabled="isLoading || !draftMessage.trim()"
    >
      Send
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue";
import FileUploader from "./FileUploader.vue";

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["send-message", "upload-file"]);
const draftMessage = ref("");

const submitMessage = () => {
  const message = draftMessage.value.trim();
  if (!message) {
    return;
  }
  emit("send-message", message);
  draftMessage.value = "";
};

const handleFileSelect = (file) => {
  emit("upload-file", file);
};
</script>
