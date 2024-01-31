<template>
	<div class="h-screen w-100 main"
		:style="{ 'background-color': rgbColorString, 'transition': `background-color ${colorTransitionDuration}s ease`, }">
		<v-chip v-if="!connected" class="connection" size="x-large" prepend-icon="mdi-lan-disconnect">Disconnected</v-chip>
		<div class="wrapper">
			<transition-group name="fade" tag="div" class="text-transition">
				<span v-if="state === 'error'" :key="'error' + keyID" class="error_text">A system error occurred!</span>
				<span v-if="state === 'inactive'" :key="'inactive' + keyID" class="offline_text">This system is
					offline!</span>
				<div v-if="state === 'idle' || state === 'active'" :key="'active' + keyID" class="active_text__wrapper"
					:style="{ 'color': getContrastColor(rgbColor) }">
					<span class="active_text__name">
						{{ GetColorName(rgbToHex(rgbColor.r, rgbColor.g, rgbColor.b)) }}
					</span>
					<br />
					<span class="active_text__hex">
						{{ rgbToHex(rgbColor.r, rgbColor.g, rgbColor.b) }}
					</span>
				</div>
				<div v-if="state === 'prompting'" :key="'prompting' + keyID"
					:style="{ 'color': getContrastColor(rgbColor) }">
					<span class="prompting_text"> {{ prompting_text }} </span>
				</div>
				<div v-if="state === 'printing'" :key="'printing' + keyID">
					<div class="card__positioner">
						<Poem :color_name="GetColorName(rgbToHex(rgbColor.r, rgbColor.g, rgbColor.b))"
							:color_hex="rgbToHex(rgbColor.r, rgbColor.g, rgbColor.b)"
							:color_contrast="getContrastColor(rgbColor)" :poem="poem" />
					</div>
				</div>
			</transition-group>
		</div>
	</div>

	<div class="offscreen-element">
		<PrintPoem ref="poemElement" :color_name="GetColorName(rgbToHex(rgbColor.r, rgbColor.g, rgbColor.b))"
			:color_hex="rgbToHex(rgbColor.r, rgbColor.g, rgbColor.b)" :color_contrast="getContrastColor(rgbColor)"
			:poem="poem" />
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import mqtt from 'mqtt';
import axios from 'axios';
import html2canvas from 'html2canvas';
import { getContrastColor, GetColorName, rgbToHex } from '@/utils/color'
import { PROMPT, PROMPT_no_weather } from '@/utils/prompt'
import Poem from '@/components/Poem.vue';
import PrintPoem from '@/components/PrintPoem.vue'
import { nextTick } from 'vue';

let stateChangeTime = Date.now();

const project_name = 'DELPHI'
const system = 'system_1'
const print_data = ref({
	ISO_location: "Delft,NL",
	location: "Delft, Netherlands",
	color: "#000000"
});
const state = ref('idle');
const rgbColor = ref({ r: 0, g: 0, b: 0 });
const colorTransitionDuration = ref(1)
const keyID = ref(0)
const connected = ref(false)
const poem = ref("")
const capturedImageData = ref(null);
const poemElement = ref(null);
const prompting_text = ref("");

async function capturePoem() {

	try {
		const poemDOMElement = poemElement.value.getPoemElement();
		if (!poemDOMElement) {
			throw new Error("Poem element not found");
		}
		const canvas = await html2canvas(poemDOMElement);
		const imageData = canvas.toDataURL('image/png');

		capturedImageData.value = imageData;
		client.publish(`${project_name}/${system}/image_data`, capturedImageData.value);
		setTimeout(() => client.publish(`${project_name}/${system}/image_sent`, 'true'), 3 * 1000);
	} catch (error) {
		console.error('Error capturing Poem component:', error);
	}
}

async function makeHttpRequest() {
	const apiKey = import.meta.env.VITE_WEATHERAPIKEY;
	const weatherLocation = print_data.value.ISO_location;
	const location = print_data.value.location;
	const color = print_data.value.color;
	const time = new Date().toLocaleDateString(new Intl.DateTimeFormat("en-us", { dateStyle: "full", timeStyle: "short" }));

	try {
		let prompt;
		try {
			const response = await axios.get(`http://api.openweathermap.org/geo/1.0/direct?q=${weatherLocation}&appid=${apiKey}`);
			const weatherData = response.data[0];
			const weather = `${weatherData.main.temp - 273.15}°C: ${weatherData.weather[0].description}`;
			prompt = PROMPT(color, time, weather, location);
		} catch {
			prompt = PROMPT_no_weather(color, time, location);
		}

		const openAIKey = import.meta.env.VITE_GPTAPIKEY;
		const gptResponse = await axios.post('https://api.openai.com/v1/chat/completions', {
			"model": "gpt-3.5-turbo",
			"messages": [{ "role": "user", "content": prompt }],
			"temperature": 0.8,
			"top_p": 1.0,
			"presence_penalty": 1.0,
		}, {
			headers: {
				'Authorization': `Bearer ${openAIKey}`,
				'Content-Type': 'application/json'
			}
		});

		poem.value = gptResponse.data.choices[0].message.content;
		await nextTick()
		capturePoem()
	} catch (error) {
		console.error('Error in HTTP request:', error);
		client.publish(`${project_name}/${system}/state`, 'error', { retain: true });
	}
}

function reset() {
	print_data.value = {};
	state.value = 'idle';
	rgbColor.value = { r: 0, g: 0, b: 0 };
	colorTransitionDuration.value = 1
	keyID.value = 0
	poem.value = ''
	capturedImageData.value = null;
}

function checkAndResetState() {
	const currentTime = Date.now();
	const elapsedTime = currentTime - stateChangeTime;
	if (state.value !== 'idle' && elapsedTime >= 5 * 60 * 1000) {
		reset()
	}

	setTimeout(checkAndResetState, 60 * 1000);
}

let promptingInterval = null;
const startPromptingLoop = () => {
	let count = 1;
	prompting_text.value = '.';
	promptingInterval = setInterval(() => {
		prompting_text.value = '.'.repeat(count);
		count = count % 3 + 1;
	}, 500);
};

const stopPromptingLoop = () => {
	if (promptingInterval) {
		clearInterval(promptingInterval);
		promptingInterval = null;
		prompting_text.value = '';
	}
};

watch(state, (newVal) => {
	if (newVal === 'prompting') {
		startPromptingLoop();
	} else {
		stopPromptingLoop();
	}
});

let client;

onMounted(() => {
	checkAndResetState();
	client = mqtt.connect('ws://80.114.175.135:9001',
		{
			clientId: `DELPHI-web${new Date().toLocaleTimeString()}`,
			username: "ie_minor",
			password: "wieditleesttrekteenbak"
		});
	client.on('connect', () => {
		console.log('connected');
		connected.value = true;
		client.subscribe(`${project_name}/${system}/state`);
		client.subscribe(`${project_name}/${system}/root_color`);
		client.subscribe(`${project_name}/${system}/system_data`);
	});

	client.on('disconnect', () => {
		console.log('disconnected');
		connected.value = false;
	})

	client.on('message', (topic, buffer) => {
		stateChangeTime = Date.now();
		keyID.value++
		const messageString = buffer.toString();

		if (topic === `${project_name}/${system}/state`) {
			state.value = messageString;
		} else if (topic === `${project_name}/${system}/reset`) {
			reset()
		} else if (topic === `${project_name}/${system}/root_color`) {
			const messageObj = JSON.parse(messageString);

			if (messageObj.color && messageObj.duration) {

				if (messageObj.color.length === 3) {
					const [r, g, b] = messageObj.color;
					rgbColor.value = { r, g, b };
				}
				colorTransitionDuration.value = messageObj.duration;
			}
		} else if (topic === `${project_name}/${system}/system_data`) {
			try {
				print_data.value = JSON.parse(messageString);
				makeHttpRequest();
			} catch (e) {
				console.error('Error parsing JSON:', e);
			}
		}
	});
});

onUnmounted(() => {
	if (client) {
		client.end();
	}
});

const rgbColorString = computed(() => {
	if (state.value === 'error') {
		return 'rgb(255, 0, 0)'
	} else if (state.value === 'inactive') {
		return 'rgb(0, 0, 0)'
	} else if (state.value === 'printing') {
		return `rgb(${rgbColor.value.r}, ${rgbColor.value.g}, ${rgbColor.value.b})`;
	}
	return `rgb(${rgbColor.value.r}, ${rgbColor.value.g}, ${rgbColor.value.b})`;
});
</script>

<style>
html {
	overflow: hidden;
}
</style>

<style scoped>
.offscreen-element {
	position: absolute;
	top: 100vh;
}

.connection {
	position: absolute;
	right: 3vw;
	top: 3vh;
	color: red;
}

.wrapper {
	position: relative;
	display: grid;
	width: 100%;
	height: 100%;
	justify-content: center;
	align-content: center;
}

.card__positioner {
	display: grid;
	width: 100%;
	height: 100%;
	justify-content: center;
	align-content: center;
}

.text-transition>* {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 100%;
	text-align: center;
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

.error_text {
	font-size: 10vh;
	color: white;
	text-align: center;
}

.offline_text {
	font-size: 10vh;
	color: white;
	text-align: center;
}

.active_text__wrapper {
	text-align: center;
}

.active_text__name {
	font-size: 10vh;
}

.active_text__hex {
	font-size: 5vh;
	opacity: 0.8;
	text-transform: uppercase;
}

.prompting_text {
	font-size: 10vh;
}
</style>
