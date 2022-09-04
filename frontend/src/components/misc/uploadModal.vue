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
                                    <td colspan="1" class="align-middle">{{folder.progress.toFixed(2)}}</td>
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
                                                    <th colspan="1">Upload Progress %</th>
                                                    <th colspan="1">Status</th>
                                                    <th colspan="1"></th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="file in folder.files" :key="file.name"  >
                                                    <td colspan="2" class="align-middle">{{file.name}}</td>
                                                    <td colspan="1" class="align-middle">{{Number(file.size/1024).toFixed(2)}}</td>
                                                    <td colspan="1" class="align-middle">{{file.progress.toFixed(2)}}</td>
                                                    <td colspan="1" class="align-middle">{{file.status}}</td>
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
                        <label class="btn btn-primary ml-1">Select Files
                          <input @change="addFolder" type="file" name="file" class="d-none" id="file" multiple/>
                        </label>
                        <label class="btn btn-primary ml-1">Select Folder
                          <input @change="addFolder" type="file" name="folder" class="d-none" id="folder" ref="folder" webkitdirectory multiple/>
                        </label>
                        <label class="ml-1">
                          Files selected: {{fileNumber()}}
                        </label>
                        <button @click="uploadFolders" class="btn btn-success ml-1">
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
import { uploadFiles } from '@/api'
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
  },
  watch: {
  },
  mounted () {
  },
  methods: {
    inputFilter (newFile, oldFile, prevent) {
    },
    addFolder (e) {
      if (!e.target.files.length > 0) {
        return false
      }

      Array.from(e.target.files).forEach(newFile => {
        var paths = ''
        if (newFile.webkitRelativePath) {
          paths = newFile.webkitRelativePath.split('/')
        } else {
          paths = newFile.name.split('/')
        }
        var foldernameNewFile
        if (paths.length > 1) {
          foldernameNewFile = paths[paths.length - 2].split('.')[0]
        } else {
          foldernameNewFile = paths[paths.length - 1].split('.')[0]
        }

        // check if similar folder already exists
        var index = this.fileFolders.findIndex(fileFolder => fileFolder.foldername === foldernameNewFile)
        if (index === -1) {
          this.fileFolders.push({
            foldername: foldernameNewFile,
            files: [],
            size: 0,
            slices: 0,
            progress: 0,
            status: '',
            error: ''
          })
          index = this.fileFolders.length - 1
        }
        this.fileFolders[index].files.push(
          {
            file: newFile,
            name: newFile.name,
            size: newFile.size,
            status: '',
            progress: 0
          }
        )
        this.fileFolders[index].size += newFile.size
        this.fileFolders[index].slices += 1
      })
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
    async uploadFolders () {
      // find folder that is currently uploading or that has not uploaded yet
      var folderToUpload
      for (var folder of this.fileFolders) {
        if (folder.status === '' && folderToUpload === undefined) {
          folderToUpload = folder
          folderToUpload.status = 'uploading'
        }
        if (folder.status === 'uploading' && folderToUpload === undefined) {
          folderToUpload = folder
        }
      }
      if (folderToUpload) {
        this.uploadFolderChunkWise(folderToUpload, 5)
      }
    },
    uploadFolderChunkWise (folder, chuncksize) {
      var promises = []
      var formData = new FormData()
      var filesUploading = []
      folder.files.forEach((file) => {
        if (filesUploading.length < chuncksize && file.status === '') {
          formData.append('file', file.file)
          filesUploading.push(file)
          file.status = ' uploading'
        }
      })
      // config request
      const config = {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: progressEvent => {
          var progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          var folderProgress = progress * (filesUploading.length / folder.files.length)
          folder.progress += folderProgress
          filesUploading.forEach((file) => {
            file.progress += progress
          })
        }
      }

      // request
      const promise = uploadFiles(this.$route.params.id, formData, config)
        .then((response) => {
          filesUploading.forEach((file) => {
            file.status = 'uploaded successfully'
          })
          if (folder.files.every((file) => file.status === 'uploaded successfully')) {
            folder.status = 'upload finished'
            const stack = response.data.stack
            console.log(stack)
            this.$store.commit('openStudy/addStack', stack)
          }
        })
        .catch(() => {
          filesUploading.forEach((file) => {
            file.status = 'error'
          })
        })
        .finally(() => {
          this.uploadFolders()
        })
      promises.push(promise)
    },
    fileNumber () {
      var fileNumb = 0
      var selectedFiles = document.getElementById('folder')
      if (selectedFiles) {
        fileNumb += selectedFiles.files.length
      }
      return fileNumb
    }
    // not used
    /*     async uploadFiles () {
      // find folder that is not uploaded yet and check the number of active uploads
      var fileNotActive
      // var activeUploads = 0
      // var maxSimUp = 1
      for (var folder of this.fileFolders) {
        for (var file of folder.files) {
          if (file.status === '' && fileNotActive === undefined) {
            fileNotActive = file
            fileNotActive.status = 'uploading'
          }
          // if (folder.status === 'uploading') {
          //   activeUploads += 1
          // }
        }
      }
      if (fileNotActive) {
        var formData = new FormData()
        formData.append('file', fileNotActive.file)

        // // start more uploads until max upload number eached
        // if (activeUploads < maxSimUp) {
        //   for (var i = 0; i < maxSimUp - activeUploads; i++) {
        //     this.uploadFiles()
        //   }
        // }

        // config request
        const config = {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: progressEvent => {
            var progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            fileNotActive.progress = progress
            folder.progress += progress / folder.files.length
          }
        }

        // request
        axios
          .post('http://localhost:5000/upload_files/' + this.$route.params.id,
            formData,
            config)
          .then(() => {
            fileNotActive.status = 'uploaded successfully'
          })
          .catch(() => {
            fileNotActive.status = 'error'
          })
          .then(() => {
            this.uploadFiles()
          })
      }
    },
    // not used
    async uploadFolders2 () {
      // find folder that is not uploaded yet and check the number of active uploads
      this.fileFolders.forEach((folder) => {
        folder.status = 'uploading'

        var formData = new FormData()
        folder.files.forEach((file, index) => {
          if (index < 15) {
            formData.append('file', file)
          }
        })

        // config request
        const config = {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: progressEvent => {
            var progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            folder.progress = progress
          }
        }

        // request
        axios
          .post('http://localhost:5000/upload_files/' + this.$route.params.id,
            formData,
            config)
          .then(() => {
            folder.status = 'uploaded successfully'
          })
          .catch(() => {
            folder.status = 'error'
          })
          .then(() => {
          })
      })
    } */
  }
}
</script>

<style scoped>
</style>
