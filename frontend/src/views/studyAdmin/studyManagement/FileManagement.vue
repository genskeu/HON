<template>
    <div class="container">
        <uploadModal id="uploadModal"></uploadModal>
        <div class="row mx-auto pt-1">
            <button class="btn btn-light btn-block" data-bs-toggle="collapse" data-bs-target="#naming"
                aria-expanded="false" aria-controls="naming">
                <h5 class="mt-1">Rules and Naming conventions for File Upload &#9776;</h5>
            </button>
            <div id="naming" class="collapse">
                <div class="row mx-auto show" id="file_upload_rules">
                    <ul class="mt-3">
                        <li>images can be uploaded as .zip files</li>
                        <li>supported formats: dicom, jpeg, png</li>
                        <li>don't upload more than 5000 files in one upload</li>
                    </ul>
                </div>
                <br>
                <p>To use all features of HON (auto study creation, stack feature) the
                    following naming scheme needs to be used: POS_CLASS_GROUP_STACK
                </p>
                <p style="text-align: justify; hyphens:auto">
                    All images that are identical in POS, CLASS and GROUP can be combined into one
                    scrollable image-stack.
                    STACK controls the position of each image within the stack.
                    POS defines he position of an stack during the study.
                    For the automatic generation of AFC image-sets it only needs to be defined
                    for the positive images i.e. images containing a signal.
                    For the negative class it can be left empty or used to avoid duplicate file names.
                    CLASS and GROUP are only relevant when creating AFC experiments.
                    CLASS defines which stacks contain the signal and which don't.
                    GROUP is used to link the positive to the negative class.
                    For each AFC stack-set one positive and n-1 negative stacks are combined.
                    If more than n-1 negative images match they will be subsampled randomly.
                </p>
                AFC-Example:
                <p>
                    014_pos_Group1.dcm will be combined with n-1 images named _neg_Group1.dcm to form
                    the 14th set of images shown during the study.
                </p>
            </div>
        </div>

        <div class="row pt-1">
            <div class="" id="uploaded_files">
                <div class="row mx-auto mt-1">
                    <div id="loader_anim_del" class=""></div>
                    <div id="loader_text_del" class="mt-3" style="display: none;">Please wait</div>
                </div>
                <div class="w-100 mt-2">
                    <div style="height:72vh;" class="overflow-auto mb-4">
                        <table class="table table-secondary table-hover text-left">
                            <thead class="thead sticky-top">
                                <tr>
                                    <th >Name</th>
                                    <th >Slices</th>
                                    <th >Size (Mb)</th>
                                    <th ></th>
                                    <th class="col-2">
                                        <button id="delete_files" class="btn-danger btn">Delete Selected Files</button>
                                    </th>
                                </tr>
                            </thead>
                            <tbody id="file_list">
                                <tr v-for="(data,imageName) in studyStacks" :key="imageName">
                                    <th>{{imageName}}</th>
                                    <th>{{data.slices}}</th>
                                    <th>{{Number(data.size/(1024*1024)).toFixed(2) }}</th>
                                    <th><button class="btn-primary btn">Show Files</button></th>
                                    <th class="align-middle mx-auto"><input type='checkBox' class="mt-1 mx-auto"></th>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="row mx-auto justify-content-end mb-2">
                    <button id="upload_files" class="btn-success btn btn-block col-2" data-bs-toggle="modal" data-bs-target="#uploadModal">Upload Files</button>
                </div>
            </div>
        </div>

        <!-- <div class="row pt-1 pb-1">
            <button class="btn btn-secondary btn-block" data-bs-toggle="collapse" data-bs-target="#files_upload"
                aria-expanded="false" aria-controls="files_upload">
                <h5 class="col-12 mt-1">Upload &#9776;</h5>
            </button>
            <div id="files_upload" class="collapse show bg-light">
                <h6 class="badge badge-light w-100">Progress</h6>
                <div id="upload_infos" class="w-100 mx-auto">
                    <div class='progress w-100'>
                        <div class='progress-bar' id='progress'></div>
                    </div>
                    <div class='row mx-auto' id='uploadStatus'></div>

                    <div style="height:300px;" class="overflow-auto row mx-auto">
                        <div class='col-4 mx-auto' id='files_uploaded_saved'></div>
                        <div class='col-4 mx-auto' id='files_uploaded_not_saved'></div>
                        <div class='col-4 mx-auto' id='files_not_uploaded'></div>
                    </div>

                </div>

                <div class="row mx-auto">
                    <div class="custom-file mx-auto col-6">
                        <input type="file" name="file" class="custom-file-input form-control w-100" id="file"
                            multiple />
                    </div>
                </div>
            </div>
        </div> -->
    </div>
</template>

<script>
import uploadModal from '@/components/misc/uploadModal'

export default {
  components: {
    uploadModal
  },
  computed: {
    studyStacks () {
      return this.$store.getters['openStudy/stacks']
    }
  }
}
</script>

<style>
ul {
  list-style-type: none;
}
</style>
