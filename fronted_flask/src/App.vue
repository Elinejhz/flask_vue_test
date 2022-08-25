<template>
  <v-app id="app">
    <!-- 删除多余的代码，设置 id 属性完成挂载 -->
    <router-view/>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>
