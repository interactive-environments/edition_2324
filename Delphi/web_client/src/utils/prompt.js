export const PROMPT = (color, time, weather, location) => {
    return `
    Write a poem that consists or 6 lines and each line can have a maximum of 7 words.
    The poem should primarily focus on the color ${color} and describe it.
    Write in a cryptic but human style and use less corporate jargon. Use a conversational tone and use poetic, beautiful words.
    The following variables can be used to write your poem and make it more unique: The user's chosen colour: ${color}, the current time and date: ${time}, the current weather: ${weather}, the current location: ${location}.
    Do not use the following words in the poem: "${color}", "${weather}", "Admidst", "Hue", and do not directly mention the time or date.
    Finally, make the last sentence an incitement. The limits on the number of lines and line length are very important, so adhere to it.
    `
}

export const PROMPT_no_weather = (color, time, location) => {
    return `
    Write a poem that consists or at most 6 lines and each line can have a maximum of 7 words.
    The poem should primarily focus on the color ${color} and describe it.
    Write in a cryptic but human style and use less corporate jargon. Use a conversational tone and use poetic, beautiful words.
    The following variables can be used to write your poem and make it more unique: The user's chosen colour: ${color}, the current time and date: ${time}, the current location: ${location}.
    Do not use the following words in the poem: "${color}", "Admidst", "Hue", and do not directly mention the time or date.
    Finally, make the last sentence an incitement. The limits on the number of lines and line length are very important, so adhere to it.
    `
}