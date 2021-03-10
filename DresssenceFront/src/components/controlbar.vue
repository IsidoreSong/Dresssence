<template>
  <div id="controlBar">
    <input
      class="left input"
      v-model="color_basic_tag"
      type="text"
      placeholder="添加色类名称"
    />
    <!--<button class="left mt-20" @click="$emit('addColorBasic', color_basic)">-->
    <button class="left mt-20" @click="addColorBasic(color_basic_tag)">
      添加色类
    </button>
    <button class="left m-20" @click="removeColorBasic">
      删除色类
    </button>
    <input
      class="left input"
      v-model="color_medium_tag"
      type="text"
      placeholder="添加色组名称"
    />
    <button class="left mt-20" @click="addColorMedium(color_medium_tag)">
      添加色组
    </button>
    <button class="left m-20" @click="removeColorMedium">
      删除色组
    </button>
    <button class="right m-20" @click="save">保存</button>
    <button class="right m-20" @click="restore">恢复</button>
    <button class="right m-20" @click="revoke">撤销</button>

    <input class="checkbox" id="autoSave" type="checkbox" v-model="autoSave" />
    <label for="autoSave">自动保存</label>
  </div>
</template>

<script>
import { mapState,mapGetters,mapActions } from 'vuex'

export default {
  name: "controlBar",
  data() {
    return {
      color_basic_tag: undefined,
      color_medium_tag:undefined,
    };
  },
  computed:{
    
    ...mapState([
      'current_tag_idx',
    ]),
    ...mapGetters([
      'current_color_idx',
      'color_medium',
      'color_basic',
      'basic_tags',
      'color_tags',
      'current_color',
    ]),
    autoSave:{
      get(){
        return this.$store.autoSave
      },
      set(val){
        this.$store.commit('set_autoSave',val)
      }
    }
  },
  methods:{
    ...mapActions([
      'opColorBasic',
      'opColorMedium',
      'save',
      'revoke',
      'restore'
    ]),
    
    addColorBasic(color_name) {
      if (color_name == undefined) {
        color_name = 'W'
        // alert("请先添加色类名称！");
        // return;
      }
      let color_tag = [color_name, "(255,255,255)",[]];
      this.opColorBasic({
        current:-1, 
        target:[this.color_medium('待定'),color_tag],
        opType:'basic'
      })
      
    },
    removeColorBasic() {
      let color_tag = this.current_color[1];
      if(color_tag[0]=='待定'){
        alert('禁止删除待定区！')
        return;
      }
      // if(this.basic_tags[this.current_tag_idx[0]].length == 1){
      //   alert('这是本组的最后一个色类，若要删除,请直接删除色组！')
      //   return 
      // }
      // if(this.color_tags[this.current_color_idx].length > 0){
      //   alert('无法删除含有色块的色类！')
      //   return 
      // }
      this.opColorBasic({
        current:this.current_color, 
        target:-1,
        opType:'basic'});
    },
    addColorMedium(color_name) {
      if (color_name == undefined) {
        // alert("请先添加色类名称！");
        // return;
        color_name = 'W'
      }
      let color_tag = [color_name, "(255,255,255)",];
      this.opColorMedium({
        current:-1, 
        target:[...color_tag,[[...color_tag,[]]]],
        opType:'medium'
        });
    },
    removeColorMedium() {
      // alert('正在删除色组！')
      let color_tag = this.current_color[0];
      if(color_tag[0]=='待定'){
        alert('禁止删除待定区！')
        return;
      }
      // for(let i=0;i<this.basic_tags[this.current_tag_idx[0]].length;i++){
      //   if(this.current_color[0][2][i][2].length > 0){
      //     alert('无法删除含有色块的色类！')
      //     return 
      //   }
      // }
      this.opColorMedium({
        current:this.current_color[0], 
        target:-1,
        opType:'medium'
        });
    },
  }
};
</script>

<style scoped>
#controlBar {
  margin: 10px 0;
  height: 80px;
}
button {
  width: 80px;
  height: 30px;
  font-size: 14px;
}
.right {
  float: right;
}
.left {
  float: left;
}
.m-20 {
  margin: 10px;
}

.mt-20 {
  margin-top: 10px;
}

.input {
  margin: 10px 0;
  width: 150px;
  height: 23px;
  font-size: 14px;
}
label {
  float: right;
  margin-top: 10px;
  width: 120px;
  height: 30px;
  font-size: 18px;
  text-align: right;
  line-height: 30px;
}

.checkbox {
  float: right;
  margin-top: 10px;
  width: 30px;
  height: 30px;
  font-size: 14px;
}
</style>