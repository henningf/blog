<template>
  <v-container grid-list-md text-xs-center>
    <v-slide-y-transition mode="out-in">
      <v-layout row wrap>
      <v-flex xs12 v-for="(post) in posts"
            :key="post.index" >
      <v-card >
        <v-card-media
          :src="post.featured_image"
          height="200px"
        ></v-card-media>

        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">{{ post.title }}</h3>
            <div>{{ post.summary }}</div>
          </div>
        </v-card-title>
        <v-card-actions>
          <v-btn router-link :to="'/post/' + post.slug" flat color="orange">View</v-btn>
        </v-card-actions>
      </v-card>

      </v-flex>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import { butter } from '@/plugins/buttercms'
export default {
  data () {
    return {
      posts: [],
      categories: []
    }
  },
  methods: {
    getPosts () {
      butter.post.list({
        page: 1,
        page_size: 10
      }).then((res) => {
        // console.log(res.data)
        this.posts = res.data.data
      })
    },
    getCategories () {
      butter.category.list()
        .then((res) => {
          console.log('List of Categories:')
          console.log(res.data.data)
        })
    },
    getPostsByCategory () {
      butter.category.retrieve('example-category', {
        include: 'recent_posts'
      })
        .then((res) => {
          console.log('Posts with specific category:')
          console.log(res)
        })
    }
  },
  created () {
    this.getPosts()
    this.getCategories()
    this.getPostsByCategory()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
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
