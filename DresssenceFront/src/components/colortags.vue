<template>
    <div id='colorTags'>
    <color-medium
    v-for='(color_medium,index) in medium_tags'
    :key='index'
      :medium_idx='index'
      ref="colorMedium"
        
      @pickColorTag='pickColorTag(index,$event)'
    ></color-medium>
    </div>
</template>
<script>

import colorMedium from './colormedium'
import {mapState,mapGetters,mapActions} from 'vuex'

export default {
    name:'colorTags',
    components:{
        colorMedium
    },
    data(){
        return{
        }
    },
    computed:{
        ...mapGetters([
            'medium_tags',
            'current_color',
            'active_color',
        ]),
        ...mapState([
        ]),
        active_idx:{
            get(){
                return this.$bus.active_idx
            },
            set(val){
                this.$bus.active_idx = val
            }
        }
    },
    mounted(){
        this.$store.getters.active_color = ()=>{
            
            return this.$store.getters.idx_to_color(this.$bus.active_idx)
        }

        this.$bus.$on('moveColor', (bgcs)=>{
            if(this.active_idx[1] >=0 && this.active_idx[0]>=0){
                let [current,target] = [this.current_color[1],this.active_color()[1]]
                console.log('square','moveColor',current,target)
                this.$store.dispatch('opColor',{
                    current:current,
                    target:target,
                    bgcs:bgcs,
                    opType:'color',
                });
            }
        })
        
    },
    methods:{
        ...mapActions([
            'opColorBasic',
            'opColor'
        ]),
        pickColorTag(medium_idx,basic_idx) {
            this.$store.commit('set_current_tag_idx',[medium_idx,basic_idx])
            console.log('tags active',this.$store.getters.active_color(),medium_idx,basic_idx)
        },
        isOverMedium(x,y){
            let color_mediums = this.$refs.colorMedium
            for(let i=0;i<color_mediums.length;i++){
                let color_medium = color_mediums[i].$el
                if(color_medium.offsetLeft<x&& x<color_medium.offsetLeft+color_medium.offsetWidth&&
                    color_medium.offsetTop<y&& y<color_medium.offsetTop+color_medium.offsetHeight){
                    return i
                }
            }
            return -1
        },
        isOverBasic(x,y){
            let active_medium_idx = this.isOverMedium(x,y)
            if(active_medium_idx > -1){
                this.active_idx[1] = this.$refs.colorMedium[active_medium_idx].isOverBasic(x,y)
            }
            if(active_medium_idx != this.active_idx[0]){
                if(this.active_idx[0]!=-1){
                    this.$refs.colorMedium[this.active_idx[0]].active_idx = -1
                }
                this.active_idx[0] = active_medium_idx
            }
            // console.log(this.$bus.active_idx)
        },
    }
}
</script>

<style scoped>
#colorTags {
    width:95%;
}

</style>