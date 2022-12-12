<template>
  <q-page class="flex justify-center">
    <div>
      
      <div class="row justify-evenly">
        <h2>Try next: {{ nextWord }}
          <q-btn round icon="info" class="q-ml-md">
            <q-tooltip>
              Copy this word paste as a guess in the <a href="https://contexto.me">contexto.me</a>.<br/>
              Then submit the order of the guess in the input field below.<br/>
              If the guess does not work, skip it.<br/>
              It takes 20-30 guesses to get the first result.
            </q-tooltip>
          </q-btn>
        
        </h2>
      </div>


      <!-- input for order -->
      <div class="row justify-center q-gutter-md q-mb-md">
        <q-input
          v-model="nextOrder"
          label="Order"
        />
        <!-- submit button -->
        <q-btn
          label="Submit"
          color="primary"
          @click="submit"
          ></q-btn>
          <!-- skip button -->
        <q-btn
          label="Skip"
          color="deep-orange"
          @click="skip"
          ></q-btn>
      </div>

      <div class="row justify-evenly q-mb-md">
        <a href="https://qdrant.tech/articles/solving-contexto/">How does it work?</a>
      </div>

      <!-- vocabulary -->
      <div class="row justify-evenly">
        <q-list bordered separator>
          <q-item v-for="word in usedWords" :key="word.word">
            <q-item-section>{{ word.word }} - {{ word.order }}</q-item-section>
          </q-item>
        </q-list>
      </div>

    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { axios } from "boot/axios";
import { useQuasar } from "quasar";

let $q;

export default defineComponent({
  name: "IndexPage",
  data: () => ({
    prediction: null,
    nextWord: "human",
    nextOrder: null,
    vocabulary: [
      {
        "word": "you", 
        "order": 10000000,
      },
      {
        "word": "of", 
        "order": 10000000,
      }
    ]
  }),

  created() {
    $q = useQuasar();
    // fetch on init
    // this.predict();
  },

  computed: {
    // computed properties
    usedWords() {
      return this.vocabulary.filter((word) => word.order < 100000);
    },
  },

  methods: {
    async submit() {
      this.vocabulary = [{
        "word": this.nextWord,
        "order": this.nextOrder,
      }, ...this.vocabulary];
      this.nextOrder = null;
      return await this.predict();
    },

    async skip() {
      this.vocabulary = [{
        "word": this.nextWord,
        "order": 10000000,
      }, ...this.vocabulary];
      this.nextOrder = null;
      return await this.predict();
    },

    async predict() {
      try {
        const response = await axios.post("api/predict", {
          "guesses": this.vocabulary
        });
        this.nextWord = response.data.result;
      } catch (e) {
        $q.notify({
          color: "negative",
          position: "top",
          message: "Loading failed: " + e,
          icon: "report_problem",
        });
      }
    },
  },
});
</script>
