<template>
  <main class="mx-auto flex h-screen w-full max-w-4xl flex-col p-4">
    <section class="flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-slate-50 shadow-lg">
      <header class="flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3">
        <h1 class="text-lg font-semibold text-slate-800">AI Agent Boilerplate</h1>
        <button
          class="rounded-md border border-slate-300 px-3 py-1 text-sm text-slate-700 transition hover:bg-slate-100"
          @click="clearHistory"
        >
          Clear
        </button>
      </header>

      <MessageList :messages="messages" :is-approving="isApproving" @action-decision="handleActionDecision" />

      <p v-if="errorMessage" class="px-4 pb-2 text-sm text-red-600">
        {{ errorMessage }}
      </p>

      <ChatInput :is-loading="isLoading" @send-message="sendMessage" @upload-file="uploadSelectedFile" />
    </section>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import ChatInput from "./ChatInput.vue";
import MessageList from "./MessageList.vue";
import {
  approveAction,
  clearConversationHistory,
  fetchConversationHistory,
  sendChatMessage,
  uploadFile
} from "../../services/api_client";

const sessionId = "demo-session";
const isLoading = ref(false);
const isApproving = ref(false);
const errorMessage = ref("");
const messages = ref([]);

const loadHistory = async () => {
  try {
    const response = await fetchConversationHistory(sessionId);
    messages.value = response.messages;
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "Could not load history.";
  }
};

const sendMessage = async (content) => {
  const userMessage = { session_id: sessionId, role: "user", content };
  messages.value.push(userMessage);
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await sendChatMessage({
      session_id: sessionId,
      prompt: content,
      context: {}
    });
    messages.value.push({ session_id: sessionId, role: "ai", content: response.response });
    if (response.pending_action) {
      messages.value.push({
        session_id: sessionId,
        role: "system",
        content: "Action proposed and waiting for your approval.",
        metadata: { pending_action: response.pending_action }
      });
    }
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "Could not send message.";
  } finally {
    isLoading.value = false;
  }
};

const uploadSelectedFile = async (file) => {
  try {
    const response = await uploadFile(file);
    messages.value.push({
      session_id: sessionId,
      role: "ai",
      content: `File uploaded: ${response.filename}`
    });
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "Could not upload file.";
  }
};

const clearHistory = async () => {
  try {
    await clearConversationHistory(sessionId);
    messages.value = [];
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "Could not clear history.";
  }
};

const handleActionDecision = async ({ actionId, decision }) => {
  isApproving.value = true;
  try {
    const response = await approveAction({
      session_id: sessionId,
      action_id: actionId,
      decision
    });
    messages.value.push({
      session_id: sessionId,
      role: "system",
      content: `Action ${response.action_id} ${response.status.toLowerCase()}.`
    });
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "Could not submit action decision.";
  } finally {
    isApproving.value = false;
  }
};

onMounted(loadHistory);
</script>
