<template>
  <div ref='colorBasic'
  :class="['colorBasic',{currentBasic: isCurrent}]"
  :style="{'background-color':background_color}"
  @mousedown='mouseDown'
>

      {{ basic_tag[0] }}
  </div>
</template>

<script>
import {mapState,mapGetters,mapActions} from 'vuex'

export default {
  name:'colorBasic',
  props:['basic_idx','isActive'],
  computed:{
    ...mapState([
      'current_tag_idx',
    ]),
    ...mapGetters([
      'current_color',
      'active_color',
    ]),
    isCurrent(){
      return this.basic_idx.toString() == this.current_tag_idx.toString()
    },
    basic_tag(){
      return this.$store.getters.basic_tags[this.basic_idx[0]][this.basic_idx[1]]
    },
    background_color(){
      if(this.isActive){
        return 'red'
      }
      else{
        return 'rgb'+this.basic_tag[1]
      }
    }
  },
  methods:{
    ...mapActions([
      'opColorBasic'
    ]),

    moveColorBasic(){
      console.log('basic','mvCB')
      
      if(this.current_color[0][2].length == 1){
        alert('这是色组中的最后一个类，无法直接移动！')
        return 
      }
      this.opColorBasic({
        current:this.current_color,
        target:[this.active_color()[0],this.current_color[1]],
        opType:'basic',
      })
    },
    mouseDown(event) {
      let basic = this.$refs.colorBasic
      let [origin_x,origin_y] = [parseInt(basic.style.left.slice(0,-2)),parseInt(basic.style.top.slice(0,-2))]
      document.onmousemove = (e) => {
          basic.style.left = e.clientX-event.clientX + origin_x + 'px'
          basic.style.top = e.clientY-event.clientY + origin_y + 'px'
      };
      document.onmouseup = () => {
        document.onmousemove = null;
        document.onmouseup = null;
        basic.style.left = origin_x  + 'px'
        basic.style.top = origin_y + 'px'
        console.log('basic act',this.$bus.active_idx)
        if(this.$bus.active_idx[0] != this.current_tag_idx[0] && this.$bus.active_idx[0] >= 0){
          this.moveColorBasic()
        }
        
      };
      
    },
  }
}
</script>

<style scoped>

.colorBasic {
  box-sizing:border-box;
  position: absolute;
  height: 60px;
  width: 60px;
  font-size: 14px;
  line-height:60px;
  border: 1px solid rgb(0, 0, 0);
}
.currentBasic {
  border: 5px solid rgb(0, 0, 0);
  height: 60px;
  width: 60px;
  line-height:50px;
  z-index:10;
}
.mt0 {
  margin-top:0;
}


</style>