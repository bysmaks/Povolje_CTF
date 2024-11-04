<template>
  <div class="container">
    <va-card>
      <va-card-title>
        <h2>Cохранить книгу</h2>
      </va-card-title>
      <va-card-content >
        <va-form ref="form" tag="form" @submit.prevent="onSubmit" style="max-width: 500px;">
          <va-input
              v-model="title"
              label="Название"
              style="width: 100%"
              :rules="[(value) => (value && value.length > 0) || 'Введите название']"
          />
          <va-list-label class="ml-3" style="text-align: left;">

          </va-list-label>
          <va-file-upload
              v-model="text"
              type="single"
              :upload-button-text="'Прикрепить книгу'"
              dropzone
              file-types="txt"
              dropzone-text=""
          />

          <div class="container">
            <va-button
                type="Отправить"
                class="mt-3"
            >
              Cохранить
            </va-button>
          </div>
        </va-form>
      </va-card-content>
    </va-card>
  </div>
</template>

<script>
import {requestSaveBook} from "@/api/books";
import router from "@/router";

export default {
  name: "SaveBookView",
  props:['token'],
  data() {
    return {
      file: undefined,
      title: "",
      text: undefined
    };
  },
  methods: {
    onSubmit(){
      if (!this.text){
        this.$vaToast.init({ message: 'Выберите файл с текстом книги', position: 'bottom-right' })
        return
      }
      requestSaveBook(this.token, this.title, this.text, this.file)
          .then((response) => {
            router.push('/books/' + response.uid)
          })
          .catch((error) => {
            this.$vaToast.init({ message: String(error), position: 'bottom-right' })
          });
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
}
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
  padding: 20px;
}
.link-small {
  font-size: 12px;
  margin-top: 10px;
}
h2{

}
</style>