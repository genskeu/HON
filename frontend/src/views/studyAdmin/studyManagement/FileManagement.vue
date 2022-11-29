<template>
    <div class="container">
        <uploadModal id="uploadModal"></uploadModal>
        <div class="row mx-auto h-100">
            <div class="h-100" id="uploaded_files">
                <div class="row mx-auto mt-1">
                    <div id="loader_anim_del" class=""></div>
                    <div id="loader_text_del" class="mt-3" style="display: none;">Please wait</div>
                </div>
                <div class="w-100 mb-4" style="height:90%">
                    <div class= "overflow-auto" style="height:100%">
                        <table class="table table-hover text-middle">
                            <thead class="thead sticky-top bg-white">
                                <tr>
                                    <th >Name</th>
                                    <th >Slices</th>
                                    <th >Size (Mb)</th>
                                    <th ></th>
                                    <th class="">
                                        <button @click="selectAll" class="btn-secondary btn mr-1">Select All</button>
                                    </th>
                                </tr>
                            </thead>
                            <tbody id="file_list">
                                <template v-for="stack in studyStacks" :key="stack.name">
                                <tr >
                                    <th>{{stack.name}}</th>
                                    <th>{{stack.slices}}</th>
                                    <th>{{Number(stack.size/(1024*1024)).toFixed(2) }}</th>
                                    <th data-bs-toggle="collapse" :data-bs-target="'#A' + stack.name"><button class="btn-light btn">Show Files</button></th>
                                    <th class="align-middle mx-auto"><input name="filesToDelete" v-model="filesToDelete" type='checkbox' :value="stack" class="mt-1"></th>
                                </tr>
                                <tr :id="'A' + stack.name" class="collapse">
                                    <td colspan="5">
                                        <div class="overflow-auto" style="max-height:200px;">
                                        <table class="table table-secondary table-borderless">
                                            <thead class="">
                                                <tr colspan="6">
                                                    <th colspan="2">Filename</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="file in stack.files" :key="file"  >
                                                    <td colspan="2" class="align-middle">{{file}}</td>
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
                </div>
                <div class="row mx-auto justify-content-end">
                    <button @click="deleteSelectedFiles()" class="btn-danger btn col-2 mr-1" :disabled="filesToDelete.length === 0">Delete Selected Files</button>
                    <button class="btn-success btn btn-block col-2" data-bs-toggle="modal" data-bs-target="#uploadModal">Upload Files</button>
                </div>
            </div>
        </div>
    </div>
<!--         <div class="row mx-auto">
            <button class="btn btn-secondary btn-block" data-bs-toggle="collapse" data-bs-target="#naming"
                aria-expanded="false" aria-controls="naming">
                <h5 class="">Instructions File Upload &#9776;</h5>
            </button>
            <div id="naming" class="collapse show">

                 <br>
                <h3>AFC Information</h3>
                <br>
                <p>To use HON feature to automatically create AFC studies the
                    following naming scheme needs to be used: POS_CLASS_GROUP
                </p>
                <p style="text-align: justify; hyphens:auto">
                    POS defines he tposition of an stack during the study.
                    For the automatic generation of AFC image-sets it only needs to be defined
                    for the positive images i.e. images containing a signal.
                    For the negative class it can be left empty or used to avoid duplicate file names.
                    CLASS and GROUP are only relevant when creating AFC experiments.
                    CLASS defines which stacks contain the signal and which don't.
                    GROUP is used to link the positive to the negative class.
                    For each AFC stack-set one positive and n-1 negative stacks are combined.
                    If more than n-1 negative images match they will be subsampled randomly.
                </p>
                <br>
                AFC-Example:
                <p>
                    014_pos_Group1.dcm will be combined with n-1 images named _neg_Group1.dcm to form
                    the 14th set of images shown during the study.
                </p>
            </div>
        </div> -->
</template>

<script>
import uploadModal from '@/components/studyDesign/uploadModal'

export default {
  name: 'FileUpload',
  components: {
    uploadModal
  },
  data () {
    return {
      filesToDelete: []
    }
  },
  computed: {
    studyStacks () {
      return this.$store.getters['currentStudy/stacks']
    }
  },
  methods: {
    selectAll () {
      if (this.studyStacks.length !== this.filesToDelete.length) {
        this.filesToDelete = []
        this.studyStacks.forEach(stack => {
          this.filesToDelete.push(stack)
        })
      } else {
        this.filesToDelete = []
      }
    },
    deleteSelectedFiles () {
      const studyId = this.$route.params.id
      this.$store.dispatch('currentStudy/deleteSelectedFiles', { studyId: studyId, files: this.filesToDelete })
      this.filesToDelete = []
    }
  }
}
</script>

<style>
ul {
  list-style-type: none;
}
</style>
