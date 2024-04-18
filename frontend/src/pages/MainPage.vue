<script setup lang="ts">
import { userdataUserApi, touchMeApi } from '../api';
import { useProfileStore } from '../store';
import { onMounted, ref } from 'vue';

const profileStore = useProfileStore();

const showUserWarn = ref(false);
const showClickWarn = ref(false);
const clickResult = ref<number | null>(null);

onMounted(async () => {
	// Get username
	if (!profileStore.full_name && profileStore.id) {
		const resp = await userdataUserApi.getById(profileStore.id);
		if (resp.status != 200) {
			showUserWarn.value = true;
			return;
		}
		const data = resp.data;
		if (!data || !data.items) {
			showUserWarn.value = true;
			return;
		}
		const nameItem = data.items.find(item => {
			return item.category == 'Личная информация' && item.param == 'Полное имя';
		});
		if (!nameItem) {
			showUserWarn.value = true;
			return;
		}
		profileStore.full_name = nameItem?.value ?? null;
	}

	// Get touch data
	const resp = await touchMeApi.getTouch();
	if (resp.status != 200) {
		showClickWarn.value = true;
		return;
	}
	const data = resp.data;
	if (!data || !data.count) {
		showClickWarn.value = true;
		return;
	}
	clickResult.value = +data.count;
});

const makeClick = async () => {
	// Make touch
	const resp = await touchMeApi.addTouch();
	if (resp.status != 200) {
		showClickWarn.value = true;
		return;
	}
	const data = resp.data;
	if (!data || !data.count) {
		showClickWarn.value = true;
		return;
	}
	clickResult.value = +data.count;
};
</script>

<template>
	<div>
		<h1 class="text-h1">
			Hello<span v-if="profileStore.full_name">, {{ profileStore.full_name }}</span
			>!
		</h1>
		<p v-if="!profileStore.full_name">
			Не удалось получить твое имя из
			<a href="https://api.profcomff.com/?urls.primaryName=userdata">Userdata API</a>
			=(
		</p>
		<p>Твой id: {{ profileStore.id }}</p>
		<div>
			<button @click="makeClick">Нажми чтобы увеличить каунтер</button>
			<h2 v-if="clickResult">
				В сумме ты кликнул эту кнопку <span>{{ clickResult }}</span> раз
			</h2>
		</div>
	</div>
</template>
