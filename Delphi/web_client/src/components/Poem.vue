<template>
	<transition name="fade">
		<div v-if="showInitialMessage" class="initial-message" :style="`color:${color_contrast}`">
			<span>{{ initialDisplayedText }}</span>
		</div>
	</transition>

	<transition name="fade">
		<div v-if="!showInitialMessage" class="poem_card__wrapper">
			<v-card class="poem_card" :style="`background-color: ${color_hex};`" flat>
				<v-card-title :style="`color: ${color_contrast}`">
					{{ color_name }}
				</v-card-title>

				<v-card-subtitle :style="`color:${color_contrast}`">
					{{ color_hex }}
				</v-card-subtitle>

				<v-card-text>
					<div class="poem_container">
						<div class="poem_inner">
							<span>{{ displayedText }}</span>
						</div>
					</div>

					<div class="title__container">
						<div class="title__logo">
							<svg viewBox="75.73 184.7194 99.21 38.6906" xmlns="http://www.w3.org/2000/svg">
								<path
									d="M104.55,219.69c2.49,0,3.85-1.66,3.85-3.98v-11.84h5.3v12.11c-0.05,5.33-4.32,7.42-9.15,7.42c-4.83,0-9.09-2.09-9.15-7.42 v-12.11h5.3v11.84C100.71,218.03,102.06,219.69,104.55,219.69z"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<polygon
									points="81.67,223 86.97,223 86.97,207.58 92.91,207.58 92.91,203.87 75.73,203.87 75.73,207.58 81.67,207.58 &#9;"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<path
									d="M94.41,194.55c-1.29,0.41-2.63,0.08-2.62-1.65c0-2.64,6.19-4.85,7.05-7.15c0.21-0.57,0.23-1.05-0.05-1.03 c-0.2,0.01-0.04,0.3-0.48,0.73c-2.56,2.57-6.86,2.56-10.16,4.04c-2.16,0.97-8.5,3.95-7.04,10.6c0.07,0.32,0.26,1.37,0.45,1.37 c0.22,0,0.22-0.63,0.22-1.39c-0.05-3.96,4.64-5.06,6.17-7.65c0.18-0.31,0.5-0.74,0.57-0.54c0.04,0.1,0.01,0.24-0.05,0.52 c-0.48,2.13-2.7,3.49-2.07,5.01c0.82,1.97,3.17,0.5,3.9-0.77c0.19-0.35,0.3-0.57,0.43-0.53c0.1,0.03,0.09,0.43,0.03,0.79 c-0.39,2.29-0.91,3.57-2.59,4.88c-0.54,0.42-1.38,0.5-1.27,0.82c0.03,0.08,0.39,0.07,0.68,0.04c4.46-0.29,8.19-5.54,9.18-8.98 c0.1-0.24,0.13-0.47,0.03-0.55c-0.13-0.1-0.33,0.13-0.53,0.31C95.75,193.88,95.05,194.35,94.41,194.55z"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<path
									d="M139.67,215.08c0.02-2.08,1.27-3.95,3.37-3.95c2.44,0,3.39,1.67,3.39,3.95H139.67z M149.09,216.83v-1.25 c0-3.68-2.09-6.28-5.86-6.28c-4.21,0-6.18,3.26-6.18,7.16c0,3.92,1.7,6.95,5.97,6.95c3.18,0,5.51-1.51,5.91-4.53h-2.65 c-0.29,1.93-1.27,2.7-3.23,2.7c-2.57,0-3.43-2.29-3.43-4.74H149.09z"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<rect x="152.14" y="203.87" width="2.52" height="19.13"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<path
									d="M162.56,223v-11.55h3.07v-1.75h-3.07v-2.15c0-1.54,0.74-1.8,2.17-1.8c0.42,0,0.85,0.05,1.27,0.08v-2.09 c-0.59-0.13-1.19-0.27-1.8-0.27c-2.38,0-4.16,1.2-4.16,3.74v2.49h-2.6v1.75h2.6V223H162.56z"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<path
									d="M167.07,209.7v1.75h2.28v8.48c0,1.77,0.03,3.47,3.77,3.47c0.58,0,1.13-0.05,1.72-0.16v-1.93c-0.41,0.1-0.93,0.16-1.33,0.16 c-0.9,0-1.64-0.45-1.64-1.4v-8.61h3.07v-1.75h-3.07v-3.63l-2.52,0.79v2.84L167.07,209.7z"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
								<path
									d="M119,223h6.57c8.18,0,9.04-6.93,9.04-9.57c0-2.64-0.86-9.57-9.04-9.57H119V223z M121.65,206.15h3.92 c4.42,0,6.26,3.34,6.26,7.29c0,3.95-1.84,7.29-6.26,7.29h-3.92V206.15z"
									transform="matrix(1, 0, 0, 1, 0, 2.842170943040401e-14)"
									:style="`fill: ${color_contrast}`" />
							</svg>
						</div>
						<div class="title__text" :style="`color: ${color_contrast}`">
							<span>DELPHI</span>
						</div>
					</div>
				</v-card-text>
			</v-card>
		</div>
	</transition>
</template>

<script setup>
import { onMounted, toRefs, ref } from 'vue';
const props = defineProps({
	color_name: {
		type: String,
		required: true,
	},
	color_hex: {
		type: String,
		required: true,
	},
	color_contrast: {
		type: String,
		required: true,
	},
	poem: {
		type: String,
		required: true,
	}
})
const { color_name, color_hex, color_contrast, poem } = toRefs(props);
const initialMessage = "Anticipate, with patience in your heart,"
	+ "\nAs verses from above shall soon depart,"
	+ "\nAnd like autumn leaves in a gentle breeze,"
	+ "\nYour poem descends, to alight with ease."
const initialWords = initialMessage.split(' ');
const poemWords = poem.value.split(' ');
const initialDisplayedText = ref('');
const displayedText = ref('');
const showInitialMessage = ref(true);

const getRandomChar = () => {
	const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
	return characters.charAt(Math.floor(Math.random() * characters.length));
};

const typeText = (words, displayedProperty, onComplete) => {
	let wordIndex = 0, charIndex = 0, makingMistake = false;
	let mistakeChars = 0, currentMistakeChars = 0, mistakeStartIndex = 0;

	const typeNextChar = () => {
		if (wordIndex >= words.length) {
			setTimeout(onComplete, 2000);
			return;
		}

		makingMistake ||= (Math.random() < 0.1 && charIndex > 0 && charIndex < words[wordIndex].length);

		if (makingMistake && charIndex === mistakeStartIndex) {
			typeMistake();
			return;
		}

		let currentChar = words[wordIndex][charIndex] || ' ';
		const isNewLine = currentChar === '\n';
		displayedProperty.value += currentChar;
		charIndex++;

		if (charIndex > words[wordIndex].length) {
			wordIndex++;
			charIndex = 0;
			if (wordIndex < words.length) displayedProperty.value += ' ';
            let endOfWordDelay = Math.random() * (300 - 100) + 100;
            setTimeout(typeNextChar, endOfWordDelay);
        } else {
            let randomCharInterval = isNewLine ? Math.random() * (800 - 400) + 400 : Math.random() * (120 - 60) + 60;
            setTimeout(typeNextChar, randomCharInterval);
		}
	};

	const typeMistake = () => {
        mistakeChars = Math.floor(Math.random() * 3) + 1;
        currentMistakeChars = 0;
        mistakeStartIndex = charIndex;

        const makeMistake = () => {
            displayedProperty.value += getRandomChar();
            currentMistakeChars++;
            if (currentMistakeChars < mistakeChars) {
                let mistakeTypingSpeed = Math.random() * (150 - 50) + 50;
                setTimeout(makeMistake, mistakeTypingSpeed);
            } else {
                let mistakePauseDuration = Math.random() * (600 - 300) + 300;
                setTimeout(deleteMistake, mistakePauseDuration);
            }
        };
        makeMistake();
    };

    const deleteMistake = () => {
        displayedProperty.value = displayedProperty.value.slice(0, -1);
        currentMistakeChars--;
        if (currentMistakeChars > 0) {
            let mistakeDeletionSpeed = Math.random() * (150 - 50) + 50;
            setTimeout(deleteMistake, mistakeDeletionSpeed);
        } else {
            charIndex = mistakeStartIndex;
            makingMistake = false;
            typeNextChar();
        }
    };

	typeNextChar();
};

const startTypingPoem = () => {
	showInitialMessage.value = false;
	displayedText.value = '';
	setTimeout(() => typeText(poemWords, displayedText, () => { }), 2 * 1000);
};

onMounted(() => {
	setTimeout(() => typeText(initialWords, initialDisplayedText, startTypingPoem), 2 * 1000);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');

.poem_card__wrapper {
	aspect-ratio: 4 / 6;
	height: 90vh;
}

.poem_card {
	position: relative;
	height: 100%;
	width: 100%;
	font: 14px "Lucida Grande", Helvetica, Arial, sans-serif;
}

.poem_card>.v-card-title {
	margin-top: 20%;
	font-size: 50px;
}

.poem_card>.v-card-subtitle {
	white-space: nowrap;
	overflow: hidden;
	text-transform: uppercase;
	text-overflow: ellipsis;
	font-weight: bold;
	font-size: 20px;
	opacity: 0.45;
}

.poem_container {
	display: flex;
	position: absolute;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	aspect-ratio: 1 / 1;
	width: 80%;
	margin: auto;
	padding: 40px;
	text-align: center;
	align-items: center;
	overflow: hidden;
	background-color: rgba(255, 255, 255, 1);
	border-radius: 50%;
	box-shadow: 0 24px 24px rgba(0, 0, 0, 0.2);
}

.poem_inner {
	position: relative;
	height: 100%;
	width: 100%;
	display: flex;
	align-items: center;
}

.poem_inner span {
	max-height: 70%;
	overflow: visable;
	font-family: 'Playfair Display', serif;
	font-size: 150%;
	font-weight: 600;
	line-height: 1.6;
	text-align: center;
	color: #333;
	max-width: 100%;
	margin-left: auto;
	margin-right: auto;
	box-sizing: border-box;
	white-space: pre-line;
}

.title__container {
	position: absolute;
	bottom: 50px;
	left: 0;
	right: 0;
	width: 100%;
	margin-left: auto;
	margin-right: auto;
	height: 23%;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	align-items: center;
	box-sizing: border-box;
}

.title__logo {
	flex: 1;
	width: 90px;
	margin-right: 82px;
	display: flex;
	box-sizing: border-box;
	align-self: flex-end;
}

.title__text {
	flex: 2;
	display: flex;
	justify-content: center;
	margin: 0 auto 27px auto;
	text-transform: uppercase;
	text-shadow: #333 3px 0 5px;
	font-size: 90px;
	font-weight: 600;
	letter-spacing: 15px;
	line-height: 96px;
}

.title__text span {
	font-size: 105px;
	font-weight: bold;
}

.st0 {
	fill: none
}

.initial-message {
	position: absolute;
	top: 0;
	bottom: 0;
	left: 0;
	right: 0;
	margin: auto;
	text-align: center;
	width: fit-content;
	height: fit-content;
}

.initial-message span {
	font-size: 32px;
	font-weight: bold;
	white-space: pre-line;
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 2s;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>
