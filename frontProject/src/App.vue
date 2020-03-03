<template>
  <div id="app">
    <nav class="navbar navbar-expand-sm bg-light mx-auto fixed-top">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/" tag="a" class="nav-link text-primary">回到首页</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/info" tag="a" class="nav-link text-primary">用户中心</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/write" tag="a" class="nav-link text-primary">写文章</router-link>
        </li>
        <li class="nav-item">
          <router-link to="" tag="a" class="nav-link"></router-link>
        </li>
      </ul>
    </nav>
    <router-view/>
  </div>
  
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
html,body,#app{
  height:100%;
}
#app{
  width:100%;
}
.navbar{
  /* border-bottom: 3px solid rgb(219, 245, 253); */
}
</style>