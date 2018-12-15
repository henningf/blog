import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import BlogPost from '@/views/BlogPost'
import CreatePost from '@/views/CreatePost'
import EditPost from '@/views/EditPost'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    {
      path: '/post/:slug',
      name: 'blog-post',
      component: BlogPost
    },
    // Will find a way to merge these into one
    {
      path: '/createpost',
      name: 'create-post',
      component: CreatePost
    },
    {
      path: '/editpost/:slug',
      name: 'edit-post',
      component: EditPost
    }
  ]
})
