<template>
    <el-button type="primary" @click="open">链接</el-button>
</template>
  
<script lang="ts" setup>
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { fetchAddLink } from '../api'
const emit = defineEmits(['uploadSuccess'])
const open = () => {
    ElMessageBox.prompt('', '输入链接', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        inputPattern: /^(ftp|http|https):\/\/[^ "]+$/,
        inputErrorMessage: '不是一个有效链接',
    })
        .then(({ value }) => {
            fetchAddLink(value).then(res => {
                emit('uploadSuccess')
            })
        })
        .catch(() => {
        })
}
</script>
  