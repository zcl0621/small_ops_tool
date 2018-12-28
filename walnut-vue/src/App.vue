<template>
  <div id="app">
    <el-container>
      <el-header class="header">
      <vheader></vheader>
      </el-header>
    </el-container>
    <el-container>
      <el-main>
        <vmain></vmain>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Header from '@/layout/Header'
import Main from '@/layout/Main'
export default {
  name: 'App',
  components: {
    'vheader': Header,
    'vmain': Main
  }
}
</script>

<style>
.header {
  background-color: #409EFF;
  color: #fff;
  line-height: 60px;
}
body {
  margin: 0px
}
</style>
