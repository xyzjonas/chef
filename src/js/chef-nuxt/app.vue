<template>
  <NuxtLoadingIndicator />
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script lang="ts" setup>
useHead({
  script: [
    {
      textContent: `
      let myTheme = localStorage.getItem("theme");
      console.info("my theme on startup:")
      console.info(myTheme)
      if (!myTheme) {
        const isDarkSchemePreferred = window?.matchMedia?.('(prefers-color-scheme:dark)')?.matches ?? false;
        myTheme = isDarkSchemePreferred ? 'dark' : 'light';
        localStorage.setItem('theme', myTheme);
      }

      document.documentElement.setAttribute('data-theme', myTheme)
      document.body.style.display = "block"
      `,
      tagPosition: "head",
      type: "text/javascript",
    },
  ],
});
</script>

<style lang="css">
:root {
    
    --primary-100:#2cbd83;
    --primary-200:#d2f9e4;
    --accent-100:#2C3E50;
    --accent-200:#b4c7dd;
    
    --color-success: var(--primary-100);
    --color-danger: #9B1C31;

    --success-100: var(--color-success);
    --error-100: var(--color-danger);

    --input-border: var(--color-grey-dark-1);
    --input-focus-h: 245;
    --input-focus-s: 100%;
    --input-focus-l: 42%;

    /* actual color tokens
    --bg-100: #000000;
    --bg-200:#141414;
    --bg-300:#404040;
    --bg-100: red; */
    --text-white:#FDF2FA;
    --text-black:#273440;
    --text-over-primary: #ffffff;
    --text-over-danger: #ffffff;
}

:root, html[data-theme="light"] {
    --bg-100: #f8faf9;
    --bg-200: #f8fafc;
    --bg-300:#adadad;

    --border-100: #e2e8f0;

    --text-100: var(--text-black);
    --text-over-secondary: #ffffff;

    --shadow-100: #141414;

    --secondary-100: #0f172a;
}

html[data-theme="dark"] {
    --bg-100: #000000;
    --bg-200:#141414;
    --bg-300:#404040;

    --border-100: #202020;

    --text-100: var(--text-white);
    --text-over-secondary: #e0e0e0;

    --shadow-100: #585858;

    --secondary-100: #404040;
}

a {
    text-decoration: none;
}

a:link, a:visited {
    color: var(--color-font-light);
}


body {
  /* font-family: "Roboto", sans-serif; */
  display: none;
  font-weight: 400;
  line-height: 1.4;
  color: var(--text-100);
  background-color: var(--bg-100);
  touch-action: pan-x pan-y;
}

.page {
  width: min(100% - .7rem, 960px);
  margin-inline: auto;
}

.icon {
  display: inline-block;
}

* {
  margin: 0;
  padding: 0;
  font: inherit;
}

*,
*::before,
*::after {
    box-sizing: border-box;
}

.page-enter-active,
.page-leave-active {
  transition: all 0.4s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(1rem);
}

.content h1 {
  font-size: 2.5rem;
  line-height: 2.5rem;
  margin-bottom: .5rem;
  text-transform: uppercase;
}

hr {
  border-bottom: none;
  margin-block: 1.5rem;
  border-color: var(--border-100);
}

.content blockquote {
  background-color: var(--bg-200);
  padding: 0.5rem;
  padding-left: 1rem;
  margin-block: 0.5rem;
  border: 1px solid var(--border-100);
  border-left: 2px solid var(--primary-100);
  box-shadow: 0 10px 30px -12px var(--border-100);
  border-top-right-radius: .5rem;
  border-bottom-right-radius: .5rem;
}

.content strong {
  font-weight: 600;
}

.content h3 {
  font-size: 1.5rem;
  text-transform: uppercase;
}

.content ol, .content ul {
  margin: 0;
  padding: 0;
  padding-left: 0.5rem;
}

.content ol {
  list-style: decimal-leading-zero;
  list-style-position: inside;
}

.content ul {
  padding-left: 2rem;
}

.content ol li {
  margin-block: 1rem;
}

.content li::marker {
  font-weight: 500;
  font-size: 1.5rem;
}
</style>