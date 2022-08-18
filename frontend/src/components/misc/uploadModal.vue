<template>
    <div class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title h4">File Upload</div>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body overflow-auto" style="height:75vh;">
                    <table class="table table-hover">
                        <thead class="thead-light">
                            <tr>
                                <th colspan="1">Stackname</th>
                                <th colspan="1">Slizes</th>
                                <th colspan="1">Size (Mb)</th>
                                <th colspan="1">Upload Progress %</th>
                                <th colspan="1"></th>
                                <th colspan="1"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="(data, foldername) in filesGroupedByFolders" :key="foldername">
                                <tr>
                                    <td colspan="1" class="align-middle">{{foldername}}</td>
                                    <td colspan="1" class="align-middle">{{data.slices}}</td>
                                    <td colspan="1" class="align-middle">{{Number(data.size/(1024*1024)).toFixed(2) }}</td>
                                    <td colspan="1" class="align-middle">{{uploadProgressFolder(data.files)}}</td>
                                    <td colspan="1" class="align-middle" data-bs-toggle="collapse" :data-bs-target="'#' + foldername"><button class="btn btn-primary">show files</button></td>
                                    <td colspan="1" class="align-middle"><button class="btn btn-danger">remove</button></td>
                                </tr>
                                <tr class="collapse" :id="foldername">
                                    <td colspan="6">
                                      <div class="overflow-auto" style="max-height:200px;">
                                        <table class="table table-dark table-borderless">
                                            <thead class="">
                                                <tr colspan="5">
                                                    <th colspan="2">Filename</th>
                                                    <th colspan="1">Size (Kb)</th>
                                                    <th colspan="1">Upload Progress %</th>
                                                    <th colspan="1">Status</th>
                                                    <th colspan="1"></th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="file in data.files" :key="file.name"  >
                                                    <td colspan="2" class="align-middle">{{file.name}}</td>
                                                    <td colspan="1" class="align-middle">{{Number(file.size/1024).toFixed(2)}}</td>
                                                    <td colspan="1" class="align-middle">{{file.progress}}</td>
                                                    <td class="align-middle" v-if="file.error">{{file.error}}</td>
                                                      <td class="align-middle" v-else-if="file.success">success</td>
                                                      <td class="align-middle" v-else-if="file.active">{{file.progress}}</td>
                                                      <td class="align-middle" v-else-if="!!file.error">{{file.error}}</td>
                                                      <td class="align-middle" v-else></td>
                                                    <td colspan="1" class="align-middle"></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                      </div>

                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>

                </div>
                <div class="modal-footer">
                    <div class="mx-auto w-100">
                        <div class="progress w-100">
                            <div id="progressbar" class="progress-bar" role="progressbar" aria-valuemin="0"
                                aria-valuemax="100" :style="{width: uploadProgressOverall() + '%',
                                                             color: 'black'}">
                                {{uploadProgressOverall() + "%"}}
                            </div>
                        </div>
                    </div>
                    <div class="example-btn">
                        <file-upload class="btn btn-primary"
                            :custom-action="customPostAction"
                            :multiple="true"
                            :drop="true"
                            :directory="true"
                            :thread="5"
                            v-model="files"
                            @input-filter="inputFilter"
                            @input-file="inputFile"
                            ref="upload">
                            Select files
                        </file-upload>
                        <button class="btn btn-success" v-if="!this.$refs.upload || !this.$refs.upload.active"
                            @click.prevent="this.$refs.upload.active = true">
                            Start Upload
                        </button>
                        <button class="btn btn-danger" v-else @click.prevent="this.$refs.upload.active = false">
                            Stop Upload
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import FileUpload from 'vue-upload-component'
import axios from 'axios'

export default {
  name: 'UploadModal',
  components: {
    FileUpload
  },
  data () {
    return {
      files: [],
      filesUploaded: []
    }
  },
  computed: {
    filesGroupedByFolders () {
      const result = {}
      this.files.forEach((file) => {
        const folder = file.name.split('/')[0].split('.')[0]
        if (!result[folder]) {
          result[folder] = []
          result[folder].files = []
          result[folder].size = 0
          result[folder].slices = 0
        }
        result[folder].files.push(file)
        result[folder].size += file.size
        result[folder].slices += 1
      })
      return result
    }
  },
  watch: {
  },
  mounted () {
  },
  methods: {
    inputFilter (newFile, oldFile, prevent) {
      if (newFile && !oldFile) {
        // Before adding a file
        // Filter system files or hide files
        if (/(\/|^)(Thumbs\.db|desktop\.ini|\..+)$/.test(newFile.name)) {
          return prevent()
        }
        // Filter php html js file
        if (/\.(php5?|html?|jsx?)$/i.test(newFile.name)) {
          return prevent()
        }
      }
    },
    inputFile (newFile, oldFile) {
      if (newFile && !oldFile) {
        // debugger // eslint-disable-line
        // add
        // console.log('add', newFile)
      }
      if (newFile && oldFile) {
        // update
        // console.log('update', newFile)
      }
      if (!newFile && oldFile) {
        // remove
        // console.log('remove', oldFile)
      }
    },
    uploadProgressFolder (files) {
      var sum = 0
      files.forEach(function (file) { sum += Number(file.progress) })
      const average = sum / files.length
      return average.toFixed(2)
    },
    uploadProgressOverall () {
      var sum = 0
      this.files.forEach(function (file) { sum += Number(file.progress) })
      if (this.files.length) {
        const average = sum / this.files.length
        return average.toFixed(2)
      } else {
        const average = 0
        return average.toFixed(2)
      }
    },
    async customPostAction (file) {
      var formData = new FormData()
      formData.append('file', file.file)
      var uploadComponent = this.$refs.upload
      const config = {
        onUploadProgress: progressEvent => {
          var progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          uploadComponent.update(file, { progress: progress })
        }
      }
      // const folder = file.name.split('/')[0]
      // const name = file.name.split('/')[1]
      axios
        .post('http://localhost:5000/upload_files/' + this.$route.params.id,
          // headers: { 'Content-Type': 'multipart/form-data' },
          formData,
          config
        ).catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
</style>
