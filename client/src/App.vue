<script setup>
import { onBeforeMount, ref, watch, onMounted, nextTick } from 'vue';
import { fetchDcoList, fetchQuery, fetchMsg, fetchDelDoc } from './api'
import { ElMessage } from 'element-plus'
import Upload from './views/Upload.vue'
import Loading from '@/assets/loading.svg?component'
import { docState, formatByteSize, docType, nameWithoutExt, docUrl, showLastMessage } from './utils'
import { DeleteFilled } from '@element-plus/icons-vue'
import AddLink from './views/AddLink.vue';
var docList = ref([])
var active = ref(null)
watch(active, () => {
  loadMsg()
})

function loadDos() {
  fetchDcoList().then(res => {
    docList.value = res?.data || []

    if (active.value == null && docList.value.length > 0) {
      const doc = docList.value[0]
      active.value = doc
    }
  })
}

var messages = ref([])
var askErr = ref()
function loadMsg() {
  fetchMsg(active.value.doc_id).then(res => {
    if (res.code) {
      askErr.value = res.message
      ElMessage.error(res.message)
    } else {
      messages.value = res.data || []
    }
    showLastMessage(1000)
  })
}

onBeforeMount(() => {
  loadDos()
})

const uploadSuccess = () => {
  loadDos()
  loadFileState()
}

const changeDoc = (doc) => {
  active.value = doc
}

var msgLoading = ref(false)
var input = ref('')
function query() {
  if (!input.value) {
    return
  }
  messages.value.push({
    content: input.value,
    role: 'user'
  })
  showLastMessage()
  msgLoading.value = true
  fetchQuery(active.value.doc_id, input.value).then(res => {
    messages.value.push({
      content: res?.data?.response || '',
      role: 'chatdoc'
    })
    showLastMessage()
    msgLoading.value = false
  })
  input.value = ""
}

const refInput = ref(null)
const getFocus = () => {
  nextTick(() => {
    refInput.value.focus();
  })
}
onMounted(() => {
  getFocus()
})

function delDoc(doc_id) {
  if (active.value.doc_id == doc_id) {
    active.value = null
  }
  if (active.value == null && docList.value.length > 0) {
    const doc = docList.value[0]
    active.value = doc
  }

  fetchDelDoc(doc_id).then(() => {
    loadDos()
  })
}

const loadFileState = () => {
  if (docList.value.filter(e => e.state != 2).length > 0) {
    setTimeout(() => {
      loadDos()
      loadFileState()
    }, 2000)
  }
}

const onerror = (e) => {
  console.log(e)
}
</script>

<template>
  <div class="container">
    <div class="sidebar">
      <div style="overflow-y: scroll;">
        <div class="add-doc">
          <Upload @upload-success="uploadSuccess" />
          <AddLink @upload-success="uploadSuccess" />
        </div>
        <div class="doc-list" v-for="(item) in docList" :key="item.doc_id">
          <div :class="{ 'doc-item': true, ellipsis: true, 'doc-active': item.doc_id === active.doc_id }"
            :title="item.doc_name" @click="changeDoc(item)">
            <div class="doc-item-title">
              <span style="display: inline-block; width: 70%; overflow: hidden; text-overflow: ellipsis;">{{
                nameWithoutExt(item.doc_name) }}</span>
              <el-icon @click.stop="delDoc(item.doc_id)" class="remove-icon">
                <DeleteFilled />
              </el-icon>
            </div>
            <div class="doc-item-info">
              <span class="doc-item-info-cell">type: {{ docType(item) }}</span>
              <span class="doc-item-info-cell">size: {{ formatByteSize(item.size || 0) }}</span>
              <span class="doc-item-info-cell">index: {{ docState(item.state) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="user-info">
        <el-avatar :size="50" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
        <span class="user-name">Anonymous</span>
      </div>
    </div>
    <div class="doc">
      <div v-if="docList.length == 0" class="empty-info">
        <div>当前没有文档, 请先上传</div>
        <div>
          <Upload @upload-success="uploadSuccess" />
        </div>
      </div>
      <iframe v-if="docList.length > 0 && active" :src="docUrl(active)" style="width:100%;height: 100%;"
        :key="active.doc_id" @onerror="onerror"></iframe>
    </div>
    <div class="chat">
      <div id="messages" class="messages">
        <div :class="{ 'message-item': true, 'message-user': item.role == 'user' }" v-for="(item, index) in messages"
          :key="index">
          {{ item.content }}
        </div>
      </div>
      <div class="loading">
        <el-icon :size="30" v-if="msgLoading">
          <Loading />
        </el-icon>
      </div>
      <input ref="refInput" class="input" :placeholder="active?.state != 2 ? '索引构建中...' : '开始与你的文档对话吧'"
        :disabled="active?.state != 2 || msgLoading" v-model="input" @keyup.up.enter="query" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.ellipsis {
  width: 300px;
  overflow: hidden;
  /*文本不会换行*/
  white-space: nowrap;
  /*当文本溢出包含元素时，以省略号表示超出的文本*/
  text-overflow: ellipsis;
}

.empty-info {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  color: #CDD0D6;
  font-size: 18px;
  align-items: center;
  justify-content: center;
}

.container {
  display: flex;
  width: 100%;
  height: 100vh;

  .sidebar {
    display: flex;
    width: 200px;
    width: 15%;
    flex-direction: column;
    justify-content: space-between;

    .add-doc {
      display: flex;
      padding: 10px;
      align-items: center;
      justify-content: space-between;
    }

    .doc-list {
      display: flex;
      align-items: center;
      justify-content: center;

      &:last-child .doc-item {
        border-bottom: none;
      }

      .doc-item {
        width: 100%;
        padding: 3px 10px;
        display: flex;
        flex-direction: column;
        border-bottom: 1px solid gray;

        .doc-item-title {
          display: flex;
          font-size: 14px;
          height: 28px;
          line-height: 28px;
          justify-content: space-between;

          .remove-icon {
            color: #CDD0D6;
            height: 100%;

            &:hover {
              color: #79bbff;
            }
          }
        }

        .doc-item-info {
          display: flex;
          font-size: 10px;
          color: gray;
          height: 10px;
          line-height: 10px;
          justify-content: space-between;

          .doc-item-info-cell {
            margin: 0 2px;
          }
        }
      }

      .doc-active {
        background-color: #a0cfff;
      }
    }

    .user-info {
      padding: 20px;
      height: 30px;
      display: flex;
      align-items: center;
      border-top: 1px solid #EBEDF0;

      .user-name {
        margin: 0 10px;
        color: #CDD0D6;
        font-size: 14px;
      }
    }
  }

  .doc {
    width: 55%;
    display: flex;
    border-right: 1px solid #EBEDF0;
    border-left: 1px solid #EBEDF0;
  }

  .chat {
    width: 30%;
    flex-direction: column;
    justify-content: space-between;
    display: flex;

    .messages {
      display: flex;
      flex-direction: column;
      padding: 10px;
      overflow-y: scroll;

      .message-item {
        border: 1px solid #CDD0D6;
        padding: 10px;
        margin: 5px 0;
      }

      .message-user {
        background-color: #a0cfff;
      }
    }

    .input {
      margin: 10px;
      padding: 10px;
      height: 30px;
      line-height: 30px;
      border: 1px solid blue;
      background-image: url('assets/send.svg');
      background-repeat: no-repeat;
      background-position: 10px;
      padding-left: 40px;
    }

    .loading {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
