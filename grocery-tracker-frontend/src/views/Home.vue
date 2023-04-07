<template>
	<HelloWorld />
	<v-btn @click="onSubmit">Submit</v-btn>
	<p>{{ JSON.stringify(data) }}</p>
</template>

<script lang="ts" setup>
	import { ref } from "vue";
	import HelloWorld from "@/components/HelloWorld.vue";

	const data = ref({});
	async function onSubmit() {
		const response = await fetch("http://localhost:5000/api/receipts");
		const json = await response.json();
		data.value = json;
	}
</script>