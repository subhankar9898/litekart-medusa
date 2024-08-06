<template>
  <div>
    <div class="tabs">
      <div
        v-for="(tab, index) in tabs"
        :key="index"
        :class="{ active: activeTab === index }"
        @click="setActiveTab(index)"
      >
        {{ tab.title }}
      </div>
    </div>
    <div class="code-content">
      <div v-if="tabs.length > 0" v-html="tabs[activeTab].code" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 0,
      tabs: [{ title: 'html' }, { title: 'css' }],
    }
  },
  methods: {
    setActiveTab(index) {
      this.activeTab = index
    },
  },
  // mounted() {
  //   this.tabs = this.$slots.default.filter(
  //     (slot) => slot.type && slot.type.name === 'CodeBlock'
  //   );
  // },
}
</script>

<style>
/* Add your styling for tabs and active tab here */
</style>
