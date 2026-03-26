<template>
  <div class="flex h-full flex-col gap-3 overflow-y-auto p-4">
    <div v-for="(message, index) in messages" :key="`${message.role}-${index}`">
      <MessageBubble :message="message" />
      <ActionApproval
        v-if="message?.metadata?.pending_action"
        :action="message.metadata.pending_action"
        :is-processing="isApproving"
        @decision="forwardDecision"
      />
    </div>
  </div>
</template>

<script setup>
import ActionApproval from "./ActionApproval.vue";
import MessageBubble from "./MessageBubble.vue";

defineProps({
  messages: {
    type: Array,
    required: true
  },
  isApproving: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["action-decision"]);

const forwardDecision = ({ actionId, decision }) => {
  emit("action-decision", { actionId, decision });
};
</script>
