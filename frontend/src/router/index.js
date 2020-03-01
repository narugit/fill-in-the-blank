import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/DrawField'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'DrawField',
      component: HelloWorld
    }
  ]
})
