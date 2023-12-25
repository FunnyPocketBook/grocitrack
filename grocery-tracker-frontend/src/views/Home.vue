<template>
	<HelloWorld />
	<v-btn @click="getReceipts">Submit</v-btn>
	<v-data-table
		v-if="receipts.length > 0"
		:headers="headers"
		:items="receipts"
		item-value="name"
		class="elevation-1"
	></v-data-table>
</template>

<script lang="ts" setup>
	import { ref, onMounted } from "vue";
	import HelloWorld from "@/components/HelloWorld.vue";

	const receipts = ref([]);
	const headers = ref([
		{
			title: "Date",
			align: "start",
			key: "datetime",
		},
		{
			title: "Total amount",
			align: "start",
			key: "total_price",
		},
		{
			title: "Total discount",
			align: "start",
			key: "total_discount",
		},
	]);

	async function getReceipts() {
		const response = await fetch("http://localhost:5000/api/receipts");
		const json = await response.json();
		receipts.value = json;
	}

	onMounted(async () => {
		getReceipts();
	});
</script> 