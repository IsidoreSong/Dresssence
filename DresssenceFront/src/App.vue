<template>
  <div id="app"
  @mousemove='mouseMove'
  ref = 'app'
  >
    <control-bar
      ref="controlBar"
    ></control-bar>

    <color-tags
      id='colorTags'
      ref='colorTags'
    ></color-tags>

    <color-square-content
    ></color-square-content>
    
  </div>
</template>

<script>
import colorTags from "./components/colortags.vue";
import colorSquareContent from "./components/colorsquarecontent.vue";
import controlBar from "./components/controlbar.vue";
import { mapState,mapGetters,mapActions } from 'vuex'

export default {
  name: "App",
  components: {
    colorTags,
    colorSquareContent,
    controlBar,
  },
  data() {
    return {
      mouseMove:()=>{}
    };
  },
  computed: {
    ...mapState([
      'colors',
    ]),
    ...mapGetters([
      
    ]),
    
  },
  created() {

    setTimeout(()=>{
      this.mouseMove = this._.throttle((e)=>{
          let [x,y] = [e.pageX,e.pageY]
          this.$refs.colorTags.isOverBasic(x,y)
          
      },40)
      
    },400)
    
    this.axios
      .get("/colorClassifier/get_complete_color")
      .then((response) => {
        // console.log(response.data.color[0])
        this.$store.commit('freshColors',{colors:response.data.color[0]})
      })
      .catch(function (error) {
        console.log(error);
      });
  },
  mounted(){
    console.log(this.$refs.app.offsetWidth)
  },
  methods: {
    ...mapActions([
    ]),

  },
};
</script>
        
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-user-select:none;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
  width:90%;
  margin:0 5%
}

</style>
