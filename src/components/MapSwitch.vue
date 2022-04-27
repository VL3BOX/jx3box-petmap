<template>
  <div class="m-map-switch">
    <span
      class="m-map-switch__item"
      v-for="(item, key) in maps"
      :key="key"
      @click="changeMap(key)"
    >
      <b :class="key == display ? 'active' : ''"></b>
      <span>{{ item.Name }}</span>
    </span>
  </div>
</template>

<script>
export default {
  name: "MapSwitch",
  props: {
    maps: {
      type: Object,
      required: true,
    },
    display: {
      type: Number,
      required: true,
    },
  },
  methods: {
    changeMap(index) {
      this.$emit("onChangeMap", index);
    },
  },
};
</script>

<style lang="less">
</style>