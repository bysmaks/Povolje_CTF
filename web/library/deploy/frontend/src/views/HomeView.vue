<template>
  <div class="container">
    <div class="centers">
      <h1>Library</h1>
      <p> Большое хранилище для Ваших книг</p>
    </div>
    <div>


    <va-stepper
        v-model="step"
        :steps="steps"
        controlsHidden
    >
      <template #step-content-0>
        <ul>
          <li>Первым делом необходимо пройти регистрацию </li>
          <li v-if="token === null"><router-link  to="/register">Регистрация</router-link></li>
        </ul>
      </template>
      <template #step-content-1>
        <ul>
          <li>Выберите книгу, которую вы хотите сохранить</li>
          <li>Введите название книги</li>
          <li>Выберите и загрузите книгу </li>
          <li v-if="token !== null"><router-link  to="/book/save">Сохранить книгу</router-link></li>
        </ul>

      </template>
    </va-stepper>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  props: ['token'],
  data(){
    return {
      step: 0,
      steps: [
        { label: 'Регистрация' },
        { label: 'Добавить книгу' },
        { label: 'Сохранить книгу' }
      ]
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 80vh;
  background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0) 20%, rgba(246, 246, 246, 1) 70%), url(/src/assets/mine_library.jpg);
  background-size: cover;
  padding: 20px;
  margin-top: -20px;
}
.centers{
  text-align: center;
  margin-top: 15px;
  margin-bottom: 15px;
}
ul:not([class^=va])>li {
  list-style: none;
  padding: 0 1rem;
  position: relative;
}
ul:not([class^=va])>li:before {
  background-color: var(--va-li-background);
  border-radius: 50%;
  content: "";
  height: 0.5rem;
  left: 0;
  margin-top: 0.5rem;
  position: absolute;
  top: 0;
  width: 0.5rem;
}
h1 {
  font-size: 2em;
}
</style>