<template>
    <v-container grid-list-md text-xs-center>
        <v-layout row wrap>
            <v-flex xs12>
                <v-img height="200px" :src="blogpost.feature_image"></v-img>
            </v-flex>
            <v-flex xs10 wrap="true">
                <div v-html="blogpost.Body"></div>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'show-post',
  data () {
    return {
      blogpost: {}
    }
  },
  methods: {
    getPost () {
      var postName = this.$route.params.slug
      // Really need to refactor so that I can load link to api from a single site
      var posturl = 'http://127.0.0.1:5000/post/' + postName
      axios.get(posturl).then(response => {
        this.blogpost = response.data
        console.log(response.data)
      })
    }
  },
  mounted () {
    this.getPost()
  }
}
</script>

<style>

</style>
