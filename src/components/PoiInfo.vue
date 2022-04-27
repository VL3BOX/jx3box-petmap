<template>
  <div class="m-poi-info">
    <p>{{ pointType }}</p>
    <p>{{ pointDesc }}</p>
    <p>{{ pointCoordinate }}</p>
  </div>
</template>

<script>
export default {
  name: "PoiInfo",
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  computed: {
    pointType: function () {
      switch (this.item.WorkType) {
        case "TRIGGER":
          return "触发点";
        case "LOOT":
          return "前置/其他";
        default:
          return "未知";
      }
    },
    pointCoordinate: function () {
      return `(${this.item.Coordinates.x},${this.item.Coordinates.y},${this.item.Coordinates.z})`;
    },
    pointDesc: function () {
      let type = this.item.ObjectType == 3 ? "NPC" : "交互物件";
      return `(${type}) ${this.item.ObjectID}`;
    },
  },
};
</script>

<style>
</style>