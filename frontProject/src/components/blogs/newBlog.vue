<template>
    <div>
        <h3 class="d-inline text-primary">分类:&nbsp;&nbsp;&nbsp;&nbsp;</h3>
        <select class="form-control" v-model="tag">
            <option v-for="item in sortItems" :key="item">{{item}}</option>
        </select>
    </div>
</template>