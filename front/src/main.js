import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

// import store from './store/index';
import VModal from 'vue-js-modal';

Vue.use(VModal, { dialog: true });

const NotFound = { template: '<p>Page not found</p>' }

const routes = {
  '/': { template: '<p>home page</p>'},
  '/app': App
}

var vm = new Vue({
  computed: {
    ViewComponent () {
      return routes[this.currentRoute] || NotFound
    }
  },
  render: h => h(App),
}).$mount('#app')

global.vm = vm;