<template>
  <div id="colorSquareContent" 
  ref="colorSquareContent"
  :style="{'padding-top':topper_width+'px'}"
  @mousedown='mouseDown'
  @mouseup='mouseUp'>
    <color-square
      v-for="(color, index) in colors"
      ref='colorSquare'
      :key="index"
      :color_idx='index'
      :bgcs='colors[index]'
      :width='width'
      :topper_width='topper_width'
      v-show="index === current_color_idx"
      
    ></color-square>
    <color-mask :position='mask_position'></color-mask>

  </div>
</template>

<script>
import colorSquare from "./colorsquare.vue";
import colorMask from './colormask.vue';
import {mapState,mapGetters} from 'vuex'

export default {
  name: "colorSquareContent",
  components: {
    colorSquare,
    colorMask,
  },
  data() {
    return {
      mask_position:{
        top:'100px',
        left:'100px',
        width:'100px',
        height:'100px'
      },
      width:0,
      topper_width:50,
      tapStart:0
      };
  },
  computed:{
    ...mapState([
      
    ]),
    ...mapGetters({
      current_color_idx:'current_color_idx',
      colors:'color_tags',
    }),
    // current_color_idx(){
    //     return this.$bus.current_color_idx
    // }
  },
  mounted(){
    this.width = this.$parent.$el.offsetWidth * 0.8;
    // console.log(this.$parent.$el.offsetWidth)
    setTimeout(()=>{
      console.log(this.width)
    },500)
  },
  methods: {

    mouseDown(e){
      console.log('content','down')
      let [top,left] = [e.pageY,e.pageX]
      let content = this.$refs.colorSquareContent
      this.$set(this.mask_position,'top',top-content.offsetTop)
      this.$set(this.mask_position,'left',left-content.offsetLeft)
      document.onmousemove = (e) => {
        if(e.pageX<left){
          this.$set(this.mask_position,'left',e.pageX-content.offsetLeft)
          this.$set(this.mask_position,'width',left-e.pageX)
        }
        else{
        this.$set(this.mask_position,'width',e.pageX-left)
        }
        if(e.pageY<top){
          this.$set(this.mask_position,'top',e.pageY-content.offsetTop)
          this.$set(this.mask_position,'height',top-e.pageY)
        }
        else{
        this.$set(this.mask_position,'height',e.pageY-top)
        }
        this.$refs.colorSquare[this.current_color_idx].isOver(this.mask_position)
      };
      document.onmouseup = () => {
        document.onmousemove = null;
        document.onmouseup = null;
        this.$set(this.mask_position,'width',0)
        this.$set(this.mask_position,'height',0)
        this.$set(this.mask_position,'top',0)
        this.$set(this.mask_position,'left',0)
      };
      this.tapStart = new Date().getTime() / 1000
    },
    mouseUp(){
      let tapEnd = new Date().getTime() / 1000
      // console.log(tapEnd-this.tapStart)
      if(tapEnd-this.tapStart < 0.2){
        this.$refs.colorSquare[this.current_color_idx].active =  []
      }
    },

  },
};
</script>

<style scoped>
#colorSquareContent {
  position:relative;

  padding: 0 10%;
}
</style>