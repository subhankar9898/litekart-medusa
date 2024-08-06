<template>
  <div>
    <!-- Add your preferred code block component here, for example, Prism.js -->
    <pre :class="`language-${lang}`"><code v-text="code" /></pre>
  </div>
</template>

<script>
export default {
  props: ['lang', 'code'],
};
</script>
