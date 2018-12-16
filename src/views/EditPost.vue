<template>
  <Post ref="postReference"></Post>
</template>

<script>
import Post from './Post.vue'

export default {
  components: {
    'Post': Post
  },
  mounted () {
    this.$refs.postReference.getPost()
  },
  data () {
    return {
      blogpost: {
        post_name: 'kamel'
      }
    }
  }
  // props: ['blogpost'],
  /*
  watch: {
    $route (to, from) {
      this.getPost()
    }
  }, */
}
</script>
