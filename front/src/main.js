import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'

Vue.config.productionTip = false

// import store from './store/index';
import VModal from 'vue-js-modal';

Vue.use(VModal, { dialog: true });


const routes = [
  {path: '/', component: { template: '<p>home page</p>'}},
  {path: '/app', component: App}
]

const router = new VueRouter({
  routes
})

var vm = new Vue({
  router
}).$mount('#app')

global.vm = vm;