<template>
    <div class="modal fade" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title h4">File Upload</div>
                    <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="row mx-auto">
                  <ul class="text-left">
                        <!-- <li>images can be uploaded as .zip files</li> -->
                        <li>Supported file formats: dicom, jpeg, png.</li>
                        <li>Don't upload more than 10000 files in one upload.</li>
                        <li>Use the Select Files button to upload multiple files. Each file will be treated as a stack. The stackname will equal the filename without the ending.</li>
                        <li>Use the Select Folder button to upload a folder containing multiple files. The files will be combined into a stack. The stack name will equal the foldername. To upload multiple folders/stacks select a folder containing subdirectories.</li>
                </ul>
              </div>
                <div class="modal-body overflow-auto" style="height:62vh;">
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
                                    <td colspan="1" class="align-middle" data-bs-toggle="collapse" :data-bs-target="'#A' + folder.foldername"><button class="btn btn-primary">show files</button></td>
                                    <!-- <td colspan="1" class="align-middle"><button class="btn btn-danger">remove</button></td> -->
                                </tr>
                                <tr class="collapse" :id="'A' + folder.foldername">
                                    <td colspan="7">
                                      <div class="overflow-auto" style="max-height:200px;">
                                        <table class="table table-secondary table-borderless">
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
                        <label class="btn btn-primary ml-auto">Select Files
                          <input @change="addFolder" type="file" name="file" class="d-none" id="file" multiple/>
                        </label>
                        <label class="btn btn-primary ml-1">Select Folder
                          <input @change="addFolder" type="file" name="folder" class="d-none" id="folder" ref="folder" webkitdirectory multiple/>
                        </label>
                        <button v-if="uploadPaused" @click.prevent="this.startUpload" class="btn btn-success ml-1">
                            Start Upload (files left {{this.fileNumber()}})
                        </button>
                        <button class="btn btn-danger ml-1" v-else @click.prevent="this.uploadPaused = true">
                            Stop Upload (files left {{this.fileNumber()}})
                        </button>
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
      uploadPaused: true
    }
  },
  computed: {
  },
  watch: {
  },
  mounted () {
  },
  methods: {
    inputFilter (files) {
      const allowedFileEndings = ['dcm', 'png', 'jpg', 'jpeg']
      const filteredFiles = files.filter(file => allowedFileEndings.includes(file.name.toLowerCase().split('.').at(-1)))
      return filteredFiles
    },
    addFolder (e) {
      const files = this.inputFilter(Array.from(e.target.files))
      if (!(files.length > 0)) {
        return false
      }
      Array.from(files).forEach(newFile => {
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
      // sort list
      this.fileFolders.sort((a, b) => (a.foldername > b.foldername) ? 1 : -1)
      // filter files finished
      this.fileFolders = this.fileFolders.filter(fileFolder => fileFolder.progress < 100)
    },
    uploadProgressOverall () {
      var sum = 0
      this.fileFolders.forEach(function (folder) { sum += Number(folder.progress) })
      const average = this.fileFolders.length ? sum / this.fileFolders.length : 0
      if (average >= 100) {
        this.uploadPaused = true
      }
      return average.toFixed(2)
    },
    startUpload () {
      if (this.fileNumber() === 0) { return }
      this.uploadPaused = false
      this.uploadFolders()
    },
    // working
    async uploadFolders () {
      if (this.uploadPaused) { return }
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
        this.uploadFolderChunkWise(folderToUpload, 10)
      }
    },
    uploadFolderChunkWise (folder, chuncksize) {
      var formData = new FormData()
      var filesUploading = []
      folder.files.forEach((file) => {
        if (filesUploading.length < chuncksize & file.status === '') {
          formData.append('file', file.file)
          filesUploading.push(file)
          file.status = 'uploading'
        }
      })
      // config request
      const config = {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const loaded = progressEvent.loaded
          const total = progressEvent.loaded
          const progress = (loaded * 100) / total
          filesUploading.forEach((file) => {
            file.progress = progress
          })
          var folderProgress = 0
          folder.files.forEach((file) => { folderProgress += Number(file.progress) })
          folder.progress = folderProgress / folder.files.length
        }
      }

      // request
      uploadFiles(this.$route.params.id, formData, config)
        .then((response) => {
          filesUploading.forEach((file) => {
            file.status = 'uploaded successfully'
          })
          const allUploadedSuccessfull = folder.files.every((file) => file.status === 'uploaded successfully')
          const allUploadedWithError = folder.files.every((file) => file.status === 'uploaded successfully' | file.status === 'error')
          if (allUploadedSuccessfull) {
            folder.status = 'upload finished'
            const stack = response.data.stack
            this.$store.commit('currentStudy/addStack', stack)
          } else if (allUploadedWithError) {
            folder.status = 'upload finished with errors'
          }
        })
        .catch(() => {
          filesUploading.forEach((file) => {
            file.status = 'error'
          })
          const allUploadedWithError = folder.files.every((file) => file.status === 'uploaded successfully' | file.status === 'error')
          if (allUploadedWithError) {
            folder.status = 'upload finished with errors'
          }
        })
        .finally(() => {
          this.uploadFolders()
        })
    },
    fileNumber () {
      var fileNumb = 0
      this.fileFolders.forEach((folder) => { fileNumb += !folder.status.includes('upload finished') ? folder.files.length : 0 })
      return fileNumb
    }
  }
}
</script>

<style scoped>
</style>
