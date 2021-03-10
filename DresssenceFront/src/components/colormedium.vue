<template>
  <div id="colorMedium" 
    :style="{ width:width}" 
    ref="colorMedium"
    :class="['colorMedium',{currentMedium:isCurrent}]"
    >
    <div id='color_tag' 
    :style="{ 'background-color':'rgb' +medium_tag[1]}"
    >
    {{medium_tag[0]}}
    </div>
    <color-basic
        v-for="(color, index) in color_basics"
      :key="index"
      ref = 'colorBasic'
      :isActive='index === active_idx'
      :basic_idx='[medium_idx,index]'
      :style="{
        left: 5+index  * interval + 'px',
        top: 30 + 'px'
      }"
      @mousedown.native='mouseDown(index)'
    >
    </color-basic>
  </div>
</template>
<script>
import colorBasic from './colorbasic.vue'
import {mapState,mapMutations} from 'vuex'
export default {
  name: "colorMedium",
  components:{
      colorBasic
  },
  props: ['medium_idx',],
  data() {
    return {
      active_idx: -1,
      background_color: 'rgb(255,55,55)',
      interval:70,
    };
  },
  computed:{
    ...mapState([
    ]),
    medium_tag(){
      return this.$store.getters.medium_tags[this.medium_idx]
    },
    color_basics(){
      return this.$store.getters.basic_tags[this.medium_idx]
    },
    width(){
      // if(this.isCurrent){
      //   return this.color_basics.length * this.interval + 4 + 'px';
      // }
      return this.color_basics.length * this.interval + 'px';
    },
    isCurrent(){
      return this.medium_idx == this.$store.state.current_tag_idx[0]
    }
    
  },

  methods: {
    ...mapMutations([
      'set_current_tag_idx',
    ]),
    mouseDown(index) {
      // console.log('medium',this.current_tag_idx[1])
      this.$emit('pickColorTag',index)
    },
    isOver(x,y){
        let color_medium = this.$refs.colorMedium
        if(color_medium.offsetLeft<x&& x<color_medium.offsetLeft+color_medium.offsetWidth&&
          color_medium.offsetTop<y&& y<color_medium.offsetTop+color_medium.offsetHeight){
              return true
          }
        return false
    },
    isOverBasic(x,y) {
      let [parentLeft, parentTop] = [
        this.$refs.colorMedium.offsetLeft,
        this.$refs.colorMedium.offsetTop,
      ];
      let [localX, localY] = [x - parentLeft, y - parentTop];
      let x_idx = parseInt(localX/this.interval)
      if(x_idx>=this.color_basics.length){
          this.active_idx = -1;
      }
      else{
          let color_basic = this.$refs.colorBasic[x_idx].$el
          if(color_basic.offsetLeft<localX&& localX<color_basic.offsetLeft+color_basic.offsetWidth
          && color_basic.offsetTop<localY&& localY<color_basic.offsetTop+color_basic.offsetHeight){
              this.active_idx = x_idx
          }
          else {
            this.active_idx = -1;
          }
      }
      return this.active_idx
    },
    
  },
};
</script>

<style scoped>
.colorMedium {
  
  display:inline-block;
  position: relative;
  margin: 5px;
  height:95px;
  border: 2px solid black;
}

#color_tag {
  cursor:pointer;
  margin:4px;
  height:20px;
  font-size:15px;
  line-height:20px;
  border: 1px solid rgb(0, 0, 0);
}

.currentMedium {
  margin: 3px;
  border: 4px solid red;
}
</style>