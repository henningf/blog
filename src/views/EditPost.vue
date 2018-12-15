<template>
  <Post></Post>
</template>

<script>
import Post from './Post.vue'

export default {
  components: {
    Post
  },
  watch: {
    $route (to, from) {
      this.getPost()
    }
  },
  created () {
    this.getPost()
    this.snackbar = true
  }
}
</script>
