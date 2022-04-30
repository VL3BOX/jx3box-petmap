<template>
  <div class="m-petmap-warpper" v-if="dataExist">
    <div class="m-petmap" :style="divSize">
      <img
        class="m-petmap-img"
        draggable="false"
        :src="petmap_url"
        alt="宠物地图"
        @click="showDesc = false"
      />
      <map-switch
        v-if="multiple_Map"
        :maps="mapScales"
        :display="displayMap"
        @onChangeMap="changeMap"
      ></map-switch>
      <el-popover
        class="m-petmap-popover"
        placement="top"
        trigger="hover"
        v-for="(point, index) in showPosition"
        :key="index"
        :style="pointStyle(point.Coordinates, mapScales[displayMap])"
      >
        <poi-info :item="point"></poi-info>
        <span class="m-petmap-point" slot="reference"></span>
      </el-popover>
    </div>
  </div>
</template>

<script>
import MapScales from "../../output/MapScales.json";
import PetPOIs from "../../output/PetPOIs.json";
import jx3box_data from "@jx3box/jx3box-common/data/jx3box.json";

import MapSwitch from "./MapSwitch.vue";
import PoiInfo from "./PoiInfo.vue";

export default {
  name: "PetMap",
  components: { PoiInfo, MapSwitch },
  props: {
    petId: {
      type: Number,
      required: true,
    },
    width: {
      type: Number,
      default: 1024,
    },
    height: {
      type: Number,
      default: 896,
    },
  },
  data() {
    return {
      positions: {},
      mapScales: {},
      displayMap: 0,
      showDesc: false,
    };
  },
  created() {
    let POIs = PetPOIs[`${this.petId}`];
    if (!POIs) return;
    for (let mapId of POIs.map((item) => parseInt(item.MapID))) {
      this.mapScales[mapId] = MapScales[mapId][0];
      this.positions[mapId] = [];
      let tmp = POIs.filter((item) => item.MapID === mapId);
      for (let poi of tmp) {
        for (let co of poi.Coordinates) {
          this.positions[mapId].push({
            WorkType: poi.WorkType,
            ObjectID: poi.ObjectID,
            ObjectType: poi.ObjectType,
            MapID: poi.MapID,
            Coordinates: co,
          });
        }
      }
    }
    this.displayMap = parseInt(Object.keys(this.mapScales)[0]);
  },
  mounted() {
    this.$emit("loaded", this.dataExist);
  },
  methods: {
    changeMap: function (index) {
      this.displayMap = parseInt(index);
      this.showDesc = false;
    },
    pointStyle: function (Coordinates, MapScales) {
      return `left: ${
        (Coordinates.x - MapScales.StartX) *
        MapScales.Scale *
        (this.width / 1024)
      }px; bottom: ${
        (Coordinates.y - MapScales.StartY) *
        MapScales.Scale *
        (this.height / 896)
      }px;`;
    },
  },
  computed: {
    petmap_url: function () {
      return `${jx3box_data.__imgPath}map/maps/map_${this.displayMap}_0.png`;
    },
    multiple_Map: function () {
      return Object.keys(this.mapScales).length > 1;
    },
    showPosition: function () {
      return this.positions[this.displayMap] || [];
    },
    dataExist: function () {
      return PetPOIs[`${this.petId}`] != undefined;
    },
    divSize: function () {
      return {
        width: this.width + "px",
        height: this.height + "px",
      };
    },
  },
};
</script>

<style lang="less">
@import "/node_modules/csslab/base.less";
@import "../assets/css/petmap.less";
</style>