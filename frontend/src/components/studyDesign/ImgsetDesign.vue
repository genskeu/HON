<template>
  <div>
    <div class="row mx-auto mt-2" id="imgset_settings_title">
      <button class="btn btn-dark col-12 mb-1" data-bs-toggle="collapse" data-bs-target="#imgset_settings"
        aria-expanded="true">
        <h4 class="w-100 mt-1">Image Sets &#9776;</h4>
      </button>
    </div>
    <div id="imgset_settings" class="collapse show">
      <div class="input-group mx-auto" data-toggle="tooltip" data-placement="left"
        title="Use the select menus to activate image handling tools for the left, middle and right mouse key.">
        <label class="input-group-text">Set Displayed</label>
        <select class='form-select' v-model="imgsetDisplayed">
          <option :value="undefined"></option>
          <option v-for="imgset in imgsets" :key="imgset.id" :value="imgset">{{ imgset.position + 1 }}</option>
        </select>
        <label class="input-group-text">/{{ imgsets.length }}</label>
      </div>
      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_displayed"
          aria-expanded="true" aria-controls="images_displayed"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Images displayed</h5>
        </button>
      </div>

      <div id="images_displayed" class="collapse show">
        <div v-if="refviewerNumb" class="input-group-text">
          <h5 class="mx-auto">Reference-Images</h5>
        </div>
        <div v-for="index in refviewerNumb" :key="index">
          <DicomViewerImageSelect :viewer-index="index - 1" viewer-type="refviewers"></DicomViewerImageSelect>
        </div>
        <div v-if="refviewerNumb" class="input-group-text">
          <h5 class="mx-auto">Images</h5>
        </div>
        <div v-for="index in viewerNumb" :key="index">
          <DicomViewerImageSelect :viewer-index="index - 1" viewer-type="viewers"></DicomViewerImageSelect>
        </div>
      </div>
      <!-- viewport settings -->
      <div id="viewport_settings_container" class="w-100 mt-1" title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images.
                        Each viewport can be controlled individually.
                        To globally control viewport settings use the defaults submenu.">
        <div class="row mt-1 mx-auto">
          <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#viewport_settings"
            aria-expanded="true" aria-controls="viewport_settings">
            <h4 class="w-100 mt-1" id="imgset_btn">Viewer Settings</h4>
          </button>
        </div>
        <div id="viewport_settings" class="collapse">
          <div v-if="refviewerNumb" class="input-group-text">
            <h5 class="mx-auto">Reference-Images</h5>
          </div>
          <div id="" v-for="(viewer, index) in refimageViewers" :key="index">
            <DicomViewportControl :target-viewer="index" viewer-type="refviewers"></DicomViewportControl>
          </div>
          <div v-if="refviewerNumb" class="input-group-text">
            <h5 class="mx-auto">Images</h5>
          </div>
          <div id="" v-for="(viewer, index) in imageViewers" :key="index">
            <DicomViewportControl :target-viewer="index" viewer-type="viewers"></DicomViewportControl>
          </div>
        </div>
      </div>
      <div id="annotations_settings_container" class="w-100 mt-1" title="">
        <div class="row mt-1 mx-auto">
          <button class="btn btn-secondary col-12" data-bs-toggle="collapse" data-bs-target="#annotation_settings"
            aria-expanded="true" aria-controls="viewport_settings">
            <h4 class="w-100 mt-1">Annotation Settings</h4>
          </button>
        </div>
        <div id="annotation_settings" class="collapse">
          <div id="" v-for="(viewer, index) in imageViewers" :key="index">
            <ToolsAnnotationControl :target-viewer="index" viewer-type="viewers"></ToolsAnnotationControl>
          </div>
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <!-- <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_create_man"
          aria-expanded="true" aria-controls="images_create_man"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (manual)</h5>
        </button> -->
      </div>
      <div id="images_create_man" class="collapse show">
        <div class="row mb-1">
          <div class="input-group">
            <button class="btn-success btn col-9" title="add image-set to the end of the study"
            @click="addImgset">add image set at position
            </button>
            <input class="form-control" type="Number" min="1" :max="imgsets.length + 1" step="1" id="numb_refimg" v-model="imagesetAddPosition"/>
          </div>
        </div>
        <div v-if="imgsetDisplayed" class="row mx-auto">
          <button value="update loaded imgset" class="imgset_btn btn-light btn mb-1" id="upd_imgset"
            title="update currently selected image-set">update loaded imgset
          </button>
        </div>
        <div v-if="imgsetDisplayed" class="row mx-auto">
          <button value="delete loaded imgset" class="imgset_btn btn-danger btn mb-1" id="del_imgset"
            title="delete currently selected image-set">delete loaded imgset
          </button>
        </div>
        <div v-if="imgsets.length" class="row mx-auto">
          <button class="btn-danger btn mb-1" @click="deleteAllImgsets">delete all
            imgsets
          </button>
        </div>
      </div>

      <div class="row mx-auto mt-1" id="general_settings_title">
        <button class="btn-secondary btn col-12" data-bs-toggle="collapse" data-bs-target="#images_create_auto"
          aria-expanded="true" aria-controls="images_create_auto"
          title="General settings include options to control the study layout and to customize the number and size of images displayed simultaneously.">
          <h5 class="mt-1">Creation (auto)</h5>
        </button>
      </div>
      <div id="images_create_auto" class="collapse">
        <!-- study type -->
        <div class="input-group w-100">
          <label class="input-group-text w-50">Imgset Type</label>
          <select class="form-select" ref="imgsetType">
            <option value="standard">standard</option>
            <option value="afc">alternative forced choice</option>
          </select>
        </div>
        <!-- order -->
        <div class="input-group w-100">
          <label class="input-group-text w-50">Imgset Order</label>
          <select class="form-select" ref="imgsetOrder">
            <option value="ordered">ordered</option>
            <option value="random">random</option>
          </select>
        </div>
        <!-- signal info -->
        <div v-if="afcCreateAuto" class="input-group w-100">
          <label class="input-group-text">Signal Present Pattern:</label>
          <select class="form-select pattern_imgset_auto" id="pos_pattern" placeholder="pattern pos class">
            <option></option>
          </select>
        </div>
        <div v-if="afcCreateAuto" class="input-group w-100">
          <label class="input-group-text">Signal Absent Pattern:</label>
          <select class="form-select pattern_imgset_auto" id="neg_pattern" placeholder="pattern neg class">
            <option></option>
          </select>
        </div>
        <div class="mt-1">
        <button @click="createImgsetsAuto" class="w-100 btn btn-success imgset_btn" value="generate imgsets" id="btn_auto_imgset">
          Create Imgsets
        </button>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
import DicomViewerImageSelect from '@/components/dicomViewer/DicomViewerImageSelect.vue'
import DicomViewportControl from '@/components/dicomViewer/DicomViewportControl.vue'
import ToolsAnnotationControl from '@/components/dicomViewer/ToolsAnnotationControl.vue'

export default {
  name: 'ImgsetControl',
  components: {
    DicomViewerImageSelect,
    DicomViewportControl,
    ToolsAnnotationControl
  },
  data () {
    return {
      imagesetAddPosition: 1
    }
  },
  computed: {
    imgsetDisplayed: {
      get () {
        return this.$store.getters['openStudy/imgsetDisplayed']
      },
      set (imgset) {
        this.$store.commit('openStudy/imgsetDisplayed', imgset)
      }
    },
    stacks () {
      return this.$store.getters['openStudy/stacks']
    },
    imgsets () {
      return this.$store.getters['openStudy/imgsets']
    },
    viewerNumb () {
      return this.$store.getters['openStudy/viewerNumb']
    },
    refviewerNumb () {
      return this.$store.getters['openStudy/refviewerNumb']
    },
    imageViewers () {
      return this.$store.getters['imageViewers/viewers']
    },
    refimageViewers () {
      return this.$store.getters['imageViewers/refviewers']
    },
    afcCreateAuto () {
      if (this.$refs.imgsetType) {
        return this.$refs.imgsetType.value === 'afc'
      }
      return false
    }
  },
  watch: {
    imgsetDisplayed: {
      handler (newImgset) {
        // code could be moved to store to avoid duplication?
        if (newImgset) {
          const viewers = this.refimageViewers.concat(this.imageViewers)
          // itterate over viewers and display stack according to div_id
          // if no stack found reset stack to trigger viewer reset
          viewers.forEach((viewer, index) => {
            var stack = newImgset.image_stacks.find(stack => stack.div_id === 'dicom_img_' + index)
            if (stack === undefined) {
              stack = {
                cs_stack: {
                  imageIds: [],
                  currentImageIdIndex: Number
                },
                name: String,
                savedSegmentation: undefined,
                savedToolstate: undefined,
                savedViewport: undefined
              }
            }
            var viewertype = this.refimageViewers.includes(viewer) ? 'refviewers' : 'viewers'
            var viewerindex = this.refimageViewers.includes(viewer) ? index : index - this.refimageViewers.length
            const stackData = {
              name: stack.name,
              stackDisplayed: stack.cs_stack,
              savedViewport: stack.viewport,
              savedToolstate: stack.tool_state,
              savedSegmentation: stack.seg_data,
              index: viewerindex,
              viewertype: viewertype
            }
            this.$store.commit('imageViewers/stackDisplayed', stackData)
          })
        }
      }
    }
  },
  methods: {
    addImgset () {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      imgset.position = this.imagesetAddPosition - 1
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('openStudy/addImgset', payload)
    },
    updateImgset () {

    },
    deleteImgset () {

    },
    deleteAllImgsets () {
      const studyId = this.$route.params.id
      this.$store.dispatch('openStudy/deleteAllImgsets', studyId)
    },
    createImgsetsAuto () {
      const studyId = this.$route.params.id
      this.$store.dispatch('openStudy/createImgsetsAuto', studyId)
    }
  }
}
</script>

<style>
</style>
