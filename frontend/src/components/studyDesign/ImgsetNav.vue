<template>
  <div>
    <div class="row mx-auto mt-2" id="imgset_settings_title">
      <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#imgset_settings"
        aria-expanded="true">
        <h4 class="w-100 mt-1">Imgsets &#9776;</h4>
      </button>
    </div>
    <div>
        <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
          title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
          <label class="input-group-text">Load Imgset</label>
          <select class='form-select' v-model="imgsetActive">
            <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{ imgset.position }}</option>
          </select>
        </div>
      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#general_settings_content"
          aria-expanded="true" aria-controls="general_settings_content"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Images displayed</h5>
        </button>
      </div>

      <div>
        <div v-for="index in viewerNumb" :key="index">
          <DicomViewerImageSelect :viewer-index="index-1"></DicomViewerImageSelect>
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#general_settings_content"
          aria-expanded="true" aria-controls="general_settings_content"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (manual)</h5>
        </button>
      </div>
      <div class="">
        <div class="row mx-auto">
          <button value="append imgset" class="imgset_btn btn-success btn" id="add_imgset"
            title="add image-set to the end of the study">create new imgset</button>
        </div>
        <div class="row mx-auto">
          <input value="update imgset" class="imgset_btn btn-light btn" id="upd_imgset"
            title="update currently selected image-set" />
        </div>
        <div class="row mx-auto">
          <input value="delete imgset" class="imgset_btn btn-danger btn" id="del_imgset"
            title="delete currently selected image-set" />
        </div>
        <div class="row mx-auto">
          <input value="delete all imgsets" class="imgset_btn btn-danger btn" id="del_all_imgsets" />
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#general_settings_content"
          aria-expanded="true" aria-controls="general_settings_content"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (auto)</h5>
        </button>
      </div>
      <div>
      </div>

    </div>
  </div>
</template>

<script>
import DicomViewerImageSelect from '@/components/dicomViewer/DicomViewerImageSelect.vue'

export default {
  name: 'ImgsetControl',
  components: {
    DicomViewerImageSelect
  },
  data () {
    return {
      imgsetActive: undefined
    }
  },
  computed: {
    imgsets () {
      return this.$store.getters['openStudy/imgsets']
    },
    viewerNumb () {
      return this.$store.getters['openStudy/viewerNumb']
    }
  },
  watch: {
    imgsetActive: {
      handler (newImgset) {
        newImgset.image_stacks.forEach((stack, index) => {
          // ensure same structure as select menu values
          stack.cs_stack.name = stack.name
          this.$store.commit('imageViewers/stackDisplayed', { stackDisplayed: stack.cs_stack, index: index })
        })
      }
    }
  }
}
</script>

<style>

</style>
