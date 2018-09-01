<template>
  <v-container grid-list-md>
    <v-slide-y-transition mode="out-in">
      <v-layout row wrap>
      <v-flex xs12 wrap="true">
        <div v-html="post.data.body"></div>
      </v-flex>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import { butter } from '@/plugins/buttercms'
export default {
  name: 'blog-post',
  data () {
    return {
      post: {}
    }
  },
  methods: {
    getPost () {
      butter.post
        .retrieve(this.$route.params.slug)
        .then(res => {
          // console.log(res.data)
          this.post = res.data
        })
        .catch(res => {
          console.log(res)
        })
    }
  },
  watch: {
    $route (to, from) {
      this.getPost()
    }
  },
  created () {
    this.getPost()
  }
}
</script>

<style>
  img {
  max-width: 100%;
  padding-right: 5px;
  padding-left: 5px;
}
</style>
