<template>
  <div class="m-petMap" :style="divSize" v-if="dataExist">
    <img class="m-petMap-img" draggable="false" :src="petMap_url" alt="宠物地图" @click="showDesc=false"/>
    <map-switch
      v-if="multiple_Map"
      :maps="mapScales"
      :display="displayMap"
      @onChangeMap="changeMap"
    ></map-switch>
    <poi-info v-if="showDesc" :item="showPoint"></poi-info>
    <span
      class="m-petMap-point"
      v-for="(point, index) in showPosition"
      :key="index"
      @click="showPointInfo(point, index)"
      :style="pointStyle(point.Coordinates, mapScales[displayMap])"
    >
    </span>
  </div>
</template>

<script>
import MapScales from "@/assets/data/MapScales.json";
import PetPOIs from "@/assets/data/PetPOIs.json";
import jx3box_data from "@jx3box/jx3box-common/data/jx3box.json";

import MapSwitch from "@/components/MapSwitch.vue";
import PoiInfo from "@/components/PoiInfo.vue";

export default {
  name: "PetMap",
  components: { MapSwitch, PoiInfo },
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
    }
  },
  data() {
    return {
      positions: {},
      mapScales: {},
      displayMap: 0,
      showDesc: false,
      showPoint: null
    };
  },
  created() {
    let POIs = PetPOIs[`${this.petId}`];
    if(!POIs) return;
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
  methods: {
    changeMap: function (index) {
      this.displayMap = parseInt(index);
      this.showDesc = false;
    },
    pointStyle: function (Coordinates, MapScales) {
      return `left: ${
        (Coordinates.x - MapScales.StartX) * MapScales.Scale * (this.width / 1024) 
      }px; bottom: ${
        (Coordinates.y - MapScales.StartY) * MapScales.Scale * (this.height / 896) }px;`;
    },
    showPointInfo(item) {
      this.showDesc = true;
      this.showPoint = item;
    },
  },
  computed: {
    petMap_url: function () {
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
    divSize: function() {
      return {
        width: this.width + 'px',
        height: this.height + 'px',
      }
    }
  },
};
</script>

<style lang="less">
@import "../../node_modules/csslab/base.less";
@import "../assets/css/petmap.less";
</style>