import Vue from 'vue'
import store from './store'
import EventBus from './store/store'
import axios from 'axios'
import _ from 'lodash'
import App from './App.vue'


Vue.config.productionTip = false
Vue.prototype.axios = axios;
Vue.prototype._ = _;
Vue.prototype.$bus = EventBus

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
