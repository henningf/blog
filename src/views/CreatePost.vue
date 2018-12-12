<template>
<!-- -->
<v-container fluid grid-list-md>
    <v-flex xs7>
          <v-text-field
            v-model='header_text'
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
        :return-value.sync="activation_date"
        lazy
      >
        <v-text-field
          slot="activator"
          v-model="activation_date"
          label="Datoen innlegget skal vises"
          prepend-icon="event"
          readonly
        ></v-text-field>
        <v-date-picker v-model="activation_date" no-title scrollable>
        </v-date-picker>
      </v-menu>
    </v-flex>
      <v-flex xs12>
        <v-text-field
          v-model="front_page_text"
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
    <editor v-model="editorContent"></editor>
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
  data () {
    return {
      axios,
      header_text: '',
      front_page_text: '',
      snackbar: false,
      y: 'top',
      x: null,
      mode: '',
      timeout: 6000,
      text: 'Hello, I\'m a snackbar',
      activation_date: new Date().toISOString().substr(0, 10),
      menu: false,
      modal: false,
      menu2: false,
      editorContent: '<h2 style="color: #339966;">Hi there from TinyMCE for Vue.js.</h2> <p>&nbsp;</p> <p><span>Hey y`all.</span></p>',
      tinyOptions: {
        'height': 500
      }
    }
  },
  components: {
    'editor': Editor,
    'axios' : axios
  },
  methods: {
    postBlogEntry () {
      axios.post('/addpost', {
        header_text: this.header_text,
        activation_date: this.activation_date,
        front_page_text: this.front_page_text,
        editorContent: this.editorContent
      })
      this.snackbar = true
      /*
      // this.text = 'test'
      // this.snackbar = false
      this.text = 'My balls'
      console.log(this.header_text)
      console.log(this.activation_date)
      console.log(this.front_page_text)
      console.log(this.editorContent)
      */
    }
  }
}
</script>
