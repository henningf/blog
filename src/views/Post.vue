<template>
<!-- -->
<v-container fluid grid-list-md>
    <v-flex xs7>
          <v-text-field
            v-model='blogpost.post_name'
            label='This is the post name'
            placeholder="Dette er navnet på posten"
            outline
          ></v-text-field>
        </v-flex>
        <v-flex xs7>
          <v-text-field
            v-model='blogpost.header_text'
            label='This is the header text'
            placeholder="Dette er teksten som kommer i headeren"
            outline
          ></v-text-field>
        </v-flex>
        <v-flex xs3>
      <v-menu
        ref="menu"
        :close-on-content-click="false"
        v-model="menu"
        :return-value.sync="blogpost.activation_date"
        lazy
      >
        <v-text-field
          slot="activator"
          v-model="blogpost.activation_date"
          label="Datoen innlegget skal vises"
          prepend-icon="event"
          readonly
        ></v-text-field>
        <v-date-picker v-model="blogpost.activation_date" no-title scrollable>
        </v-date-picker>
      </v-menu>
    </v-flex>
      <v-flex xs12>
        <v-text-field
          v-model="blogpost.front_page_text"
          name="input-7-1"
          label="Info på forsiden, kort tekst"
          placeholder="Infotekst rundt blogginlegget (kort sammendrag)"
          outline
        ></v-text-field>
      </v-flex>
      <v-flex xs12>
  <div class="about">
      <!-- https://github.com/tinymce/tinymce-vue -->
    <h1>TinyMCE Quick start guide</h1>
    <editor v-model="blogpost.blog_body"></editor>
  </div>
      </v-flex>
      <v-flex xs4>
      <div>
        <v-btn depressed large
        @click="postBlogEntry()">Post blogginlegg</v-btn>
      </div>
    </v-flex>
        <v-snackbar
      v-model="snackbar"
      :bottom="y === 'bottom'"
      :left="x === 'left'"
      :multi-line="mode === 'multi-line'"
      :right="x === 'right'"
      :timeout="timeout"
      :top="y === 'top'"
      :vertical="mode === 'vertical'"
    >
      {{ text }}
    </v-snackbar>
</v-container>
</template>

<script>
import Editor from '@tinymce/tinymce-vue'
import axios from 'axios'
export default {
  name: 'Post',
  data () {
    return {
      blogpost: {
        post_name: '',
        header_text: '',
        activation_date: new Date().toISOString().substr(0, 10),
        front_page_text: '',
        blog_body: '<h2 style="color: #339966;">Hi there from TinyMCE for Vue.js.</h2> <p>&nbsp;</p> <p><span>Hey y`all.</span></p>'
      },
      axios,
      snackbar: false,
      y: 'top',
      x: null,
      mode: '',
      timeout: 6000,
      text: 'Hello, I\'m a snackbar',
      menu: false,
      modal: false,
      menu2: false,
      tinyOptions: {
        'height': 500
      }
    }
  },
  components: {
    'editor': Editor,
    'axios': axios
  },
  methods: {
    postBlogEntry () {
      var posturl = 'http://127.0.0.1:5000/post/' + this.blogpost.post_name
      axios.post(posturl, {
        post_name: this.blogpost.post_name,
        header_text: this.blogpost.header_text,
        activation_date: this.blogpost.activation_date,
        front_page_text: this.blogpost.front_page_text,
        blog_body: this.blogpost.blog_body
      })
      this.snackbar = true
    },
    getPost () {
      var postName = this.$route.params.slug
      var posturl = 'http://127.0.0.1:5000/post/' + postName
      axios.get(posturl).then(response => {
        this.blogpost = response.data
      })
    }
  }
}
</script>
