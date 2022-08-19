<template>
    <div class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title h4">File Upload</div>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body overflow-auto" style="height:75vh;" @drop="addF">
                    <table class="table table-hover">
                        <thead class="thead-light">
                            <tr>
                                <th colspan="1">Stackname</th>
                                <th colspan="1">Slizes</th>
                                <th colspan="1">Size (Mb)</th>
                                <th colspan="1">Upload Progress %</th>
                                <th colspan="1">Status</th>
                                <th colspan="1"></th>
                                <th colspan="1"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="folder in fileFolders" :key="folder.foldername">
                                <tr>
                                    <td colspan="1" class="align-middle">{{folder.foldername}}</td>
                                    <td colspan="1" class="align-middle">{{folder.slices}}</td>
                                    <td colspan="1" class="align-middle">{{Number(folder.size/(1024*1024)).toFixed(2) }}</td>
                                    <td colspan="1" class="align-middle">{{folder.progress}}</td>
                                    <td colspan="1" class="align-middle">{{folder.status}}</td>
                                    <td colspan="1" class="align-middle" data-bs-toggle="collapse" :data-bs-target="'#' + folder.foldername"><button class="btn btn-primary">show files</button></td>
                                    <td colspan="1" class="align-middle"><button class="btn btn-danger">remove</button></td>
                                </tr>
                                <tr class="collapse" :id="folder.foldername">
                                    <td colspan="7">
                                      <div class="overflow-auto" style="max-height:200px;">
                                        <table class="table table-dark table-borderless">
                                            <thead class="">
                                                <tr colspan="6">
                                                    <th colspan="2">Filename</th>
                                                    <th colspan="1">Size (Kb)</th>
                                                    <th colspan="1">Status</th>
                                                    <th colspan="1"></th>
                                                    <th colspan="1"></th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="file in folder.files" :key="file.name"  >
                                                    <td colspan="2" class="align-middle">{{file.name}}</td>
                                                    <td colspan="1" class="align-middle">{{Number(file.size/1024).toFixed(2)}}</td>
                                                    <td class="align-middle" v-if="file.error">{{file.error}}</td>
                                                      <td class="align-middle" v-else-if="file.success">success</td>
                                                      <td class="align-middle" v-else-if="file.active">{{file.progress}}</td>
                                                      <td class="align-middle" v-else-if="!!file.error">{{file.error}}</td>
                                                      <td class="align-middle" v-else></td>
                                                    <td colspan="1" class="align-middle"></td>
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
                        <label class="btn btn-primary">Select Files
                          <input @change="addFiles" type="file" name="file" class="d-none" id="file" multiple/>
                        </label>
                        <label class="btn btn-primary">Select Folder
                          <input @change="addFolder" type="file" name="folder" class="d-none" id="folder" webkitdirectory multiple/>
                        </label>
                        <button @click="uploadFolders" class="btn btn-success">
                            Start Upload
                        </button>
<!--                         <button class="btn btn-danger" v-else @click.prevent="this.$refs.upload.active = false">
                            Stop Upload
                        </button> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UploadModal',
  components: {
  },
  data () {
    return {
      fileFolders: [],
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
    addFiles (e) {
      if (!e.target.files.length > 0) {
        return false
      }

      Array.from(e.target.files).forEach(newFile => {
        const foldernameNewFile = newFile.name.split('/')[0].split('.')[0]

        // check if similar folder already exists
        const index = this.fileFolders.findIndex(fileFolder => fileFolder.foldername === foldernameNewFile)
        if (index > -1) {
          this.fileFolders[index].files.push(newFile)
          this.fileFolders[index].size += newFile.size
          this.fileFolders[index].slices += 1
        } else {
          this.fileFolders.push({
            foldername: foldernameNewFile,
            files: [newFile],
            size: newFile.size,
            slices: 1,
            progress: 0,
            status: '',
            error: ''
          })
        }
      })
    },
    addF (e) {
      debugger // eslint-disable-line no-debugger
    },
    addFolder (e) {
      if (!e.target.files.length > 0) {
        return false
      }

      Array.from(e.target.files).forEach(newFile => {
        const paths = newFile.webkitRelativePath.split('/')
        var foldernameNewFile
        if (paths.length > 1) {
          foldernameNewFile = paths[paths.length - 2].split('.')[0]
        } else {
          foldernameNewFile = paths[paths.length - 1].split('.')[0]
        }

        // check if similar folder already exists
        const index = this.fileFolders.findIndex(fileFolder => fileFolder.foldername === foldernameNewFile)
        if (index > -1) {
          this.fileFolders[index].files.push(newFile)
          this.fileFolders[index].size += newFile.size
          this.fileFolders[index].slices += 1
        } else {
          this.fileFolders.push({
            foldername: foldernameNewFile,
            files: [newFile],
            size: newFile.size,
            slices: 1,
            progress: 0,
            status: '',
            error: ''
          })
        }
      })
    },
    uploadProgressFolder (files) {
      var sum = 0
      files.forEach(function (file) { sum += Number(file.progress) })
      const average = sum / files.length
      return average.toFixed(2)
    },
    uploadProgressOverall () {
      var sum = 0
      this.fileFolders.forEach(function (folder) { sum += Number(folder.progress) })
      if (this.fileFolders.length) {
        const average = sum / this.fileFolders.length
        return average.toFixed(2)
      } else {
        const average = 0
        return average.toFixed(2)
      }
    },
    // working
    // todos: maxSImUploads should be respnisve to size and have an upper limit
    // eg. 20 but if size is over x limit to y
    uploadFolders (maxSimUp = 5) {
      // find folder that is not uploaded yet and check the number of active uploads
      var folderNotActive
      var activeUploads = 0
      for (var folder of this.fileFolders) {
        if (folder.status === '' && folderNotActive === undefined) {
          folderNotActive = folder
          folderNotActive.status = 'uploading'
        }
        if (folder.status === 'uploading') {
          activeUploads += 1
        }
      }

      if (folderNotActive) {
        var formData = new FormData()
        folderNotActive.files.forEach((file) => formData.append('file', file))

        // start more uploads until max upload number eached
        if (activeUploads < maxSimUp) {
          for (var i = 0; i < maxSimUp - activeUploads; i++) {
            this.uploadFolders()
          }
        }

        // config request
        const config = {
          onUploadProgress: progressEvent => {
            var progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            folderNotActive.progress = progress
          }
        }

        // request
        axios
          .post('http://localhost:5000/upload_files/' + this.$route.params.id,
            // headers: { 'Content-Type': 'multipart/form-data' },
            formData,
            config)
          .then(() => {
            folderNotActive.status = 'uploaded successfully'
          })
          .catch(() => {
            folderNotActive.status = 'error'
          })
          .then(() => {
            this.uploadFolders()
          })
      } else {
        return false
      }
    }
  }
}
</script>

<style scoped>
</style>
