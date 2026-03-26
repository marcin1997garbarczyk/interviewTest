<template>
  <label
    class="inline-flex cursor-pointer items-center rounded-md border border-slate-300 bg-white px-3 py-2 text-slate-600 transition hover:bg-slate-100"
    title="Attach file"
  >
    <span class="text-sm">📎</span>
    <input class="hidden" type="file" @change="onFileSelected" />
  </label>
</template>

<script setup>
const emit = defineEmits(["select-file"]);

const onFileSelected = (event) => {
  const file = event.target.files?.[0];
  if (file) {
    emit("select-file", file);
  }
  event.target.value = "";
};
</script>
