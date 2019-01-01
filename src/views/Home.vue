<template>
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-container v-for="(post) in posts" :key="post.index">
        <v-card v-on:click="goto_post">
          <v-img class="white--text" height="200px" :src="img_src">
            <v-container fill-height fluid>
              <v-layout fill-height>
                <v-flex xs12 align-end flexbox>
                  <span class="headline">{{ post.Title }}</span>
                </v-flex>
              </v-layout>
            </v-container>
          </v-img>
          <v-card-title>
            <div>
              <span class="grey--text">Date posted: {{ post.Created_at }}</span>
              <br>
              <span>{{ post_content }}</span>
              <br>
            </div>
          </v-card-title>
        </v-card>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      posts: [],
      categories: [],
      img_src: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg',
      post_content: 'This is my first blogpost, on this blog I\'ll write about ...... xx.xx.xxx'
    }
  },
  /*
  mounted () {
    axios
      .get('http://127.0.0.1:5000/api/v1.0/posts')
      .then(response => (this.posts = response))
  }, */
  methods: {
    getPosts () {
      // rewrite this, at first just return all posts this function needs to be written in the backend.
      axios
        .get('http://127.0.0.1:5000/api/v1.0/posts')
        .then(response => (this.posts = response.data.blog_posts))
        .catch(function (error) {
          // handle error
          console.log(error)
        })
        .then(function () {
          // always executed
        })
    },
    goto_post: function (event) {
      // Rewrite this to do something more useful!
      alert(this.post_url)
    }
  },
  created () {
    this.getPosts()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
