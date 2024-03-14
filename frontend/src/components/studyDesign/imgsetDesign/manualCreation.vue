<template>
  <div>
    <div class="row">
      <div class="col-2 mx-auto">
        <button class="btn btn-secondary btn-lg" data-bs-toggle="popover" :data-bs-title="this.popoverTitle"
          :data-bs-content="this.popoverText" data-bs-placement="left">&#9432;
        </button>
      </div>

      <div class="col-10">
        <h2 class="accordion-header" id="general_settings_title">
          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#images_create_man"
            aria-expanded="true" aria-controls="images_create_man">
            Manual-Creation
          </button>
        </h2>
      </div>
    </div>
    <div class="collapse accordion-collapse show" id="images_create_man">
      <div>
        <div class="row mx-auto">
        <div class="col-4 px-0">
          <button class="text-center btn-success btn imgset_btn w-100" title="add image-set after the currently display image-set or to the end of the study"
            @click.prevent="addImgset"><strong>&#43;</strong>
          </button>
        </div>
        <div v-if="imgsetDisplayed" class="col-4 px-0">
          <button value="update loaded imgset" class="text-center imgset_btn btn-light btn w-100" id="upd_imgset"
            title="update currently selected image-set" @click.prevent="updateImgset"><strong>&#8635;</strong>
          </button>
        </div>
        <div v-if="imgsetDisplayed" class="col-4 px-0">
          <button value="Delete Image-Set" class="text-center imgset_btn btn-danger btn w-100" id="del_imgset"
            title="delete currently selected image-set" @click.prevent="deleteImgset"><strong>&#128465;</strong>
          </button>
        </div>
      </div>
        <div class="row mx-auto">
          <button class="border-0 text-start btn btn-secondary input-group-text" data-bs-toggle="collapse"
            data-bs-target="#images_displayed" aria-expanded="true" aria-controls="images_displayed">
            <div class="mr-auto">Images displayed</div>
          </button>
        </div>

        <div id="images_displayed" class="collapse show">
          <div v-if="refviewerNumb" class="input-group-text">
            <h5 class="mx-auto">Reference-Images</h5>
          </div>
          <div v-for="index in refviewerNumb" :key="index">
            <DicomViewerImageSelect :viewer-index="index - 1" viewer-type="refviewers">
            </DicomViewerImageSelect>
          </div>
          <div v-if="refviewerNumb" class="input-group-text">
            <h5 class="mx-auto">Images</h5>
          </div>
          <div v-for="index in viewerNumb" :key="index">
            <DicomViewerImageSelect :viewer-index="index - 1" viewer-type="viewers">
            </DicomViewerImageSelect>
          </div>
        </div>
        <!-- viewport settings -->
        <div id="viewport_settings_container" class="w-100"
          title="Image Viewer settings control display options (zoom, position, window) for the uploaded study images. Each viewport can be controlled individually.">
          <div class="row mx-auto">
            <button class="text-start btn btn-secondary input-group-text" data-bs-toggle="collapse"
              data-bs-target="#viewport_settings" aria-expanded="true" aria-controls="viewport_settings">
              <div class="mr-auto" id="">Viewer Settings</div>
            </button>
          </div>
          <div id="viewport_settings" class="collapse">
            <div v-if="refviewerNumb" class="input-group-text">
              <h5 class="mx-auto">Reference-Images</h5>
            </div>
            <div id="" v-for="(viewer, index) in refimageViewers" :key="index">
              <DicomViewportControl :target-viewer="index" viewer-type="refviewers">
              </DicomViewportControl>
            </div>
            <div v-if="refviewerNumb" class="input-group-text">
              <h5 class="mx-auto">Images</h5>
            </div>
            <div id="" v-for="(viewer, index) in imageViewers" :key="index">
              <DicomViewportControl :target-viewer="index" viewer-type="viewers"></DicomViewportControl>
            </div>
          </div>
        </div>
        <div v-if="false" id="annotations_settings_container" class="w-100 mt-1" title="">
          <div class="row mt-1 mx-auto">
            <button class="btn bg-gray-300 col-12" data-bs-toggle="collapse" data-bs-target="#annotation_settings"
              aria-expanded="true" aria-controls="viewport_settings">
              <h4 class="w-100 mt-1">Annotation Settings</h4>
            </button>
          </div>
          <div id="annotation_settings" class="collapse">
            <div id="" v-for="(viewer, index) in imageViewers" :key="index">
              <ToolsAnnotationControl :target-viewer="index" viewer-type="viewers">
              </ToolsAnnotationControl>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DicomViewerImageSelect from '@/components/dicomViewer/DicomViewerImageSelect.vue'
import ToolsAnnotationControl from '@/components/dicomViewer/ToolsAnnotationControl.vue'
import DicomViewportControl from '@/components/dicomViewer/DicomViewportControl.vue'

export default {
  components: {
    DicomViewerImageSelect,
    ToolsAnnotationControl,
    DicomViewportControl
  },
  data() {
    return {
      popoverTitle: 'Section Info',
      popoverText: 'This section can be used to create, modify and delete individual Image-Sets. Existing Image-Sets can be loaded via the "Set Displayed Menu". For each viewer an image can be selected using the "Images Displayed" dropdown menus. Settings such as image position, windowing and zoom level can be controlled via the "Viewer Settings" Menus.'
    }
  },
  computed: {
    stacks() {
      return this.$store.getters['currentStudy/stacks']
    },
    imgsets() {
      return this.$store.getters['currentStudy/imgsets']
    },
    viewerNumb() {
      return this.$store.getters['currentStudy/viewerNumb']
    },
    refviewerNumb() {
      return this.$store.getters['currentStudy/refviewerNumb']
    },
    imageViewers() {
      return this.$store.getters['imageViewers/viewers']
    },
    refimageViewers() {
      return this.$store.getters['imageViewers/refviewers']
    },
    imgsetDisplayed: {
      get() {
        const imageSet = this.$store.getters['currentStudy/imgsetDisplayed']
        return imageSet
      }
    }
  },
  methods: {
    addImgset() {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      if (this.imgsetDisplayed === undefined && this.imgsets.length > 0) {
        imgset.position = this.imgsets[this.imgsets.length - 1].position + 1
      } else if (this.imgsetDisplayed === null) {
        imgset.position = 0
      } else {
        imgset.position = this.imgsetDisplayed.position + 1
      }
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('currentStudy/addImgset', payload)
    },
    updateImgset() {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      imgset.position = this.imgsetDisplayed.position
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('currentStudy/updImgset', payload)
    },
    deleteImgset() {
      const studyId = this.$route.params.id
      const imgset = this.$store.getters['imageViewers/getImgset']
      imgset.position = this.imgsetDisplayed.position
      const payload = {
        studyId: studyId,
        imgset: imgset
      }
      this.$store.dispatch('currentStudy/delImgset', payload)
    }
  }
}
</script>

<style></style>
