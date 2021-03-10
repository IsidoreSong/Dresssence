import Vue from 'vue'
// import axios from 'axios'

var EventBus = new Vue({
    data: {
        active_idx: [-1, -1],
        active_color: [undefined, undefined],
    },
})

export default EventBus

