<template>
  <div id="colorSquare" ref='colorSquare'
    :style="{
        height:height
      }"
    >
    <div
      v-for="(bgc, index) in bgcs"
      ref = 'bgcs'
      :class=" ['squareClass',{'activeClass':active.indexOf(index)>-1}] "
      :key="index"
      :style="{
        'background-color': 'rgb' + bgc[1],
        left: position[index][0] + 'px',
        top: position[index][1] + 'px',
      }"
      @mousedown.stop="mouseDown($event,index)"
    >
      {{ bgc[0] }}
    </div>
  </div>
</template>

<script>
import {mapState,mapGetters} from 'vuex'

export default {
  props: ['width','topper_width','color_idx','bgcs'],
  data() {
    return {
      active: [],
      interval:65,
      tapStart:0,
    };
  },
  computed:{
    lineNumber(){
      return parseInt(this.width * 0.9 / this.interval)
    },
    height(){
      
      let tmp = (parseInt(this.bgcs.length/this.lineNumber)+1)*this.interval + 100
      if(tmp<350){
        tmp = 350
      }
      return tmp +'px'
    },
    // bgcs(){
    //   return this.$store.getters.color_tags[this.color_idx]
    // },
    position(){
      return new Array(this.bgcs.length).fill('').map((item,index)=>[
        (index % this.lineNumber) * this.interval , 
        parseInt(index / this.lineNumber) * this.interval ])
    },
    ...mapState([
    ]),
    ...mapGetters([
    ])
  },
  methods: {
    isOver(mask_position){
      // console.log()
      let square = this.$refs.colorSquare
      let left = parseInt((mask_position['left']-square.offsetLeft) / this.interval+1)
      let top = parseInt((mask_position['top']-this.topper_width) / this.interval+1)
      let width = parseInt((mask_position['width']-(left*this.interval-mask_position['left']+square.offsetLeft)+20)/ this.interval)
      let height = parseInt((mask_position['height']-(top*this.interval-mask_position['top']+50)+20)/ this.interval)
      width= width > this.lineNumber-left?this.lineNumber-left:width
      
      this.active = []
      for(let j=0;j<height;j++){
        for(let i=0;i<width;i++){
          let idx = i+left+(j+top)*this.lineNumber
          if(idx<this.bgcs.length){
            this.active.push(idx)
          }
        }
      }
    },

    mouseDown(event,index) {
      let flag = true
      if(this.active.indexOf(index) == -1){
        this.active.push(index)
        flag = false
      }
      let [bgcs,origin] = [[],[]]
      for(let i=0;i<this.active.length;i++){
        origin.push([this.position[this.active[i]][0],this.position[this.active[i]][1]])
        bgcs.push(this.bgcs[this.active[i]])
      }
      document.onmousemove = (e) => {
  
        for(let i=0;i<this.active.length;i++){
          this.$refs.bgcs[this.active[i]].style.left = e.clientX-event.clientX+origin[i][0] + 'px'
          this.$refs.bgcs[this.active[i]].style.top = e.clientY-event.clientY+origin[i][1]+ 'px'
        }
      };
      document.onmouseup = () => {
        document.onmousemove = null;
        document.onmouseup = null;
        for(let i=0;i<this.active.length;i++){
          this.$refs.bgcs[this.active[i]].style.left = origin[i][0] + 'px'
          this.$refs.bgcs[this.active[i]].style.top = origin[i][1]+ 'px'
        }
        if(this.$bus.active_idx[1] >=0 && this.$bus.active_idx[0]>=0){
          console.log('sqare',bgcs)
          this.$bus.$emit('moveColor',bgcs)
          this.active = []
        }
        else{
          let tapEnd = new Date().getTime() / 1000
          if(tapEnd-this.tapStart < 0.2 &&flag){
            this.active.splice(this.active.indexOf(index),1)
          }
        }
      };
      this.tapStart = new Date().getTime() / 1000
      
    },
  },
};
</script>

<style scoped>
#colorSquare {
  position: relative;
  margin: 0 5%;
}

.squareClass {
  position: absolute;
  display: block;
  cursor: pointer;
  width: 56px;
  height: 56px;
  text-align: center;
  line-height: 56px;
  font-size: 4px;
}

.activeClass{
  border: 3px solid black;
  width:56px;
  height:56px;
  line-height:56px;
  z-index:100;
}
</style>